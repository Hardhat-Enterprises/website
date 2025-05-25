// Configuration for the Hardhat Enterprises Chatbot

// Define API endpoints
const CHATBOT_API = {
    // Message API endpoint to send and receive messages
    MESSAGE_API: '/api/message/',
    
    // Session creation endpoint
    SESSION_CREATE: '/api/session/create/',
    
    // Session details endpoint (format: /api/session/{session_id}/)
    SESSION_DETAIL: '/api/session/',
    
    // Connection verification endpoint
    VERIFY_CONNECTION: '/api/verify/',
    
    // Configuration endpoint
    CONFIG: '/api/config/'
};

// Default chatbot settings
const CHATBOT_SETTINGS = {
    initialMessageDelay: 500,
    typingIndicatorDelay: 1000,
    autoOpenOnFirstVisit: false,
    persistHistory: true,
    maxHistoryLength: 50,
    defaultBotName: 'HardHat Assistant'
};

// Export configuration
window.CHATBOT_CONFIG = {
    API: CHATBOT_API,
    SETTINGS: CHATBOT_SETTINGS
}; 