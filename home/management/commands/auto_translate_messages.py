# -*- coding: utf-8 -*-
"""
Auto-translate .po/.po(djangojs) using DeepL only (no manual msgstr).
- Fills empty msgstr / msgstr_plural (use --force to overwrite).
- Preserves %(placeholders)s
- Handles plurals
- Adds tcomment "[auto-translated provider=DeepL]"
"""

import os, re
from pathlib import Path
import polib
from django.core.management.base import BaseCommand
import deepl

# Django locale -> DeepL target language code
DEEPL_LOCALES = {
    "zh_Hans": "ZH",   # 简体中文
    "fr":      "FR",
    "es":      "ES",
    "ja":      "JA",
    "ko":      "KO",
}

PLACEHOLDER_RE = re.compile(r"%\([^)]+\)s")

def _mask(s: str):
    mp = {}
    def repl(m):
        k = f"__PH_{len(mp)}__"
        mp[k] = m.group(0)
        return k
    return PLACEHOLDER_RE.sub(repl, s), mp

def _unmask(s: str, mp: dict):
    for k, v in mp.items():
        s = s.replace(k, v)
    return s

def _nplurals(po: polib.POFile) -> int:
    m = re.search(r"nplurals\s*=\s*(\d+)", po.metadata.get("Plural-Forms",""))
    return int(m.group(1)) if m else 1

def _defuzz(entry):
    # Remove fuzzy marks; some tools keep history in previous_msgid
    if 'fuzzy' in entry.flags:
        entry.flags.remove('fuzzy')
    # Clear old msgids that were previously guessed to be matches to avoid them being marked as fuzzy again
    if getattr(entry, "previous_msgid", None):
        entry.previous_msgid = ""

class Command(BaseCommand):
    help = "Auto-translate .po via DeepL (no manual msgstr)."

    def add_arguments(self, parser):
        parser.add_argument("--locale_dir", default="locale")
        parser.add_argument("--force", action="store_true", help="overwrite existing msgstr/msgstr_plural")

    def handle(self, *args, **opts):
        api_key = os.getenv("DEEPL_API_KEY")
        if not api_key:
            self.stderr.write("ERROR: DEEPL_API_KEY not set.")
            return

        translator = deepl.Translator(api_key)
        root = Path(opts["locale_dir"])
        domains = ("django", "djangojs")

        for loc, target in DEEPL_LOCALES.items():
            for dom in domains:
                po_path = root / loc / "LC_MESSAGES" / f"{dom}.po"
                if not po_path.exists():
                    self.stdout.write(f"Skip: {po_path} (not found)")
                    continue

                po = polib.pofile(str(po_path))
                changed = False
                npl = _nplurals(po)

                for e in po:
                    if e.obsolete:
                        continue

                    # plural entries
                    if e.msgid_plural:
                        already = any(v.strip() for v in e.msgstr_plural.values())
                        if already and not opts["force"]:
                            continue
                        s1 = self._tx(translator, e.msgid, target)
                        s2 = self._tx(translator, e.msgid_plural, target)
                        for i in range(npl):
                            e.msgstr_plural[i] = s1 if i == 0 else s2
                        e.tcomment = ((e.tcomment or "") + " [auto-translated provider=DeepL]").strip()
                        _defuzz(e)
                        changed = True
                        continue

                    # normal entries
                    if e.msgstr.strip() and not opts["force"]:
                        continue
                    if not e.msgid.strip():
                        continue

                    out = self._tx(translator, e.msgid, target)
                    e.msgstr = out
                    e.tcomment = ((e.tcomment or "") + " [auto-translated provider=DeepL]").strip()
                    _defuzz(e)
                    changed = True

                if changed:
                    po.save(str(po_path))
                    self.stdout.write(f"Updated: {po_path}")
                else:
                    self.stdout.write(f"No change: {po_path}")

        self.stdout.write(self.style.SUCCESS("Auto-translate finished. Now run compilemessages."))

    @staticmethod
    def _tx(translator, text: str, target: str) -> str:
        if not text.strip():
            return text
        masked, mp = _mask(text)
        res = translator.translate_text(masked, target_lang=target, preserve_formatting=True)
        return _unmask(res.text, mp)
