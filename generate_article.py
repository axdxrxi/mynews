import requests
import datetime
import os
import re
import slugify
import yaml
import sys

# Vérification clé API
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY or not MISTRAL_API_KEY.startswith("mistral-"):
    print("❌ Erreur : clé API MISTRAL_API_KEY invalide ou absente.")
    sys.exit(1)

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
    if response.status_code != 200:
        print(f"❌ Erreur HTTP : {response.status_code} - {response.text}")
        sys.exit(1)
    return response.json()["choices"][0]["message"]["content"]

# 📁 Debug : Répertoire actuel
print("📁 Working directory:", os.getcwd())

# Étape 1 : Générer le sujet
print("⏳ Génération du sujet d'article...")
topic_raw = call_mistral(
    "Donne uniquement un titre d'article de blog original en lien avec l'actualité mondiale récente en anglais. "
    "Entoure uniquement le titre de guillemets. Aucune autre phrase."
)
match = re.search(r'["“](.{10,200})["”]', topic_raw, re.DOTALL)
topic = match.group(1).replace('\n', ' ').strip() if match else topic_raw.strip()
print(f"✅ Sujet généré : {topic}")

# Étape 2 : Générer l'article
print("⏳ Génération de l'article...")
article_raw = call_mistral(
    f"Rédige un article de blog optimisé SEO en anglais avec ce sujet : {topic}. "
    "Fais un article structuré avec un titre, une introduction, 2-3 paragraphes et une conclusion. "
    "Écris en bon anglais."
)
article_clean = article_raw.replace("MORE", "").strip()
article_clean = re.sub(r'\n{3,}', '\n\n', article_clean)

# Étape 3 : Sauvegarde du fichier Markdown
today = datetime.date.today()
slug = slugify.slugify(topic)[:80] + "-" + today.strftime("%Y-%m-%d")
filename = f"content/posts/{slug}.md"

front_matter = {
    "title": topic,
    "date": str(today),
    "draft": False
}
markdown = "---\n" + yaml.safe_dump(front_matter, sort_keys=False).strip() + "\n---\n\n" + article_clean

os.makedirs("content/posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"✅ Article sauvegardé dans : {filename}")
