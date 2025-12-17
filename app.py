import streamlit as st
import google.generativeai as genai

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉")

st.title("🐉 Targaryen Yapay Zekası")
st.write("Dracarys! 🔥")

# ---------------- AKILLI ŞİFRE SİSTEMİ ----------------
# Önce gizli kasaya (Secrets) bakar. Yoksa kutucuk açar.
api_key = None

try:
    # İnternet sitesi için (Secrets'tan alır)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# Eğer kasada şifre yoksa (Bilgisayarında çalışıyorsa) kutu göster
if not api_key:
    with st.sidebar:
        st.warning("⚠️ Gizli anahtar bulunamadı (Bilgisayar modundasın).")
        api_key = st.text_input("API Anahtarını Elle Gir:", type="password")

# ------------------------------------------------------

# Yan Menü (Model Seçimi)
with st.sidebar:
    st.header("⚙️ Ejderha Seçimi")
    
    model_haritasi = {}
    gorunen_isimler = []

    # Eğer anahtar varsa modelleri listele
    if api_key:
        try:
            genai.configure(api_key=api_key)
            sayac = 1
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    gercek_isim = m.name
                    takma_isim = f"Targaryen AI {sayac}"
                    model_haritasi[takma_isim] = gercek_isim
                    gorunen_isimler.append(takma_isim)
                    sayac += 1
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")

    # Listeden Model Seçtir
    if gorunen_isimler:
        secilen_takma_isim = st.selectbox("Hangi ejderha konuşsun?", gorunen_isimler)
        secilen_gercek_model = model_haritasi[secilen_takma_isim]
    else:
        secilen_gercek_model = "gemini-1.5-flash" # Yedek model

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mesaj Gönderme
if prompt := st.chat_input("Valar Morghulis..."):
    
    if not api_key:
        st.warning("Konuşmak için anahtar gerekli!")
        st.stop()

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        model = genai.GenerativeModel(secilen_gercek_model)
        
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")