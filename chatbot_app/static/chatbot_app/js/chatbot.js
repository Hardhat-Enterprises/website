// Global variables
let currentUser = { isLoggedIn: false, name: 'Guest', sender_id: null };
let chatHistory = []; // Array to hold message objects { sender: 'user'/'bot', text: 'message', timestamp: number }
let messageInput;
let chatBox;
let connectionStatus;
let isResizing = false;

// Get URL from configuration or fall back to default
let DJANGO_MESSAGE_API_URL = window.CHATBOT_CONFIG?.API?.MESSAGE_API || '/api/message/';
let VERIFY_CONNECTION_URL = window.CHATBOT_CONFIG?.API?.VERIFY_CONNECTION || '/api/verify/';
let CONFIG_API_URL = window.CHATBOT_CONFIG?.API?.CONFIG || '/api/config/';
let SESSION_CREATE_URL = window.CHATBOT_CONFIG?.API?.SESSION_CREATE || '/api/session/create/';
let SESSION_DETAIL_URL = window.CHATBOT_CONFIG?.API?.SESSION_DETAIL || '/api/session/';

let chatbotSettings = window.CHATBOT_CONFIG?.SETTINGS || {
    initialMessageDelay: 500,
    typingIndicatorDelay: 1000, 
    autoOpenOnFirstVisit: false,
    persistHistory: true,
    maxHistoryLength: 50,
    defaultBotName: 'HardHat Assistant'
};

// Function to load configuration from the API
async function loadChatbotConfig() {
    try {
        // First, check if config was loaded via the script tag
        if (window.CHATBOT_CONFIG) {
            console.log("Using preloaded chatbot configuration");
        }
        
        // Try to get additional config from the API endpoint
        try {
            const configResponse = await fetch(CONFIG_API_URL);
            if (configResponse.ok) {
                const configData = await configResponse.json();
                console.log("Loaded additional config from API:", configData);
                // Merge with any config already available
                if (configData.settings) {
                    chatbotSettings = {...chatbotSettings, ...configData.settings};
                }
            }
        } catch (configError) {
            console.warn("Could not load additional config from API:", configError);
        }
        
        // Get current user info if available (for personalization)
        const response = await fetch('/get-current-user/');
        if (response.ok) {
            const userData = await response.json();
            console.log("Loaded user configuration:", userData);
            // Update currentUser based on fetched data
            currentUser.isLoggedIn = userData.is_authenticated;
            currentUser.name = userData.is_authenticated ? userData.name : 'Guest';

            // Store sender_id from backend if provided
            if (userData.sender_id) {
                localStorage.setItem('chatbot_sender_id', userData.sender_id);
                currentUser.sender_id = userData.sender_id;
            } else if (userData.session_id) {
                 localStorage.setItem('chatbot_sender_id', userData.session_id);
                 currentUser.sender_id = userData.session_id;
            } else {
                // If backend provides neither, check local storage or generate new
                 currentUser.sender_id = localStorage.getItem('chatbot_sender_id') || generateUniqueId();
                 localStorage.setItem('chatbot_sender_id', currentUser.sender_id);
            }
        } else {
            console.warn("Error loading user config:", response.status, response.statusText);
            // Continue as guest user, try local storage or generate new ID
            currentUser = { 
                isLoggedIn: false, 
                name: 'Guest', 
                sender_id: localStorage.getItem('chatbot_sender_id') || generateUniqueId() 
            };
            localStorage.setItem('chatbot_sender_id', currentUser.sender_id);
        }
    } catch (error) {
        console.error("Error loading config:", error);
         // Continue as guest user, try local storage or generate new ID
        currentUser = { 
            isLoggedIn: false, 
            name: 'Guest', 
            sender_id: localStorage.getItem('chatbot_sender_id') || generateUniqueId() 
        };
        localStorage.setItem('chatbot_sender_id', currentUser.sender_id);
    }
     
     // Final check: Ensure a sender_id is set
     if (!currentUser.sender_id) {
        currentUser.sender_id = localStorage.getItem('chatbot_sender_id') || generateUniqueId();
        localStorage.setItem('chatbot_sender_id', currentUser.sender_id);
     }
     
     console.log("Final currentUser state:", currentUser);
    
    // Verify connection with the server
    try {
        const verifyResponse = await fetch(VERIFY_CONNECTION_URL);
        if (verifyResponse.ok) {
            const status = await verifyResponse.json();
            console.log("Chatbot connection status:", status);
            if (connectionStatus) {
                if (status.status === 'success') {
                    connectionStatus.textContent = "Connected to HardHat Assistant";
                    connectionStatus.classList.remove('connecting', 'disconnected');
                    connectionStatus.classList.add('connected');
                } else {
                    connectionStatus.textContent = "Connection warning: " + status.message;
                    connectionStatus.classList.remove('connecting', 'disconnected', 'connected');
                    connectionStatus.classList.add('warning');
                }
            }
        }
    } catch (verifyError) {
        console.error("Connection verification failed:", verifyError);
        if (connectionStatus) {
            connectionStatus.textContent = "Connection issue. You can still try sending a message.";
            connectionStatus.classList.remove('connecting', 'connected');
            connectionStatus.classList.add('disconnected');
        }
    }
}

