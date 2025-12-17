import streamlit as st
import google.generativeai as genai

# ---------------- TASARIM ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉")
st.title("🐉 Targaryen Yapay Zekası")
st.write("Dracarys! 🔥")

# ---------------- ŞİFRE KONTROLÜ ----------------
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

if not api_key:
    with st.sidebar:
        st.warning("⚠️ Gizli anahtar bulunamadı.")
        api_key = st.text_input("API Anahtarını Elle Gir:", type="password")

# --- DEBUG: HANGİ ŞİFREYİ KULLANIYORUZ? ---
if api_key:
    goster = api_key[:5] + "..." # Şifrenin başını gösterir
    st.sidebar.caption(f"🔑 Aktif Anahtar: {goster}")
    st.sidebar.info("Eğer bu eski şifrense, siteyi 'Reboot' etmelisin.")

# ---------------- MODEL SEÇİMİ ----------------
with st.sidebar:
    st.header("⚙️ Ejderha Seçimi")
    
    # Hepsini kapsayan liste
    aday_modeller = [
        "gemini-1.5-flash",       # Standart Hesaplar (ÖNERİLEN)
        "gemini-2.0-flash-exp",   # Öğrenci/Beta Hesapları
        "gemini-1.5-pro",
        "gemini-2.0-flash" 
    ]
    
    secim_listesi = [f"Ejderha {i+1} ({m})" for i, m in enumerate(aday_modeller)]
    secim = st.selectbox("Modeli Değiştir:", secim_listesi)
    secilen_gercek_model = secim.split("(")[1].replace(")", "")

# ---------------- SOHBET ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Valar Morghulis..."):
    if not api_key:
        st.warning("Anahtar yok!")
        st.stop()

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(secilen_gercek_model)
        
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        hata = str(e)
        if "404" in hata:
             st.error(f"❌ Bu model ({secilen_gercek_model}) senin şifrenle çalışmıyor. Lütfen sol menüden 'Ejderha 2'yi (gemini-2.0) seç.")
        elif "429" in hata:
            st.warning("⚠️ Ejderha yoruldu (Kota Doldu). Biraz bekle veya başka model seç.")
        else:
            st.error(f"Hata: {e}")