document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav-btn');
    const contents = document.querySelectorAll('.content');
    const carousel = document.querySelector('.carousel-inner');
    const prevBtn = document.querySelector('.carousel-control.prev');
    const nextBtn = document.querySelector('.carousel-control.next');
    
    // Display content based on button clicks
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');

            contents.forEach(content => {
                content.classList.remove('active');
            });

            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.add('active');
            }

            // Show carousel controls only on the "Home" section
            if (targetId === 'home') {
                carousel.parentElement.style.display = 'block';
            } else {
                carousel.parentElement.style.display = 'none';
            }
        });
    });

    // Carousel functionality
    let currentIndex = 0;

    function updateCarousel() {
        const items = document.querySelectorAll('.carousel-item');
        items.forEach((item, index) => {
            item.style.transform = `translateX(-${currentIndex * 100}%)`;
        });
    }

    prevBtn.addEventListener('click', function() {
        const items = document.querySelectorAll('.carousel-item');
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
        updateCarousel();
    });

    nextBtn.addEventListener('click', function() {
        const items = document.querySelectorAll('.carousel-item');
        currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
        updateCarousel();
    });

    // Initialize
    updateCarousel();
});
