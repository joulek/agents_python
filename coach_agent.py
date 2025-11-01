from fastapi import FastAPI, Request
from groqChatbot import get_groq_response
import random

app = FastAPI()

@app.post("/agent/chat")
async def coach_agent(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    print("user:", prompt)

    motivation_prompt = f"""
L'utilisateur dit : '{prompt}'

Tu es un coach motivant et bienveillant.
Ta mission : aider l’utilisateur à retrouver l'énergie et la motivation pour continuer ses révisions.

Réponds avec :
- Un message très motivant, humain et positif
- Empathie + compréhension émotionnelle
- Conseils concrets et simples à appliquer immédiatement
- 2 ou 3 petits exercices pratiques (ex : respiration, pomodoro, mini-pause active, affirmation positive)
- Ton chaleureux, encourageant, jamais robotique
- Pas de jugement, pas de clichés

But : redonner confiance, énergie et clarté.

Termine toujours avec une question motivante pour réengager l'utilisateur.
"""


    motivation_message = get_groq_response(motivation_prompt)

    print("💬 Motivation CoachAgent :\n\n👨‍🏫 Motivation:\n", motivation_message)

    return {"reply": motivation_message}
## Stockage local des messages générés
MESSAGES = [
    "💪 Continue comme ça, tu es sur la bonne voie !",
    "🚀 Tu progresses chaque jour, ne lâche rien !",
]

@app.get("/coach/motivate")
def motivate():
    prompt = (
        "Generate a short motivational, positive and human message in English for a student "
        "who is doing a quiz or studying. Keep it short and encouraging."
    )

    try:
        new_message = get_groq_response(prompt).strip()

        if new_message and new_message not in MESSAGES:
            MESSAGES.append(new_message)
            print("🆕 Nouveau message ajouté :", new_message)

        return {"message": new_message}  # ✅ on renvoie toujours le nouveau

    except Exception as e:
        print("❌ Erreur get_groq_response:", str(e))
        return {"message": random.choice(MESSAGES)}  # fallback local
