import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

st.set_page_config(page_title="Jonli Ovozli Tarjimon", page_icon="🎤")

st.title("🎤 Ovozli va Gapiradigan Tarjimon")
st.write("Tugmani bosing, o'zbekcha gapiring va '🛑 To'xtatish' tugmasini bosing.")

recognizer = sr.Recognizer()

audio = mic_recorder(
    start_prompt="🎤 Gapirishni boshlash",
    stop_prompt="🛑 To'xtatish",
    just_once=True,
    use_container_width=True,
    callback=None
)

if audio:
    with st.spinner("Ovozingiz tahlil qilinmoqda..."):
        try:
            audio_bytes = audio['bytes']

            # Ba'zi brauzerlarda sample_rate 16000 bo'lsa yaxshi ishlaydi.
            # Shuni o'zgartirib ko'ramiz:
            audio_data = sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2)

            # Ovozni matnga o'girish
            text = recognizer.recognize_google(audio_data, language="uz-UZ")

            if text:
                st.subheader("Siz aytdingiz:")
                st.info(text)

                # Ingliz tiliga tarjima
                tarjima = GoogleTranslator(source='uz', target='en').translate(text)

                st.subheader("Inglizcha tarjimasi:")
                st.success(tarjima)

                # Tarjimani ovozga aylantirish
                tts = gTTS(text=tarjima, lang='en', slow=False)
                tts_audio_buffer = io.BytesIO()
                tts.write_to_fp(tts_audio_buffer)
                tts_audio_buffer.seek(0)

                st.subheader("🔊 Ovozli tarjima:")
                st.audio(tts_audio_buffer, format="audio/mp3")

        except sr.UnknownValueError:
            st.error(
                "Kechirasiz, brauzeringiz yuborgan audio formatini tizim tushunmadi. Iltimos, Google Chrome brauzerida sinab ko'ring yoki ovozni balandroq yozing.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")