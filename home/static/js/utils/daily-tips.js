// static/js/utils/daily-tips.js

document.addEventListener("DOMContentLoaded", async function () {
  const tipEl = document.getElementById("hhTipText");
  if (!tipEl) return;

  // --- one-time cleanup: remove any legacy localStorage schedules ---
  try {
    Object.keys(localStorage)
      .filter(k => k.startsWith("dailyTipSchedule:"))
      .forEach(k => localStorage.removeItem(k));
  } catch (_) {}

  // fetch today's tip from Django
  try {
    const res = await fetch("/api/tip/today/", { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch tip");
    const data = await res.json();
    tipEl.textContent = data.tip || "Stay safe online!";
  } catch (e) {
    console.error("Error loading tip:", e);
    tipEl.textContent = "Stay safe online!";
  }

  // optional blink to show update
  const box = document.getElementById("hhTipBox");
  if (box) {
    box.classList.add("blink-animation");
    box.addEventListener("animationend", () => box.classList.remove("blink-animation"), { once: true });
  }
});
