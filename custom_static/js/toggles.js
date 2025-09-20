// Unified theme management system
// This script works in harmony with the settings page and base.html inline script
(function () {
  var body = document.body;
  
  // Check if we have a server-side theme preference from session
  var sessionTheme = (body.dataset && body.dataset.sessionTheme) ? body.dataset.sessionTheme.toLowerCase() : "";
  
  // If server has a valid theme preference, respect it and don't override
  if (sessionTheme === "dark" || sessionTheme === "light" || sessionTheme === "system") {
    // Clean up any old localStorage that might conflict
    try {
      var oldDarkMode = localStorage.getItem('darkMode');
      if (oldDarkMode !== null) {
        // Convert old boolean system to new theme system
        var convertedTheme = (oldDarkMode === 'true') ? 'dark' : 'light';
        localStorage.setItem('theme_preference', convertedTheme);
        localStorage.removeItem('darkMode'); // Clean up old system
      }
    } catch(e) {
      // Handle localStorage errors gracefully
    }
    return; // Exit early - let the unified system handle everything
  }
  
  // Fallback: if no session theme, check for old localStorage system
  try {
    var oldDarkMode = localStorage.getItem('darkMode');
    if (oldDarkMode !== null) {
      var convertedTheme = (oldDarkMode === 'true') ? 'dark' : 'light';
      localStorage.setItem('theme_preference', convertedTheme);
      localStorage.removeItem('darkMode');
      
      // Apply the converted theme immediately
      applyThemeClasses(convertedTheme);
    }
  } catch(e) {
    // Handle localStorage errors
  }
})();

// Helper function to apply theme classes consistently
function applyThemeClasses(theme) {
  var body = document.body;
  
  // Remove existing theme classes
  body.classList.remove('dark-mode', 'light-mode');
  
  // Apply new theme classes
  if (theme === 'dark') {
    body.classList.add('dark-mode');
    body.setAttribute('data-theme', 'dark');
  } else if (theme === 'light') {
    body.classList.add('light-mode');
    body.setAttribute('data-theme', 'light');
  } else {
    // For system, determine actual theme and apply it
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      body.classList.add('dark-mode');
    } else {
      body.classList.add('light-mode');
    }
    body.setAttribute('data-theme', 'system');
  }
}

document.addEventListener('DOMContentLoaded', function () {
    // Legacy elements that might still exist in some templates
    const icon = document.getElementById('darkModeIcon');
    const navbar = document.querySelector('.navbar-main');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    const whiteboardContainers = document.querySelectorAll('.whiteboard-container');
    const mobileToggle = document.getElementById('darkmode-toggle');

    // Get current theme from the unified system
    function getCurrentTheme() {
        try {
            return localStorage.getItem('theme_preference') || 
                   document.body.dataset.sessionTheme || 
                   'system';
        } catch(e) {
            return 'system';
        }
    }

    // Check if we're currently in dark mode (accounting for system preference)
    function isCurrentlyDark() {
        var theme = getCurrentTheme().toLowerCase();
        if (theme === 'dark') return true;
        if (theme === 'light') return false;
        
        // For system, check the actual applied classes or media query
        if (document.body.classList.contains('dark-mode')) return true;
        if (document.body.classList.contains('light-mode')) return false;
        
        // Fallback to media query
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    // Update legacy UI elements to reflect current theme
    function updateLegacyElements(isDark) {
        // Update icon if it exists
        if (icon) {
            icon.classList.remove(isDark ? 'fa-sun' : 'fa-moon');
            icon.classList.add(isDark ? 'fa-moon' : 'fa-sun');
            icon.style.color = '#ffcd11';
        }

        // Update navbar styling (legacy support)
        if (navbar) {
            navbar.style.backgroundColor = isDark ? '#333333' : '#ffffff';
        }

        // Update dropdown menus (legacy support)
        dropdownMenus.forEach(menu => {
            menu.style.backgroundColor = isDark ? '#333333' : '#ffffff';
            menu.style.color = isDark ? '#ffffff' : '#333333';
        });

        // Update whiteboard containers (legacy support)
        whiteboardContainers.forEach(container => {
            container.style.backgroundColor = isDark ? '#222222' : '#ffffff';
            container.style.color = isDark ? '#ffffff' : '#000000';
        });

        // Sync mobile toggle if it exists
        if (mobileToggle) {
            mobileToggle.checked = isDark;
        }
    }

    // Initialize legacy elements with current theme
    updateLegacyElements(isCurrentlyDark());

    // Save theme to all storage locations
    function saveTheme(theme) {
        // Save to localStorage
        try {
            localStorage.setItem('theme_preference', theme);
        } catch(e) {
            // Handle localStorage errors
        }
        
        // Save to cookie
        try {
            document.cookie = "theme_preference=" + encodeURIComponent(theme) +
                            "; Path=/; Max-Age=31536000; SameSite=Lax";
        } catch(e) {
            // Handle cookie errors
        }
        
        // Sync with server session if possible
        try {
            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            var token = csrfToken ? csrfToken.value : '';
            
            fetch('/settings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'fetch',
                    'X-CSRFToken': token
                },
                body: 'theme=' + encodeURIComponent(theme),
                credentials: 'same-origin'
            }).catch(function(err) {
                // Handle fetch errors silently - not critical
            });
        } catch(e) {
            // Handle any errors with the fetch operation
        }
    }

    // Mobile sidebar toggle handler (if it still exists)
    if (mobileToggle) {
        mobileToggle.addEventListener('change', function () {
            var newTheme = mobileToggle.checked ? 'dark' : 'light';
            
            // Save theme to all locations
            saveTheme(newTheme);
            
            // Apply theme immediately
            applyThemeClasses(newTheme);
            
            // Update legacy elements
            updateLegacyElements(newTheme === 'dark');
        });
    }

    // Listen for theme changes from other parts of the application
    window.addEventListener('storage', function(e) {
        if (e.key === 'theme_preference') {
            var newTheme = e.newValue || 'system';
            applyThemeClasses(newTheme);
            updateLegacyElements(newTheme === 'dark' || (newTheme === 'system' && isCurrentlyDark()));
        }
    });
    
    // Listen for system theme changes if current preference is 'system'
    if (window.matchMedia) {
        var mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        var changeHandler = function(e) {
            var currentTheme = getCurrentTheme();
            if (currentTheme.toLowerCase() === 'system') {
                // For system theme, update the classes but keep system preference
                applyThemeClasses('system');
                updateLegacyElements(e.matches);
            }
        };
        
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', changeHandler);
        } else if (mediaQuery.addListener) {
            mediaQuery.addListener(changeHandler);
        }
    }

    // Expose theme functions for debugging/other scripts
    window.themeHelpers = {
        getCurrentTheme: getCurrentTheme,
        isCurrentlyDark: isCurrentlyDark,
        applyTheme: applyThemeClasses,
        saveTheme: saveTheme
    };
});