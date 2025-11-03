from fastapi import FastAPI
from pydantic import BaseModel
from groqChatbot import get_groq_response
import uvicorn
import asyncio

app = FastAPI()

class ChapterPrompt(BaseModel):
    description: str

@app.post("/agent/generate-chapter")
async def generate_chapter(data: ChapterPrompt):
    description = data.description.strip()

    if not description:
        return {"error": "Veuillez entrer une description."}

    print("\n📘 Description reçue :", description)

    # Prompt IA – génération chapitre structuré
    system_prompt = (
        "Tu es un expert pédagogique. "
        "Génère un chapitre complet, structuré et clair avec :\n"
        "- 🎯 Introduction\n"
        "- 🧠 Concepts clés\n"
        "- 📌 Titres & sous-titres\n"
        "- ✅ Points importants\n"
        "- 📊 Tableaux ou exemples si nécessaire\n"
        "- 📝 Résumé final\n"
        "Langue: Française. Style académique mais simple pour un étudiant."
    )

    full_input = f"{system_prompt}\n\nSujet du chapitre : {description}"

    try:
        print("⏳ Appel au modèle Groq...")
        # Run sync function in thread (avoid blocking FastAPI)
        chapter = await asyncio.to_thread(get_groq_response, full_input)
        print("✅ Chapitre généré avec succès !")
    except Exception as e:
        print("❌ Erreur Groq:", e)
        return {"error": str(e)}

    return {"reply": chapter}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)