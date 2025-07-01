// UTM Campus Assistant Chatbot - Client-side JavaScript

class ChatBot {
    constructor() {
        this.messagesContainer = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatForm = document.getElementById('chatForm');
        
        this.isTyping = false;
        this.messageCount = 0;
        
        this.initializeEventListeners();
        this.scrollToBottom();
    }
    
    initializeEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Quick action buttons
        document.querySelectorAll('.quick-action').forEach(button => {
            button.addEventListener('click', () => {
                const message = button.getAttribute('data-message');
                this.messageInput.value = message;
                this.sendMessage();
            });
        });
        
        // Enter key handling
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize input (if needed for multi-line)
        this.messageInput.addEventListener('input', () => {
            this.adjustInputHeight();
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isTyping) {
            return;
        }
        
        // Disable input and show loading state
        this.setInputState(false);
        
        // Get chat history
        const history = this.getChatHistory();

        // Add user message to chat
        this.addUserMessage(message);
        
        // Clear input
        this.messageInput.value = '';
        this.adjustInputHeight();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await this.sendToAPI(message, history);
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addBotMessage(response.response, response.intent, response.entities);
            
        } catch (error) {
            console.error('Chat error:', error);
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            // Show error message
            this.addBotMessage(
                "I'm sorry, I'm having trouble processing your request right now. Please try again or contact support for assistance.",
                'error'
            );
        } finally {
            // Re-enable input
            this.setInputState(true);
            this.messageInput.focus();
        }
    }
    
    async sendToAPI(message, history) {
        // Prepare chat history if not provided
        if (!history) {
            history = [];
        }
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: history // <-- send history to backend
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }
    
    getChatHistory() {
        const messages = [];
        this.messagesContainer.querySelectorAll('.message').forEach(msgDiv => {
            // User message
            if (msgDiv.classList.contains('user-message')) {
                const text = msgDiv.querySelector('.message-bubble p')?.textContent || '';
                messages.push({ sender: 'user', text });
            }
            // Bot message
            else if (msgDiv.classList.contains('bot-message')) {
                // Get the first child div inside .message-bubble (the actual bot reply)
                const bubble = msgDiv.querySelector('.message-bubble');
                let text = '';
                if (bubble) {
                    // Find the first child that is a DIV and not a time/debug info
                    const firstDiv = Array.from(bubble.children).find(
                        el => el.tagName === 'DIV' && !el.className.includes('message-time')
                    );
                    text = firstDiv ? firstDiv.textContent : bubble.textContent;
                }
                messages.push({ sender: 'bot', text: text.trim() });
            }
            // System message
            else if (msgDiv.classList.contains('system-message')) {
                const text = msgDiv.textContent || '';
                messages.push({ sender: 'system', text });
            }
        });
        return messages;
    }

    addUserMessage(message) {
        const messageElement = this.createMessageElement(message, true);
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
        this.messageCount++;
    }
    
    addBotMessage(message, intent = null, entities = null) {
        const messageElement = this.createMessageElement(message, false, intent, entities);
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
        this.messageCount++;
    }
    
    createMessageElement(message, isUser, intent = null, entities = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="d-flex align-items-start justify-content-end">
                        <div class="message-bubble bg-primary text-white p-3 rounded me-2">
                            <p class="mb-0">${this.escapeHtml(message)}</p>
                            <div class="message-time text-end mt-1" style="font-size: 0.7rem; opacity: 0.8;">
                                ${timestamp}
                            </div>
                        </div>
                        <div class="user-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                    </div>
                </div>
            `;
        } else {
            let debugInfo = '';
            if (intent || entities) {
                debugInfo = `
                    <div class="mt-2 p-2 rounded" style="font-size: 0.75rem; background-color: #e2e3e5;">
                        ${intent ? `<div><strong>Intent:</strong> ${intent}</div>` : ''}
                        ${entities && Object.keys(entities).length > 0 ? `<div><strong>Entities:</strong> ${JSON.stringify(entities)}</div>` : ''}
                    </div>
                `;
            }
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="d-flex align-items-start">
                        <div class="bot-avatar me-2">
                            <i class="fas fa-robot text-primary"></i>
                        </div>
                        <div class="message-bubble bg-light p-3 rounded">
                            <div>${this.formatBotMessage(message)}</div>
                            <div class="message-time mt-1" style="font-size: 0.7rem; color: #6c757d;">
                                ${timestamp}
                            </div>
                            ${debugInfo}
                        </div>
                    </div>
                </div>
            `;
        }
        
        return messageDiv;
    }
    
    formatBotMessage(message) {
        // Convert newlines to breaks and format lists
        let formatted = this.escapeHtml(message);

        // Convert newlines to <br>
        formatted = formatted.replace(/\n/g, '<br>');

        // Convert numbered lists
        formatted = formatted.replace(/(\d+\.\s)/g, '<br>$1');

        // Convert bullet points
        formatted = formatted.replace(/(\*\s|\-\s)/g, '<br>• ');

        // Convert URLs to links
        formatted = formatted.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" class="text-decoration-none">$1</a>'
        );

        // Bold text
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        return formatted;
    }
    
    showTypingIndicator() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator-message';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="d-flex align-items-start">
                    <div class="bot-avatar me-2">
                        <i class="fas fa-robot text-primary"></i>
                    </div>
                    <div class="typing-indicator">
                        <span class="text-muted small">Assistant is typing</span>
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = this.messagesContainer.querySelector('.typing-indicator-message');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.classList.remove('btn-loading');
            this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        } else {
            this.sendButton.classList.add('btn-loading');
            this.sendButton.innerHTML = '';
        }
    }
    
    adjustInputHeight() {
        // Reset height to auto to get the correct scrollHeight
        this.messageInput.style.height = 'auto';
        
        // Set the height to match the content, with a maximum
        const maxHeight = 120; // Maximum height in pixels
        const newHeight = Math.min(this.messageInput.scrollHeight, maxHeight);
        
        this.messageInput.style.height = newHeight + 'px';
    }
    
    scrollToBottom() {
        requestAnimationFrame(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Public methods for external use
    addSystemMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message text-center';
        messageDiv.innerHTML = `
            <div class="alert alert-info py-2 px-3 d-inline-block">
                <small><i class="fas fa-info-circle me-1"></i>${this.escapeHtml(message)}</small>
            </div>
        `;
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    clearChat() {
        // Keep only the welcome message
        const messages = this.messagesContainer.querySelectorAll('.message:not(:first-child)');
        messages.forEach(message => message.remove());
        this.messageCount = 1; // Reset count but keep welcome message
    }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.chatBot = new ChatBot();
    
    // Add some helpful keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+L or Cmd+L to clear chat
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            if (confirm('Clear chat history?')) {
                window.chatBot.clearChat();
                window.chatBot.addSystemMessage('Chat history cleared');
            }
        }
        
        // Escape to focus on input
        if (e.key === 'Escape') {
            window.chatBot.messageInput.focus();
        }
    });
    
    // Handle visibility change to focus input when tab becomes active
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(() => {
                window.chatBot.messageInput.focus();
            }, 100);
        }
    });
    
    // Focus on input initially
    window.chatBot.messageInput.focus();
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatBot;
}
