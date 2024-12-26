import streamlit as st
import pandas as pd

# Charger le fichier Excel
def load_excel(file):
    return pd.read_excel(file)

# Chargement du fichier Excel téléchargé
uploaded_file = st.file_uploader("Téléversez votre fichier Excel", type="xlsx")
if uploaded_file:
    data = load_excel(uploaded_file)
    st.write("### Aperçu des données chargées")
    st.dataframe(data)
else:
    st.write("Veuillez téléverser un fichier Excel pour commencer.")
