let currentIndex = 0;
const slider = document.querySelector('.testimonial-slider');
const testimonials = Array.from(document.querySelectorAll('.testimonial-item'));
const totalTestimonials = testimonials.length;
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
let autoSlide;

function updateSlider(withTransition = true) {
  const offset = testimonials[currentIndex].offsetLeft;
  slider.style.transition = withTransition ? "transform 0.5s ease-in-out" : "none";
  slider.style.transform = `translateX(-${offset}px)`;
}

function changeIndex(delta) {
  currentIndex = (currentIndex + delta + totalTestimonials) % totalTestimonials;
  updateSlider();
}

function startAutoSlide() {
  autoSlide = setInterval(() => changeIndex(1), 6000);
}

function stopAutoSlide() {
  clearInterval(autoSlide);
}

if (prevBtn && nextBtn) {
  prevBtn.addEventListener('click', () => changeIndex(-1));
  nextBtn.addEventListener('click', () => changeIndex(1));
}

slider.addEventListener("mouseenter", stopAutoSlide);
slider.addEventListener("mouseleave", startAutoSlide);

window.addEventListener('resize', () => updateSlider(false));

updateSlider(false);
startAutoSlide();
