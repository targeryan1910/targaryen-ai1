import streamlit as st
import google.generativeai as genai
import time

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉")

st.title("🐉 Targaryen Yapay Zekası")
st.write("Dracarys! 🔥")

# ---------------- ŞİFREYİ ALMA ----------------
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

if not api_key:
    with st.sidebar:
        st.warning("⚠️ Gizli anahtar bulunamadı (Bilgisayar modundasın).")
        api_key = st.text_input("API Anahtarını Elle Gir:", type="password")

# ------------------------------------------------------

with st.sidebar:
    st.header("⚙️ Ejderha Seçimi")
    
    # --- DÜZELTME BURADA: 1.5 FLASH'ı EN BAŞA ALDIK ---
    # Artık site açılınca otomatik olarak en sağlam modeli seçecek.
    aday_modeller = [
        "gemini-1.5-flash",       # EN SAĞLAM VE HIZLI (Varsayılan)
        "gemini-1.5-pro",         # Daha zeki ama yavaş
        "gemini-2.0-flash-exp",   # Deneysel (Hata verebilir)
    ]
    
    # Kullanıcıya seçtirmece
    secim_listesi = [f"Targaryen AI {i+1} ({m})" for i, m in enumerate(aday_modeller)]
    
    # Kutucuk oluştur
    secim = st.selectbox("Ejderha Modeli:", secim_listesi)
    
    # Seçilenin parantez içindeki gerçek ismini al (örn: gemini-1.5-flash)
    secilen_gercek_model = secim.split("(")[1].replace(")", "")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Valar Morghulis..."):
    
    if not api_key:
        st.warning("Konuşmak için anahtar gerekli!")
        st.stop()

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(secilen_gercek_model)
        
        with st.chat_message("assistant"):
            with st.spinner("Ejderha düşünüyor... 🔥"):
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        hata = str(e)
        if "429" in hata or "Quota" in hata:
            st.warning("⚠️ **Ejderha Çok Yoruldu! (Kota Doldu)**")
            st.info("Şu an kullandığın modelin limiti doldu. Lütfen yan menüden 'Targaryen AI 2' (gemini-1.5-pro) seçeneğini seçip tekrar dene.")
        elif "404" in hata:
             st.error(f"⚠️ Bu model ({secilen_gercek_model}) senin anahtarınla çalışmıyor. Yan menüden diğer ejderhayı seç.")
        else:
            st.error(f"Beklenmedik bir hata: {e}")