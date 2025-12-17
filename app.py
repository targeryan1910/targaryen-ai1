import streamlit as st
import google.generativeai as genai

# ---------------- TASARIM AYARLARI ----------------
st.set_page_config(page_title="House of Targaryen AI", page_icon="🐉")

st.title("🐉 Targaryen Yapay Zekası")
st.write("Dracarys! 🔥 Sorunu sor, ejderhalar cevaplasın.")
# --------------------------------------------------

# 1. API Anahtarını Al
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("API Anahtarını Gir:", type="password")
    
    # Gerçek model isimlerini ve bizim takacağımız isimleri tutacak sözlük
    model_haritasi = {}
    gorunen_isimler = []

    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # Google'dan gerçek modelleri çekiyoruz
            sayac = 1
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Gerçek ismi (örn: gemini-1.5-flash) alıyoruz
                    gercek_isim = m.name
                    
                    # Ona senin istediğin ismi takıyoruz
                    takma_isim = f"Targaryen AI {sayac}"
                    
                    # Listelere ekliyoruz
                    model_haritasi[takma_isim] = gercek_isim
                    gorunen_isimler.append(takma_isim)
                    sayac += 1
                    
        except Exception as e:
            st.error(f"Anahtar hatası: {e}")

    # 2. Listeden Model Seçtir (Targaryen İsimleri ile)
    if gorunen_isimler:
        secilen_takma_isim = st.selectbox("Ejderhanı Seç:", gorunen_isimler)
        # Seçilen takma ismin gerçek karşılığını bul
        secilen_gercek_model = model_haritasi[secilen_takma_isim]
    else:
        secilen_gercek_model = None
        if not api_key:
            st.info("🔥 Lütfen önce API anahtarını gir.")

# 3. Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Mesaj Gönderme
if prompt := st.chat_input("Valar Morghulis... (Sorunu yaz)"):
    if not api_key:
        st.warning("Önce anahtarı girmelisin.")
        st.stop()
    
    if not secilen_gercek_model:
        st.warning("Bir model seçilmedi.")
        st.stop()

    # Kullanıcı mesajını ekle
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Arka planda gerçek model ismini kullanıyoruz
        model = genai.GenerativeModel(secilen_gercek_model)
        
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")