import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Parti Bilet Takip", page_icon="🎉", layout="centered")

def init_db():
    conn = sqlite3.connect("davetliler.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS davetliler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            durum TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

def davetlileri_getir():
    return pd.read_sql_query("SELECT * FROM davetliler", conn)

def davetli_ekle(isimler):
    c = conn.cursor()
    for isim in isimler:
        c.execute("INSERT INTO davetliler (isim, durum) VALUES (?, ?)", (isim, "Bekleniyor"))
    conn.commit()

def durum_guncelle(davetli_id, yeni_durum):
    c = conn.cursor()
    c.execute("UPDATE davetliler SET durum = ? WHERE id = ?", (yeni_durum, davetli_id))
    conn.commit()

def davetli_sil(davetli_id):
    c = conn.cursor()
    c.execute("DELETE FROM davetliler WHERE id = ?", (davetli_id,))
    conn.commit()

st.title("🎉 Parti Davetli & Bilet Takip")

with st.expander("➕ Yeni Davetli Ekle"):
    yeni_isimler = st.text_area("İsimleri virgülle ayırarak yazın (Örn: Ahmet, Ayşe):")
    if st.button("Listeye Ekle"):
        if yeni_isimler.strip():
            eklenecekler = [i.strip() for i in yeni_isimler.split(",") if i.strip()]
            davetli_ekle(eklenecekler)
            st.success(f"{len(eklenecekler)} kişi başarıyla eklendi!")
            st.rerun()

st.divider()

arama = st.text_input("🔍 Davetli Ara:", "").lower()

df = davetlileri_getir()

if not df.empty:
    if arama:
        df = df[df["isim"].str.lower().str.contains(arama)]

    tab1, tab2 = st.tabs(["⏳ Beklenenler", "✅ İçeridekiler"])

    with tab1:
        bekleyenler = df[df["durum"] == "Bekleniyor"]
        if bekleyenler.empty:
            st.info("Bekleyen davetli yok.")
        for _, row in bekleyenler.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"👤 **{row['isim']}**")
            if col2.button("İçeri Al", key=f"giris_{row['id']}"):
                durum_guncelle(row['id'], "Geldi")
                st.rerun()
            if col3.button("🗑️ Sil", key=f"sil_{row['id']}"):
                davetli_sil(row['id'])
                st.rerun()

    with tab2:
        iceridekiler = df[df["durum"] == "Geldi"]
        if iceridekiler.empty:
            st.info("İçeride henüz kimse yok.")
        for _, row in iceridekiler.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"🎉 **{row['isim']}**")
            if col2.button("Geri Al", key=f"cikis_{row['id']}"):
                durum_guncelle(row['id'], "Bekleniyor")
                st.rerun()
            if col3.button("🗑️ Sil", key=f"sil_in_{row['id']}"):
                davetli_sil(row['id'])
                st.rerun()
else:
    st.info("Henüz eklenmiş bir davetli bulunmuyor.")
