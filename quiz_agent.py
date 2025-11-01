# ✅ agents-python/quiz_agent.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests


app = FastAPI()

# Autoriser les appels CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion MongoDB

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["test"]
flashcards_collection = db["flashcards"]

@app.post("/quiz/next")
async def get_next_question(request: Request):
    body = await request.json()
    all_questions = body.get("questions", [])
    index = body.get("index", 0)

    if index >= len(all_questions):
        return {"end": True}

    question = all_questions[index]

    # Appel au coach
    try:
        res = requests.get("http://localhost:8002/coach/motivate")
        coach_message = res.json().get("message", "")
    except Exception as e:
        print("❌ Coach fallback:", str(e))
        coach_message = "You're doing great!"

    return {
        "question": question,
        "coach": coach_message,
        "index": index
    }


@app.post("/quiz/init")
async def init_quiz(request: Request):
    body = await request.json()
    course_id = body.get("courseId")
    print("📩 course_id reçu :", course_id)

    if not course_id or not ObjectId.is_valid(course_id):
        return {"questions": [], "error": "courseId invalide ou manquant"}

    try:
        object_id = ObjectId(course_id)
        found = flashcards_collection.find({"courseId": object_id})
        questions = []

        for card in found:
            print("✅ Question trouvée :", card.get("question"))
            questions.append({
                "title": card.get("question", ""),
                "choices": [
                    {
                        "text": choice,
                        "correct": choice == card.get("answer")
                    }
                    for choice in card.get("choices", [])
                ]
            })

        # ✅ Ajout du message motivant ici :
        coach_message = get_coach_message()

        print(f"✅ Total questions : {len(questions)}")
        return {
            "questions": questions,
            "coach": coach_message
        }

    except Exception as e:
        print("❌ Erreur :", str(e))
        return {"questions": [], "error": str(e)}

def get_coach_message():
    try:
        res = requests.get("http://localhost:8002/coach/motivate")
        data = res.json()
        return data.get("message", "Keep going! 💪")
    except Exception as e:
        print("❌ Erreur CoachAgent dans quiz_agent:", str(e))
        return "Stay strong! You're doing great! 🚀"
