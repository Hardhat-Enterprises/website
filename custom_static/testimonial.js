let currentIndex = 0;
const testimonials = document.querySelectorAll('.testimonial-item');
const totalTestimonials = testimonials.length;

function updateSlider() {

  document.querySelector('.testimonial-slider').style.transform = `translateX(-${currentIndex * 100}%)`;
}


// document.querySelector('.prev-btn').addEventListener('click', () => {
//   currentIndex = (currentIndex === 0) ? totalTestimonials - 1 : currentIndex - 1;
//   updateSlider();
// });

// document.querySelector('.next-btn').addEventListener('click', () => {
//   currentIndex = (currentIndex === totalTestimonials - 1) ? 0 : currentIndex + 1;
//   updateSlider();
// });


setInterval(() => {
  currentIndex = (currentIndex + 1) % totalTestimonials;
  updateSlider();
}, 6000); 


updateSlider();
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
