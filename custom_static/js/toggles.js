document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('darkModeButton');
    const icon = document.getElementById('darkModeIcon');

    
    const darkMode = localStorage.getItem('darkMode') === 'true';

    if (darkMode) {
        document.body.classList.add('dark-mode');
        toggleButton.style.backgroundColor = '#333333'; 
        icon.setAttribute('name', 'moon-sharp'); 
        icon.style.color = '#ffcd11'; 
    } else {
        toggleButton.style.backgroundColor = '#f0f0f0'; 
        icon.style.color = '#ffcd11'; 
    }

    
    toggleButton.addEventListener('click', function () {
        if (document.body.classList.contains('dark-mode')) {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
            toggleButton.style.backgroundColor = '#f0f0f0'; 
            icon.setAttribute('name', 'sunny-sharp'); 
            icon.style.color = '#ffcd11'; 
        } else {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
            toggleButton.style.backgroundColor = '#333333'; 
            icon.setAttribute('name', 'moon-sharp'); 
            icon.style.color = '#ffcd11'; 
        }
    });
});