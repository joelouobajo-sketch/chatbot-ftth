import streamlit as st
from chatbot import charger_base, poser_question

st.set_page_config(
    page_title="Chatbot FTTH",
    page_icon="",
    layout="centered"
)

st.title(" Support Technique FTTH")
st.caption("Posez vos questions techniques — je réponds à partir de votre environnement.")

# Charger la base une seule fois
if "db" not in st.session_state:
    with st.spinner("Chargement des documents..."):
        st.session_state.db = charger_base()

# Historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
question = st.chat_input("Posez votre question ici...")

if question:
    # Afficher la question du technicien
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Générer et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            reponse = poser_question(question, st.session_state.db)
        st.markdown(reponse)

    st.session_state.messages.append({"role": "assistant", "content": reponse})