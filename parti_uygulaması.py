import streamlit as st
st.set_page_config(page_title="Parti Bilet Takip", page_icon="🎉", layout="centered")

st.title("🎉 Parti Davetli & Bilet Takip")

if "beklenenler" not in st.session_state:
    st.session_state.beklenenler = ["x", "y", "z"]
if "gelenler" not in st.session_state:
    st.session_state.gelenler = []

with st.expander("➕ Yeni Davetli Ekle", expanded=False):
    yeni_isim = st.text_input("Davetli Adı (Çoklu eklemek için virgül kullanın):", key="input_isim")
    if st.button("Listeye Ekle", type="primary"):
        if yeni_isim.strip():
            isimler = [i.strip() for i in yeni_isim.split(",") if i.strip()]
            for isim in isimler:
                if isim not in st.session_state.beklenenler and isim not in st.session_state.gelenler:
                    st.session_state.beklenenler.append(isim)
            st.rerun()

col1, col2, col3 = st.columns(3)
col1.metric("Total Bilet", len(st.session_state.beklenenler) + len(st.session_state.gelenler))
col2.metric("⏳ Beklenenler", len(st.session_state.beklenenler))
col3.metric("🎉 İçeridekiler", len(st.session_state.gelenler))

st.divider()

arama_query = st.text_input("🔍 Kapıda İsim Ara:",
                            placeholder="Bulmak istediğiniz kişinin adını yazın...").strip().lower()

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("⏳ Beklenen Misafirler")

    if arama_query:
        süzülen_beklenenler = [isim for isim in st.session_state.beklenenler if arama_query in isim.lower()]
    else:
        süzülen_beklenenler = sorted(st.session_state.beklenenler)

    if not st.session_state.beklenenler:
        st.info("Herkes geldi, beklenen kimse kalmadı! 🎈")
    elif not süzülen_beklenenler:
        st.warning("Aramanıza uygun beklenen misafir bulunamadı.")
    else:
        for isim in süzülen_beklenenler:
            c1, c2 = st.columns([2, 1])
            c1.write(f"• **{isim}**")
            if c2.button("Geldi ✅", key=f"geldi_{isim}"):
                st.session_state.beklenenler.remove(isim)
                st.session_state.gelenler.append(isim)
                st.rerun()

with right_col:
    st.subheader("🎉 İçeridekiler")

    if not st.session_state.gelenler:
        st.write("Henüz kimse gelmedi.")
    else:
        for isim in reversed(st.session_state.gelenler):
            c1, c2 = st.columns([2, 1])
            c1.write(f"✔️ {isim}")
            if c2.button("Geri Al ↩", key=f"gerial_{isim}"):
                st.session_state.gelenler.remove(isim)
                st.session_state.beklenenler.append(isim)
                st.rerun()