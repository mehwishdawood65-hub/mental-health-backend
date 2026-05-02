from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq

app = FastAPI()

# ---------------- AI SETUP ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- MEMORY ----------------
user_memory = {}
journal_memory = {}

# ---------------- MODELS ----------------
class Mood(BaseModel):
    user_id: str
    mood: str

class Journal(BaseModel):
    user_id: str
    text: str

class Chat(BaseModel):
    message: str

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"status": "Backend Running"}

# ---------------- MOOD ----------------
@app.post("/mood")
def mood(data: Mood):

    if data.user_id not in user_memory:
        user_memory[data.user_id] = []

    user_memory[data.user_id].append(data.mood)

    return {"history": user_memory[data.user_id]}

# ---------------- JOURNAL ----------------
@app.post("/journal")
def journal(data: Journal):

    if data.user_id not in journal_memory:
        journal_memory[data.user_id] = []

    journal_memory[data.user_id].append(data.text)

    return {"saved": True}

# ---------------- PANIC ----------------
@app.get("/panic")
def panic():
    return {
        "steps": [
            "Name 5 things you see",
            "Touch something near you",
            "Breathe slowly",
            "Relax shoulders"
        ]
    }

# ---------------- HELPLINE ----------------
@app.get("/helpline/pakistan")
def helpline():
    return {
        "emergency": "1122",
        "health": "1166",
        "edhi": "115"
    }

# ---------------- AI CHATBOT (GROQ) ----------------
@app.post("/chat")
def chat(data: Chat):

    prompt = f"""
You are a safe mental health support assistant.

Rules:
- Do NOT give medical diagnosis
- Be calm and supportive
- If panic → suggest breathing exercise
- If sadness → give emotional support

User: {data.message}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Safe mental health assistant"},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
