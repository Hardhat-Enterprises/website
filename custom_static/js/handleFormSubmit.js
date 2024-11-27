/*

How to implement in the code:

1.make sure form has div with id form-header and form-body (in our code structure we have follow structure where generally heading comes in div with id=form-header and rest of the form is in div with id=form-body )

2.Import handleFormSubmit.js file in html page where form issues occures as described above.	Make sure you add this at the end of the code just to prevent overwriting.
Ex: <script src="{% static 'js/handleFormSubmit.js' %}"></script>

3.In the form tag just add onsubmit=”handelFormSubmit(event)”

*/
function handleFormSubmit(event) {
  // Prevent default behavior so we can control the submission
  event.preventDefault();

  // Get the form data
  const form = event.target; // This is the form element
  const formData = new FormData(form); // Create FormData object
  //console.log(form.method);
  //console.log(formData);
  // Send data to the server using Fetch API
  fetch(form.action, {
    method: form.method, // POST in this case
    body: formData,
    headers: {
      "X-CSRFToken": formData.get("csrfmiddlewaretoken"), // Pass CSRF token for Django
    },
  })
    .then((response) => {
      if (response.ok) {
        // Show thank-you message on success
        document.getElementById("form-header").innerHTML = `
          <h2 style="color: #ffc107; text-align: center;">Thank you for reaching out!</h2>
          <p style="text-align: center;">We appreciate your message and will get back to you as soon as possible.</p>`;
        // Hide the form body
        document.getElementById("form-body").style.display = "none";
      } else {
        // Handle errors
        alert("There was an error submitting the form. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Something went wrong. Please try again later.");
    });
}
