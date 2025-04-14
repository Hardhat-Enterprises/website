document.addEventListener("DOMContentLoaded", function () {
  const chatPopup = document.getElementById("chat-popup");
  const chatOpenButton = document.getElementById("chatOpenButton");
  const chatCloseButton = document.getElementById("chatCloseButton");
  const messageInput = document.getElementById("message-input");
  const chatBox = document.getElementById("chat-box");
  const sendButton = document.getElementById("send-button");

  // Open the chat popup
  chatOpenButton.addEventListener("click", function () {
    chatPopup.classList.remove("hidden");
    messageInput.focus(); // Focus the input when chat opens
  });

  // Close the chat popup
  chatCloseButton.addEventListener("click", function () {
    chatPopup.classList.add("hidden");
  });

  function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    // Format messages with appropriate prefixes
    if (isUser) {
      messageDiv.textContent = `Guest: ${message}`;
    } else {
      messageDiv.textContent = `Hardie Hat 🤖 : ${message}`;
    }
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Define sendMessage function
  function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
      // Add user message to chat
      addMessage(message, true);
      
      // Clear input
      messageInput.value = '';
      
      // Add dummy response without sending to server
      addMessage('Hi! I am currently being developed and cannot answer your queries. Come back soon!');
      
      // Scroll to bottom
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  // Attach click event listener to send button
  sendButton.addEventListener("click", sendMessage);

  // Allow sending message with Enter key
  messageInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
}); 