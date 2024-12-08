document.addEventListener('DOMContentLoaded', function() {
    let callButton = document.getElementById("callButton");
    let callPopup = document.getElementById("callPopup");
    let overlay = document.getElementById("overlay");
    let closePopupButton = document.getElementById("closePopup");

    // Show the call popup when the floating button is clicked
    callButton.onclick = function() {
        overlay.style.display = 'block';
        callPopup.style.display = 'block';
    };

    // Close the popup when the close button is clicked
    closePopupButton.onclick = function() {
        overlay.style.display = 'none';
        callPopup.style.display = 'none';
    };

    function closePopup() {
        overlay.style.display = 'none';
        callPopup.style.display = 'none';
    }


    // Close the popup if the overlay is clicked
    overlay.onclick = function() {
        overlay.style.display = 'none';
        callPopup.style.display = 'none';
    };
});