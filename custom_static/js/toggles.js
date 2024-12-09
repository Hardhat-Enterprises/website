document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('darkModeButton');
    const icon = document.getElementById('darkModeIcon');
    const navbar = document.querySelector('.navbar-main');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');

    const darkMode = localStorage.getItem('darkMode') === 'true';

    function applyDarkMode(isDark) {
        document.body.classList.toggle('dark-mode', isDark);
        toggleButton.style.backgroundColor = isDark ? '#333333' : '#f0f0f0';
        icon.setAttribute('name', isDark ? 'moon-sharp' : 'sunny-sharp');
        icon.style.color = '#ffcd11';
        navbar.style.backgroundColor = isDark ? '#333333' : '#ffffff';

        dropdownMenus.forEach(menu => {
            menu.style.backgroundColor = isDark ? '#333333' : '#ffffff'; // Apply dark or light mode color
            menu.style.color = isDark ? '#ffffff' : '#333333'; // Adjust text color
        });
    }

    // Apply saved mode on load
    applyDarkMode(darkMode);

    // Toggle mode on button click
    toggleButton.addEventListener('click', function () {
        const isDark = !document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark.toString());
        applyDarkMode(isDark);
    });
});
