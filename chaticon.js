const chatIcon = document.getElementById("chatIcon");
const chatBox = document.getElementById("chatBox");
const closeChat = document.getElementById("closeChat");

chatIcon.addEventListener("click", () => {
  chatBox.style.display = "block";
});

closeChat.addEventListener("click", () => {
  chatBox.style.display = "none";
});
