document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('darkModeButton'); // top right sun/moon button
    const icon = document.getElementById('darkModeIcon');
    const navbar = document.querySelector('.navbar-main');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    const whiteboardContainers = document.querySelectorAll('.whiteboard-container');

    const mobileToggle = document.getElementById('darkmode-toggle'); // sidebar switch

    const darkMode = localStorage.getItem('darkMode') === 'true';
    applyDarkMode(darkMode);

    // Apply mode change visually
    function applyDarkMode(isDark) {
        document.body.classList.toggle('dark-mode', isDark);
        if (toggleButton) toggleButton.style.backgroundColor = isDark ? '#333333' : '#f0f0f0';

        if (icon) {
            icon.classList.remove(isDark ? 'fa-sun' : 'fa-moon');
            icon.classList.add(isDark ? 'fa-moon' : 'fa-sun');
            icon.style.color = '#ffcd11';
        }

        if (navbar) navbar.style.backgroundColor = isDark ? '#333333' : '#ffffff';

        dropdownMenus.forEach(menu => {
            menu.style.backgroundColor = isDark ? '#333333' : '#ffffff';
            menu.style.color = isDark ? '#ffffff' : '#333333';
        });

        whiteboardContainers.forEach(container => {
            container.style.backgroundColor = isDark ? '#222222' : '#ffffff';
            container.style.color = isDark ? '#ffffff' : '#000000';
        });

        // Sync both toggle switches
        if (mobileToggle) mobileToggle.checked = isDark;
    }

    // Desktop toggle button
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            const isDark = !document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark.toString());
            applyDarkMode(isDark);
        });
    }

    // Mobile sidebar toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('change', function () {
            const isDark = mobileToggle.checked;
            localStorage.setItem('darkMode', isDark.toString());
            applyDarkMode(isDark);
        });
    }
});
    