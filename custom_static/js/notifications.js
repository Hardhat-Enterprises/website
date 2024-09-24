function fetchNotifications() {
    $.ajax({
        url: "/fetch-notifications/",  // Update with the correct URL pattern
        success: function(data) {
            // Update the notifications dropdown or area
            $('#notifications').html(data.html);  // data.html will contain the rendered HTML
        }
    });
}

// Call the fetchNotifications function periodically (every 5 seconds)
setInterval(fetchNotifications, 5000);
