import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Sahifa sarlavhasi va dizayni
st.set_page_config(page_title="Jonli Tarjimon", page_icon="🎤", layout="centered")

st.title("🎤 Jonli Ovozli Tarjimon")
st.write("Matnni kiriting yoki quyidagi maydonga yozing (O'zbekcha -> Inglizcha):")

# Foydalanuvchidan matn qabul qilish
# (Eslatma: Streamlit Cloud serverida mikrofon bilan jonli ishlash uchun qo'shimcha komponentlar kerak,
# shuning uchun veb-versiyada matnli va ovozli tarjima eng barqaror yo'ldir)
matn = st.text_area("O'zbekcha matn:", placeholder="Bu yerga biror narsa yozing...")

if st.button("Tarjima qilish va Ovozlashtirish", type="primary"):
    if matn.strip() != "":
        with st.spinner("Tarjima qilinmoqda..."):
            try:
                # 1. Tarjima
                tarjima = GoogleTranslator(source='uz', target='en').translate(matn)

                # 2. Natijalarni ko'rsatish
                st.success(f"**Tarjima (Inglizcha):** {tarjima}")

                # 3. Ovozga aylantirish
                tts = gTTS(text=tarjima, lang='en', slow=False)
                audio_fayl = "translation.mp3"
                tts.save(audio_fayl)

                # Audio pleyerni ekranga chiqarish
                st.audio(audio_fayl, format="audio/mp3")

            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")
    else:
        st.warning("Iltimos, avval matn kiriting!")