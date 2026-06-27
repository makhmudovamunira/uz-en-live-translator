import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
import io

st.set_page_config(page_title="Jonli Ovozli Tarjimon", page_icon="🎤")

st.title("🎤 Mukammal Ovozli Tarjimon")
st.write("Quyidagi tugmani bosing, gapiring va 'Stop' tugmasini bosing.")

# Ovozni aniqlovchi obyekt
recognizer = sr.Recognizer()

# Mikrofondan yozish tugmasi (Chiroyli interfeys bilan)
audio = mic_recorder(
    start_prompt="🎤 Gapirishni boshlash",
    stop_prompt="🛑 To'xtatish",
    just_once=True,
    use_container_width=True,
    callback=None
)

# Agar ovoz yozib bo'lingan bo'lsa
if audio:
    with st.spinner("Ovoz tahlil qilinmoqda va tarjima qilinmoqda..."):
        try:
            # Kelgan audio baytlarni xotiraga yuklaymiz
            audio_bytes = audio['bytes']
            audio_file = io.BytesIO(audio_bytes)

            # SpeechRecognition audio faylni o'qiydi
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

                # 1. Ovozni matnga o'girish
                text = recognizer.recognize_google(audio_data, language="uz-UZ")

                if text:
                    st.audio(audio_bytes, format="audio/wav")  # Yozilgan ovozingizni qayta eshitish uchun

                    st.subheader("Siz aytdingiz:")
                    st.info(text)

                    # 2. Ingliz tiliga tarjima qilish
                    tarjima = GoogleTranslator(source='uz', target='en').translate(text)

                    st.subheader("Inglizcha tarjimasi:")
                    st.success(tarjima)

        except sr.UnknownValueError:
            st.error("Ovozingizni aniqlab bo'lmadi. Iltimos, balandroq va aniqroq gapiring.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")