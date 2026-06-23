import os
from ingest import charger_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOSSIER_VECTEURS = "vecteurs"

def vectoriser():
    print("Chargement des documents...")
    documents = charger_documents()

    print("Découpage en morceaux...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    morceaux = []
    for doc in documents:
        if len(doc["texte"]) > 0:
            chunks = splitter.create_documents(
                [doc["texte"]],
                metadatas=[{"source": doc["source"]}]
            )
            morceaux.extend(chunks)

    print(f"{len(morceaux)} morceaux créés.")

    print("Création de la base vectorielle...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = Chroma.from_documents(
        morceaux,
        embeddings,
        persist_directory=DOSSIER_VECTEURS
    )

    print("Base vectorielle sauvegardée avec succès !")

if __name__ == "__main__":
    vectoriser()