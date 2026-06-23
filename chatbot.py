import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq

load_dotenv()

DOSSIER_VECTEURS = "vecteurs"

def charger_base():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = Chroma(
        persist_directory=DOSSIER_VECTEURS,
        embedding_function=embeddings
    )
    return db

def poser_question(question, db):
    # Chercher les passages pertinents dans les documents
    resultats = db.similarity_search(question, k=3)
    contexte = "\n\n".join([r.page_content for r in resultats])

    # Construire le prompt
    prompt = f"""Tu es un assistant technique spécialisé en FTTH.
Réponds uniquement en te basant sur le contexte fourni.
Si la réponse n'est pas dans le contexte, dis-le clairement.

Contexte extrait des documents techniques :
{contexte}

Question du technicien : {question}

Réponse :"""

    # Appeler le modèle Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Chargement de la base vectorielle...")
    db = charger_base()
    print("Chatbot FTTH prêt. Tapez 'quitter' pour arrêter.\n")

    while True:
        question = input("Technicien : ")
        if question.lower() == "quitter":
            break
        reponse = poser_question(question, db)
        print(f"\nChatbot : {reponse}\n")