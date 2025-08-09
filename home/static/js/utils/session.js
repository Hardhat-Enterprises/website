// session.js v1.2.0 — aligned with /session/auto-logout/
// Audit-aligned session expiry handling with modal, CSRF-safe logout, and beacon fallback

(() => {
  // ────────────────────────────────────────────────────────────────
  // Configuration
  const SESSION_COOKIE_AGE_MS = 5 * 60 * 1000;   // 5 minutes
  const WARNING_OFFSET_MS = 1 * 60 * 1000;       // Warn 1 minute before expiry

  const ENDPOINTS = {
    EXTEND: '/session/extend-session/',
    LOGOUT: '/logout/',
    AUDIT: '/session/session-events/',
    AUTO_LOGOUT: '/auto-logout/',
    BEACON_LOGOUT: '/session/auto-logout-beacon/'
  };

  // ────────────────────────────────────────────────────────────────
  // DOM References
  const modalEl = document.getElementById('sessionExpiryModal');
  const countdownEl = document.getElementById('countdown');
  const extendBtn = document.getElementById('extendSessionBtn');
  const logoutBtn = document.getElementById('logoutBtn');
  const modal = new bootstrap.Modal(modalEl);

  // ────────────────────────────────────────────────────────────────
  // Countdown Logic
  let countdownMinutes = WARNING_OFFSET_MS / 60000;
  let countdownIntervalId = null;

  const startCountdown = () => {
    updateCountdownDisplay();
    countdownIntervalId = setInterval(() => {
      countdownMinutes--;
      updateCountdownDisplay();
      if (countdownMinutes <= 0) {
        clearInterval(countdownIntervalId);
        triggerAutoLogout();
      }
    }, 60000);
  };

  const updateCountdownDisplay = () => {
    countdownEl.textContent = countdownMinutes;
  };

  // ────────────────────────────────────────────────────────────────
  // Modal Trigger
  const modalTriggerDelay = SESSION_COOKIE_AGE_MS - WARNING_OFFSET_MS;
  setTimeout(() => {
    modal.show();
    startCountdown();
    logEvent('modal_shown', 'xhr');
  }, modalTriggerDelay);

  modalEl.addEventListener('hidden.bs.modal', () => {
    logEvent('modal_dismissed', 'xhr');
  });

  // ────────────────────────────────────────────────────────────────
  // Button Actions
  extendBtn.addEventListener('click', () => {
    postJSON(
      ENDPOINTS.EXTEND,
      { action: 'extend' },
      'session_extended',
      'session_extension_failed'
    ).then(success => {
      if (success) location.reload();
    });
  });

  logoutBtn.addEventListener('click', () => {
    logEvent('user_logged_out', 'manual');
    submitLogoutForm();
  });

  // ────────────────────────────────────────────────────────────────
  // Auto Logout (CSRF-protected)
  function triggerAutoLogout() {
    postJSON(
      ENDPOINTS.AUTO_LOGOUT,
      buildPayload('session_expired', 'xhr'),
      'auto_logout_success',
      'auto_logout_failed'
    ).finally(() => {
      submitLogoutForm();
    });
  }

  // ────────────────────────────────────────────────────────────────
  // Beacon Logout (CSRF-exempt)
  function sendBeaconLogout() {
    const payload = buildPayload('session_expired', 'beacon');
    const blob = new Blob([JSON.stringify(payload)], {
      type: 'application/json'
    });
    navigator.sendBeacon(ENDPOINTS.BEACON_LOGOUT, blob);
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) sendBeaconLogout();
  });

  // ────────────────────────────────────────────────────────────────
  // Payload Builder
  function buildPayload(reason, transport) {
    return {
      reason,
      transport,
      timestamp: new Date().toISOString(),
      user_agent: navigator.userAgent
    };
  }

  // ────────────────────────────────────────────────────────────────
  // CSRF Token
  function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta?.getAttribute('content') || '';
  }

  // ────────────────────────────────────────────────────────────────
  // Audit Logging
  function logEvent(eventType, transport = 'xhr') {
    const payload = {
      event: eventType,
      ...buildPayload(eventType, transport)
    };
    postJSON(ENDPOINTS.AUDIT, payload);
  }

  // ────────────────────────────────────────────────────────────────
  // Generic POST Helper
  async function postJSON(url, payload, successEvent = null, failureEvent = null) {
    try {
      const res = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        if (successEvent) logEvent(successEvent);
        return true;
      } else {
        console.warn(`POST to ${url} failed:`, res.status);
        if (failureEvent) logEvent(failureEvent);
        return false;
      }
    } catch (err) {
      console.error(`POST to ${url} error:`, err);
      if (failureEvent) logEvent(`${failureEvent}_error`);
      return false;
    }
  }

  // ────────────────────────────────────────────────────────────────
  // Logout Form Submission (CSRF-safe POST)
  function submitLogoutForm() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = ENDPOINTS.LOGOUT;

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCSRFToken();

    form.appendChild(csrfInput);
    document.body.appendChild(form);
    form.submit();
  }
})();