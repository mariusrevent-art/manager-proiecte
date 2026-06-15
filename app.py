import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurarea conexiunii (vom pune cheia JSON în Streamlit Secrets)
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
# Streamlit va citi cheia din setările de "Secrets"
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open("BazaDateProiecte").sheet1

st.title("Manager Proiecte Echipa")

# Formular
with st.form("proiect_nou"):
    titlu = st.text_input("Titlu")
    desc = st.text_area("Descriere")
    asignat = st.selectbox("Asignat către", ["Marius", "Coleg"])
    submit = st.form_submit_button("Salvează")
    
    if submit:
        sheet.append_row([titlu, desc, asignat, "Fara fisier"])
        st.success("Adăugat în Google Sheets!")

# Afișare date
data = sheet.get_all_values()
for row in data[1:]: # Sarim peste header
    st.write(f"**{row[0]}** - {row[2]}")
