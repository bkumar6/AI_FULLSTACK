# Full-Stack AI Application (FastAPI + Vue.js)

This project implements a full-stack web application demonstrating AI integration, robust user authentication, and CRUD operations, fulfilling all assignment requirements.

# 🚀 Technology Stack

This application uses a modular architecture combining Python for the backend logic and Vue.js for the dynamic frontend interface.

| Layer | Technology | Purpose |
| ----- | ----- | ----- |
| **Backend (API)** | **FastAPI (Python)** | High-performance API server for authentication, user management, and secure AI calls. | 
| **Frontend (UI)** | **Vue.js 3 (Composition API)** | Component-based UI development and client-side state management. |





Backend (API)

FastAPI (Python)

High-performance API server for authentication, user management, and secure AI calls.

Frontend (UI)

Vue.js 3 (Composition API)

Component-based UI development and client-side state management.

Database

SQLModel / SQLite

Lightweight, file-based ORM for persistent storage of user data.

Security

JWT (JSON Web Tokens)

Stateless token-based authentication (Login/Protected Routes).

AI Integration

Google Gemini API

Used for Chatbot and Autocomplete generation.

📦 Project Structure

The project is split into two primary directories, one for the backend API and one for the frontend client.

full-stack-ai-app/
├── backend/
│   ├── main.py        # Core FastAPI application (AI, Auth, CRUD endpoints)
│   └── .env           # Environment variables (AI Key, JWT Secret)
│   └── database.db    # SQLite database file (automatically generated on startup)
├── frontend/
│   ├── src/
│   │   ├── composables/ # Reusable state logic (useAuth.js, useDebounce.js)
│   │   ├── router/      # Vue Router config with authentication guard
│   │   └── views/       # Vue pages (Login, Signup, UsersList, Chat)
└── venv/              # Python virtual environment


⚙️ How to Run the Application

The application requires running two separate servers concurrently in two different terminal windows.

Prerequisites

Python 3.10+ and Node.js 18+ installed.

A Gemini API Key is required for AI functionality.

Step 1: Backend Setup (FastAPI)

Activate Environment: Navigate to the project root and activate the Python virtual environment.

# For macOS/Linux
source venv/bin/activate
# For Windows
.\venv\Scripts\activate


Install Dependencies:

pip install fastapi uvicorn google-genai pydantic python-dotenv sqlmodel passlib python-jose[cryptography]


Configure API Key: Open backend/.env and replace the placeholder with your actual key.

GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"


Run Server: Navigate to the backend directory and start the Uvicorn server.

cd backend
uvicorn main:app --reload --env-file .env


The server will run on http://127.0.0.1:8000.

Step 2: Frontend Setup (Vue.js)

Install Dependencies: Open a second terminal window and navigate to the frontend directory.

cd frontend
npm install


Run Client: Start the Vite development server.

npm run dev


The frontend will run on http://localhost:5173. Open this URL in your browser.

✨ Implemented Objectives

1. Chatbot Integration

Feature

Detail

Endpoint

POST http://127.0.0.1:8000/api/chat

Implementation

Vue sends the prompt; FastAPI securely relays it to the Gemini API and returns the AI's response text.

2. AI-Powered Autocomplete Field

Feature

Detail

Endpoint

GET http://127.0.0.1:8000/api/suggest?query={input}

Implementation

Uses client-side debouncing (400ms delay) to limit API usage. The AI generates 5 semicolon-separated suggestions based on the user's partial input.

3. Authentication & User Management (CRUD)

Hashing: Passwords are securely hashed using the PBKDF2-SHA256 scheme.

Security: All user data endpoints are protected by JWTs. The client redirects unauthorized users via a Vue Router Navigation Guard.

Feature

Endpoint

Method

Security

Sign Up

/auth/signup

POST

Public (Registers user)

Log In

/auth/login

POST

Public (Returns JWT)

Users List

/api/users

GET

Protected (Requires JWT)

Edit User

/api/users/{id}

PUT

Protected (Self-Update Only)

Delete User

/api/users/{id}

DELETE

Protected (Self-Delete Only)

⚠️ Assumptions and Limitations

Local Storage for Tokens: The JWT is stored in localStorage for simplicity. In production, secure HTTP-only cookies are preferred.

Database: Uses SQLite for development ease. This would be swapped for a robust relational database (PostgreSQL/MySQL) in a production environment.

User CRUD Scope: Users can only view all users but can only Edit or Delete their own profile.