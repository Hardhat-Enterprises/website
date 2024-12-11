document.addEventListener('DOMContentLoaded', function () {
    const visitCounterElement = document.getElementById('visit-counter');

    // Get the current page URL as a unique identifier
    const pageKey = `visitCount_${window.location.pathname}`;

    // Retrieve the visit count for the current page
    let visitCount = localStorage.getItem(pageKey);

    if (visitCount) {
        visitCount = parseInt(visitCount) + 1;
    } else {
        visitCount = 1; // First visit
    }

    // Update localStorage with the new count
    localStorage.setItem(pageKey, visitCount);

    // Display the visit count
    if (visitCounterElement) {
        visitCounterElement.textContent = visitCount;
    }
});