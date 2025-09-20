document.addEventListener('DOMContentLoaded', function () {
    const faqButtons = document.querySelectorAll('.faq-button');
    
    faqButtons.forEach(button => {
        button.addEventListener('click', function () {
            const content = this.nextElementSibling;
            const icon = this.querySelector('.icon');
            
            // Toggle the visibility of the content
            if (content.style.display === "block") {
                content.style.display = "none";
                this.classList.remove('open');
            } else {
                content.style.display = "block";
                this.classList.add('open');
            }
        });
    });
});
