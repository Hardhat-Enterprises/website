document.addEventListener('DOMContentLoaded', function() {
    const whiteboard = document.getElementById('whiteboard');
    const reviewText = document.getElementById('reviewText');
    const submitReview = document.getElementById('submitReview');
    const clearReviews = document.getElementById('clearReviews');
    const stickyColors = ['#ffc107', '#ff5722', '#8bc34a', '#03a9f4', '#e91e63']; // Modern bold colors
    let usedColors = [];

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

    // Create a sticky note
    const createStickyNote = (text, color = null) => {
        const note = document.createElement('div');
        note.className = 'sticky-note';
        note.textContent = text;
        note.style.backgroundColor = color || getUniqueColor();
        
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
            createStickyNote(text);
            reviewText.value = '';
            saveReviews();
        } else {
            alert('Please enter a review.');
        }
    });

    // Clear all reviews
    clearReviews.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear all reviews?')) {
            whiteboard.innerHTML = '';
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