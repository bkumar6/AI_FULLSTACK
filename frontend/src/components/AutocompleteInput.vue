<script setup>
import { ref } from 'vue';
import { useDebounce } from '../composables/useDebounce';

const query = ref('');
const suggestions = ref([]);
const isFetching = ref(false);

const API_URL = 'http://127.0.0.1:8000/api/suggest';
const { debounce } = useDebounce(400);

// Fetch Suggestions -----------------------------------
const fetchSuggestions = async (searchTerm) => {
    console.log("🔻 fetchSuggestions() called with:", searchTerm);

    if (searchTerm.length < 3) {
        console.log("⚪ Query too short, clearing suggestions");
        suggestions.value = [];
        return;
    }

    console.log("🌐 Sending request to:", `${API_URL}?query=${encodeURIComponent(searchTerm)}`);

    isFetching.value = true;

    try {
        const response = await fetch(`${API_URL}?query=${encodeURIComponent(searchTerm)}`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        suggestions.value = data.suggestions || [];

        console.log("📥 Suggestions received:", suggestions.value);

    } catch (error) {
        console.error("🔥 Suggestion API Error:", error);
        suggestions.value = ["Error fetching suggestions."];

    } finally {
        isFetching.value = false;
    }
};

// Watch Input -----------------------------------------
// watch(query, (newQuery) => {
//     console.log("🔹 Watcher triggered:", newQuery);
//     // console.log("Input changed. New value:", newQuery); // Redundant line removed

//     // 🎯 CRITICAL CHANGE HERE: The debounce function should execute fetchSuggestions 
//     // using the LATEST value of the reactive 'query' ref, not the potentially stale 'newQuery' argument.
//     // However, since we are only passing a callback to debounce, we need to ensure the correct 
//     // argument (newQuery) is captured or we reference the reactive 'query.value'.
    
//     // Efficient fix is to pass the callback function which encapsulates the newQuery:
//     debounce(() => {
//         console.log("🟢 Debounce fired for:", newQuery);
//         fetchSuggestions(newQuery); 
//     });
// });


const handleInput = (event) => {
    // 1. Update the reactive variable manually
    query.value = event.target.value; 
    
    // 2. Log to confirm this function runs on every keystroke
    console.log("🟢 @input triggered, new query:", query.value); 
    
    // 3. Trigger the debounced fetch
    debounce(() => {
        console.log("🟢 Debounce fired for:", query.value); 
        fetchSuggestions(query.value);
    });
};


// When selecting suggestion ----------------------------
const selectSuggestion = (suggestion) => {
    console.log("🎯 Selected suggestion:", suggestion);
    query.value = suggestion;
    suggestions.value = [];
};

const handleBlur = () => {
    setTimeout(() => {
        console.log("👁️ Blur triggered — closing suggestions");
        suggestions.value = [];
    }, 150);
};
</script>

<template>
    <div class="autocomplete-wrapper">
        <label for="task-title">Task Title / Product Name</label>

        <div class="input-group">
            <input
                id="task-title"
                type="text"
                :value="query"
                @input="handleInput"
                placeholder="Start typing to get AI suggestions..."
                @blur="handleBlur"
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
/* unchanged styling */
</style>