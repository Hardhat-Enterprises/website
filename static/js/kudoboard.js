document.addEventListener('DOMContentLoaded', function() {
    const whiteboard = document.getElementById('whiteboard');
    const reviewText = document.getElementById('reviewText');
    const submitReview = document.getElementById('submitReview');
    const clearReviews = document.getElementById('clearReviews');
    const stickyColors = ['#ffc107', '#ff5722', '#8bc34a', '#03a9f4', '#e91e63']; // Modern bold colors
    let usedColors = [];
    const noteColor = document.getElementById('noteColor');

    // Load saved reviews from localStorage
    const loadReviews = () => {
        const savedReviews = JSON.parse(localStorage.getItem('reviews')) || [];
        savedReviews.forEach((review) => createStickyNote(review.text, review.color));
        toggleClearButton();
    };

    // Save reviews to localStorage
    const saveReviews = () => {
        const reviews = Array.from(whiteboard.children).map((note) => ({
            text: note.textContent,
            color: note.style.backgroundColor,
        }));
        localStorage.setItem('reviews', JSON.stringify(reviews));
    };

    // Helper: get contrast color (white or black) for a given background
    function getContrastYIQ(hexcolor) {
        if (!hexcolor) return '#222';
        hexcolor = hexcolor.replace('#', '');
        if (hexcolor.length === 3) {
            hexcolor = hexcolor.split('').map(x => x + x).join('');
        }
        var r = parseInt(hexcolor.substr(0,2),16);
        var g = parseInt(hexcolor.substr(2,2),16);
        var b = parseInt(hexcolor.substr(4,2),16);
        var yiq = ((r*299)+(g*587)+(b*114))/1000;
        return (yiq >= 128) ? '#222' : '#fff';
    }

    // Create a sticky note
    const createStickyNote = (text, color = null) => {
        const note = document.createElement('div');
        note.className = 'sticky-note';
        note.textContent = text;
        note.style.backgroundColor = color || getUniqueColor();
        
        // Set font color for contrast
        let bg = note.style.backgroundColor;
        let hex = bg;
        if (bg.startsWith('rgb')) {
            // Convert rgb to hex
            let rgb = bg.match(/\d+/g);
            if (rgb) {
                hex = "#" + rgb.map(x => (+x).toString(16).padStart(2, '0')).join('');
            }
        }
        // If dark mode, force white text
        if (document.body.classList.contains('dark-mode')) {
            note.style.color = '#fff';
        } else {
            note.style.color = getContrastYIQ(hex);
        }
        
        // Calculate size based on text length
        const textLength = text.length;
        let width, height;
        
        if (textLength <= 50) {
            width = 150;
            height = 150;
        } else if (textLength <= 100) {
            width = 200;
            height = 200;
        } else if (textLength <= 200) {
            width = 250;
            height = 250;
        } else {
            width = 300;
            height = 300;
        }
        
        note.style.width = width + 'px';
        note.style.height = height + 'px';
        note.style.padding = '15px';
        note.style.fontSize = '14px';
        note.style.overflow = 'auto';
        
        // Add random position within the whiteboard
        const maxX = whiteboard.clientWidth - width;
        const maxY = whiteboard.clientHeight - height;
        note.style.position = 'absolute';
        note.style.left = Math.random() * maxX + 'px';
        note.style.top = Math.random() * maxY + 'px';
        
        // Add random rotation
        note.style.transform = `rotate(${Math.random() * 10 - 5}deg)`;
        
        whiteboard.appendChild(note);
        toggleClearButton();
    };

    // Get a unique color that hasn't been used yet
    const getUniqueColor = () => {
        if (usedColors.length === stickyColors.length) {
            usedColors = [];
        }
        let randomColor;
        do {
            randomColor = stickyColors[Math.floor(Math.random() * stickyColors.length)];
        } while (usedColors.includes(randomColor));
        usedColors.push(randomColor);
        return randomColor;
    };

    // Submit review
    submitReview.addEventListener('click', function() {
        const text = reviewText.value.trim();
        if (text) {
            createStickyNote(text, noteColor ? noteColor.value : undefined);
            reviewText.value = '';
            saveReviews();
        }
    });

    // Clear all reviews
    clearReviews.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear all reviews?')) {
            // Clear all child elements safely
            while (whiteboard.firstChild) {
                whiteboard.removeChild(whiteboard.firstChild);
            }
            usedColors = [];
            localStorage.removeItem('reviews');
            toggleClearButton();
        }
    });

    const toggleClearButton = () => {
        clearReviews.disabled = whiteboard.children.length === 0;
    };

    // Initial display
    loadReviews();
}); 