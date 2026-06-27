import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pydub
import numpy as np

st.set_page_config(page_title="Jonli Tarjimon", page_icon="🎤")
st.title("🎤 Haqiqiy Jonli Ovozli Tarjimon")

# Ovozni aniqlash obyektini yaratish va uning sezgirligini sozlash
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Ovoz sezgirligi
recognizer.pause_threshold = 0.8  # Gaplar orasidagi qisqa tanaffus

# Bepul xavfsiz ulanish serverlari (STUN)
RTC_CONFIGURATION = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]
}

# Mikrofon oqimini yoqish
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=2048,  # Bo'laklar hajmini kattalashtirdik
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": False, "audio": True},
)

if webrtc_ctx.state.playing:
    st.info("Mikrofon faol. Gapiring...")

    # Ekranda natijalarni ko'rsatish uchun bo'sh joylar
    original_placeholder = st.empty()
    translation_placeholder = st.empty()

    audio_receiver = webrtc_ctx.audio_receiver
    if audio_receiver:
        try:
            # Audio bo'laklarini olish
            audio_frames = audio_receiver.get_frames()

            if len(audio_frames) > 0:
                # Barcha kelgan audio kadrlarni massivga yig'ish
                sound_chunk = b"".join([frame.to_ndarray().tobytes() for frame in audio_frames])

                # Agar ovoz bo'lagi yetarli darajada katta bo'lsa, uni tahlil qilamiz
                if len(sound_chunk) > 10000:
                    # Streamlit serveri odatda 48000Hz yoki 16000Hz chastotada audio qabul qiladi
                    audio_data = sr.AudioData(sound_chunk, sample_rate=48000, sample_width=2)

                    # 1. Ovozni matnga aylantirish (O'zbekcha)
                    text = recognizer.recognize_google(audio_data, language="uz-UZ")

                    if text.strip():
                        original_placeholder.markdown(f"**Siz aytdingiz:** {text}")

                        # 2. Matnni ingliz tiliga tarjima qilish
                        tarjima = GoogleTranslator(source='uz', target='en').translate(text)
                        translation_placeholder.markdown(f"🎉 **Tarjima:** `{tarjima}`")

        except sr.UnknownValueError:
            # Ovoz hali to'liq aniqlanmagan bo'lsa, xato bermasdan kutib turadi
            original_placeholder.text("Eshityapman... Aniqroq gapiring.")
        except Exception as e:
            st.error(f"Kutilmagan xatolik: {e}")
else:
    st.write("Boshlash uchun yuqoridagi **Start** tugmasini bosing.")