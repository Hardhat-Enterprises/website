document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('darkModeButton');
    const icon = document.getElementById('darkModeIcon');
    const navbar = document.querySelector('.navbar-main');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');

    const darkMode = localStorage.getItem('darkMode') === 'true';
    applyDarkMode(darkMode);

    function applyDarkMode(isDark) {
        document.body.classList.toggle('dark-mode', isDark);
        toggleButton.style.backgroundColor = isDark ? '#333333' : '#f0f0f0';

        if (isDark) {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }

        icon.style.color = '#ffcd11';
        navbar.style.backgroundColor = isDark ? '#333333' : '#ffffff';

        dropdownMenus.forEach(menu => {
            menu.style.backgroundColor = isDark ? '#333333' : '#ffffff';
            menu.style.color = isDark ? '#ffffff' : '#333333';
        });
    }

    toggleButton.addEventListener('click', function () {
        const isDark = !document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark.toString());
        applyDarkMode(isDark);
    });
});
