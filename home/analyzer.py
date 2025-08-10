from __future__ import annotations
import ipaddress, re, socket, ssl, difflib, hashlib, time
from datetime import datetime, timezone
from urllib.parse import urlparse
import requests
from django.conf import settings

try:
    import whois
except Exception:
    whois = None

SUSPICIOUS_TLDS   = {"zip","mov","click","country","stream","biz","work","club","top","link","xyz"}
SHORTENER_HOSTS   = {"bit.ly","tinyurl.com","goo.gl","t.co","ow.ly","is.gd","cutt.ly","buff.ly","rebrand.ly"}
PHISHY_KEYWORDS   = {"login","verify","update","secure","account","wallet","bank","free","win","bonus","confirm"}
WELL_KNOWN_BRANDS = {"google","facebook","microsoft","apple","paypal","amazon","instagram","netflix","deakin"}

HTTP_TIMEOUT = 6
USER_AGENT   = "Hardhat-Link-Analyzer/1.1"

_cache: dict[str, tuple[float, dict]] = {}
CACHE_TTL = 60 * 30

def _cache_get(key: str):
    v = _cache.get(key)
    if not v: return None
    ts, data = v
    if time.time() - ts > CACHE_TTL:
        _cache.pop(key, None)
        return None
    return data

def _cache_set(key: str, data: dict):
    _cache[key] = (time.time(), data)

def _normalize(u:str)->str:
    u = u.strip()
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', u):
        u = 'http://' + u
    return u

def _is_ip(host:str)->bool:
    try: ipaddress.ip_address(host); return True
    except: return False

def _public_ip(host:str)->bool:
    try:
        ip = ipaddress.ip_address(host)
        return not (ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local)
    except:
        return True

def _resolve_host(host:str)->tuple[bool,str|None]:
    try: return True, socket.gethostbyname(host)
    except Exception: return False, None

def _domain_age_days(domain:str):
    if not whois: return None
    try:
        w = whois.whois(domain)
        created = w.creation_date
        if isinstance(created, list): created = created[0]
        if not created: return None
        if created.tzinfo is None: created = created.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - created).days
    except: return None

