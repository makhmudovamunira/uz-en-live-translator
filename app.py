import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS  # Yangi kutubxona
import io

st.set_page_config(page_title="Jonli Ovozli Tarjimon", page_icon="🎤")

st.title("🎤 Mukammal Ovozli Tarjimon")
st.write("Quyidagi tugmani bosing, gapiring va 'Stop' tugmasini bosing.")

recognizer = sr.Recognizer()

audio = mic_recorder(
    start_prompt="🎤 Gapirishni boshlash",
    stop_prompt="🛑 To'xtatish",
    just_once=True,
    use_container_width=True,
    callback=None
)

if audio:
    with st.spinner("Ovoz tahlil qilinmoqda va tarjima qilinmoqda..."):
        try:
            audio_bytes = audio['bytes']
            audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)

            # 1. Ovozni matnga o'girish
            text = recognizer.recognize_google(audio_data, language="uz-UZ")

            if text:
                st.subheader("Siz aytdingiz:")
                st.info(text)

                # 2. Ingliz tiliga tarjima qilish
                tarjima = GoogleTranslator(source='uz', target='en').translate(text)

                st.subheader("Inglizcha tarjimasi:")
                st.success(tarjima)

                # --- YANGI QISM: Matnni ovozga aylantirish (TTS) ---
                # Tarjimani ingliz tilida (lang='en') ovozli faylga aylantiramiz
                tts = gTTS(text=tarjima, lang='en', slow=False)

                # Ovozni xotiraga bayt ko'rinishida yozamiz
                tts_audio_buffer = io.BytesIO()
                tts.write_to_fp(tts_audio_buffer)
                tts_audio_buffer.seek(0)

                # Ovozli tarjimani pleyerda chiqarish va avtomatik chalish
                st.subheader("🔊 Ovozli tarjima:")
                st.audio(tts_audio_buffer, format="audio/mp3")

        except sr.UnknownValueError:
            st.error("Ovozingizni aniqlab bo'lmadi. Iltimos, balandroq va aniqroq gapiring.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")