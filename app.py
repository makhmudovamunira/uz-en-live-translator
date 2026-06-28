import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import io

st.set_page_config(page_title="Jonli Ovozli Tarjimon", page_icon="🎤")

st.title("🎤 Mukammal Ovozli Tarjimon")
st.write("Quyidagi tugmani bosing, gapiring va 'Stop' tugmasini bosing.")

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

# Agar ovoz muvaffaqiyatli yozib bo'lingan bo'lsa
if audio:
    with st.spinner("Ovoz tahlil qilinmoqda va tarjima qilinmoqda..."):
        try:
            # 1. Audio baytlarni olish
            audio_bytes = audio['bytes']

            # 2. Pydub orqali audioni standart WAV formatiga o'tkazish
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
            wav_io = io.BytesIO()
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)

            # 3. SpeechRecognition formatiga o'tkazish
            with sr.AudioFile(wav_io) as source:
                audio_data = recognizer.record(source)

                # 4. Ovozni Google API orqali matnga o'girish
                text = recognizer.recognize_google(audio_data, language="uz-UZ")

                if text:
                    st.audio(audio_bytes, format="audio/wav")  # Ovozni qayta eshitish

                    st.subheader("Siz aytdingiz:")
                    st.info(text)

                    # 5. Ingliz tiliga tarjima qilish
                    tarjima = GoogleTranslator(source='uz', target='en').translate(text)

                    st.subheader("Inglizcha tarjimasi:")
                    st.success(tarjima)

        except sr.UnknownValueError:
            st.error("Ovozingizni aniqlab bo'lmadi. Iltimos, balandroq va aniqroq gapiring.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")