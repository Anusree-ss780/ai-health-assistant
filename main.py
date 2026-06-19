from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import database as db   # 👈 using your database.py

# ---------- LOAD ENV ----------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ---------- APP ----------
app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- REQUEST MODEL ----------
class ChatRequest(BaseModel):
    message: str

# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "AI Health Assistant running 🚀"}

# ---------- CHAT ----------
@app.post("/chat")
def chat(req: ChatRequest):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical AI assistant. "
                    "Give safe, simple advice and always suggest a doctor for serious symptoms."
                )
            },
            {
                "role": "user",
                "content": req.message
            }
        ]
    )

    ai_reply = response.choices[0].message.content

    # 💾 SAVE CHAT USING DATABASE.PY
    db.save_chat(req.message, ai_reply)

    return {
        "response": ai_reply
    }

# ---------- HISTORY ----------
@app.get("/history")
def history():
    return {
        "history": db.get_history()
    }