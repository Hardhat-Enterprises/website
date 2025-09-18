document.addEventListener("DOMContentLoaded", function () {
  const availableKeywords = [
    { label: 'Blog', url: '/feedback' },
    { label: 'Careers', url: '/careers' },
    { label: 'Cyber Challenges', url: '/challenges' },
    { label: 'AppAttack' }, 
    { label: 'Malware (On Hold)' },
    { label: 'PT-GUI' },
    { label: 'Smishing Detection' },
    { label: 'Deakin CyberSafe VR' },
    { label: 'Deakin Threat mirror (On Hold)' },
    { label: 'The Policy Deployment Engine' },
    { label: 'Projects' }
  ];

  const inputBox = document.querySelector(".search-box");
  const resultBox = document.querySelector(".result-box");

  if (!inputBox || !resultBox) {
    console.warn("Missing .search-box or .result-box");
    return;
  }

  inputBox.addEventListener("input", function () {
    const input = this.value.trim().toLowerCase();
    resultBox.innerHTML = "";

    if (input.length === 0) {
      resultBox.classList.add("d-none");
      return;
    }

    const filtered = availableKeywords.filter(item =>
      item.label.toLowerCase().includes(input)
    );

    if (filtered.length === 0) {
      resultBox.innerHTML = `<div class="suggestion-item">No results found</div>`;
    } else {
      resultBox.innerHTML = filtered.map(item =>
        `<div class="suggestion-item" data-label="${item.label}" ${item.url ? `data-url="${item.url}"` : ''}>${item.label}</div>`
      ).join('');
    }

    resultBox.classList.remove("d-none");

    const allSuggestions = document.querySelectorAll(".suggestion-item");
    allSuggestions.forEach(item => {
      item.addEventListener("click", function () {
        const label = this.getAttribute("data-label");
        const url = this.getAttribute("data-url");

        inputBox.value = label;
        resultBox.classList.add("d-none");

        if (url) {
          window.location.href = url;
        } else {
          inputBox.closest("form").submit();
        }
      });
    });
  });

  // Optional: hide dropdown on outside click
  document.addEventListener("click", function (e) {
    if (!inputBox.contains(e.target) && !resultBox.contains(e.target)) {
      resultBox.classList.add("d-none");
    }
  });
});
document.addEventListener("DOMContentLoaded", function () {
  const availableKeywords = [
    { label: 'Blog', url: '/feedback' },
    { label: 'Careers', url: '/careers' },
    { label: 'Cyber Challenges', url: '/challenges' },
    { label: 'AppAttack' }, 
    { label: 'Malware (On Hold)' },
    { label: 'PT-GUI' },
    { label: 'Smishing Detection' },
    { label: 'Deakin CyberSafe VR' },
    { label: 'Deakin Threat mirror (On Hold)' },
    { label: 'The Policy Deployment Engine' },
    { label: 'Projects' }
  ];

  const inputBox = document.querySelector(".search-box");
  const resultBox = document.querySelector(".result-box");

  if (!inputBox || !resultBox) {
    console.warn("Missing .search-box or .result-box");
    return;
  }

  inputBox.addEventListener("input", function () {
    const input = this.value.trim().toLowerCase();
    resultBox.innerHTML = "";

    if (input.length === 0) {
      resultBox.classList.add("d-none");
      return;
    }

    const filtered = availableKeywords.filter(item =>
      item.label.toLowerCase().includes(input)
    );

    if (filtered.length === 0) {
      resultBox.innerHTML = `<div class="suggestion-item">No results found</div>`;
    } else {
      resultBox.innerHTML = filtered.map(item =>
        `<div class="suggestion-item" data-label="${item.label}" ${item.url ? `data-url="${item.url}"` : ''}>${item.label}</div>`
      ).join('');
    }

    resultBox.classList.remove("d-none");

    const allSuggestions = document.querySelectorAll(".suggestion-item");
    allSuggestions.forEach(item => {
      item.addEventListener("click", function () {
        const label = this.getAttribute("data-label");
        const url = this.getAttribute("data-url");

        inputBox.value = label;
        resultBox.classList.add("d-none");

        if (url) {
          window.location.href = url;
        } else {
          inputBox.closest("form").submit();
        }
      });
    });
  });

  // Optional: hide dropdown on outside click
  document.addEventListener("click", function (e) {
    if (!inputBox.contains(e.target) && !resultBox.contains(e.target)) {
      resultBox.classList.add("d-none");
    }
  });
});
