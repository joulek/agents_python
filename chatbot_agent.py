from fastapi import FastAPI
from pydantic import BaseModel
import requests
from groqChatbot import get_groq_response

app = FastAPI()

# Liste des mots qui déclenchent CoachAgent
triggers = [
    
  "i'm tired", "i feel tired", "so tired", "i'm exhausted", "i feel exhausted",
  "i feel down", "i'm discouraged", "i feel discouraged", "i feel lost",
  "i'm lost", "i can't anymore", "i give up", "i feel stuck",
  "no motivation", "i have no motivation", "i lost motivation",
  "i'm unmotivated", "i feel empty", "i feel hopeless", "i'm hopeless",
  "i feel useless", "i'm stressed", "i'm overwhelmed", "i feel overwhelmed",
  "i'm anxious", "i feel anxious", "i panic", "i feel panic",
  "i feel sad", "i’m sad", "i'm depressed", "i feel depressed",
  "i need support", "i need help", "help me", "please help me",
  "i can't handle this", "i don't know what to do",
  "everything is too much", "i feel weak", "i feel like crying",
  "i'm burned out", "burned out", "i want to quit",
  "i feel pressure", "i'm not okay", "i'm not fine",

  
  "i'm done", "i'm so done", "mentally drained", "i’m drained",
  "life is hard", "struggling", "i can't fight anymore",
  "i fail", "i keep failing", "nothing works",


  "je suis fatigué", "je suis fatiguée", "trop fatigué", "épuisé", "épuisée",
  "je suis épuisé", "je suis épuisée", "je n’en peux plus",
  "j’en peux plus", "c’est trop", "c’est dur", "je suis découragé",
  "je suis découragée", "je me sens perdu", "je me sens perdue",
  "je suis perdu", "je suis perdue", "je me sens vide",
  "je suis stressé", "je suis stressée", "je suis dépassé",
  "je suis dépassée", "je suis triste", "je me sens triste",
  "je suis anxieux", "je suis anxieuse", "je panique",
  "je n’ai plus de motivation", "pas de motivation",
  "j’ai perdu la motivation", "je veux abandonner",
  "je baisse les bras", "j'abandonne", "j’ai peur",
  "je ne vais pas bien", "ça ne va pas", "aidez moi",
  "j’ai besoin d’aide", "aide moi", "s'il vous plaît aidez moi",
  "je ne sais plus quoi faire", "je me sens inutile",
  "je suis à bout", "ça suffit", "marre de tout",
  "je craque", "je pleure", "envie de pleurer",
  "je suis en burn out", "burnout", "trop de pression",
  "je n’y arrive pas", "rien ne marche", "je suis perdu mentalement"
]

class Prompt(BaseModel):
    prompt: str

@app.post("/agent/chat")
async def chatbot_agent(prompt: Prompt):
    user_input = prompt.prompt.lower()
    print("\n📥 Prompt reçu :", user_input)

    # 🔹 Appel à Groq normalA
    groq_reply = get_groq_response(user_input)
    print("🤖 Groq reply:", groq_reply)

    # 🔸 Détection mots-clés => appel CoachAgent
    should_call_coach = any(trigger in user_input for trigger in TRIGGERS)
    coach_message = ""

    if should_call_coach:
        try:
            res = requests.post("http://localhost:8002/agent/chat", json={"prompt": user_input})
            coach_message = res.json().get("reply", "")
            print("💬 Motivation CoachAgent :\n", coach_message)
        except Exception as e:
            print("❌ Erreur CoachAgent:", str(e))

    # 🔁 Fusion réponse si Coach actif
    if coach_message:
        full_reply = f"{groq_reply}\n\n🧠 Coach says:\n{coach_message}"
    else:
        full_reply = groq_reply

    return {  "reply": groq_reply, "coachReply": coach_message}