// Function to generate a simple unique ID (if backend doesn't provide one)
function generateUniqueId() {
    // More robust UUID generation
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

// Function to ensure chat scrolls to bottom
function scrollChatToBottom() {
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Core Functions
function addMessage(messageObject, isLoadingHistory = false) {
    if (!chatBox) {
        chatBox = document.getElementById("chat-box");
    }
    if (!chatBox) {
        console.error("Chat box not found, cannot add message.");
        return;
    }
    const messageDiv = document.createElement('div');
    const isUser = messageObject.sender === 'user';
    const isBot = messageObject.sender === 'bot';
    const isIndicator = messageObject.sender === 'indicator';

    messageDiv.className = `message ${isUser ? 'user-message' : isBot ? 'bot-message' : 'typing-indicator'}`;

    let prefix = '';
    if (isUser) {
        // Use the name from currentUser
        prefix = `${currentUser.name || 'User'}: `;
        messageDiv.textContent = prefix + messageObject.text;
    } else if (isBot) {
        // Use a span with a specific class for the bot prefix
        const botPrefix = document.createElement('span');
        botPrefix.className = 'bot-prefix';
        botPrefix.textContent = 'Hardhat Assistant:';
        
        messageDiv.appendChild(botPrefix);
        
        // Add the message text in a separate span
        const messageText = document.createElement('span');
        messageText.className = 'bot-message-text';
        
        // Format the message content
        let formattedMessage = messageObject.text || "";
        formattedMessage = formattedMessage.replace(/\\n/g, '\n');
        
        // Simple link detection
        const pathRegex = /(\/[a-zA-Z0-9\/_-]+)/g;
        formattedMessage = formattedMessage.replace(pathRegex, '<a href="$1" target="_blank">$1</a>');
        
        // Add the text
        messageText.innerHTML = ' ' + formattedMessage; // Space after prefix
        messageDiv.appendChild(messageText);

         // Initialize interactive elements in formatted responses if any are added by the backend
         initializeFormattedResponse(messageDiv);

    } else if (isIndicator) {
        messageDiv.id = 'typing-indicator';
        messageDiv.textContent = messageObject.text;
    }

    chatBox.appendChild(messageDiv);

    if ((isUser || isBot) && !isLoadingHistory) {
        messageObject.timestamp = messageObject.timestamp || Date.now();
        chatHistory.push(messageObject);
        saveChatHistory();
    }

    // Adjust scroll behavior based on the message type
    if (isBot) {
        // For bot messages, scroll to show the start of the message
        scrollToMessageStart(messageDiv);
    } else {
        // For user messages and typing indicators, scroll to bottom
        scrollChatToBottom();
    }
}

// Function to initialize interactive elements within bot messages (e.g., suggestion buttons, links)
// This is crucial if your Django view or Rasa actions return rich content/HTML
function initializeFormattedResponse(messageElement) {
    // Example: If your bot message contains buttons with a specific class
    const suggestionButtons = messageElement.querySelectorAll('.suggestion-btn');
    suggestionButtons.forEach(button => {
        // Prevent adding multiple listeners if re-initialized
        if (!button.hasAttribute('data-listener-added')) {
            button.addEventListener('click', () => {
                const message = button.textContent.trim();
                sendMessage(message); // Use the sendMessage function to send the button text
            });
            button.setAttribute('data-listener-added', 'true');
        }
    });

    // Example: If your bot message contains links you want to handle
    const links = messageElement.querySelectorAll('a');
    links.forEach(link => {
       // You can add event listeners here if you want to do something special with links,
       // otherwise, they will behave as normal links. Make sure they open in a new tab.
       link.target = '_blank';
       link.rel = 'noopener noreferrer';
    });

    // Add more initialization for other interactive elements (tables, etc.) if needed
    // based on how your backend formats responses.
}

function saveChatHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    } catch (e) {
        console.error("Error saving chat history:", e);
    }
}

