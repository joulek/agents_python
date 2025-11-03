from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import asyncio
import os
import requests

app = FastAPI()

def get_groq_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Tu es un assistant pédagogique intelligent et bienveillant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

class ChapterPrompt(BaseModel):
    description: str

@app.post("/agent/generate-chapter")
async def generate_chapter(data: ChapterPrompt):
    description = data.description.strip()

    if not description:
        return {"error": "Veuillez entrer une description."}

    print("\n📘 Description reçue :", description)

    system_prompt = (
        "Tu es un expert pédagogique universitaire et auteur de livres éducatifs. "
        "Tu génères des chapitres académiques complets, ultra clairs, modernes et faciles à comprendre.\n\n"
        "🔥 Objectif : créer un chapitre pédagogique complet, très détaillé, structuré, riche en exemples, "
        "et adapté à des étudiants débutants à intermédiaires.\n\n"
        "🎯 Structure obligatoire :\n"
        "1️⃣ Introduction (contexte + objectif d’apprentissage)\n"
        "2️⃣ Plan du chapitre (bullet points)\n"
        "3️⃣ Définitions fondamentales\n"
        "4️⃣ Explications détaillées par sections\n"
        "   → Pour chaque section :\n"
        "      - Concept expliqué clairement\n"
        "      - Exemple simple\n"
        "      - Métaphore pédagogique\n"
        "      - Mini-quiz (2 questions)\n\n"
        "5️⃣ Tableau comparatif ou synthèse\n"
        "6️⃣ Cas pratique réel (mise en situation)\n"
        "7️⃣ Bonnes pratiques ✅ & erreurs courantes ❌\n"
        "8️⃣ Notes du professeur (conseils + astuces)\n"
        "9️⃣ Diagramme textuel si utile (ASCII)\n"
        "🔟 Résumé final clair et structuré\n"
        "📌 Glossaire de 5 à 10 mots clés\n"
        "📝 Exercices finaux :\n"
        "   - QCM (5 questions) avec réponses\n"
        "   - Question ouverte avec correction\n\n"
        "📚 Références suggérées (livres, sites fiables)\n\n"
        "⚙️ Règles d'écriture :\n"
        "- Ton académique mais simple\n"
        "- 100% original, paraphrase si nécessaire (pas de plagiat)\n"
        "- Utilise titres, tableaux, listes\n"
        "- Ajoute des emojis pédagogiques si approprié 🎓📘🧠📊💡\n"
        "- Clarifie chaque notion comme si tu formais un étudiant\n"
        "- Minimum 1400 mots\n"
        "- Style = professeur + mentor + coach éducatif\n"
    )

    full_input = f"{system_prompt}\n\nSujet du chapitre : {description}"

    try:
        print("⏳ Appel au modèle Groq...")
        chapter = await asyncio.to_thread(get_groq_response, full_input)
        print("✅ Chapitre généré avec succès !")
    except Exception as e:
        print("❌ Erreur Groq:", e)
        return {"error": str(e)}

    return {"reply": chapter}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
