let backToTopButton = document.getElementById("backToTop");

window.onscroll = function() {
    let scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;
    let windowHeight = window.innerHeight;
    let documentHeight = document.documentElement.scrollHeight;

    // Check if the user has scrolled past 50% of the document height
    if (scrollPosition > (documentHeight - windowHeight) / 2) {
        backToTopButton.style.display = "block"; // 
    } else {
        backToTopButton.style.display = "none"; // 
    }
};

// Ensure the button is hidden 
backToTopButton.style.display = "none";

// Smooth scroll to the top 
backToTopButton.onclick = function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};