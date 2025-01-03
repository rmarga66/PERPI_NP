import streamlit as st
import pandas as pd
from fpdf import FPDF

# Créer une classe pour générer le PDF
class PDF(FPDF):
    def header(self):
        self.set_fill_color(255, 0, 0)  # Couleur rouge pour le header
        self.set_text_color(255, 255, 255)  # Texte en blanc
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PERPI NP - Facture de Santé', 0, 1, 'C', fill=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(255, 0, 0)  # Texte en rouge pour le footer
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_invoice(self, data):
        self.set_text_color(0, 0, 0)  # Texte en noir pour les détails
        self.set_font('Arial', '', 12)
        for i, row in data.iterrows():
            self.cell(0, 10, self.encode_text(f"Nom / Prénom du Patient: {row['Nom / Prénom du Patient']}"), ln=True, border=0, align='L')
            self.cell(0, 10, self.encode_text(f"Numero SAP: {row['Numero SAP']}"), ln=True, border=0, align='L')
            self.cell(0, 10, self.encode_text(f"Traitement: {row['Traitement']}"), ln=True, border=0, align='L')
            self.cell(0, 10, self.encode_text(f"Montant HT: {row['Montant HT']}"), ln=True, border=0, align='L')
            self.ln(5)

    def encode_text(self, text):
        return text.encode('latin-1', 'replace').decode('latin-1')

# Créer un tableau de données vide avec des colonnes prédéfinies
def create_empty_dataframe():
    columns = ["Nom / Prénom du Patient", "Numero SAP", "Traitement", "Montant HT"]
    data = pd.DataFrame(columns=columns)
    return data

# Interface principale
def main():
    st.set_page_config(page_title="PERPI NP - Santé", page_icon="👩🏻‍⚕️", layout="centered")
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(90deg, rgba(255,0,0,1) 0%, rgba(255,255,0,1) 100%);
            background-attachment: fixed;
            color: black;
        }
        .stButton>button {
            background-color: #FF0000;
            color: white;
            border-radius: 5px;
        }
        .stMarkdown {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("👩🏻‍⚕️ PERPI NP - Gestion des Patients")

    if "data" not in st.session_state:
        st.session_state.data = create_empty_dataframe()

    st.write("### C'est tarpin facile à remplir !")

    # Interface pour remplir les données ligne par ligne
    data = st.session_state.data
    with st.form("formulaire_patient"):
        nom = st.text_input("Nom / Prénom du Patient")
        sap = st.text_input("Numero SAP")
        traitement = st.text_input("Traitement")
        prix = st.number_input("Montant HT", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Ajouter")

        if submit:
            new_row = pd.DataFrame({
                "Nom / Prénom du Patient": [nom],
                "Numero SAP": [sap],
                "Traitement": [traitement],
                "Montant HT": [f"{prix:.2f}"]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.success("C'est Perpi Bébé !")

    # Afficher les données saisies
    st.write("### Données Actuelles")
    st.dataframe(st.session_state.data)

    if st.button("Valide avant ta shtoumpe !"):
        if st.session_state.data.empty:
            st.error("Veuillez remplir au moins une ligne avant de valider.")
        else:
            generate_pdf(st.session_state.data)

# Générer un PDF à partir des données
def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Fiche Patient', 0, 1, 'C')
    pdf.ln(10)
    pdf.add_invoice(data)

    pdf_output = "facture_output.pdf"
    pdf.output(pdf_output, dest='F')

    with open(pdf_output, "rb") as file:
        st.download_button(
            label="📥 Télécharge la Facture le Fry (PDF)",
            data=file,
            file_name="facture_fry_sante.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
