import sqlite3
import os

# ---------- DB PATH ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chat.db")

# ---------- CONNECT ----------
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ---------- CREATE TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL
)
""")

conn.commit()

# ---------- SAVE CHAT ----------
def save_chat(user_message: str, ai_response: str):
    cursor.execute(
        "INSERT INTO chats (user_message, ai_response) VALUES (?, ?)",
        (user_message, ai_response)
    )
    conn.commit()

# ---------- GET HISTORY ----------
def get_history():
    cursor.execute("SELECT * FROM chats ORDER BY id DESC")
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "user_message": r[1],
            "ai_response": r[2]
        }
        for r in rows
    ]