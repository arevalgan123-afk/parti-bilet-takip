import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Parti Bilet Takip", page_icon="🎉", layout="centered")

st.title("🎉 Parti Davetli & Bilet Takip")

conn = st.connection("gsheets", type=GSheetsConnection)

def verileri_getir():
    return conn.read(ttl=0)

try:
    df = verileri_getir()
except Exception as e:
    st.error("Google Sheets bağlantısı henüz ayarlanmadı. Lütfen Streamlit Secrets ayarını yapın.")
    st.stop()

with st.expander("➕ Yeni Davetli Ekle"):
    yeni_isimler = st.text_area("İsimleri virgülle ayırarak yazın (Örn: Ahmet Yılmaz, Ayşe Kaya):")
    if st.button("Listeye Ekle"):
        if yeni_isimler.strip():
            eklenecekler = [i.strip() for i in yeni_isimler.split(",") if i.strip()]
            yeni_veri = pd.DataFrame({"Isim": eklenecekler, "Durum": ["Bekleniyor"] * len(eklenecekler)})
            guncel_df = pd.concat([df, yeni_veri], ignore_index=True)
            conn.update(data=guncel_df)
            st.success(f"{len(eklenecekler)} kişi listeye eklendi!")
            st.rerun()

st.divider()
arama = st.text_input("🔍 Davetli Ara:", "").lower()

if not df.empty:
    filtreli_df = df[df["Isim"].astype(str).str.lower().str.contains(arama)] if arama else df

    tab1, tab2 = st.tabs(["⏳ Beklenenler", "✅ İçeridekiler"])

    with tab1:
        bekleyenler = filtreli_df[filtreli_df["Durum"] == "Bekleniyor"]
        for idx, row in bekleyenler.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.write(f"👤 **{row['Isim']}**")
            if col2.button("İçeri Al", key=f"giris_{idx}"):
                df.at[idx, "Durum"] = "Geldi"
                conn.update(data=df)
                st.rerun()

    with tab2:
        iceridekiler = filtreli_df[filtreli_df["Durum"] == "Geldi"]
        for idx, row in iceridekiler.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.write(f"🎉 **{row['Isim']}**")
            if col2.button("Geri Al", key=f"cikis_{idx}"):
                df.at[idx, "Durum"] = "Bekleniyor"
                conn.update(data=df)
                st.rerun()
            
