import streamlit as st
import sqlite3
import os

# Configurare baza de date
if not os.path.exists('uploads'):
    os.makedirs('uploads')

conn = sqlite3.connect('proiecte.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS proiecte 
             (id INTEGER PRIMARY KEY, titlu TEXT, descriere TEXT, asignat TEXT, fisier TEXT)''')
conn.commit()

st.title("🚀 Manager Proiecte (Echipa Noastră)")

# 1. Formular pentru proiect nou
with st.expander("➕ Adaugă un proiect nou"):
    with st.form("proiect_nou", clear_on_submit=True):
        titlu = st.text_input("Titlu Proiect")
        desc = st.text_area("Descriere Extinsă")
        col1, col2 = st.columns(2)
        with col1:
            asignat = st.selectbox("Alocat către", ["Marius", "Coleg"])
        with col2:
            file = st.file_uploader("Atașează fișier", type=['png', 'jpg', 'pdf', 'docx'])
        
        submit = st.form_submit_button("Salvează Proiectul")
        
        if submit:
            file_path = None
            if file is not None:
                file_path = os.path.join("uploads", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            
            c.execute("INSERT INTO proiecte (titlu, descriere, asignat, fisier) VALUES (?,?,?,?)", 
                      (titlu, desc, asignat, file_path))
            conn.commit()
            st.success("Proiect salvat!")

# 2. Afișare proiecte
st.header("📋 Proiecte în lucru")
proiecte = c.execute("SELECT * FROM proiecte ORDER BY id DESC").fetchall()

for p in proiecte:
    with st.container(border=True):
        st.subheader(f"{p[1]}")
        st.write(f"**Alocat către:** {p[3]}")
        st.write(f"**Descriere:** {p[2]}")
        if p[4]:
            st.write(f"📎 [Descarcă fișier atașat](sandbox:/{p[4]})") # Notă: link-ul va fi local