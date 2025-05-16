/**
 * Chatbot.js - Frontend script for the Hardhat Assistant chatbot
 * Handles UI interactions and API communication
 */

document.addEventListener('DOMContentLoaded', function() {
  // DOM Elements
  const chatPopup = document.getElementById("chat-popup");
  const chatOpenButton = document.getElementById("chatOpenButton");
  const chatCloseButton = document.getElementById("chatCloseButton");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const chatBox = document.getElementById("chat-box");
  const connectionStatus = document.getElementById("connection-status");
  
  // Session and state variables
  let sessionId = localStorage.getItem('chatSessionId');
  let chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
  const currentUser = {
    isLoggedIn: false,
    name: 'Guest'
  };
  
  /**
   * Initialize the chatbot interface and connections
   */
  function initChatbot() {
    // Set up event listeners
    chatOpenButton.addEventListener("click", toggleChat);
    chatCloseButton.addEventListener("click", toggleChat);
    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", handleKeyPress);
    
    // Load chat history if available
    loadChatHistory();
    
    // Connect to API and create a session if needed
    connectToApi();
  }
  
  /**
   * Toggle chat visibility
   */
  function toggleChat() {
    chatPopup.classList.toggle("hidden");
    
    if (!chatPopup.classList.contains("hidden")) {
      messageInput.focus();
    }
  }
  
  /**
   * Handle enter key press in message input
   */
  function handleKeyPress(e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  }
  
  /**
   * Create a new session with the API
   */
  async function createSession() {
    try {
      const response = await fetch('/chatbot/api/session/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to create session');
      }
      
      const data = await response.json();
      sessionId = data.session_id;
      
      // Store session ID in local storage
      localStorage.setItem('chatSessionId', sessionId);
      
      console.log('Session created:', sessionId);
      return sessionId;
    } catch (error) {
      console.error('Error creating session:', error);
      showErrorMessage('Could not create chat session. Please try again.');
      return null;
    }
  }
  
  /**
   * Connect to the chatbot API and verify its status
   */
  async function connectToApi() {
    try {
      // Try to verify connection first
      const verifyResponse = await fetch('/chatbot/api/verify/');
      const verifyData = await verifyResponse.json();
      
      if (verifyData.status === 'success' || verifyData.status === 'warning') {
        updateConnectionStatus('connected');
        
        // Create a new session or verify existing one
        if (!sessionId) {
          await createSession();
        } else {
          // Verify existing session
          try {
            const sessionResponse = await fetch(`/chatbot/api/session/${sessionId}/`);
            if (!sessionResponse.ok) {
              // Session not found or expired, create a new one
              await createSession();
            }
          } catch (error) {
            console.error('Error verifying session:', error);
            await createSession();
          }
        }
        
        // Show welcome message if chat history is empty
        if (chatHistory.length === 0) {
          showWelcomeMessage();
        }
      } else {
        updateConnectionStatus('error');
        showErrorMessage('Could not connect to the assistant. Please try again later.');
      }
    } catch (error) {
      console.error('Error connecting to API:', error);
      updateConnectionStatus('error');
      showErrorMessage('Could not connect to the assistant. Please try again later.');
    }
  }
  
  /**
   * Show a welcome message and suggestions
   */
  function showWelcomeMessage() {
    addMessage({
      sender: 'bot',
      text: "Hello! I'm the Hardhat Assistant. I can help you learn about our company, projects, services, and more. How can I assist you today?",
      timestamp: Date.now()
    });
    
    // Add suggested questions
    addSuggestedQuestions();
  }
  
  /**
   * Add suggested questions for users to click on
   */
  function addSuggestedQuestions() {
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.classList.add('suggested-questions');
    suggestionsDiv.innerHTML = `
      <p>Here are some things you can ask:</p>
      <button class="suggestion-btn" onclick="sendSuggestion('What is AppAttack?')">What is AppAttack?</button>
      <button class="suggestion-btn" onclick="sendSuggestion('Tell me about VR Security')">Tell me about VR Security</button>
      <button class="suggestion-btn" onclick="sendSuggestion('What projects do you have?')">What projects do you have?</button>
      <button class="suggestion-btn" onclick="sendSuggestion('How can I join?')">How can I join?</button>
    `;
    chatBox.appendChild(suggestionsDiv);
    
    // Add click handlers for suggestion buttons
    const buttons = suggestionsDiv.querySelectorAll('.suggestion-btn');
    buttons.forEach(button => {
      button.addEventListener('click', function() {
        const text = this.textContent;
        sendSuggestion(text);
      });
    });
    
    scrollChatToBottom();
  }
  
  /**
   * Send a suggested question as a message
   */
  function sendSuggestion(text) {
    messageInput.value = text;
    sendMessage();
  }
  
  /**
   * Send a message to the API
   */
  async function sendMessage() {
    const messageText = messageInput.value.trim();
    
    if (!messageText) return;
    
    // Add user message to chat
    addMessage({
      sender: 'user',
      text: messageText,
      timestamp: Date.now()
    });
    
    // Clear input
    messageInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
      if (!sessionId) {
        await createSession();
      }
      
      const response = await fetch(`/chatbot/api/session/${sessionId}/message/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
          message: messageText,
          user_info: {
            is_authenticated: currentUser.isLoggedIn,
            username: currentUser.name
          }
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Hide typing indicator
      hideTypingIndicator();
      
      // Add bot response
      addMessage({
        sender: 'bot',
        text: data.response,
        timestamp: Date.now()
      });
      
    } catch (error) {
      console.error('Error sending message:', error);
      hideTypingIndicator();
      showErrorMessage('Failed to send message. Please try again.');
    }
  }
  
  /**
   * Add a message to the chat box
   */
  function addMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    
    if (message.sender === 'user') {
      messageDiv.classList.add('user-message');
      messageDiv.textContent = message.text;
    } else if (message.sender === 'bot') {
      messageDiv.classList.add('bot-message');
      messageDiv.innerHTML = message.text;
    }
    
    chatBox.appendChild(messageDiv);
    
    // Add to history
    chatHistory.push(message);
    saveChatHistory();
    
    // Scroll to bottom
    scrollChatToBottom();
  }
  
  /**
   * Show the typing indicator
   */
  function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.classList.add('typing-indicator');
    indicator.innerHTML = '<span></span><span></span><span></span>';
    chatBox.appendChild(indicator);
    scrollChatToBottom();
  }
  
  /**
   * Hide the typing indicator
   */
  function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.remove();
    }
  }
  
  /**
   * Show an error message in the chat
   */
  function showErrorMessage(message) {
    addMessage({
      sender: 'bot',
      text: `<div class="error-message">${message}</div>`,
      timestamp: Date.now()
    });
  }
  
  /**
   * Update the connection status display
   */
  function updateConnectionStatus(status) {
    if (!connectionStatus) return;
    
    connectionStatus.classList.remove('connecting', 'connected', 'error');
    
    switch (status) {
      case 'connecting':
        connectionStatus.innerText = 'Connecting to Hardhat Assistant...';
        connectionStatus.classList.add('connecting');
        break;
      case 'connected':
        connectionStatus.innerText = 'Connected to Hardhat Assistant';
        connectionStatus.classList.add('connected');
        break;
      case 'error':
        connectionStatus.innerText = 'Connection error. Please try again later.';
        connectionStatus.classList.add('error');
        break;
    }
  }
  
  /**
   * Scroll the chat box to the bottom
   */
  function scrollChatToBottom() {
    if (chatBox) {
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }
  
  /**
   * Scroll to show the start of a message
   */
  function scrollToMessageStart(messageElement) {
    if (messageElement && chatBox) {
      messageElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
  
  /**
   * Load chat history from localStorage
   */
  function loadChatHistory() {
    if (chatHistory.length > 0) {
      for (const message of chatHistory) {
        addMessage(message);
      }
    }
  }
  
  /**
   * Save chat history to localStorage
   */
  function saveChatHistory() {
    // Keep only last 50 messages to avoid localStorage limits
    if (chatHistory.length > 50) {
      chatHistory = chatHistory.slice(chatHistory.length - 50);
    }
    
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }
  
  /**
   * Get CSRF token from cookie
   */
  function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    
    return cookieValue;
  }
  
  // Expose functions to be accessible from HTML
  window.sendSuggestion = sendSuggestion;
  
  // Initialize the chatbot
  initChatbot();
});
