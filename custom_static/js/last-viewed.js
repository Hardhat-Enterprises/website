const maxPages = 5; // Set maximum number of pages to store

function updateRecentlyViewedPages() {
    console.log("Starting updateRecentlyViewedPages...");

    // Fetch the current stored pages from localStorage
    let pages = JSON.parse(localStorage.getItem('lastViewedPages')) || [];
    console.log("Fetched pages from localStorage:", pages);

    // Get the current page URL
    const currentPage = window.location.pathname;
    console.log("Current page:", currentPage);

    // Remove duplicates
    pages = pages.filter(page => page !== currentPage);
    console.log("After removing duplicates:", pages);

    // Add the current page to the top
    pages.unshift(currentPage);
    console.log("After adding current page:", pages);

    // Limit the array to the maxPages
    if (pages.length > maxPages) {
        pages = pages.slice(0, maxPages);
    }
    console.log("After limiting pages to maxPages:", pages);

    // Save the updated pages back to localStorage
    localStorage.setItem('lastViewedPages', JSON.stringify(pages));
    console.log("Updated pages saved to localStorage");

    // Update the UI with the new list of pages
    renderRecentlyViewedPages(pages);
}

function renderRecentlyViewedPages(pages) {
    console.log("Rendering Recently Viewed Pages...");

    const listElement = document.getElementById('recent-pages-list');
    if (!listElement) {
        console.error("Element with ID 'recent-pages-list' not found in DOM");
        return;
    }

    // Clear existing content
    listElement.innerHTML = '';

    // Populate the list with updated pages
    pages.forEach(page => {
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = page;
        link.textContent = page;
        listItem.appendChild(link);
        listElement.appendChild(listItem);
    });
    console.log("Rendered recently viewed pages successfully");
}

// Initialize the script on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log("Last Viewed Pages Script Loaded");
    updateRecentlyViewedPages();
});
