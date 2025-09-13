/**
 * Working Healthcare Search Assistant - Guaranteed Functionality
 */

console.log('🚀 Loading working.js...');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM loaded, initializing...');
    
    // Get elements
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const charCount = document.getElementById('charCount');
    const chatHistory = document.getElementById('chatHistory');
    const queryButtons = document.querySelectorAll('.query-btn');
    
    // New elements for radio button functionality
    const quickQueries = document.getElementById('quickQueries');
    const queryList = document.getElementById('queryList');
    // Buttons removed - auto-select on radio button click
    const resizeHandle = document.getElementById('resizeHandle');
    
    // Section resize elements
    const leftSection = document.getElementById('leftSection');
    const rightSection = document.getElementById('rightSection');
    const leftSectionResizeHandle = document.getElementById('leftSectionResizeHandle');
    const rightSectionResizeHandle = document.getElementById('rightSectionResizeHandle');
    
    // Logs section elements
    const logsSection = document.getElementById('logsSection');
    const logsContent = document.getElementById('logsContent');
    const clearLogsBtn = document.getElementById('clearLogsBtn');
    const toggleLogsBtn = document.getElementById('toggleLogsBtn');
    
    console.log('📋 Elements found:', {
        messageInput: !!messageInput,
        sendBtn: !!sendBtn,
        clearChatBtn: !!clearChatBtn,
        charCount: !!charCount,
        chatHistory: !!chatHistory,
        queryButtons: queryButtons.length,
        quickQueries: !!quickQueries,
        queryList: !!queryList,
        // Buttons removed
        resizeHandle: !!resizeHandle,
        leftSection: !!leftSection,
        rightSection: !!rightSection,
        leftSectionResizeHandle: !!leftSectionResizeHandle,
        rightSectionResizeHandle: !!rightSectionResizeHandle
    });
    
    // Add message to chat
    function addMessage(content, isUser = false) {
        console.log(`💬 Adding ${isUser ? 'user' : 'bot'} message:`, content);
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = `<p>${content}</p>`;
        
        messageDiv.appendChild(messageContent);
        chatHistory.appendChild(messageDiv);
        
        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Send message function
    async function sendMessage() {
        console.log('📤 Send message called');
        addLogEntry('info', 'Send message initiated');
        
        if (!messageInput) {
            console.error('❌ Message input not found');
            addLogEntry('error', 'Message input element not found');
            return;
        }
        
        const message = messageInput.value.trim();
        console.log('📝 Message:', message);
        addLogEntry('info', 'Processing query', { query: message });
        
        if (!message) {
            console.log('⚠️ Empty message, ignoring');
            addLogEntry('warning', 'Empty message ignored');
            return;
        }
        
        // Add user message
        addMessage(message, true);
        
        // Clear input
        messageInput.value = '';
        updateCharCount();
        
        // Disable send button
        if (sendBtn) {
            sendBtn.disabled = true;
            sendBtn.textContent = 'Sending...';
        }
        
        try {
            console.log('🌐 Calling API...');
            addLogEntry('debug', 'Making API request to /api/chat');
            const startTime = Date.now();
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: []
                })
            });
            
            const endTime = Date.now();
            const duration = endTime - startTime;
            
            console.log('📥 API response status:', response.status);
            addLogEntry('debug', `API response received`, { 
                status: response.status, 
                duration: `${duration}ms` 
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                addLogEntry('error', `HTTP error: ${response.status}`, { 
                    status: response.status,
                    response: errorText 
                });
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📊 API data:', data);
            addLogEntry('success', 'Query processed successfully', { 
                responseType: typeof data.response,
                hasResults: !!(data.results && data.results.length > 0),
                resultCount: data.results ? data.results.length : 0
            });
            
            // Add bot response
            if (data.response) {
                addMessage(data.response);
                addLogEntry('info', 'Bot response added to chat');
            } else {
                addMessage('I received your message but couldn\'t process it properly.');
                addLogEntry('warning', 'No response data from API');
            }
            
        } catch (error) {
            console.error('❌ API Error:', error);
            addLogEntry('error', 'Query processing failed', { 
                error: error.message,
                stack: error.stack 
            });
            addMessage('Sorry, I encountered an error: ' + error.message);
        } finally {
            // Re-enable send button
            if (sendBtn) {
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
            }
        }
    }
    
    // Update character count
    function updateCharCount() {
        if (charCount && messageInput) {
            const count = messageInput.value.length;
            charCount.textContent = `${count}/500`;
            
            if (count > 450) {
                charCount.style.color = '#dc2626';
            } else if (count > 400) {
                charCount.style.color = '#d97706';
            } else {
                charCount.style.color = '#64748b';
            }
        }
    }
    
    // Clear chat function
    function clearChat() {
        console.log('🗑️ Clearing chat...');
        if (chatHistory) {
            chatHistory.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">
                        <p><strong>Chat cleared!</strong></p>
                        <p>How can I help you today?</p>
                    </div>
                </div>
            `;
        }
    }
    
    // Handle quick query buttons (legacy support)
    function handleQuickQuery(query) {
        console.log('🔘 Quick query clicked:', query);
        if (messageInput) {
            messageInput.value = query;
            updateCharCount();
            sendMessage();
        }
    }
    
    // Handle radio button selection - removed duplicate function
    
    // Copy selected query to input (don't auto-submit)
    function copyQueryToInput() {
        const selectedRadio = document.querySelector('input[name="quickQuery"]:checked');
        if (selectedRadio && messageInput) {
            const queryText = selectedRadio.value;
            console.log('📝 Copying query to input:', queryText);
            
            // Copy the query text to the message input
            messageInput.value = queryText;
            
            // Update character count
            updateCharCount();
            
            // Auto-resize the textarea
            autoResizeTextarea();
            
            // Focus the input for immediate editing if needed
            messageInput.focus();
        } else {
            console.log('⚠️ No query selected or input not found');
        }
    }
    
    // Clear selection
    // Clear selection function removed - not needed with copy-only behavior
    
    // Logging functionality
    function addLogEntry(level, message, details = null) {
        const logsContent = document.getElementById('logsContent');
        const logsSection = document.getElementById('logsSection');
        
        if (!logsContent) return;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit',
            fractionalSecondDigits: 3
        });
        
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${level}`;
        
        let logHtml = `
            <span class="log-time">[${timeString}]</span>
            <span class="log-level ${level}">${level.toUpperCase()}</span>
            <span class="log-message">${message}</span>
        `;
        
        if (details) {
            logHtml += `<div style="margin-left: 120px; margin-top: 0.25rem; color: #9ca3af; font-size: 0.7rem;">${details}</div>`;
        }
        
        logEntry.innerHTML = logHtml;
        logsContent.appendChild(logEntry);
        
        // Auto-scroll to bottom
        logsContent.scrollTop = logsContent.scrollHeight;
        
        // Show logs section if it was hidden
        if (logsSection && logsSection.style.display === 'none') {
            logsSection.style.display = 'flex';
        }
        
        console.log(`[${level.toUpperCase()}] ${message}`, details || '');
    }
    
    function clearLogs() {
        const logsContent = document.getElementById('logsContent');
        if (logsContent) {
            logsContent.innerHTML = '';
            addLogEntry('info', 'Logs cleared');
        }
    }
    
    function toggleLogs() {
        const logsSection = document.getElementById('logsSection');
        const toggleBtn = document.getElementById('toggleLogsBtn');
        
        if (logsSection && toggleBtn) {
            if (logsSection.style.display === 'none') {
                logsSection.style.display = 'flex';
                toggleBtn.textContent = 'Hide Logs';
            } else {
                logsSection.style.display = 'none';
                toggleBtn.textContent = 'Show Logs';
            }
        }
    }
    
    // Log button event listeners - moved to avoid duplicates
    
    function clearLogs() {
        if (logsContent) {
            logsContent.innerHTML = '';
            addLogEntry('info', 'Logs cleared');
        }
    }
    
    function toggleLogs() {
        if (logsSection) {
            const isHidden = logsSection.style.display === 'none';
            logsSection.style.display = isHidden ? 'flex' : 'none';
            if (toggleLogsBtn) {
                toggleLogsBtn.textContent = isHidden ? 'Hide Logs' : 'Show Logs';
            }
        }
    }
    
    // Resize functionality
    let isResizing = false;
    let startX = 0;
    let startY = 0;
    let startWidth = 0;
    let startHeight = 0;
    let currentResizeTarget = null;
    
    function startResize(e, target = quickQueries) {
        console.log('🔧 Starting resize for:', target.id);
        isResizing = true;
        currentResizeTarget = target;
        startX = e.clientX;
        startY = e.clientY;
        
        // Get current dimensions
        const rect = target.getBoundingClientRect();
        startWidth = rect.width;
        startHeight = rect.height;
        
        console.log('📏 Initial dimensions:', { 
            target: target.id,
            width: startWidth, 
            height: startHeight 
        });
        
        // Add visual feedback
        target.classList.add('resizing');
        
        // Set appropriate cursor based on target
        if (target === quickQueries) {
            document.body.style.cursor = 'nw-resize'; // Both width and height
        } else if (target === leftSection || target === rightSection) {
            document.body.style.cursor = 'ew-resize'; // Horizontal only
        } else {
            document.body.style.cursor = 'nw-resize'; // Default
        }
        document.body.style.userSelect = 'none';
        
        // Prevent default behavior
        e.preventDefault();
        e.stopPropagation();
        
        // Add event listeners
        document.addEventListener('mousemove', doResize);
        document.addEventListener('mouseup', stopResize);
        
        console.log('✅ Resize started');
    }
    
    function doResize(e) {
        if (!isResizing || !currentResizeTarget) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        // Calculate new dimensions
        const newWidth = startWidth + deltaX;
        const newHeight = startHeight + deltaY;
        
        // Apply constraints based on target
        let minWidth, maxWidth, minHeight, maxHeight;
        
        if (currentResizeTarget === quickQueries) {
            minWidth = 300; maxWidth = 600;
            minHeight = 150; maxHeight = window.innerHeight * 0.5; // 50% max height
        } else if (currentResizeTarget === leftSection) {
            // Left section: 40% to 80% of screen width
            minWidth = window.innerWidth * 0.4; 
            maxWidth = window.innerWidth * 0.8;
            minHeight = 200; maxHeight = window.innerHeight * 0.9;
        } else if (currentResizeTarget === rightSection) {
            // Right section: 20% to 60% of screen width
            minWidth = window.innerWidth * 0.2; 
            maxWidth = window.innerWidth * 0.6;
            minHeight = 200; maxHeight = window.innerHeight * 0.9;
        } else {
            minWidth = 200; maxWidth = window.innerWidth;
            minHeight = 150; maxHeight = window.innerHeight;
        }
        
        const constrainedWidth = Math.max(minWidth, Math.min(maxWidth, newWidth));
        const constrainedHeight = Math.max(minHeight, Math.min(maxHeight, newHeight));
        
        // Apply the new dimensions
        if (currentResizeTarget === quickQueries) {
            // Quick queries can resize both width and height
            currentResizeTarget.style.width = constrainedWidth + 'px';
            currentResizeTarget.style.height = constrainedHeight + 'px';
        } else if (currentResizeTarget === leftSection || currentResizeTarget === rightSection) {
            // Left and right sections only resize width (horizontal only)
            currentResizeTarget.style.width = constrainedWidth + 'px';
        } else {
            // Default behavior
            currentResizeTarget.style.width = constrainedWidth + 'px';
            currentResizeTarget.style.height = constrainedHeight + 'px';
        }
        
        console.log('📐 Resizing to:', { 
            target: currentResizeTarget.id,
            width: constrainedWidth, 
            height: constrainedHeight 
        });
    }
    
    function stopResize() {
        if (!isResizing || !currentResizeTarget) return;
        
        console.log('🛑 Stopping resize...');
        isResizing = false;
        
        // Remove event listeners
        document.removeEventListener('mousemove', doResize);
        document.removeEventListener('mouseup', stopResize);
        
        // Remove visual feedback
        currentResizeTarget.classList.remove('resizing');
        document.body.style.cursor = 'default';
        document.body.style.userSelect = '';
        
        console.log('✅ Resize completed:', {
            target: currentResizeTarget.id,
            width: currentResizeTarget.style.width,
            height: currentResizeTarget.style.height
        });
        
        currentResizeTarget = null;
    }
    
    // Attach event listeners
    console.log('🔗 Attaching event listeners...');
    
    // Send button
    if (sendBtn) {
        sendBtn.addEventListener('click', function(e) {
            console.log('🖱️ Send button clicked');
            e.preventDefault();
            sendMessage();
        });
        console.log('✅ Send button listener attached');
    } else {
        console.error('❌ Send button not found');
    }
    
    // Message input (Enter key)
    if (messageInput) {
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                console.log('⌨️ Enter key pressed');
                e.preventDefault();
                sendMessage();
            }
        });
        
        messageInput.addEventListener('input', updateCharCount);
        console.log('✅ Message input listeners attached');
    } else {
        console.error('❌ Message input not found');
    }
    
    // Clear chat button
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', function(e) {
            console.log('🖱️ Clear chat button clicked');
            e.preventDefault();
            if (confirm('Are you sure you want to clear the chat?')) {
                clearChat();
            }
        });
        console.log('✅ Clear chat button listener attached');
    } else {
        console.error('❌ Clear chat button not found');
    }
    
    // Quick query buttons (legacy support)
    queryButtons.forEach((button, index) => {
        button.addEventListener('click', function(e) {
            console.log(`🖱️ Quick query button ${index + 1} clicked`);
            e.preventDefault();
            const query = this.textContent.trim();
            handleQuickQuery(query);
        });
    });
    console.log(`✅ ${queryButtons.length} quick query button listeners attached`);
    
    // Radio button selection
    const radioButtons = document.querySelectorAll('input[name="quickQuery"]');
    radioButtons.forEach((radio, index) => {
        radio.addEventListener('change', function() {
            console.log(`📻 Radio button ${index + 1} changed`);
            copyQueryToInput();
        });
    });
    console.log(`✅ ${radioButtons.length} radio button listeners attached`);
    
    // Buttons removed - functionality moved to auto-select on radio click
    
    // Logs section elements - declared above
    
    // Logs section event listeners
    if (clearLogsBtn) {
        clearLogsBtn.addEventListener('click', clearLogs);
    }
    
    if (toggleLogsBtn) {
        toggleLogsBtn.addEventListener('click', toggleLogs);
    }
    
    // Quick Queries resize handle
    if (resizeHandle) {
        console.log('🔧 Attaching quick queries resize handle listener...');
        resizeHandle.addEventListener('mousedown', (e) => startResize(e, quickQueries));
        console.log('✅ Quick queries resize handle listener attached');
    } else {
        console.error('❌ Quick queries resize handle not found!');
    }
    
    // Left Section resize handle
    if (leftSectionResizeHandle && leftSection) {
        console.log('🔧 Attaching left section resize handle listener...');
        leftSectionResizeHandle.addEventListener('mousedown', (e) => {
            console.log('🖱️ Left section resize handle clicked!', e);
            startResize(e, leftSection);
        });
        console.log('✅ Left section resize handle listener attached');
    } else {
        console.error('❌ Left section resize handle not found!');
    }
    
    // Right Section resize handle
    if (rightSectionResizeHandle && rightSection) {
        console.log('🔧 Attaching right section resize handle listener...');
        rightSectionResizeHandle.addEventListener('mousedown', (e) => {
            console.log('🖱️ Right section resize handle clicked!', e);
            startResize(e, rightSection);
        });
        console.log('✅ Right section resize handle listener attached');
    } else {
        console.error('❌ Right section resize handle not found!');
    }
    
    // Check if scrolling is needed
    function checkScrollable() {
        if (queryList) {
            const isScrollable = queryList.scrollHeight > queryList.clientHeight;
            if (isScrollable) {
                queryList.classList.add('scrollable');
            } else {
                queryList.classList.remove('scrollable');
            }
        }
    }
    
    // Check scrollable state on load and resize
    checkScrollable();
    window.addEventListener('resize', checkScrollable);
    
    // Check scrollable state when content changes
    if (queryList) {
        queryList.addEventListener('scroll', checkScrollable);
    }
    
    // Initial character count
    updateCharCount();
    
    // Add welcome message
    addMessage('Hello! I\'m your Healthcare Search Assistant. How can I help you today?');
    
    // Initialize logs
    addLogEntry('info', 'Healthcare Search Assistant initialized');
    addLogEntry('info', 'System ready to process queries');
    
    // Show logs section by default
    if (logsSection) {
        logsSection.style.display = 'flex';
    }
    
    console.log('🎉 Initialization complete!');
});

// Make functions available globally for debugging
window.testChat = function() {
    console.log('🧪 Testing chat functionality...');
    addMessage('This is a test message from the console!');
};

window.clearChat = function() {
    const chatHistory = document.getElementById('chatHistory');
    if (chatHistory) {
        chatHistory.innerHTML = '';
    }
};

console.log('📄 working.js loaded');
