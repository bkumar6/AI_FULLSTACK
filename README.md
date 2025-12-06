# AI_FULLSTACK

## Project Overview

Full-stack demo that combines:
- FastAPI backend with user authentication, protected routes, and AI endpoints.
  - See implementation in [backend/main.py](backend/main.py) — endpoints: [`process_chat_request`](backend/main.py), [`get_suggestions`](backend/main.py), [`signup`](backend/main.py), [`login_for_access_token`](backend/main.py), [`read_users`](backend/main.py), [`update_user`](backend/main.py), [`delete_user`](backend/main.py).
- Vue 3 + Vite frontend demonstrating chat, autocomplete, signup/login, and protected users list.
  - Key frontend files: [frontend/src/components/AutocompleteInput.vue](frontend/src/components/AutocompleteInput.vue), [frontend/src/views/ChatView.vue](frontend/src/views/ChatView.vue), [frontend/src/composables/useAuth.js](frontend/src/composables/useAuth.js), [frontend/src/composables/useDebounce.js](frontend/src/composables/useDebounce.js), [frontend/src/router/index.js](frontend/src/router/index.js), [frontend/src/views/UsersListView.vue](frontend/src/views/UsersListView.vue).

---

## Which AI API is used

This project uses Google GenAI (Gemini) via the official GenAI client:
- Client initialization and model configuration live in [backend/main.py](backend/main.py): see the [`client`](backend/main.py) initialization and [`MODEL_NAME`](backend/main.py).
- The backend reads credentials from environment variable `GEMINI_API_KEY` (configured in [backend/.env](backend/.env)).

Do NOT commit real keys to source control — keep them in [backend/.env](backend/.env).

---

## Where to configure API keys

Set the Gemini API key as an environment variable named `GEMINI_API_KEY`. The repo includes an env file used by the backend at:
- [backend/.env](backend/.env)

Example (do NOT commit real keys):
GEMINI_API_KEY=your_real_key_here

The backend code reads it in [backend/main.py](backend/main.py) as `os.environ.get("GEMINI_API_KEY")`.

---

## Run instructions

Backend (FastAPI)
1. Create and activate a Python venv:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows