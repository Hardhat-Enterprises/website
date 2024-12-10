document.addEventListener('DOMContentLoaded', function () {
    const toggle1 = document.getElementById('darkmode-toggle-1');
    const toggle2 = document.getElementById('darkmode-toggle-2');

    function syncToggles(isDarkMode) {
        toggle1.checked = isDarkMode;
        toggle2.checked = isDarkMode;
    }

    const darkMode = localStorage.getItem('darkMode') === 'true';
    syncToggles(darkMode);

    if (darkMode) {
        document.body.classList.add('dark-mode');
    }

    function handleToggle(event) {
        const isDarkMode = event.target.checked; // Get the current toggle's state
        syncToggles(isDarkMode); // Update both toggles to match
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    }

    toggle1.addEventListener('change', handleToggle);
    toggle2.addEventListener('change', handleToggle);
});

document.addEventListener("DOMContentLoaded", () => {
    // Get all dropdown toggles
    const dropdownToggles = document.querySelectorAll(".nav-item.dropdown1 > .nav-link");
  
    dropdownToggles.forEach((toggle) => {
      toggle.addEventListener("click", (event) => {
        event.preventDefault();
  
        const dropdownMenu = toggle.nextElementSibling;
  
        // Toggle the visibility of the dropdown menu
        if (dropdownMenu.style.display === "block") {
          dropdownMenu.style.display = "none";
        } else {
          dropdownMenu.style.display = "block";
        }
  
        // Close other open dropdowns
        document.querySelectorAll(".dropdown-menu1").forEach((menu) => {
          if (menu !== dropdownMenu) {
            menu.style.display = "none";
          }
        });
      });
    });
  
    // Close dropdowns when clicking outside
    document.addEventListener("click", (event) => {
      const isDropdown = event.target.closest(".nav-item.dropdown1");
      if (!isDropdown) {
        document.querySelectorAll(".dropdown-menu1").forEach((menu) => {
          menu.style.display = "none";
        });
      }
    });
  });
