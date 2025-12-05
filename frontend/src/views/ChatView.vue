<script setup>
import { ref } from 'vue';

// Define the structure for a message
const messages = ref([]);
const currentPrompt = ref('');
const isLoading = ref(false);

const API_URL = 'http://127.0.0.1:8000/api/chat'; // <-- Your FastAPI Backend URL

const sendMessage = async () => {
    const prompt = currentPrompt.value.trim();
    if (!prompt) return;

    // 1. Add user message to the conversation
    messages.value.push({
        sender: 'user',
        text: prompt
    });

    // Clear the input and set loading state
    currentPrompt.value = '';
    isLoading.value = true;

    try {
        // 2. POST request to FastAPI backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt })
        });

        // Check for HTTP errors (e.g., 500, 400)
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 3. Add AI response to the conversation
        messages.value.push({
            sender: 'ai',
            text: data.response_text // Matches the key returned by FastAPI
        });

    } catch (error) {
        // Display any API or network errors
        messages.value.push({
            sender: 'error', // <-- Use 'error' for dedicated styling
            text: `Error: ${error.message}`
        });
        console.error("Chat API Error:", error);
    } finally {
        // 4. Reset loading state
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="chat-container">
        <h2>🤖 How may I assist you?</h2>
        <div class="conversation">
            <div 
                v-for="(message, index) in messages" 
                :key="index" 
                :class="['message', message.sender]"
            >
                <div class="sender-tag">
                    {{ message.sender === 'user' ? 'You' : 'AI' }}
                </div>
                <div class="message-text">
                    {{ message.text }}
                </div>
            </div>
            
            <div v-if="isLoading" class="message ai loading">
                <div class="sender-tag">AI</div>
                <div class="message-text">...Thinking...</div>
            </div>
        </div>

        <form @submit.prevent="sendMessage" class="chat-input-form">
            <input
                type="text"
                v-model="currentPrompt"
                placeholder="Ask the AI a question..."
                :disabled="isLoading"
            />
            <button type="submit" :disabled="isLoading">
                Send
            </button>
        </form>
    </div>
</template>

<style scoped>
/* Basic styling for the chat UI */
.chat-container {
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.conversation {
    height: 300px;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #eee;
    border-radius: 4px;
    background-color: #f9f9f9;
}

.message {
    display: flex;
    margin-bottom: 10px;
}

.sender-tag {
    font-weight: bold;
    margin-right: 10px;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
}

.user .sender-tag {
    background-color: #d1e7ff;
}

.ai .sender-tag {
    background-color: #d4edda;
}

.user {
    justify-content: flex-end;
}

.user .message-text {
    background-color: #e6f2ff;
    padding: 8px 12px;
    border-radius: 15px 15px 0 15px;
    max-width: 75%;
    color: #333;
}

.ai .message-text {
    background-color: #e6f9e6;
    padding: 8px 12px;
    border-radius: 15px 15px 15px 0;
    max-width: 75%;
    color: #333;
}

.ai.loading .message-text {
    font-style: italic;
    color: #888;
}

.chat-input-form {
    display: flex;
}

.chat-input-form input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px 0 0 4px;
}

.chat-input-form button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
}

.chat-input-form button:disabled {
    background-color: #99cfff;
    cursor: not-allowed;
}

/* Add this new styling block */
.message.error {
    justify-content: center; /* Center the error message */
    margin-top: 20px;
}

.error .sender-tag {
    /* Hide the sender tag for a centered system error */
    display: none; 
}

.error .message-text {
    background-color: #f8d7da; /* Light red background */
    color: #721c24;             /* Dark red text */
    padding: 8px 15px;
    border-radius: 8px;
    font-weight: bold; /* Make it stand out */
    text-align: center;
    max-width: 90%;
}
</style>