# Terminalda: pip install pydub
from pydub import AudioSegment
import io

# Audio baytlarni pydub orqali WAV ga o'tkazish
audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
wav_io = io.BytesIO()
audio_segment.export(wav_io, format="wav")
wav_io.seek(0)

# Keyin esa siz yozgan eski kod:
with sr.AudioFile(wav_io) as source:
    audio_data = recognizer.record(source)


import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator

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

            # --- TUXATISH SHU YERDA ---
            # io.BytesIO(audio_file) o'rniga, baytlarni to'g'ridan-to'g'ri AudioData formatiga o'tkazamiz
            # sample_rate brauzerga qarab 16000, 44100 yoki 48000 bo'lishi mumkin (odatda 16000 yoki 44100)
            audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)

            # 1. Ovozni matnga o'girish (Google API yordamida)
            text = recognizer.recognize_google(audio_data, language="uz-UZ")

            if text:
                st.audio(audio_bytes, format="audio/wav")

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