document.addEventListener("DOMContentLoaded", function() {
  const tips = [
    "Lock your devices with biometrics or a strong password.",
    "Keep your software and apps up to date.",
    "Use multi-factor authentication whenever possible.",
    "Be cautious when clicking links in emails.",
    "Regularly back up your important data.",
    "Do not reuse the same password across sites.",
    "Avoid using public Wi-Fi without a VPN.",
    "Verify the sender before opening attachments.",
    "Use a password manager to store complex passwords securely.",
    "Cover your webcam when not in use.",
    "Log out of accounts on shared devices.",
    "Install antivirus or endpoint protection software.",
    "Check your bank statements for unusual activity.",
    "Enable automatic updates on your operating system.",
    "Don’t overshare personal information on social media.",
    "Clear cookies and browser cache regularly.",
    "Use encrypted messaging apps for private conversations.",
    "Beware of urgent or threatening messages—they’re often scams.",
    "Disable Bluetooth and Wi-Fi when not in use.",
    "Review app permissions before installing.",
    "Don’t click 'Remember password' in browsers.",
    "Lock your phone with a PIN or pattern when unattended.",
    "Avoid plugging unknown USB drives into your computer.",
    "Enable 'Find My Device' or equivalent tracking features.",
    "Don’t use the same email for work and personal accounts.",
    "Check website URLs carefully before entering credentials.",
    "Set strong, unique PINs for SIM cards and voicemail.",
    "Be careful with QR codes—they can lead to malicious sites.",
    "Enable notifications for logins from new devices.",
    "Secure your home Wi-Fi with WPA3 and a strong password."
  ];

  const tipElement = document.getElementById("hhTipText");
  if (!tipElement) return;

  // Build a key for the current month (e.g., "2025-09")
  const now = new Date();
  const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
  const scheduleKey = `dailyTipSchedule:${monthKey}`;

  // Try to load an existing schedule for this month
  let schedule = [];
  try {
    const raw = localStorage.getItem(scheduleKey);
    if (raw) schedule = JSON.parse(raw);
  } catch (_) {
    schedule = [];
  }

  // If no schedule or size mismatch, create a fresh monthly shuffle
  if (!Array.isArray(schedule) || schedule.length !== tips.length) {
    schedule = shuffleArray(tips.slice()); // fresh shuffled copy
    localStorage.setItem(scheduleKey, JSON.stringify(schedule));
  }

  // Day-of-month is 1..31; convert to 0-based index
  const dayIndex = now.getDate() - 1;

  // If the month has more days than tips (e.g., 31 vs 30), reuse the last
  const tipToShow = schedule[Math.min(dayIndex, schedule.length - 1)];

  tipElement.textContent = tipToShow;

  // --- helpers ---
  function shuffleArray(arr) {
    // Fisher–Yates shuffle
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }
});
