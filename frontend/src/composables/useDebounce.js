import { ref } from "vue";

export function useDebounce(delay = 400) {
    const timeoutId = ref(null);

    const debounce = (callback, ...args) => {
        if (timeoutId.value) clearTimeout(timeoutId.value);

        timeoutId.value = setTimeout(() => {
            callback(...args);
            timeoutId.value = null;
        }, delay);
    };

    return { debounce };
}