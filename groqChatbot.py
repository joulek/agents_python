import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()

def get_groq_response(prompt, system_prompt=None, temperature=0.7, max_retries=2):
    url = "https://api.groq.com/openai/v1/chat/completions"

    # ✅ Prompt système amélioré
    system_message = system_prompt or (
        "Tu es un assistant pédagogique universitaire, expert, patient et très structuré. "
        "Tu expliques avec clarté, exemples, et étapes. "
        "Toujours répondre de manière complète, logique, bien organisé."
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "temperature": temperature,      # ✅ contrôle créativité
        "max_tokens": 4096,              # ✅ plus long output
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
    }

    # ✅ Retry system robust
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"].strip()
            
            # ✅ Vérifier si réponse pas vide
            if not content or len(content) < 20:
                raise ValueError("Réponse trop courte ou vide, retry...")

            return content

        except Exception as e:
            print(f"⚠️ Groq API error (attempt {attempt+1}/{max_retries}) :", e)
            if attempt < max_retries - 1:
                time.sleep(1)  # attendre avant retry
            else:
                return "❌ Erreur : impossible d'obtenir une réponse AI actuellement."

