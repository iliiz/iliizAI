from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone 

from fastapi import FastAPI, Form, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import bcrypt 
import uvicorn

from .groq import iliiz
from .models import Base, User, Message
from .email import generate_otp, send_otp_email

DATABASE_URL="sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 15}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pending_users: dict = {}
OTP_LIFETIME_MINUTES = 5

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield 

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session) -> User | None:
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    try:
        return db.get(User, int(user_id))
    except (ValueError, TypeError):
        return None


@app.get("/")
async def read_intro(request: Request): 
    return templates.TemplateResponse(request, "intro.html")

@app.get("/signup")
async def read_signup(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse("/chat", status_code=302)
    return templates.TemplateResponse(request, "signup.html")

@app.get("/login")
async def read_login(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse("/chat", status_code=302)
    return templates.TemplateResponse(request, "login.html")

@app.get("/chat")
async def read_chat(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    messages = (
        db.query(Message)
        .filter(Message.user_id == user.id)
        .order_by(Message.id.asc()) 
        .all()
    )
    return templates.TemplateResponse(
        request,
        "chat.html",
        {"user": user, "messages": messages}
    )

@app.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        return JSONResponse(status_code=400, content={"message": "username already exists", "success": False})
    if db.query(User).filter(User.email == email).first():
        return JSONResponse(status_code=400, content={"message": "email already exists", "success": False})
    
    otp = generate_otp()
    await send_otp_email(email, otp)
    pending_users[email] = {
        "username": username,
        "password": hash_password(password),
        "otp": otp,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=OTP_LIFETIME_MINUTES)
    }
    return JSONResponse(status_code=202, content={"success": True})

@app.post("/verify")
async def verify(
    request: Request,
    email: str = Form(...),
    otp: str = Form(...),
    db: Session = Depends(get_db)
):
    entry = pending_users.get(email)
    if not entry:
        return JSONResponse(status_code=200, content={"success": False, "message": "No pending signup found. Please start over."})
        
    if datetime.now(timezone.utc) > entry["expires_at"]:
        del pending_users[email]
        return JSONResponse(status_code=200, content={"success": False, "message": f"Code expired ({OTP_LIFETIME_MINUTES} min limit). Please sign up again."})
        
    if entry["otp"] != otp.strip():
        return JSONResponse(status_code=200, content={"success": False, "message": "Incorrect code. Please try again."})

    new_user = User(
        username=entry["username"],
        email=email,
        password=entry["password"],
    )
    db.add(new_user)
    db.commit()

    del pending_users[email]
    return JSONResponse(content={"success": True, "message": "Account created! Redirecting to login…"})


@app.post("/login") 
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return JSONResponse(status_code=401, content={"success": False, "error": "Invalid username or password."})

    response = JSONResponse(content={"success": True})
    response.set_cookie(key="user_id", value=str(user.id), httponly=True)
    return response


@app.post("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("user_id")
    return response

@app.post("/chat")
async def handle_chat(
    request: Request, 
    message: str = Form(...), 
    tags: str = Form("[]"), 
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse(status_code=401, content={"success": False, "error": "Unauthorized"})

    try:
        user_msg = Message(user_id=user.id, content=message, role="user")
        db.add(user_msg)
        db.commit()

        bot_response = await iliiz(message)

        bot_msg = Message(user_id=user.id, content=bot_response, role="assistant")
        db.add(bot_msg)
        db.commit()

        return JSONResponse(content={"success": True, "reply": bot_response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"success": False, "error": f"Groq API Connection Error: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run("apps.main:app", host="127.0.0.1", port=8000, reload=True)
