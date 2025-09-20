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
      // Create safe "No results found" element
      resultBox.innerHTML = '';
      const noResultsDiv = document.createElement('div');
      noResultsDiv.className = 'suggestion-item';
      noResultsDiv.textContent = 'No results found';
      resultBox.appendChild(noResultsDiv);
    } else {
      // Clear previous content
      resultBox.innerHTML = '';
      
      // Create elements safely to prevent XSS
      filtered.forEach(item => {
        // Sanitize label to prevent HTML injection
        const sanitizedLabel = String(item.label).replace(/[<>&"']/g, function(match) {
          const escapeMap = {
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
            "'": '&#x27;'
          };
          return escapeMap[match];
        });
        
        const suggestionDiv = document.createElement('div');
        suggestionDiv.className = 'suggestion-item';
        suggestionDiv.setAttribute('data-label', sanitizedLabel);
        if (item.url) {
          suggestionDiv.setAttribute('data-url', item.url);
        }
        // Use textContent to prevent HTML injection
        suggestionDiv.textContent = sanitizedLabel;
        resultBox.appendChild(suggestionDiv);
      });
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
