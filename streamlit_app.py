import streamlit as st
import pandas as pd

# Charger le fichier Excel
def load_excel(file):
    return pd.read_excel(file)

# Fonction pour éditer les champs dans les colonnes
def edit_dataframe(data):
    edited_data = st.experimental_data_editor(data, use_container_width=True)
    return edited_data

# Chargement du fichier Excel téléchargé
uploaded_file = st.file_uploader("Téléversez votre fichier Excel", type="xlsx")
if uploaded_file:
    data = load_excel(uploaded_file)
    st.write("### Aperçu des données chargées et modifiables")
    edited_data = edit_dataframe(data)

    # Enregistrer les données modifiées en mémoire
    st.session_state["modified_data"] = edited_data
    st.write("Les données modifiées sont maintenant sauvegardées en mémoire.")
else:
    st.write("Veuillez téléverser un fichier Excel pour commencer.")
