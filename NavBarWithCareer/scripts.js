document.getElementById('link1').addEventListener('click', function(event) {
    event.preventDefault();
    loadCarousel('link1');
});

document.getElementById('link2').addEventListener('click', function(event) {
    event.preventDefault();
    loadCarousel('link2');
});

document.getElementById('link3').addEventListener('click', function(event) {
    event.preventDefault();
    loadCarousel('link3');
});

let slideIndex = 0;

function loadCarousel(link) {
    const carouselImagesDiv = document.querySelector('.carousel-images');
    let images;

    switch (link) {
        case 'link1':
            images = [
                'https://www.shutterstock.com/image-photo/career-businessman-on-blurred-abstract-260nw-1152345887.jpg',
                'https://www.pascotata.com/uploads/cms/8587carredutyu.jpg',
                'https://watermark.lovepik.com/photo/50076/9860.jpg_wh1200.jpg'
            ];
            break;
        case 'link2':
            images = [
                'https://via.placeholder.com/800x400/33FF57/FFFFFF?text=Link+2+Image+1',
                'https://via.placeholder.com/800x400/33FFBD/FFFFFF?text=Link+2+Image+2',
                'https://via.placeholder.com/800x400/5733FF/FFFFFF?text=Link+2+Image+3'
            ];
            break;
        case 'link3':
            images = [
                'https://via.placeholder.com/800x400/FF5733/FFFFFF?text=Link+3+Image+1',
                'https://via.placeholder.com/800x400/33FFBD/FFFFFF?text=Link+3+Image+2',
                'https://via.placeholder.com/800x400/FF33FF/FFFFFF?text=Link+3+Image+3'
            ];
            break;
    }

    carouselImagesDiv.innerHTML = '';
    images.forEach((src, index) => {
        const img = document.createElement('img');
        img.src = src;
        if (index === 0) img.classList.add('active');
        carouselImagesDiv.appendChild(img);
    });

    slideIndex = 0;
}

function changeSlide(n) {
    const images = document.querySelectorAll('.carousel-images img');
    images[slideIndex].classList.remove('active');
    slideIndex = (slideIndex + n + images.length) % images.length;
    images[slideIndex].classList.add('active');
}
