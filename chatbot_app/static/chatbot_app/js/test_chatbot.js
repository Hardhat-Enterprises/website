// Test script for chatbot functionality
// This script helps identify issues with API endpoints and responses

document.addEventListener('DOMContentLoaded', function() {
    // Configuration - API endpoints
    const endpoints = {
        config: '/api/config/',
        user: '/get-current-user/',
        verify: '/api/verify/',
        message: '/api/message/'
    };

    // Create test interface
    const testContainer = document.createElement('div');
    testContainer.id = 'chatbot-test-container';
    testContainer.style.padding = '20px';
    testContainer.style.backgroundColor = '#f5f5f5';
    testContainer.style.border = '1px solid #ddd';
    testContainer.style.margin = '20px';

    testContainer.innerHTML = `
        <h2>Chatbot API Test Tool</h2>
        <div>
            <button id="test-config">Test Config API</button>
            <button id="test-user">Test User API</button>
            <button id="test-verify">Test Verify API</button>
            <button id="test-message">Test Message API</button>
        </div>
        <div style="margin-top: 10px;">
            <label>Test message: <input type="text" id="test-message-input" value="Tell me about AppAttack"></label>
        </div>
        <div style="margin-top: 20px;">
            <h3>API Response</h3>
            <pre id="test-response" style="background: #000; color: #fff; padding: 10px; overflow: auto; max-height: 400px;">No test run yet</pre>
        </div>
    `;

    document.body.appendChild(testContainer);

    // Function to display test results
    function displayResult(title, response, error = null) {
        const resultElement = document.getElementById('test-response');
        
        let content = `=== ${title} ===\n`;
        
        if (error) {
            content += `ERROR: ${error}\n`;
        }
        
        if (response) {
            if (typeof response === 'object') {
                content += JSON.stringify(response, null, 2);
            } else {
                content += response.toString();
            }
        }
        
        resultElement.textContent = content;
    }

    // Function to get sender ID from local storage or generate one
    function getSenderId() {
        let senderId = localStorage.getItem('chatbot_sender_id');
        if (!senderId) {
            senderId = ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
            localStorage.setItem('chatbot_sender_id', senderId);
        }
        return senderId;
    }

    // Test config API
    document.getElementById('test-config').addEventListener('click', async function() {
        try {
            const response = await fetch(endpoints.config);
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            }
            const data = await response.json();
            displayResult('Config API Test', data);
        } catch (error) {
            displayResult('Config API Test', null, error.toString());
        }
    });

    // Test user API
    document.getElementById('test-user').addEventListener('click', async function() {
        try {
            const response = await fetch(endpoints.user);
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            }
            const data = await response.json();
            displayResult('User API Test', data);
        } catch (error) {
            displayResult('User API Test', null, error.toString());
        }
    });

    // Test verify API
    document.getElementById('test-verify').addEventListener('click', async function() {
        try {
            const response = await fetch(endpoints.verify);
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            }
            const data = await response.json();
            displayResult('Verify API Test', data);
        } catch (error) {
            displayResult('Verify API Test', null, error.toString());
        }
    });

    // Test message API
    document.getElementById('test-message').addEventListener('click', async function() {
        try {
            const messageText = document.getElementById('test-message-input').value.trim();
            if (!messageText) {
                throw new Error('Please enter a test message');
            }

            const senderId = getSenderId();
            
            // Get CSRF token for Django
            const csrfToken = getCookie('csrftoken');
            
            // Display test being performed
            displayResult('Message API Test', {
                'test_in_progress': true,
                'message': messageText,
                'sender_id': senderId
            });

            const response = await fetch(endpoints.message, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Accept': 'application/json',
                    ...(csrfToken && { 'X-CSRFToken': csrfToken })
                },
                body: JSON.stringify({
                    message: messageText,
                    sender: senderId
                })
            });

            // Get full response text
            let respText;
            try {
                respText = await response.text();
            } catch (e) {
                respText = "Could not read response body";
            }

            // Try parsing as JSON if possible
            let data;
            try {
                data = JSON.parse(respText);
                displayResult('Message API Test', {
                    status: response.status,
                    statusText: response.statusText,
                    headers: Object.fromEntries([...response.headers]),
                    data: data
                });
            } catch (jsonError) {
                // Display as text if not JSON
                displayResult('Message API Test', {
                    status: response.status,
                    statusText: response.statusText,
                    headers: Object.fromEntries([...response.headers]),
                    rawResponse: respText
                });
            }
        } catch (error) {
            displayResult('Message API Test', null, error.toString());
        }
    });

    // Helper function to get cookie (for CSRF)
    function getCookie(name) {
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

    console.log('Chatbot test script loaded');
}); 