document.addEventListener('DOMContentLoaded', () => {
    // Get the page path
    const pagePath = window.location.pathname;

    // Retrieve visits data from localStorage
    const visitsData = JSON.parse(localStorage.getItem('pageVisits')) || {};

    // Increment the visit count for the current page
    if (!visitsData[pagePath]) {
        visitsData[pagePath] = 1;
    } else {
        visitsData[pagePath] += 1;
    }

    // Update localStorage with the new data
    localStorage.setItem('pageVisits', JSON.stringify(visitsData));

    // Display the visit count on the page
    const visitCounterElement = document.getElementById('visit-counter');
    if (visitCounterElement) {
        visitCounterElement.textContent = visitsData[pagePath];
    }
});
