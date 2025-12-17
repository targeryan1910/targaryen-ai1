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
    
    # --- BURAYI GENİŞLETTİK: Hem senin 2.0 modellerin hem de standart 1.5 var ---
    # Senin anahtarın "gemini-2.0-flash-exp" ile çalışacak.
    aday_modeller = [
        "gemini-2.0-flash-exp",   # SENİN İÇİN (Hızlı ve Yeni)
        "gemini-2.0-flash",       # SENİN İÇİN
        "gemini-1.5-flash",       # Standart kullanıcılar için
        "gemini-1.5-flash-001",
        "gemini-1.5-pro"
    ]
    
    secilen_gercek_model = "gemini-2.0-flash-exp" # Varsayılan olarak senin modelin
    
    # Kullanıcıya seçtirmece (İsterse değiştirebilsin)
    secim_listesi = [f"Targaryen AI {i+1} ({m})" for i, m in enumerate(aday_modeller)]
    secim = st.selectbox("Model Seç:", secim_listesi)
    
    # Seçilenin parantez içindeki gerçek ismini al
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
        if "404" in hata:
             st.error(f"⚠️ Seçilen model ({secilen_gercek_model}) anahtarınla uyumlu değil. Lütfen yan menüden başka bir model seç.")
        elif "429" in hata or "Quota" in hata:
            st.warning("⚠️ **Ejderha Çok Yoruldu! (Hız Limiti)**")
            st.info("Çok fazla kişi yüklendiği için kısa bir mola verdik. 1-2 dakika bekle.")
        else:
            st.error(f"Hata: {e}")