def _get_cert_dates(host:str, port:int=443):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=HTTP_TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        nb = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        na = datetime.strptime(cert["notAfter"],  "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - nb).days, (na - datetime.now(timezone.utc)).days
    except: return None, None

def _homoglyph_or_punycode(host:str)->bool:
    if host.startswith("xn--"): return True
    try: host.encode("ascii"); return False
    except: return True

def _looks_like_brand_impersonation(host:str)->tuple[bool,str|None]:
    parts = host.split(".")
    if len(parts) < 2: return (False, None)
    name = parts[-2]
    best, score = None, 0
    for b in WELL_KNOWN_BRANDS:
        r = difflib.SequenceMatcher(a=name.lower(), b=b).ratio()
        if r > score: score, best = r, b
    return (score >= 0.75 and name.lower() != best, best if score >= 0.75 else None)

def _google_safe_browsing_lookup(url:str)->dict|None:
    key = settings.SAFE_BROWSING_API_KEY or ""
    if not key: return None
    cache_key = f"gsb:{hashlib.sha256(url.encode()).hexdigest()}"
    if (c := _cache_get(cache_key)) is not None: return c
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={key}"
    body = {
        "client": {"clientId":"hardhat","clientVersion":"1.1"},
        "threatInfo":{
            "threatTypes":["MALWARE","SOCIAL_ENGINEERING","UNWANTED_SOFTWARE","POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes":["ANY_PLATFORM"],
            "threatEntryTypes":["URL"],
            "threatEntries":[{"url": url}]
        }
    }
    try:
        r = requests.post(endpoint, json=body, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        _cache_set(cache_key, data)
        return data
    except: return None

def _virustotal_domain_reputation(host:str)->dict|None:
    key = settings.VIRUSTOTAL_API_KEY or ""
    if not key or _is_ip(host): return None
    cache_key = f"vt:{host}"
    if (c := _cache_get(cache_key)) is not None: return c
    headers = {"x-apikey": key, "User-Agent": USER_AGENT}
    try:
        resp = requests.get(f"https://www.virustotal.com/api/v3/domains/{host}", headers=headers, timeout=HTTP_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            _cache_set(cache_key, data)
            return data
    except: pass
    return None

def analyze_url(raw_url:str)->dict:
    url = _normalize(raw_url)
    p = urlparse(url)
    host = (p.hostname or "").strip()
    scheme = (p.scheme or "").lower()

    reasons: list[tuple[str,int]] = []
    critical_flags = []
    risk = 0

    if not host:
        return {"risk": 100, "verdict":"Invalid URL", "badge":"danger",
                "normalized_url": url, "final_url": url, "reasons":[("Missing host", 100)]}

    # DNS
    ok, ip = _resolve_host(host) if not _is_ip(host) else (True, host)
    if not ok:
        risk += 45; reasons.append(("Hostname does not resolve (NXDOMAIN)", 45))
        critical_flags.append("nxdomain")
    if ip and not _public_ip(ip):
        risk += 20; reasons.append(("Resolves to private/non-public address", 20))

    # Structure / lexical
    if scheme != "https":
        risk += 15; reasons.append(("Not using HTTPS", 15))
    if _is_ip(host):
        risk += 18; reasons.append(("Uses raw IP instead of a domain", 18))
    if host.count(".") >= 3:
        risk += 6; reasons.append(("Too many subdomains", 6))
    if len(url) > 120:
        risk += 6; reasons.append(("Very long URL", 6))
    if '@' in url:
        risk += 8; reasons.append(("Contains '@' in URL", 8))
    tld = host.split(".")[-1] if "." in host else ""
    if tld in SUSPICIOUS_TLDS:
        risk += 6; reasons.append((f"Suspicious TLD .{tld}", 6))
    if host in SHORTENER_HOSTS:
        risk += 10; reasons.append(("URL shortener detected", 10))
    if any(k in url.lower() for k in PHISHY_KEYWORDS):
        risk += 8; reasons.append(("Phishing-related keywords in URL", 8))
    if sum(c.isdigit() for c in host) >= max(3, len(host)//4):
        risk += 6; reasons.append(("Domain has many digits", 6))
    if host.count("-") >= 3:
        risk += 4; reasons.append(("Domain has many hyphens", 4))
    if _homoglyph_or_punycode(host):
        risk += 10; reasons.append(("Internationalized/punycode domain", 10))
    imp, brand = _looks_like_brand_impersonation(host)
    if imp:
        risk += 12; reasons.append((f"Looks like '{brand}' impersonation", 12))

    # HTTP(S) & headers
    final_url = url; http_status = None; redirects = 0
    try:
        r = requests.get(url, allow_redirects=True, timeout=HTTP_TIMEOUT, verify=True,
                         headers={"User-Agent": USER_AGENT})
        http_status = r.status_code
        final_url = r.url
        redirects = len(r.history)

        hdrs = {k.lower(): v for k,v in r.headers.items()}
        hsts = "strict-transport-security" in hdrs
        csp  = "content-security-policy" in hdrs
        xfo  = "x-frame-options" in hdrs

        if redirects >= 4:
            risk += 8; reasons.append((f"Too many redirects ({redirects})", 8))
        if scheme == "https" and not hsts:
            risk += 5; reasons.append(("Missing HSTS header", 5))
        if not csp:
            risk += 3; reasons.append(("Missing Content-Security-Policy", 3))
        if not xfo:
            risk += 2; reasons.append(("Missing X-Frame-Options", 2))
    except requests.exceptions.SSLError:
        risk += 12; reasons.append(("TLS/SSL error while connecting", 12))
    except requests.exceptions.RequestException:
        risk += 5; reasons.append(("Host did not respond to quick check", 5))

    # Certificate posture
    if scheme == "https" and not _is_ip(host):
        age_days, exp_days = _get_cert_dates(host)
        if age_days is not None:
            if age_days < 7:   risk += 6; reasons.append(("TLS certificate issued very recently (<7d)", 6))
            elif age_days < 30: risk += 3; reasons.append(("TLS certificate new (<30d)", 3))
        if exp_days is not None and exp_days <= 14:
            risk += 8; reasons.append(("TLS certificate expiring soon (≤14d)", 8))

    # Domain age
    if host and not _is_ip(host):
        age = _domain_age_days(host)
        if age is not None:
            if age < 90:   risk += 10; reasons.append(("Very new domain (<90 days)", 10))
            elif age < 365: risk += 5; reasons.append(("Newish domain (<1 year)", 5))

    # Threat intel
    sb = _google_safe_browsing_lookup(final_url)
    if sb and sb.get("matches"):
        reasons.append(("Listed by Google Safe Browsing", 40))
        critical_flags.append("safebrowsing")
        risk = max(risk, 95)

    vt = _virustotal_domain_reputation(host)
    if vt:
        try:
            stats = vt["data"]["attributes"]["last_analysis_stats"]
            malicious  = int(stats.get("malicious", 0))
            suspicious = int(stats.get("suspicious", 0))
            if malicious >= 1 or suspicious >= 3:
                add = min(30, 10*malicious + 5*suspicious)
                reasons.append((f"VirusTotal detections (m:{malicious}, s:{suspicious})", add))
                critical_flags.append("virustotal")
                risk = max(risk, 90)
            else:
                if malicious == 0 and suspicious == 0:
                    reasons.append(("VirusTotal: no engines flagged", -5))
                    risk = max(0, risk - 5)
        except Exception:
            pass

    # Escalation + verdict
    if critical_flags:
        risk = max(risk, 85)

    risk = max(0, min(100, risk))
    if risk < 30:   verdict, badge = "Likely Safe", "success"
    elif risk < 60: verdict, badge = "Use Caution", "warning"
    else:           verdict, badge = "High Risk", "danger"

    return {
        "input": raw_url,
        "normalized_url": url,
        "final_url": final_url,
        "http_status": http_status,
        "risk": risk,
        "verdict": verdict,
        "badge": badge,
        "reasons": reasons,
        "redirects": redirects,
    }
