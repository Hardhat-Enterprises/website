// Handles the Recently Viewed Pages logic
document.addEventListener("DOMContentLoaded", () => {
    // Track the current page details
    const currentPage = {
        url: window.location.pathname,
        title: document.title.replace(" - Hardhat Enterprises", "").trim(),
    };

    // Retrieve the recently viewed pages from localStorage or initialize as empty
    let recentlyViewed = JSON.parse(localStorage.getItem("recentlyViewed")) || [];

    // Remove duplicates
    recentlyViewed = recentlyViewed.filter((page) => page.url !== currentPage.url);

    // Add current page to the top
    recentlyViewed.unshift(currentPage);

    // Limit to 5 items
    recentlyViewed = recentlyViewed.slice(0, 5);

    // Save updated list
    localStorage.setItem("recentlyViewed", JSON.stringify(recentlyViewed));

    // Update the dropdown menu
    const dropdownMenu = document.getElementById("recently-viewed-list");
    if (dropdownMenu) {
        dropdownMenu.innerHTML = "";

        recentlyViewed.forEach((page) => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `<a class="dropdown-item" href="${page.url}">${page.title}</a>`;
            dropdownMenu.appendChild(listItem);
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const sidebarHeader = document.querySelector(".recently-viewed-sidebar h5");
    const arrowIcon = sidebarHeader.querySelector(".arrow-icon");

    if (sidebarHeader && arrowIcon) {
        sidebarHeader.addEventListener("click", () => {
            arrowIcon.classList.toggle("rotate");
        });
    }
});