function addTypingIndicator() {
    console.log("Adding typing indicator");
    removeTypingIndicator();
    showTypingIndicator();
}

// Show typing indicator
function showTypingIndicator() {
    console.log("Showing typing indicator");
    if (!chatBox) {
        chatBox = document.getElementById("chat-box");
        console.log("Getting chat box element:", chatBox);
    }
    
    const typingIndicator = document.createElement('div');
    // Add both classes for better targeting
    typingIndicator.classList.add('message', 'typing-message');
    typingIndicator.id = 'typing-indicator';
    
    // Create a more direct structure for the typing indicator
    typingIndicator.innerHTML = `
        <div class="chat-bubble" style="opacity: 1 !important; display: block !important;">
            <div class="typing" style="opacity: 1 !important; display: flex !important;">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    
    chatBox.appendChild(typingIndicator);
    console.log("Typing indicator added to DOM:", typingIndicator);
    
    // Ensure element is visible with inline styles as a last resort
    typingIndicator.style.display = "flex";
    typingIndicator.style.opacity = "1";
    typingIndicator.style.visibility = "visible";
    
    chatBox.scrollTop = chatBox.scrollHeight;
    
    // Debug check if indicator is visible after short delay
    setTimeout(() => {
        const indicator = document.getElementById('typing-indicator');
        console.log("Typing indicator after delay:", indicator);
        if (indicator) {
            console.log("Indicator styles:", window.getComputedStyle(indicator));
            const bubbleEl = indicator.querySelector('.chat-bubble');
            if (bubbleEl) {
                console.log("Chat bubble styles:", window.getComputedStyle(bubbleEl));
            }
        }
    }, 100);
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function removeTypingIndicator() {
    hideTypingIndicator();
    
    // Clear the animation interval
    if (window.typingAnimationInterval) {
        clearInterval(window.typingAnimationInterval);
        window.typingAnimationInterval = null;
    }
}

// Chat Functions
async function sendMessage(directMessage = null) {
    if (!messageInput) {
        messageInput = document.getElementById("message-input");
    }

    const messageText = directMessage || (messageInput ? messageInput.value.trim() : '');

    if (messageText) {
        // Clear input before sending
        if (!directMessage && messageInput) {
            messageInput.value = '';
        }

        try {
            // Add user message to chat
            const userMessage = {
                sender: 'user',
                text: messageText,
                timestamp: Date.now()
            };
            addMessage(userMessage);

            // Show typing indicator immediately after user sends message
            addTypingIndicator();
            
            // Store typing start time to ensure minimum display duration of 1.8 seconds
            const typingStartTime = Date.now();

            // Get CSRF token if needed by your Django view (remove if using @csrf_exempt)
            const csrfToken = getCookie('csrftoken'); // Keep this function call, but only include token if needed

            // Get sender_id from currentUser (loaded during init/updated by backend)
            const senderIdToSend = currentUser.sender_id;
            if (!senderIdToSend) {
                console.error("Missing sender_id. Cannot send message.");
                removeTypingIndicator();
                addMessage({ sender: 'bot', text: "Error: Cannot send message due to missing session identifier." });
                return; // Stop execution
            }

            // Send message to your Django backend endpoint
            let responseData;
            try {
                const response = await fetch(DJANGO_MESSAGE_API_URL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'Accept': 'application/json',
                        // Only include CSRF token if your backend view requires it (i.e., not @csrf_exempt)
                        ...(csrfToken && { 'X-CSRFToken': csrfToken })
                    },
                    body: JSON.stringify({
                        message: messageText,
                        sender: senderIdToSend // Send the stored/current sender_id
                        // You might include other info if needed, e.g., user auth token if applicable
                    })
                });

                if (!response.ok) {
                    // Handle non-200 responses from your Django backend
                    let errorText = `Server responded with status ${response.status}`;
                    try {
                        const errorData = await response.json(); // Try to parse JSON error
                        console.error(`Failed to send message to Django backend: ${response.status}`, errorData);
                        if (errorData.error_type === 'database_error') {
                            errorText = `Database error: ${errorData.detail || 'Unable to retrieve data from database'}`;
                        } else if (errorData.search_error) {
                            errorText = `Search error: ${errorData.search_error}`;
                            console.error("Search engine error:", errorData.search_error);
                        } else {
                            errorText = errorData.error || errorData.detail || errorData.message || "Sorry, I couldn't get a response from the server.";
                        }
                        // Log more detailed debugging information
                        console.log("Full error response:", errorData);
                    } catch (parseError) {
                        // If response is not JSON, use the status text
                        errorText = response.statusText || errorText;
                        console.error(`Failed to send message to Django backend: ${response.status}`, errorText);
                        console.error("Parse error:", parseError);
                    }
                    responseData = { error: true, errorText };
                } else {
                    // Get the response data
                    responseData = await response.json(); // Expecting {messages: [...], sender_id: ...}
                }
            } catch (fetchError) {
                console.error("Error fetching from API:", fetchError);
                responseData = { 
                    error: true, 
                    errorText: "Sorry, I couldn't connect to the server. Please check your connection and try again." 
                };
                
                if (connectionStatus) {
                    connectionStatus.textContent = "Connection Error";
                    connectionStatus.classList.remove('connecting', 'connected');
                    connectionStatus.classList.add('disconnected');
                }
            }

            // Calculate how much time has elapsed since showing the typing indicator
            const elapsedTime = Date.now() - typingStartTime;
            const minTypingTime = 1800; // 1.8 seconds in milliseconds
            
            // If we got the response too quickly, wait until 1.8 seconds have passed
            if (elapsedTime < minTypingTime) {
                await new Promise(resolve => setTimeout(resolve, minTypingTime - elapsedTime));
            }
            
            // Now remove the typing indicator
            removeTypingIndicator();

            // Handle the response after ensuring minimum typing indicator display time
            if (responseData.error) {
                // Handle error response
                const errorMessage = {
                    sender: 'bot',
                    text: responseData.errorText,
                    timestamp: Date.now()
                };
                addMessage(errorMessage);
                return;
            }

            // Update sender_id if the backend sent a new one (or confirms the current one)
            if (responseData.sender_id && responseData.sender_id !== currentUser.sender_id) {
                currentUser.sender_id = responseData.sender_id;
                localStorage.setItem('chatbot_sender_id', responseData.sender_id);
                console.log("Updated sender_id:", currentUser.sender_id);
            }

            // Add bot responses from the 'messages' array
            if (responseData.messages && Array.isArray(responseData.messages)) {
                if (responseData.messages.length === 0) {
                    addMessage({ sender: 'bot', text: "Sorry, I didn't understand that." });
                } else {
                    // Add each message received from the bot
                    for (const botMsg of responseData.messages) {
                        if (botMsg.text) {
                            addMessage({ sender: 'bot', text: botMsg.text, timestamp: Date.now() });
                        }
                        // Handle other message types (image, buttons, custom JSON) if your backend passes them through
                    }
                }
            } else if (responseData.reply) { // Fallback for the older response format {reply: "...", sender_id: "..."}
                addMessage({ sender: 'bot', text: responseData.reply, timestamp: Date.now() });
            } else if (responseData.response) { // Handle the response from message_api view
                addMessage({ sender: 'bot', text: responseData.response, timestamp: Date.now() });
            } else {
                // Handle unexpected response format from backend
                console.error("Unexpected response format from backend:", responseData);
                addMessage({ sender: 'bot', text: "Sorry, I received an unexpected response." });
            }
        } catch (error) {
            console.error('Error in message flow:', error);
            removeTypingIndicator(); // Ensure indicator is removed on error

            // Check if the last message added wasn't already the error message to avoid duplicates
            const lastMessageElement = chatBox.lastElementChild;
            if (!lastMessageElement || !lastMessageElement.textContent.includes("encountered an issue")) {
                const errorMessage = {
                    sender: 'bot',
                    text: "Sorry, I encountered an issue while sending your message. Please check your connection or try again later.",
                    timestamp: Date.now()
                };
                addMessage(errorMessage);
            }

            if (connectionStatus) {
                connectionStatus.textContent = "Connection Error";
                connectionStatus.classList.remove('connecting', 'connected');
                connectionStatus.classList.add('disconnected'); // Use 'disconnected' or a specific 'error' class
            }
        }
    }
}

// Helper function to get cookie value (Keep this function if using CSRF tokens)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to scroll to specific message by selector - Refined
function scrollToMessageStart(messageElement) {
    if (!chatBox || !messageElement) return;

    // Get the position of the message element relative to the chatBox's scrollable area
    const messageRelativeTop = messageElement.offsetTop;

    // Calculate the target scroll position: the message's top position minus a small margin
    const topMargin = 10; // Small margin at the top for better visibility
    const targetScrollTop = messageRelativeTop - chatBox.offsetTop - topMargin; // Adjust for chatBox offset if needed

    // Use smooth scrolling if supported, otherwise fall back to instant
    if ('scrollBehavior' in document.documentElement.style) {
        chatBox.scrollTo({
            top: Math.max(0, targetScrollTop), // Ensure scroll position is not negative
            behavior: 'smooth'
        });
    } else {
        chatBox.scrollTop = Math.max(0, targetScrollTop);
    }

    // Highlight the message briefly
    messageElement.classList.add('highlight-message');
    // Remove the highlight after a short delay
    setTimeout(() => {
        messageElement.classList.remove('highlight-message');
    }, 1500); // Increased highlight duration slightly
}

// Function to load chat history - Refined
function loadChatHistory() {
    if (!chatBox) return [];

    const savedHistory = localStorage.getItem('chatHistory');
    if (savedHistory) {
        try {
            const parsedHistory = JSON.parse(savedHistory);
            chatBox.innerHTML = ''; // Clear chat box before loading

            // First load all messages synchronously
            parsedHistory.forEach(msg => addMessage(msg, true));

            // Initialize interactive elements after all messages are added
            setTimeout(() => {
                const allMessages = chatBox.querySelectorAll('.message');
                allMessages.forEach(initializeFormattedResponse); // Initialize buttons/links in all loaded messages

                // Add suggested questions after loading history
                addSuggestedQuestions();

                // Scroll to the bottom after loading history to show the latest messages
                scrollChatToBottom();

            }, 50); // Short delay to ensure DOM is updated

            return parsedHistory;
        } catch (e) {
            console.error("Error parsing chat history:", e);
            localStorage.removeItem('chatHistory');
            return [];
        }
    }
    return [];
}

// Function to add suggested questions - Updated
function addSuggestedQuestions() {
    if (!chatBox) return;
    
    // Check if suggestions already exist - if so, don't add them again
    if (chatBox.querySelector('.suggested-questions')) {
        return; // Exit if suggestion buttons already exist
    }

    const suggestedQuestionsContainer = document.createElement('div');
    suggestedQuestionsContainer.className = 'suggested-questions';

    // Add a paragraph for the introductory text
    const p = document.createElement('p');
    p.textContent = "What would you like to know?";
    p.style.fontSize = "0.85em";
    p.style.marginBottom = "8px";
    suggestedQuestionsContainer.appendChild(p);

    // Create the grid container for buttons
    const gridContainer = document.createElement('div');
    gridContainer.className = 'suggested-questions-grid';

    const questions = [
        "What is Deakin Threatmirror?",
        "Tell me about malware visualization",
        "What is PT GUI?", 
        "What is smishing detection?", 
        "How can I upskill?", 
        "Tell me about VR projects"
    ];

    questions.forEach(questionText => {
        const button = document.createElement('button');
        button.className = 'suggestion-btn';
        button.textContent = questionText;
        button.style.fontSize = "0.75em";
        button.style.padding = "6px";
        button.onclick = () => {
            sendMessage(questionText);
        };
        gridContainer.appendChild(button); // Add button to the grid
    });

    suggestedQuestionsContainer.appendChild(gridContainer); // Add grid to the main container
    chatBox.appendChild(suggestedQuestionsContainer);
    scrollChatToBottom(); // Ensure chat scrolls down to show suggestions
}

// Function to initialize chat - Updated
async function initializeChat() {
    if (!chatBox) {
        console.error("Chat box not found during initialization.");
        return;
    }

    // Load user info and sender_id first
    await loadChatbotConfig();

    chatHistory = loadChatHistory(); // Load history (which now scrolls to bottom)

    if (chatHistory.length === 0) { // Only add welcome if history is empty
        const welcomeMessage = {
            sender: 'bot',
            text: "Welcome to Hardhat Enterprises. How can I help you today?",
            timestamp: Date.now()
        };

        // Add the welcome message
        addMessage(welcomeMessage); // This will call initializeFormattedResponse

        // Add suggested questions
        addSuggestedQuestions(); // This also calls initializeFormattedResponse

        // Scroll to the top of the welcome message after a short delay
        setTimeout(() => {
            const firstMessage = chatBox.querySelector('.message:first-child');
            if (firstMessage) {
                scrollToMessageStart(firstMessage);
            } else {
                 scrollChatToBottom(); // Fallback
            }
        }, 150); // Slightly longer delay to ensure rendering
    }
    // No need for else scrollChatToBottom() as loadChatHistory already does this

     // Update connection status display
     if (connectionStatus) {
        connectionStatus.textContent = "Connected"; // Simplified status
        connectionStatus.className = 'connection-status connected'; // Use class for styling
     }

     // Consider sending a session start event if needed by Rasa logic
     // Example: if (!sessionStorage.getItem('rasa_session_started')) {
     //    sendMessage('/session_start'); // Or use a custom event name
     //    sessionStorage.setItem('rasa_session_started', 'true');
     // }
}

// Function to hide chat popup
function hideChat() {
    const chatPopup = document.getElementById("chat-popup");
    const chatOpenButton = document.getElementById("chatOpenButton");
    
    if (chatPopup) {
        chatPopup.classList.add("hidden");
        // Force hide with inline style as a backup
        chatPopup.style.display = "none";
    }
    
    if (chatOpenButton) {
        chatOpenButton.textContent = "💬 Chat with us";
        chatOpenButton.classList.remove("active");
        // Make sure chat button is visible
        chatOpenButton.style.display = "block";
    }
}

// Function to show chat popup
function showChat() {
    const chatPopup = document.getElementById("chat-popup");
    const chatOpenButton = document.getElementById("chatOpenButton");
    
    if (chatPopup) {
        chatPopup.classList.remove("hidden");
        // Remove any inline display style
        chatPopup.style.display = "";
        
        // Always position the chat popup at the bottom right corner
        chatPopup.style.right = "20px";
        chatPopup.style.bottom = "20px";
        chatPopup.style.left = "auto";
        chatPopup.style.top = "auto";
    }
    
    if (chatOpenButton) {
        chatOpenButton.textContent = "Close Chat";
        chatOpenButton.classList.add("active");
    }
}

// Function to reset chat position/size
function resetChatPosition() {
    const chatPopup = document.getElementById("chat-popup");

    if (chatPopup) {
        // Always maintain bottom right position
        chatPopup.style.right = "20px";
        chatPopup.style.bottom = "20px";
        chatPopup.style.left = "auto";
        chatPopup.style.top = "auto";

        // Reset localStorage values related to position (keep size defaults)
        localStorage.removeItem('chatbot-top');
        localStorage.removeItem('chatbot-left');

        // Apply default width/height
        const defaultWidth = "350px";
        const defaultHeight = "500px";
        chatPopup.style.width = defaultWidth;
        chatPopup.style.height = defaultHeight;
        localStorage.setItem('chatbot-width', defaultWidth);
        localStorage.setItem('chatbot-height', defaultHeight);

        // Ensure chat scrolls to bottom
        scrollChatToBottom();
    }
}

// Function to reset chat content and history
function resetChat() {
    // Remove stored history and clear current messages
    localStorage.removeItem('chatHistory');
    chatHistory = [];
    if (chatBox) chatBox.innerHTML = '';

    // Add a fresh welcome message
    const welcomeMessage = {
        sender: 'bot',
        text: "Welcome to Hardhat Enterprises. How can I help you today?",
        timestamp: Date.now()
    };
    addMessage(welcomeMessage);

    // Add suggested questions below welcome
    addSuggestedQuestions();
}

// DOMContentLoaded listener - Updated
document.addEventListener("DOMContentLoaded", async function() {
    // Get DOM elements
    const chatPopup = document.getElementById("chat-popup");
    const chatOpenButton = document.getElementById("chatOpenButton");
    const chatCloseButton = document.getElementById("chatCloseButton");
    messageInput = document.getElementById("message-input");
    chatBox = document.getElementById("chat-box");
    connectionStatus = document.getElementById("connection-status"); // Ensure this element exists in HTML
    const sendButton = document.getElementById("send-button");

    // Add animation class to chat button
    if (chatOpenButton) {
        chatOpenButton.classList.add('animate');
        // Remove animation after 5 seconds
        setTimeout(() => {
            chatOpenButton.classList.remove('animate');
        }, 5000);
    }

    // Initialize resize functionality
    initResizableChatbox(); // This now enforces bottom-right

    // Ensure chat popup is hidden on load
    hideChat();

    // Initial load of user info and sender_id (even if chat is hidden)
    await loadChatbotConfig();

    // Set up chat open button listener
    if (chatOpenButton) {
        chatOpenButton.addEventListener("click", async function(e) {
            e.preventDefault();
            console.log("Chat open button clicked");

            if (chatPopup) {
                if (chatPopup.classList.contains("hidden")) {
                    // Open chat
                    showChat(); // This now enforces bottom-right position
                    if (messageInput) messageInput.focus();

                    // Initialize chat if not already initialized
                    if (chatHistory.length === 0) {
                    chatHistory = loadChatHistory();
                    if (chatHistory.length === 0) {
                            const welcomeMsg = chatbotSettings.defaultBotName || 'HardHat Assistant';
                            const welcomeText = `Welcome to Hardhat Enterprises. How can I help you today?`;
                            addMessage({ 
                                sender: 'bot', 
                                text: welcomeText, 
                                timestamp: Date.now() 
                            });
                        addSuggestedQuestions();
                        setTimeout(() => {
                           const firstMsg = chatBox.querySelector('.message:first-child');
                           if(firstMsg) scrollToMessageStart(firstMsg);
                        }, 150);
                    }
                    }
                } else {
                    hideChat();
                }
            }
        });
    }

    // Add event listener for the close button
    if (chatCloseButton) {
        chatCloseButton.addEventListener("click", function(e) {
            e.preventDefault();
            console.log("Chat close button clicked");
            hideChat();
        });
    }

    // Add event listener for the send button
    if (sendButton) {
        sendButton.addEventListener("click", function(e) {
            e.preventDefault();
            sendMessage();
        });
    }

    // Add event listener for the message input
    if (messageInput) {
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
                e.preventDefault();
            sendMessage();
        }
    });
    }

    // Auto open chat if configured to do so
    if (chatbotSettings.autoOpenOnFirstVisit && !localStorage.getItem('chatbot-opened-before')) {
        setTimeout(() => {
            if (chatOpenButton) {
                chatOpenButton.click();
                localStorage.setItem('chatbot-opened-before', 'true');
            }
        }, 2000); // Delay 2 seconds before auto-opening
    }

    // Add event listener for the reset chat button
    const resetChatButton = document.getElementById("resetChatButton");
    if (resetChatButton) {
        resetChatButton.addEventListener("click", function(e) {
            e.preventDefault();
            resetChat();
        });
    }
});

// Resize Functions - Refined for fixed bottom-right positioning
function initResizableChatbox() {
    const chatPopup = document.getElementById("chat-popup");
    if (!chatPopup) return;

    // Remove previous handles if they exist
    chatPopup.querySelectorAll('[class^="resize-handle-"]').forEach(h => h.remove());

    // Create side resize handles ONLY for left and top (relative to the element)
    const handleNames = ['left', 'top'];
    handleNames.forEach(side => {
        const sideHandle = document.createElement('div');
        sideHandle.className = `resize-handle-${side}`;
        chatPopup.appendChild(sideHandle);
    });

    // Initialize side resize functionality for left and top only
    setupSideResize(chatPopup); // This internal function sets up both handles

    // Apply stored dimensions (width and height)
    const storedWidth = localStorage.getItem('chatbot-width') || '350px'; // Provide default
    const storedHeight = localStorage.getItem('chatbot-height') || '500px'; // Provide default

    chatPopup.style.width = storedWidth;
    chatPopup.style.height = storedHeight;

     // Always set position to bottom right regardless of history
     chatPopup.style.position = 'fixed'; // Ensure it's fixed
     chatPopup.style.right = "20px";
     chatPopup.style.bottom = "20px";
     chatPopup.style.left = "auto";
     chatPopup.style.top = "auto";


    // Ensure chat scrolls to bottom after applying dimensions
    setTimeout(scrollChatToBottom, 100);
}

// Function to setup side resize functionality (now only for left and top)
function setupSideResize(chatPopup) {
    const leftHandle = chatPopup.querySelector('.resize-handle-left');
    const topHandle = chatPopup.querySelector('.resize-handle-top');

    if (leftHandle) setupLeftResize(chatPopup, leftHandle);
    if (topHandle) setupTopResize(chatPopup, topHandle);
}

// Left side resize (keeps bottom/right fixed)
function setupLeftResize(chatPopup, handle) {
    let startX, startWidth;

    const startResize = (e) => {
        // Use pageX/pageY for touch events, clientX/clientY for mouse
        startX = e.type.startsWith('touch') ? e.touches[0].pageX : e.clientX;
        startWidth = parseInt(document.defaultView.getComputedStyle(chatPopup).width, 10);
        document.body.style.userSelect = 'none'; // Prevent text selection during drag
        chatPopup.classList.add('resizing');

        document.addEventListener('mousemove', resize);
        document.addEventListener('touchmove', resize, { passive: false }); // Need passive false to prevent scroll
        document.addEventListener('mouseup', stopResize);
        document.addEventListener('touchend', stopResize);
    };

    const resize = (e) => {
        if (e.type === 'touchmove') e.preventDefault(); // Prevent page scroll on touch

        const currentX = e.type.startsWith('touch') ? e.touches[0].pageX : e.clientX;
        const dx = currentX - startX;
        let newWidth = startWidth - dx;

        const minWidth = 300;
        const maxWidth = window.innerWidth - 40; // Max width considering potential padding/margins

        newWidth = Math.max(minWidth, Math.min(newWidth, maxWidth)); // Clamp width

        chatPopup.style.width = `${newWidth}px`;
        // Position is fixed bottom-right, no need to adjust left/right here
    };

    const stopResize = () => {
        document.body.style.userSelect = ''; // Re-enable text selection
        chatPopup.classList.remove('resizing');
        localStorage.setItem('chatbot-width', chatPopup.style.width); // Save final width
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('touchmove', resize);
        document.removeEventListener('mouseup', stopResize);
        document.removeEventListener('touchend', stopResize);
        // No scroll needed here, scroll handled by message adding
    };

    handle.addEventListener('mousedown', startResize);
    handle.addEventListener('touchstart', startResize, { passive: false });
}

// Top side resize (keeps bottom/right fixed)
function setupTopResize(chatPopup, handle) {
    let startY, startHeight;

    const startResize = (e) => {
        startY = e.type.startsWith('touch') ? e.touches[0].pageY : e.clientY;
        startHeight = parseInt(document.defaultView.getComputedStyle(chatPopup).height, 10);
        document.body.style.userSelect = 'none';
        chatPopup.classList.add('resizing');

        document.addEventListener('mousemove', resize);
        document.addEventListener('touchmove', resize, { passive: false });
        document.addEventListener('mouseup', stopResize);
        document.addEventListener('touchend', stopResize);
    };

    const resize = (e) => {
        if (e.type === 'touchmove') e.preventDefault();

        const currentY = e.type.startsWith('touch') ? e.touches[0].pageY : e.clientY;
        const dy = currentY - startY;
        let newHeight = startHeight - dy;

        const minHeight = 300; // Adjusted min height
        const maxHeight = window.innerHeight - 40; // Max height considering potential padding/margins

        newHeight = Math.max(minHeight, Math.min(newHeight, maxHeight)); // Clamp height

        chatPopup.style.height = `${newHeight}px`;
        // Position is fixed bottom-right, no need to adjust top/bottom here
    };

    const stopResize = () => {
        document.body.style.userSelect = '';
        chatPopup.classList.remove('resizing');
        localStorage.setItem('chatbot-height', chatPopup.style.height); // Save final height
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('touchmove', resize);
        document.removeEventListener('mouseup', stopResize);
        document.removeEventListener('touchend', stopResize);
         // Scroll to bottom might be useful after height resize
        setTimeout(scrollChatToBottom, 50);
    };

    handle.addEventListener('mousedown', startResize);
    handle.addEventListener('touchstart', startResize, { passive: false });
}

// scrollToMessageStart already refined above

// scrollToSixthMessage (utility/debug function)
function scrollToSixthMessage() {
    const sixthMessage = chatBox.querySelector('.message:nth-child(6)');
    if(sixthMessage) {
        scrollToMessageStart(sixthMessage);
    } else {
        console.log("Sixth message not found.");
    }
}

// Final notes comment block
/*
Note on JS Consolidation:
If you also have chat logic in `chatbot_views.js`, ensure you are only using *one* script
for the floating chat popup to avoid conflicts. This script (`chatbot.js`) is now updated
assuming it's the primary client for the popup. Adapt or remove `chatbot_views.js` as needed
based on whether you have a separate dedicated chat page.
*/ 