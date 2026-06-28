import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

st.set_page_config(page_title="Jonli Ovozli Tarjimon", page_icon="🎤")

st.title("🎤 Ovozli va Gapiradigan Tarjimon")
st.write("Tugmani bosing, o'zbekcha gapiring va '🛑 To'xtatish' tugmasini bosing.")

# Ovozni aniqlovchi obyekt
recognizer = sr.Recognizer()

# Mikrofondan yozish tugmasi
audio = mic_recorder(
    start_prompt="🎤 Gapirishni boshlash",
    stop_prompt="🛑 To'xtatish",
    just_once=True,
    use_container_width=True,
    callback=None
)

# DIQQAT: Hamma jarayon faqat audio kelgandagina (shart ichida) bajarilishi shart!
if audio:
    with st.spinner("Ovozingiz eshitilmoqda va tarjima qilinmoqda..."):
        try:
            audio_bytes = audio['bytes']

            # Kelgan audioni Google tushunadigan formatga o'tkazish
            audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)

            # 1. Ovozni o'zbekcha matnga o'girish
            text = recognizer.recognize_google(audio_data, language="uz-UZ")

            if text:
                st.subheader("Siz aytdingiz:")
                st.info(text)

                # 2. Ingliz tiliga tarjima qilish
                tarjima = GoogleTranslator(source='uz', target='en').translate(text)

                st.subheader("Inglizcha tarjimasi:")
                st.success(tarjima)

                # 3. Tarjimani inglizcha OVOZGA aylantirish (TTS)
                tts = gTTS(text=tarjima, lang='en', slow=False)

                # Audio faylni xotirada vaqtinchalik saqlash
                tts_audio_buffer = io.BytesIO()
                tts.write_to_fp(tts_audio_buffer)
                tts_audio_buffer.seek(0)

                # 4. Ovozli tarjimani pleyerda chiqarish
                st.subheader("🔊 Ovozli tarjimani eshiting:")
                st.audio(tts_audio_buffer, format="audio/mp3")

        except sr.UnknownValueError:
            st.error("Ovozingizni aniqlab bo'lmadi. Iltimos, balandroq va mikrofoningizga yaqinroq gapiring.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")