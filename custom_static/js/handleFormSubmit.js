function handleFormSubmit(event) {
  event.preventDefault(); // Prevent the form

  // Hide the form and header
  document.getElementById("form-header").style.display = "none";
  document.getElementById("form-body").style.display = "none";

  // Show the thank-you message
  document.getElementById("thank-you-message").style.display = "block";
}
