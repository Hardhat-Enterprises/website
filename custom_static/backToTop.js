document.addEventListener('DOMContentLoaded', function() {
    let backToTopButton = document.getElementById("backToTop");
    let footer = document.querySelector('footer'); 
    let footerHeight = footer.offsetHeight;

    window.onscroll = function() {
        let scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;
        let windowHeight = window.innerHeight;
        let documentHeight = document.documentElement.scrollHeight;
        let footerOffsetTop = footer.offsetTop;

        if (documentHeight > windowHeight * 2) {
            if (scrollPosition > (documentHeight - windowHeight) / 2) {
                if (backToTopButton.style.display === "none") {
                    backToTopButton.style.display = "flex"; 
                    backToTopButton.offsetHeight; 
                }
                backToTopButton.style.opacity = ""; 

                if (scrollPosition + windowHeight > footerOffsetTop) {
                    backToTopButton.style.bottom = (windowHeight - (footerOffsetTop - scrollPosition) + 20) + 'px';
                } else {
                    backToTopButton.style.bottom = "50px"; 
                }

            } else {
                backToTopButton.style.opacity = "0"; 
                setTimeout(() => {
                    if (backToTopButton.style.opacity === "0") {
                        backToTopButton.style.display = "none"; 
                    }
                }, 500); 
            }
        } else {
            backToTopButton.style.display = "none"; 
        }
    };

    backToTopButton.onclick = function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };
});