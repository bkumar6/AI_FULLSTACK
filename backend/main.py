import os
from datetime import datetime, timedelta
from typing import Annotated, Optional

# FastAPI and dependencies
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from dotenv import load_dotenv

# Security and Database Imports
from sqlmodel import Field, Session, SQLModel, create_engine, select
from passlib.context import CryptContext
from jose import JWTError, jwt

# AI Imports
from google import genai
from google.genai.errors import APIError

# --- CONFIGURATION & INITIALIZATION ---

# Load environment variables from .env file
load_dotenv()

# --- Security Constants ---
JWT_SECRET_KEY = "your-jwt-secret-key-replace-me-with-a-long-random-string"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Database Configuration (SQLite) ---
DATABASE_FILE = "database.db"
sqlite_url = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(sqlite_url, echo=False) 

# --- AI Configuration ---
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

try:
    if not API_KEY:
         raise ValueError("GEMINI_API_KEY not found in environment variables.")
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"🔥 Gemini Client Initialization Error: {e}")
    client = None


# --- Pydantic & SQLModel Schemas ---

class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None

class ChatRequest(BaseModel):
    prompt: str


# --- Security Helper Functions ---

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a raw password using PBKDF2_SHA256."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": str(data["user_id"])})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- FastAPI Application Setup ---

app = FastAPI(title="Full-Stack AI App Backend")

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") 

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
        
    return user

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Chatbot Integration Endpoint ---

@app.post("/api/chat")
async def process_chat_request(request: ChatRequest):
    print("🟢 /api/chat triggered with:", request.prompt)
    if client is None:
        raise HTTPException(status_code=503, detail="AI service is unavailable. Check server configuration.")
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=request.prompt)
        return {"response_text": response.text}
    except Exception as e:
        print("🔥 Gemini API Error:", e)
        raise HTTPException(status_code=500, detail="Gemini API request failed.")


# --- Autocomplete Endpoint ---

@app.get("/api/suggest")
async def get_suggestions(query: str = None):
    print("🔵 /api/suggest triggered with query:", query)
    if client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI service is unavailable. Check server configuration.")
    if not query or len(query.strip()) < 1:
        print("⚪ Empty or too short query. Returning []")
        return {"suggestions": []}
        
    prompt = ("You are a suggestion engine. Generate exactly 5 short title suggestions based on: " 
              f"{query}\n"
              "Return them separated ONLY by semicolons (;). No numbering.")
    try:
        print("🟡 Sending prompt to Gemini...")
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        print("🟢 Gemini responded!")
        
        raw = response.text.strip()
        suggestions = [s.strip() for s in raw.split(";") if s.strip()]
        
        print("✨ Suggestions:", suggestions[:5])
        return {"suggestions": suggestions[:5]}
    except APIError as e:
        print("🔥 Gemini API Error:", e)
        raise HTTPException(status_code=500, detail="Suggestion API failed")
    except Exception as e:
        print("🔥 Unexpected Error:", e)
        raise HTTPException(status_code=500, detail="Unexpected error")


# --- Signup Endpoint ---
@app.post("/auth/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """Creates a new user, hashes the password, and stores them in the database."""
    
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    hashed_password = hash_password(user_data.password)
    db_user = User(
        name=user_data.name, 
        email=user_data.email, 
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


# --- Login Endpoint ---
@app.post("/auth/login")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: Session = Depends(get_session)
):
    """Validates credentials and returns an access token (JWT)."""
    email = form_data.username 
    password = form_data.password

    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "email": user.email}


# --- Protected Users List ---

@app.get("/api/users", response_model=list[UserRead])
def read_users(
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Session = Depends(get_session)
):
    """Retrieves a list of all users. Only accessible by logged-in users."""
    
    print(f"User {current_user.email} accessed the protected user list.")
    users = session.exec(select(User)).all()
    
    return users


# --- Protected User Update ---

@app.put("/api/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session)
):
    """Updates a user's name or email. Requires authentication."""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to update this user")

    update_data = user_data.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(update_data)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# --- Protected User Delete ---

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session)
):
    """Deletes a user from the database. Requires authentication."""
    db_user = session.get(User, user_id)
    if not db_user:
        return 

    if db_user.id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to delete this user")
         
    session.delete(db_user)
    session.commit()
    return