import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

# Charger le fichier Excel
def load_excel(file):
    return pd.read_excel(file)

# Fonction pour envoyer un email
def send_email(to_email, subject, body, attachment=None, attachment_name="attachment.xlsx"):
    sender_email = "your_email@example.com"  # Remplacez par votre email
    sender_password = "your_password"  # Remplacez par votre mot de passe

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    if attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_name}"
        )
        message.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            return True
    except Exception as e:
        return str(e)

# Chargement du fichier Excel téléchargé
uploaded_file = st.file_uploader("Téléversez votre fichier Excel", type="xlsx")
if uploaded_file:
    data = load_excel(uploaded_file)
    st.write("### Aperçu des données chargées")
    st.dataframe(data)

    # Sélection et calcul des montants HT
    st.write("## Calculette des montants HT")
    selected_rows = st.multiselect(
        "Sélectionnez les lignes à inclure dans le calcul",
        options=data.index,
        format_func=lambda x: f"{data.loc[x, 'Designation']} ({data.loc[x, 'Tarif_HT']} € HT)",
    )

    total_ht = 0
    details = []

    for row in selected_rows:
        quantity = st.number_input(
            f"Quantité pour {data.loc[row, 'Designation']}",
            min_value=0,
            step=1,
            key=row,
        )
        if quantity > 0:
            cost = data.loc[row, 'Tarif_HT'] * quantity
            total_ht += cost
            details.append(f"{data.loc[row, 'Designation']}: {quantity} x {data.loc[row, 'Tarif_HT']}€ HT = {cost:.2f}€ HT")

    if st.button("Calculer"):
        st.success("Calcul terminé !")
        st.write("### Détails de la facture")
        for detail in details:
            st.write(detail)
        st.write(f"### Total HT: {total_ht:.2f}€")

    # Export des résultats et envoi par email
    if st.button("Exporter les résultats"):
        output = BytesIO()
        export_data = pd.DataFrame({"Détails": details, "Total HT": [total_ht]})
        export_data.to_excel(output, index=False)
        output.seek(0)
        st.download_button(
            label="Télécharger les résultats",
            data=output,
            file_name="resultats_calcul.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    email = st.text_input("Entrez l'email pour envoyer les résultats")
    if st.button("Envoyer par email"):
        if email:
            output = BytesIO()
            export_data = pd.DataFrame({"Détails": details, "Total HT": [total_ht]})
            export_data.to_excel(output, index=False)
            output.seek(0)

            success = send_email(
                to_email=email,
                subject="Résultats du calcul",
                body="Veuillez trouver ci-joint les résultats du calcul.",
                attachment=output.getvalue(),
                attachment_name="resultats_calcul.xlsx",
            )

            if success is True:
                st.success(f"Email envoyé avec succès à {email}")
            else:
                st.error(f"Erreur lors de l'envoi de l'email: {success}")
        else:
            st.error("Veuillez entrer une adresse email valide.")
