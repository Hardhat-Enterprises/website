document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('darkmode-toggle');

    const darkMode = localStorage.getItem('darkMode') === 'true';

    if (darkMode) {
        toggleButton.checked = darkMode;
        document.body.classList.add('dark-mode');
    }

    toggleButton.addEventListener('click', function () {
        if(toggleButton.checked){
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');

        }else{
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    });
});
