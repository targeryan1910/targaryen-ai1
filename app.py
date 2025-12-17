import streamlit as st
import google.generativeai as genai

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉", layout="centered")

st.title("🐉 Targaryen Yapay Zekası")
st.caption("Google Gemini 2.5 & 2.0 (Gelecek Nesil Modeller)")
st.markdown("---") # Çizgi çek

# ---------------- ŞİFREYİ GİZLİ KASADAN ALMA ----------------
api_key = None
try:
    # Streamlit Secrets üzerinden şifreyi çekiyoruz
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# Eğer kasada şifre yoksa (Bilgisayarda test ediyorsan) elle gir
if not api_key:
    with st.sidebar:
        st.warning("⚠️ Gizli anahtar bulunamadı (Test Modu).")
        api_key = st.text_input("Anahtarı Elle Gir:", type="password")

# ---------------- MODEL SEÇİMİ (SENİN ÖZEL LİSTEN) ----------------
with st.sidebar:
    st.header("⚙️ Ejderha Seçimi")
    st.write("Senin hesabına özel açılan yeni nesil modeller:")
    
    # Senin ekran görüntüsündeki çalışan modelleri buraya ekledim
    model_secenekleri = {
        "🐉 Balerion (Gemini 2.5 Flash)": "gemini-2.5-flash",
        "🐲 Vhagar (Gemini 2.0 Flash)": "gemini-2.0-flash",
        "🔥 Caraxes (Gemini 2.0 Exp)": "gemini-2.0-flash-exp",
        "🦎 Syrax (Gemini 2.0 Lite)": "gemini-2.0-flash-lite-preview-02-05"
    }
    
    secilen_isim = st.selectbox("Hangi ejderha konuşsun?", list(model_secenekleri.keys()))
    secilen_kod = model_secenekleri[secilen_isim]
    
    st.success(f"Seçili Motor: {secilen_kod}")
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# ---------------- SOHBET GEÇMİŞİ ----------------
if "messages" not in st.session_state:
    # İlk açılış mesajı
    st.session_state.messages = [
        {"role": "assistant", "content": "Valar Morghulis... Ben Targaryen hanesi hizmetindeki yapay zekayım. Sana nasıl yardım edebilirim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- MESAJ GÖNDERME ----------------
if prompt := st.chat_input("Sorunu buraya yaz..."):
    
    if not api_key:
        st.error("Lütfen önce API Anahtarını ayarlara (Secrets) kaydet.")
        st.stop()

    # Kullanıcı mesajını ekrana bas
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Cevap üret
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(secilen_kod)
        
        with st.chat_message("assistant"):
            with st.spinner(f"{secilen_isim} alev hazırlıyor... 🔥"):
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        hata = str(e)
        if "429" in hata or "Quota" in hata:
            st.warning("⚠️ **Ejderha Yoruldu (Kota Doldu)**")
            st.info("Bu model çok yeni olduğu için Google geçici bir sınır koydu. Yan menüden 'Syrax (Lite)' veya 'Vhagar' seçip tekrar dene.")
        elif "404" in hata:
             st.error(f"⚠️ {secilen_kod} şu an ulaşılamıyor. Lütfen menüden başka bir model seç.")
        else:
            st.error(f"Bir hata oluştu: {e}")