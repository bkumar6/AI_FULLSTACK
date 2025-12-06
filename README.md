# AI-POWERED-FULL-STACK-APPLICATION

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
2. Install dependencies:
    ```sh
    pip install fastapi uvicorn sqlmodel python-dotenv passlib python-jose google-genai
3. Configure your Gemini API key in (backend/.env) or in your environment.
4. Run the backend:
    ```sh
    cd backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
- The backend exposes endpoints the frontend expects:
  - Chat: POST/api/chat handled by [`process_chat_requests`](backend/main.py)
  - Autocomplete: GET /api/suggest handled by [`get_suggestions`](backend/main.py)
  - Signup/Login: POST /auth/signup and POST /auth/login handled by [`signup`](backend/main.py) and [`login_for_access_token`](backend/main.py)
  - Protected users: GET/PUT/DELETE /api/users handled by [`read_users`](backend/main.py), [`update_user`](backend/main.py), [`delete_user`](backend/main.py)

Frontend (Vue 3 / Vite)

  1. Install Node.js that matches engines in [frontend/package.json].
  2. From repository root:
      ```sh
      cd frontend
      npm install
      npm run dev
  3. Open the dev server (Vite default) at http://localhost:5173 (the backend CORS allows this origin by default — see [backend/main.py] CORS config).
*******
## Frontend <> Backend integration notes
- Autocomplete component sends requests to
  `http://127.0.0.1:8000/api/suggest`:
  - See [frontend/src/components/AutocompleteInput.vue].
  - Debounce helper: [`useDebounce`](frontend/composables/useDebounce.js).
- Chat UI posts messages to `http://127.0.0.1:8000/api/chat`:
  - See [frontend/src/views/ChatView.vue].
- Authentication:
  - Client-side auth helpers are in [`useAuth`](frontend/composables/useAuth.js). Token and user info are stored in localStorage and used by `fetchProtected` for protected API calls.
  - Login endpoint expects form-encoded data (FastAPI's OAuth2 form) — implemented in [`useAuth`](frontend/composables/useAuth.js) and [`login_for_access_token`](backend/main.py).
  - Router enforces protected routes via the guard in [frontend/src/router/index.js].
*********
## Assumptions, limitations, and extra features
Assumptions
- Local development: frontend served by Vite (port 5173) and backend by Uvicorn (port 8000).
- Gemini API key is valid and has access to the chosen model.
- No production-grade DB migrations — SQLite file `database.db` is used (created automatically by [backend/main.py]).

Limitations

- JWT secret is hard-coded in [backend/main.py] and must be replaced for production.
- No HTTPS in local dev.
- No rate limiting or advanced error retry logic for the GenAI API.
- Minimal authorization model: users may only edit/delete their own account (enforced in [backend/main.py] and UI logic in [frontend/src/views/UsersListView.vue]).

Extra / Helpful features implemented

- Protected routes and helper `fetchProtected` in [`useAuth`](frontend/composables/useAuth.js).
- Password hashing (PBKDF2_SHA256) with passlib in [backend/main.py].
********
Important files / entry points (quick links)

- Backend main: [backend/main.py] — server, AI client, auth, endpoints
  - Chat endpoint: [`process_chat_request`](backend/main.py)
  - Suggest endpoint: [`get_suggestions`](backend/main.py)
  - Auth endpoints: signup, [`login_for_access_token`](backend/main.py)
  - Protected user endpoints: [`read_users`](backend/main.py), [`update_user`](backend/main.py), [`delete_user`](backend/main.py)
  - AI client and config: see [`client`](backend/main.py) and [`MODEL_NAME`](backend/main.py)
- Backend env: [backend/.env]
- Frontend app: [frontend/package.json]
- Autocomplete: [frontend/src/components/AutocompleteInput.vue]
- Chat UI: [frontend/src/views/ChatView.vue]
- Auth composable: [frontend/src/composables/useAuth.js]
- Debounce composable: [frontend/src/composables/useDebounce.js]
- Router and guards: [frontend/src/router/index.js]
- Router and guards: [frontend/src/router/index.js]
- Users list (protected UI): [frontend/src/views/UsersListView.vue]
*********
