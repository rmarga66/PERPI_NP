import streamlit as st
import pandas as pd

# Créer un tableau de données vide avec des colonnes prédéfinies
def create_empty_dataframe():
    columns = ["Colonne 1", "Colonne 2", "Colonne 3"]  # Remplacez par vos colonnes
    data = pd.DataFrame(columns=columns)
    return data

# Fonction pour éditer les champs dans les colonnes
def edit_dataframe(data):
    edited_data = st.experimental_data_editor(data, use_container_width=True)
    return edited_data

# Créer un tableau initial vide
if "data" not in st.session_state:
    st.session_state.data = create_empty_dataframe()

st.write("### Remplissez les champs des colonnes")

data = edit_dataframe(st.session_state.data)

# Enregistrer les données modifiées
st.session_state.data = data

st.write("Les données modifiées sont sauvegardées en mémoire.")
