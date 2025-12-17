import streamlit as st
import google.generativeai as genai
import time

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉")

st.title("🐉 Targaryen Yapay Zekası")
st.write("Dracarys! 🔥")

# ---------------- AKILLI ŞİFRE SİSTEMİ ----------------
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
    model_haritasi = {}
    gorunen_isimler = []

    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # --- KRİTİK DÜZELTME: LİSTEYİ GENİŞLETTİK ---
            # Senin anahtarın 2.0 görüyor, başkasınınki 1.5 görebilir.
            # Hepsini ekliyoruz ki kim girerse girsin çalışsın.
            aday_modeller = [
                "gemini-2.0-flash-exp", # Senin anahtarın için
                "gemini-2.0-flash",     # Senin anahtarın için
                "gemini-1.5-flash",     # Standart anahtarlar için
                "gemini-1.5-flash-001",
                "gemini-1.5-pro"
            ]
            
            sayac = 1
            for m in aday_modeller:
                 # Hata vermemesi için basit bir takma isim veriyoruz
                 # Çalışıp çalışmadığını kod aşağıda deneyecek
                 gercek_isim = m
                 takma_isim = f"Targaryen AI {sayac}"
                 model_haritasi[takma_isim] = gercek_isim
                 gorunen_isimler.append(takma_isim)
                 sayac += 1
                 
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")

    if gorunen_isimler:
        secilen_takma_isim = st.selectbox("Hangi ejderha konuşsun?", gorunen_isimler)
        secilen_gercek_model = model_haritasi[secilen_takma_isim]
    else:
        # Liste boşsa bile en azından senin modelini varsayılan yapalım
        secilen_gercek_model = "gemini-2.0-flash-exp"

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
        model = genai.GenerativeModel(secilen_gercek_model)
        
        with st.chat_message("assistant"):
            with st.spinner("Ejderha düşünüyor... 🔥"):
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        hata_mesaji = str(e)
        # Hata Yönetimi:
        if "404" in hata_mesaji:
             st.error(f"⚠️ Bu ejderha ({secilen_gercek_model}) senin bölgende yaşamıyor. Lütfen yan menüden 'Targaryen AI 2' veya '3'ü seçip tekrar dene.")
        elif "429" in hata_mesaji or "Quota" in hata_mesaji:
            st.warning("⚠️ **Ejderha Çok Yoruldu! (Hız Limiti)**")
            st.info("Çok fazla kişi yüklendiği için kısa bir mola verdik. 1-2 dakika bekle.")
        else:
            st.error(f"Bir hata oluştu: {e}")