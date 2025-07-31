import requests
import datetime
import os
import re
import slugify

# Renseigne ici ta clé API Mistral :
MISTRAL_API_KEY = "RxwuBh7NtTUH5vnSv8XYicmIVdUZyLnO"

def call_mistral(prompt, model="mistral-small"):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "top_p": 1,
        "max_tokens": 800
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Étape 1 : Génération du sujet
print("⏳ Génération du sujet d'article...")
topic_raw = call_mistral(
    "Donne uniquement un titre d'article de blog original en lien avec l'actualité mondiale récente en anglais. "
    "Entoure uniquement le titre de guillemets. Aucune autre phrase."
)

match = re.search(r'["“](.{10,200})["”]', topic_raw, re.DOTALL)
topic = match.group(1).replace('\n', ' ').strip() if match else topic_raw.strip()
print(f"✅ Sujet généré : {topic}")

# Étape 2 : Génération de l'article
print("⏳ Génération de l'article...")
article_raw = call_mistral(
    f"Rédige un article de blog optimisé SEO en anglais avec ce sujet : {topic}. "
    "Fais un article structuré avec un titre, une introduction, 2-3 paragraphes et une conclusion. "
    "Écris en bon anglais."
)

article_clean = article_raw.replace("MORE", "").strip()
article_clean = re.sub(r'\n{3,}', '\n\n', article_clean)

# Étape 3 : Création du fichier markdown
today = datetime.date.today()
slug = slugify.slugify(topic)[:80] + "-" + today.strftime("%Y-%m-%d")
filename = f"content/posts/{slug}.md"

markdown = f"""---
title: "{topic}"
date: {today}
draft: false
---

{article_clean}
"""

os.makedirs("content/posts", exist_ok=True)
with open(filename, "w", encoding="utf-8-sig") as f:
    f.write(markdown)

print(f"✅ Article enregistré : {filename}")
