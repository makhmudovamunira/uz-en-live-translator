import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
from deep_translator import GoogleTranslator
import queue

st.set_page_config(page_title="Jonli Stream Tarjimon", page_icon="🔊")
st.title("🔊 Haqiqiy Jonli Ovozli Tarjimon")
st.write("Mikrofonni yoqing va to'xtamasdan gapiring. Dastur sizni jonli eshitib, tarjima qiladi.")

# Ovoz bo'laklarini yig'ish uchun navbat (Queue)
if "audio_queue" not in st.session_state:
    st.session_state.audio_queue = queue.Queue()

# Ovozni aniqlovchi obyekt
recognizer = sr.Recognizer()

# WebRTC komponenti - Brauzer mikrofonidan jonli audio oqimini oladi
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"video": False, "audio": True},
)

# Agar mikrofon ulangan va ishlayotgan bo'lsa
if webrtc_ctx.state.playing:
    status_placeholder = st.empty()
    status_placeholder.info("Jonli eshitish rejimi faol... Gapiring!")

    original_placeholder = st.empty()
    translation_placeholder = st.empty()

    # Audio resiverdan ma'lumotlarni o'qiymiz
    audio_receiver = webrtc_ctx.audio_receiver
    if audio_receiver:
        try:
            audio_frames = audio_receiver.get_frames()
            if len(audio_frames) > 0:
                # Ovoz bo'laklarini yagona obyektga yig'amiz
                all_audio = b"".join([frame.to_ndarray().tobytes() for frame in audio_frames])

                # Audio ma'lumotni SpeechRecognition tushunadigan formatga keltiramiz
                audio_data = sr.AudioData(all_audio, sample_rate=48000, sample_width=2)

                # Jonli matnga o'girish (O'zbekcha)
                text = recognizer.recognize_google(audio_data, language="uz-UZ")

                if text:
                    original_placeholder.markdown(f"**Siz aytdingiz (Jonli):** {text}")

                    # Jonli tarjima qilish (Inglizchaga)
                    tarjima = GoogleTranslator(source='uz', target='en').translate(text)
                    translation_placeholder.markdown(f"**Tarjima (Jonli):** {tarjima}")

        except sr.UnknownValueError:
            # Ovoz aniq bo'lmasa yoki qisqa bo'lsa xato bermasligi uchun o'tkazib yuboramiz
            pass
        except Exception as e:
            st.error(f"Xatolik: {e}")
else:
    st.write("Mikrofon o'chiq. Boshlash uchun 'Start' tugmasini bosing.")