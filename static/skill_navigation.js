console.log('JavaScript file is loaded');
const progressId = window.progressId;
const csrfToken = window.csrfToken;
let currentSectionIndex = 0;
const sections = document.querySelectorAll(".section");
const nextButton = document.getElementById("next-button");
const backButton = document.getElementById("back-button");
const finishButton = document.getElementById("finishButton");
let maxProgress = 0;

console.log('nextButton:', nextButton);
console.log('backButton:', backButton);
console.log('finishButton:', finishButton);


nextButton.addEventListener("click", () => {
  // Hide the current section if it exists
  if (sections[currentSectionIndex]) {
    sections[currentSectionIndex].style.display = "none";
  }

  // If there is a next section, show it and the back button
  if (currentSectionIndex < sections.length - 1) {
    // Increment the current section index
    currentSectionIndex++;
    sections[currentSectionIndex].style.display = "block";
    backButton.style.display = "block";
  }

  // If the user is on the last section, hide the next button and show the finish button
  if (currentSectionIndex === sections.length - 1) {
    nextButton.style.display = "none";
    finishButton.style.display = "block";
  }

  // Update progress
  const progress = ((currentSectionIndex + 1) / sections.length) * 100;
  console.log(progress);
  if (progress > maxProgress) {
    maxProgress = progress;
    fetch(`/update-progress/${progressId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        progress: maxProgress,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
        }
      });
  }
});

backButton.addEventListener("click", () => {
  // Hide the current section if it exists
  if (sections[currentSectionIndex]) {
    sections[currentSectionIndex].style.display = "none";
  }

  // If there is a previous section, show it and the next button
  if (currentSectionIndex > 0) {
    // Decrement the current section index
    currentSectionIndex--;
    sections[currentSectionIndex].style.display = "block";
    nextButton.style.display = "block";
  }

  // If there is no previous section, hide the back button
  if (currentSectionIndex <= 0) {
    backButton.style.display = "none";
  }
});

finishButton.addEventListener("click", () => {
  // Set progress to 100%
  progress = 100;

  // Send a POST request to update the progress
  fetch(`/update-progress/${progressId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      progress: progress,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        // Redirect to /upskilling/
        window.location.href = "/upskilling/";
      }
    });
});