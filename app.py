import streamlit as st
import google.generativeai as genai

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉", layout="centered")

st.title("🐉 Targaryen Yapay Zekası")
st.caption("Google Gemini 2.5 & 2.0 (Next Gen Altyapısı)")
st.markdown("---")

# ---------------- ŞİFREYİ ALMA ----------------
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

if not api_key:
    with st.sidebar:
        st.warning("⚠️ Test Modu: Anahtar Elle Giriliyor")
        api_key = st.text_input("Anahtar:", type="password")

# ---------------- EKRAN TEMİZLEME BUTONU ----------------
with st.sidebar:
    if st.button("🧹 Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# ---------------- MODEL SEÇİMİ (KOTA DOSTU LİSTE) ----------------
with st.sidebar:
    st.header("⚙️ Ejderha Seçimi")
    st.info("İpucu: Eğer 'Yoruldu' hatası alırsan 'Syrax' veya 'Yedek Güç' seç.")
    
    # Senin listendeki en mantıklı modeller
    model_secenekleri = {
        "🦎 Syrax (2.0 Lite - En Hızlı)": "gemini-2.0-flash-lite-preview-02-05",
        "⚡ Yedek Güç (Flash Latest)": "gemini-flash-latest",
        "🐉 Balerion (2.5 Flash - Çok Güçlü)": "gemini-2.5-flash",
        "🔥 Caraxes (2.0 Flash)": "gemini-2.0-flash",
    }
    
    secilen_isim = st.selectbox("Ejderha:", list(model_secenekleri.keys()))
    secilen_kod = model_secenekleri[secilen_isim]

# ---------------- SOHBET GEÇMİŞİ ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Dracarys! 🔥 Hangi konuda yardım istersin?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- MESAJ GÖNDERME ----------------
if prompt := st.chat_input("Bir şeyler yaz..."):
    
    if not api_key:
        st.error("Anahtar yok!")
        st.stop()

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(secilen_kod)
        
        with st.chat_message("assistant"):
            with st.spinner(f"{secilen_isim} düşünüyor..."):
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        hata = str(e)
        if "429" in hata or "Quota" in hata:
            st.warning("⚠️ **Ejderha Yoruldu (Kota Sınırı)**")
            st.info("Seçtiğin model (2.5 veya 2.0) çok yeni olduğu için Google hız sınırı koymuş. Lütfen yan menüden **'Syrax (Lite)'** veya **'Yedek Güç'** seçeneğini seçip tekrar dene.")
        elif "404" in hata:
             st.error(f"⚠️ {secilen_kod} şu an bakımda. Başka bir ejderha seç.")
        else:
            st.error(f"Hata: {e}")