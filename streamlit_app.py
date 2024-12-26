import streamlit as st
import pandas as pd
from fpdf import FPDF

# Créer une classe pour générer le PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PERPI NP - Document de Santé', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_table(self, data):
        self.set_font('Arial', '', 12)
        for i, row in data.iterrows():
            for col in row:
                self.cell(40, 10, str(col), border=1)
            self.ln()

# Créer un tableau de données vide avec des colonnes prédéfinies
def create_empty_dataframe():
    columns = ["Nom du Patient", "Âge", "Pathologie", "Traitement"]  # Exemples de colonnes liées à la santé
    data = pd.DataFrame(columns=columns)
    return data

# Interface principale
def main():
    st.set_page_config(page_title="PERPI NP - Santé", page_icon="🩺", layout="centered")
    st.title("🩺 PERPI NP - Gestion des Patients")

    if "data" not in st.session_state:
        st.session_state.data = create_empty_dataframe()

    st.write("### Remplissez les informations ci-dessous")

    # Interface pour remplir les données ligne par ligne
    data = st.session_state.data
    with st.form("formulaire_patient"):
        nom = st.text_input("Nom du Patient")
        age = st.number_input("Âge", min_value=0, step=1)
        pathologie = st.text_input("Pathologie")
        traitement = st.text_input("Traitement")
        submit = st.form_submit_button("Ajouter")

        if submit:
            new_row = {"Nom du Patient": nom, "Âge": age, "Pathologie": pathologie, "Traitement": traitement}
            data = data.append(new_row, ignore_index=True)
            st.session_state.data = data
            st.success("Données ajoutées avec succès !")

    # Afficher les données saisies
    st.write("### Données Actuelles")
    st.dataframe(st.session_state.data)

    if st.button("Valider et Générer le PDF"):
        if st.session_state.data.empty:
            st.error("Veuillez remplir au moins une ligne avant de valider.")
        else:
            generate_pdf(st.session_state.data)

# Générer un PDF à partir des données
def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Résumé des Données', 0, 1, 'C')
    pdf.ln(10)
    pdf.add_table(data)

    pdf_output = "output.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as file:
        st.download_button(
            label="📥 Télécharger le PDF",
            data=file,
            file_name="document_sante.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
