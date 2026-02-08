/**
 * University Admissions Chatbot - Frontend JavaScript
 * Handles chat interactions, API communication, and UI updates
 */

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',
    MAX_MESSAGE_LENGTH: 500,
    SHOW_COMPRESSION_STATS: true, // Set to false to hide compression stats
    TYPING_DELAY: 500, // ms
    REQUEST_TIMEOUT: 45000 // ms (45 seconds - increased from default)
};

// DOM Elements
const elements = {
    messagesContainer: document.getElementById('messages'),
    userInput: document.getElementById('user-input'),
    sendBtn: document.getElementById('send-btn'),
    typingIndicator: document.getElementById('typing-indicator'),
    themeToggle: document.getElementById('theme-toggle'),
    snackbar: document.getElementById('snackbar'),
    snackbarMessage: document.getElementById('snackbar-message'),
    compressionStats: document.getElementById('compression-stats'),
    statsText: document.getElementById('stats-text'),
    quickActionChips: document.querySelectorAll('.chip')
};

// State
const state = {
    conversationHistory: [],
    isProcessing: false,
    currentTheme: 'light'
};

// ========================================
// INITIALIZATION
// ========================================

function init() {
    // Load saved theme
    loadTheme();

    // Event listeners
    elements.sendBtn.addEventListener('click', handleSendMessage);
    elements.userInput.addEventListener('keypress', handleKeyPress);
    elements.themeToggle.addEventListener('click', toggleTheme);

    // Quick action chips
    elements.quickActionChips.forEach(chip => {
        chip.addEventListener('click', handleQuickAction);
    });

    // Auto-focus input
    elements.userInput.focus();

    // Check backend health
    checkBackendHealth();

    console.log('University Admissions Chatbot initialized');
}

// ========================================
// MESSAGE HANDLING
// ========================================

async function handleSendMessage() {
    const message = elements.userInput.value.trim();

    if (!message || state.isProcessing) {
        return;
    }

    if (message.length > CONFIG.MAX_MESSAGE_LENGTH) {
        showSnackbar(`Message too long. Maximum ${CONFIG.MAX_MESSAGE_LENGTH} characters.`);
        return;
    }

    // Clear input
    elements.userInput.value = '';

    // Add user message to UI
    addMessage(message, 'user');

    // Set processing state
    state.isProcessing = true;
    elements.sendBtn.disabled = true;

    // Show typing indicator with initial status
    showTypingIndicator('Processing...');

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CONFIG.REQUEST_TIMEOUT);

    try {
        // Update status: Compressing context
        setTimeout(() => updateTypingIndicator('Compressing context...'), 500);

        // Send to backend
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: state.conversationHistory
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        // Update status: Generating response
        updateTypingIndicator('Generating response...');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        if (data.error) {
            showSnackbar(data.message || 'An error occurred');
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } else {
            // Add bot response
            addMessage(data.response, 'bot');

            // Update conversation history
            state.conversationHistory.push({
                user: message,
                assistant: data.response
            });

            // Show compression stats if enabled
            if (CONFIG.SHOW_COMPRESSION_STATS && data.compression_stats) {
                showCompressionStats(data.compression_stats);
            }
        }

    } catch (error) {
        console.error('Chat error:', error);
        clearTimeout(timeoutId);
        hideTypingIndicator();

        let errorMessage;
        if (error.name === 'AbortError') {
            errorMessage = 'Request timed out. The server is taking too long to respond. Please try again.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Cannot connect to server. Please make sure the backend is running.';
        } else {
            errorMessage = `Error: ${error.message}`;
        }

        showSnackbar(errorMessage);
        addMessage('Sorry, I could not process your request. Please check your connection and try again.', 'bot');
    } finally {
        // Reset processing state
        state.isProcessing = false;
        elements.sendBtn.disabled = false;
        elements.userInput.focus();
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleSendMessage();
    }
}

function handleQuickAction(event) {
    const chip = event.currentTarget;
    const query = chip.getAttribute('data-query');

    if (query) {
        elements.userInput.value = query;
        handleSendMessage();
    }
}

// ========================================
// UI UPDATES
// ========================================

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    // Create avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    const avatarIcon = document.createElement('span');
    avatarIcon.className = 'material-icons';
    avatarIcon.textContent = type === 'user' ? 'person' : 'support_agent';
    avatarDiv.appendChild(avatarIcon);

    // Create message bubble
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Format message text (support for basic HTML)
    contentDiv.innerHTML = formatMessageText(text);

    bubbleDiv.appendChild(contentDiv);

    // Assemble message
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);

    // Add to container
    elements.messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();
}

function formatMessageText(text) {
    // Escape HTML to prevent XSS
    const escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');

    // Convert line breaks to <br>
    let formatted = escaped.replace(/\n/g, '<br>');

    // Convert **bold** to <strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Convert bullet points - and *
    formatted = formatted.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');

    // Wrap consecutive list items in ul tags
    formatted = formatted.replace(/(<li>.*?<\/li>(<br>)?)+/g, function(match) {
        return '<ul>' + match.replace(/<br>/g, '') + '</ul>';
    });

    // Convert numbered lists
    formatted = formatted.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');

    // Wrap consecutive numbered list items in ol tags
    formatted = formatted.replace(/(<li>.*?<\/li>(<br>)?)+/g, function(match) {
        // Only wrap if not already wrapped in ul
        if (!match.includes('<ul>')) {
            return '<ol>' + match.replace(/<br>/g, '') + '</ol>';
        }
        return match;
    });

    return formatted;
}

