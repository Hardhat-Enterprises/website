// custom_static/js/search-filters.js
(function () {
  console.log('[search-filters] JS is loaded');

  // Helpers
  const $ = (s, r = document) => r.querySelector(s);

  // DOM
  const filterBtn   = $('#filterBtn');
  const filterModal = $('#filterModal');
  const closeModal  = $('#closeModal');
  const applyBtn    = $('#applyBtn');
  const resetBtn    = $('#resetBtn');
  const didYouMean  = $('#didYouMean');

  // Open/close modal
  filterBtn?.addEventListener('click', () => {
    if (!filterModal) return;
    filterModal.style.display = 'flex';
    filterModal.setAttribute('aria-hidden', 'false');
  });
  closeModal?.addEventListener('click', () => {
    if (!filterModal) return;
    filterModal.style.display = 'none';
    filterModal.setAttribute('aria-hidden', 'true');
  });
  filterModal?.addEventListener('click', (e) => {
    if (e.target === filterModal) {
      filterModal.style.display = 'none';
      filterModal.setAttribute('aria-hidden', 'true');
    }
  });
  applyBtn?.addEventListener('click', () => {
    if (!filterModal) return;
    filterModal.style.display = 'none';
    filterModal.setAttribute('aria-hidden', 'true');
  });
  resetBtn?.addEventListener('click', () => {
    // placeholder: no inputs yet
  });

  // Read your app's param FIRST (searched), then fallback to q
  function getQuery() {
    const p = new URLSearchParams(location.search);
    const s = (p.get('searched') || '').trim();
    if (s) return s;
    return (p.get('q') || '').trim();
  }
  const q = getQuery();
  console.log('[search-filters] query =', q);

  // Did-you-mean demo so you have a screenshot
  if (q && didYouMean) {
    if (q.toLowerCase() === 'cybersecirty') {
      didYouMean.classList.remove('d-none');
      // use ?searched= because your template uses {{ searched }}
      didYouMean.innerHTML = `Did you mean: <a href="/search/?searched=cybersecurity"><strong>cybersecurity</strong></a>?`;
    }
  }

  // Highlight the query in plain text nodes
  if (q) {
    const safeQ = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp('(' + safeQ + ')', 'ig');
    document.querySelectorAll('h2, h3, h5, p, li, a').forEach((el) => {
      if (el.childElementCount === 0 && re.test(el.textContent)) {
        el.innerHTML = el.textContent.replace(re, '<span class="hh-highlight">$1</span>');
      }
    });
  }
})();
