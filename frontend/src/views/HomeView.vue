<!-- <script setup>
import AutocompleteInput from '../components/AutocompleteInput.vue';
</script>

<template>
  <main>
    <h1>Full-Stack AI Application</h1>
    <AutocompleteInput />
  </main>
</template> -->

<script setup>
import { ref } from 'vue';
import { useDebounce } from '../composables/useDebounce'; 

// --- STATE VARIABLES ---
const query = ref('');
const suggestions = ref([]);
const isFetching = ref(false);

// --- CONFIG & DEBOUNCER ---
const API_URL = 'http://127.0.0.1:8000/api/suggest';
const { debounce } = useDebounce(400); // 400ms delay

// --- FETCH LOGIC ---
const fetchSuggestions = async (searchTerm) => {
    if (searchTerm.length < 3) {
        suggestions.value = [];
        return;
    }

    isFetching.value = true;
    try {
        const response = await fetch(`${API_URL}?query=${encodeURIComponent(searchTerm)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        suggestions.value = data.suggestions || [];

    } catch (error) {
        console.error("🔥 Suggestion API Error:", error);
        suggestions.value = ["Error fetching suggestions."];
    } finally {
        isFetching.value = false;
    }
};

// --- INPUT & DEBOUNCE HANDLER (The Fix) ---
const handleInput = (event) => {
    // 1. Manually update the reactive variable
    query.value = event.target.value; 
    
    // 2. Trigger the debounced fetch
    debounce(() => {
        fetchSuggestions(query.value);
    });
};

// --- SELECTION LOGIC ---
const selectSuggestion = (suggestion) => {
    query.value = suggestion;
    suggestions.value = []; // Hide dropdown after selection
};

const handleBlur = () => {
  setTimeout(() => {
    suggestions.value = [];
  }, 150);
};
</script>

<template>
    <div class="autocomplete-wrapper">
        <h1>AI-Powered Autocomplete Field</h1>
        <label for="task-title">Task Title / Product Name</label>
        
        <div class="input-group">
            <input
                id="task-title"
                type="text"
                :value="query"               @input="handleInput"         @blur="handleBlur"           placeholder="Start typing..."
                autocomplete="off"
            />
            <span v-if="isFetching" class="loading-indicator">...</span>
        </div>

        <ul v-if="suggestions.length" class="suggestions-dropdown">
            <li 
                v-for="(suggestion, index) in suggestions" 
                :key="index"
                @mousedown.prevent="selectSuggestion(suggestion)"
            >
                {{ suggestion }}
            </li>
        </ul>
    </div>
</template>

<style scoped>
/* 🎯 ALL STYLES ARE CORRECTLY PLACED OUTSIDE <template> */

.autocomplete-wrapper {
    max-width: 500px;
    margin: 40px auto;
    position: relative; 
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.input-group {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding-right: 10px;
}

.input-group input {
    flex-grow: 1;
    padding: 10px;
    border: none;
    outline: none;
    font-size: 16px;
}

.loading-indicator {
    color: #888;
    font-style: italic;
    font-size: 0.9em;
}

.suggestions-dropdown {
    position: absolute;
    width: 100%;
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-top: none;
    list-style: none;
    padding: 0;
    margin: 0;
    z-index: 10; 
    background-color: white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.suggestions-dropdown li {
    padding: 10px;
    cursor: pointer;
    font-size: 14px;
    color: #333;
}

.suggestions-dropdown li:hover {
    background-color: #f0f0f0;
}
</style>