function showTypingIndicator(message = 'Typing...') {
    elements.typingIndicator.style.display = 'flex';
    const dots = elements.typingIndicator.querySelector('.typing-dots');
    if (dots) {
        const textSpan = document.createElement('span');
        textSpan.className = 'typing-status';
        textSpan.textContent = message;
        textSpan.style.marginLeft = '8px';
        textSpan.style.fontSize = '0.85em';
        textSpan.style.opacity = '0.7';

        // Remove existing status if any
        const existing = elements.typingIndicator.querySelector('.typing-status');
        if (existing) existing.remove();

        dots.appendChild(textSpan);
    }
    scrollToBottom();
}

function updateTypingIndicator(message) {
    const statusSpan = elements.typingIndicator.querySelector('.typing-status');
    if (statusSpan) {
        statusSpan.textContent = message;
    }
}

function hideTypingIndicator() {
    elements.typingIndicator.style.display = 'none';
    // Clean up status message
    const statusSpan = elements.typingIndicator.querySelector('.typing-status');
    if (statusSpan) statusSpan.remove();
}

function scrollToBottom() {
    setTimeout(() => {
        elements.messagesContainer.parentElement.scrollTop =
            elements.messagesContainer.parentElement.scrollHeight;
    }, 100);
}

function showCompressionStats(stats) {
    if (!elements.compressionStats || !elements.statsText) return;

    const original = stats.original_tokens || 0;
    const compressed = stats.compressed_tokens || 0;
    const cached = stats.cached || false;

    if (original > 0 && compressed > 0) {
        const reduction = ((original - compressed) / original * 100).toFixed(1);
        const cacheText = cached ? ' (cached ⚡)' : '';
        elements.statsText.textContent = `Compressed: ${original} → ${compressed} tokens (${reduction}% reduction)${cacheText}`;
        elements.compressionStats.style.display = 'flex';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            elements.compressionStats.style.display = 'none';
        }, 5000);
    }
}

function showSnackbar(message) {
    if (!elements.snackbar || !elements.snackbarMessage) return;

    elements.snackbarMessage.textContent = message;
    elements.snackbar.style.display = 'block';

    // Auto-hide after 4 seconds
    setTimeout(() => {
        elements.snackbar.style.display = 'none';
    }, 4000);
}

// ========================================
// THEME MANAGEMENT
// ========================================

function toggleTheme() {
    state.currentTheme = state.currentTheme === 'light' ? 'dark' : 'light';
    applyTheme();
    saveTheme();
}

function applyTheme() {
    document.body.setAttribute('data-theme', state.currentTheme);

    // Update theme icon
    const icon = elements.themeToggle.querySelector('.material-icons');
    icon.textContent = state.currentTheme === 'light' ? 'dark_mode' : 'light_mode';
}

function saveTheme() {
    try {
        localStorage.setItem('theme', state.currentTheme);
    } catch (e) {
        console.warn('Could not save theme preference:', e);
    }
}

function loadTheme() {
    try {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
            state.currentTheme = savedTheme;
        }
    } catch (e) {
        console.warn('Could not load theme preference:', e);
    }

    applyTheme();
}

// ========================================
// BACKEND HEALTH CHECK
// ========================================

async function checkBackendHealth() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Backend health:', data);

            if (data.status !== 'healthy') {
                showSnackbar('Backend is not fully operational. Some features may not work.');
            }
        } else {
            throw new Error('Health check failed');
        }

    } catch (error) {
        console.error('Backend health check failed:', error);
        showSnackbar('Warning: Cannot connect to backend server. Please start the backend.');
    }
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

function clearChat() {
    // Clear messages (keep welcome message)
    const welcomeMessage = elements.messagesContainer.querySelector('.bot-message');
    elements.messagesContainer.innerHTML = '';
    if (welcomeMessage) {
        elements.messagesContainer.appendChild(welcomeMessage);
    }

    // Clear history
    state.conversationHistory = [];

    console.log('Chat cleared');
}

function exportChat() {
    const messages = Array.from(elements.messagesContainer.querySelectorAll('.message'));
    const chatLog = messages.map(msg => {
        const type = msg.classList.contains('user-message') ? 'User' : 'Bot';
        const content = msg.querySelector('.message-content').textContent;
        return `${type}: ${content}`;
    }).join('\n\n');

    // Create downloadable file
    const blob = new Blob([chatLog], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-log-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('Chat exported');
}

// ========================================
// KEYBOARD SHORTCUTS
// ========================================

document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + K: Focus input
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        elements.userInput.focus();
    }

    // Ctrl/Cmd + L: Clear chat
    if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
        event.preventDefault();
        if (confirm('Clear chat history?')) {
            clearChat();
        }
    }

    // Escape: Blur input
    if (event.key === 'Escape') {
        elements.userInput.blur();
    }
});

// ========================================
// AUTO-SUGGESTIONS (Future Enhancement)
// ========================================

const SUGGESTED_QUESTIONS = [
    "What are the admission requirements?",
    "What programs do you offer?",
    "How much is tuition?",
    "What is the application deadline?",
    "Do you offer scholarships?",
    "What are the housing options?",
    "How do I apply as an international student?",
    "What is the acceptance rate?"
];

// ========================================
// START APPLICATION
// ========================================

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export functions for debugging (accessible via browser console)
window.chatbot = {
    clearChat,
    exportChat,
    checkHealth: checkBackendHealth,
    state,
    config: CONFIG
};

console.log('💬 University Admissions Chatbot loaded');
console.log('📝 Available commands: chatbot.clearChat(), chatbot.exportChat(), chatbot.checkHealth()');
