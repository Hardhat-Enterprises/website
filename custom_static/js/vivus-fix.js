// Safely override Vivus if it is loaded
window.Vivus = function () {
    console.warn("Vivus initialization suppressed.");
};
