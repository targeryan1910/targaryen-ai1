import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Test Modu", page_icon="🔧")
st.title("🔧 Arıza Tespit Modu")
st.warning("Bu modda 'Secrets' kullanılmaz. Yeni anahtarını aşağıya elle yapıştır.")

# 1. Anahtarı KESİN OLARAK elle alıyoruz (Hatayı bulmak için)
api_key = st.text_input("AIzaSyCWe6t77hGFVrWQ8HIPYMXz3c4oIVa4v-I", type="password")

if api_key:
    # 2. Anahtarı sisteme tanıt
    try:
        genai.configure(api_key=api_key)
        
        # 3. Bu anahtarın neleri çalıştırdığını listele (Kanıt görelim)
        st.write("🔍 Bu anahtarın erişebildiği modeller aranıyor...")
        modeller = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modeller.append(m.name)
        
        if not modeller:
            st.error("❌ Bu anahtar HİÇBİR modele erişemiyor! Anahtar bozuk veya hesap kısıtlı.")
        else:
            st.success(f"✅ Bağlantı Başarılı! Erişim iznin olan {len(modeller)} model bulundu.")
            st.json(modeller) # Listeyi ekrana basar

            # 4. En garanti model ile test mesajı at
            test_model = "models/gemini-1.5-flash"
            if test_model in modeller:
                st.info(f"🧪 {test_model} ile deneme yapılıyor...")
                model = genai.GenerativeModel(test_model)
                response = model.generate_content("Merhaba, çalışıyor musun?")
                st.balloons()
                st.success(f"CEVAP GELDİ: {response.text}")
                st.write("🎉 SORUN ÇÖZÜLDÜ! Demek ki suçlu 'Secrets' kısmıymış.")
            else:
                st.warning("⚠️ Anahtar çalışıyor ama '1.5-flash' listende yok. Listeden başka model seçmelisin.")

    except Exception as e:
        st.error(f"💥 ANAHTAR HATASI: {e}")
        st.write("Hata mesajında '429' varsa kota bitik, '403' veya 'Key not valid' varsa anahtar yanlıştır.")