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
    // Clear content safely
    while (resultBox.firstChild) {
      resultBox.removeChild(resultBox.firstChild);
    }

    if (input.length === 0) {
      resultBox.classList.add("d-none");
      return;
    }

    const filtered = availableKeywords.filter(item =>
      item.label.toLowerCase().includes(input)
    );

    if (filtered.length === 0) {
      // Create safe "No results found" element - clear content safely
      while (resultBox.firstChild) {
        resultBox.removeChild(resultBox.firstChild);
      }
      const noResultsDiv = document.createElement('div');
      noResultsDiv.className = 'suggestion-item';
      noResultsDiv.textContent = 'No results found';
      resultBox.appendChild(noResultsDiv);
    } else {
      // Clear previous content safely
      while (resultBox.firstChild) {
        resultBox.removeChild(resultBox.firstChild);
      }
      
      // Create elements safely to prevent XSS - using DOMPurify-style approach
      filtered.forEach(item => {
        // Create element first
        const suggestionDiv = document.createElement('div');
        suggestionDiv.className = 'suggestion-item';
        
        // Validate and sanitize the label - only allow alphanumeric and safe characters
        const safeLabel = String(item.label || '').replace(/[^\w\s\-\(\)]/g, '');
        
        // Use createTextNode for ultimate safety - this cannot be interpreted as HTML
        const textNode = document.createTextNode(safeLabel);
        suggestionDiv.appendChild(textNode);
        
        // Set data attributes safely
        suggestionDiv.setAttribute('data-label', safeLabel);
        if (item.url && typeof item.url === 'string' && item.url.match(/^\/[a-zA-Z0-9\-_\/]*$/)) {
          suggestionDiv.setAttribute('data-url', item.url);
        }
        
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
