import streamlit as st
import google.generativeai as genai
import time

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉")

st.title("🐉 Targaryen Yapay Zekası")
st.write("Dracarys! 🔥 (Google Gemini 1.5 Altyapısı)")

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
            sayac = 1
            # Sadece en hızlı ve kotası bol olan Flash modelini zorlayalım
            # Diğerleri hataya sebep olabilir.
            aday_modeller = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-pro"]
            
            for m in aday_modeller:
                 # Manuel ekleme yapıyoruz ki kota sorunu olmasın
                 gercek_isim = m
                 takma_isim = f"Targaryen AI {sayac} (Hızlı)"
                 model_haritasi[takma_isim] = gercek_isim
                 gorunen_isimler.append(takma_isim)
                 sayac += 1
                 
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")

    if gorunen_isimler:
        secilen_takma_isim = st.selectbox("Hangi ejderha konuşsun?", gorunen_isimler)
        secilen_gercek_model = model_haritasi[secilen_takma_isim]
    else:
        secilen_gercek_model = "gemini-1.5-flash"

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
        # Hata mesajını analiz et
        hata_mesaji = str(e)
        if "429" in hata_mesaji or "Quota" in hata_mesaji:
            st.warning("⚠️ **Ejderha Çok Yoruldu! (Hız Limiti Aşıldı)**")
            st.info("Çok fazla kişi aynı anda soru sorduğu için Google bizi kısa süreliğine durdurdu. Lütfen 1-2 dakika bekleyip tekrar dene. (Ücretsiz sürüm olduğu için bu normaldir).")
        else:
            st.error(f"Bir hata oluştu: {e}")