# import streamlit as st
# from streamlit_mic_recorder import mic_recorder
# import speech_recognition as sr
# from deep_translator import GoogleTranslator
# from pydub import AudioSegment
# import io
#
# st.set_page_config(page_title="Jonli Ovozli Tarjimon", page_icon="🎤")
#
# st.title("🎤 Mukammal Ovozli Tarjimon")
# st.write("Quyidagi tugmani bosing, gapiring va 'Stop' tugmasini bosing.")
#
# # Ovozni aniqlovchi obyekt
# recognizer = sr.Recognizer()
#
# # Mikrofondan yozish tugmasi
# audio = mic_recorder(
#     start_prompt="🎤 Gapirishni boshlash",
#     stop_prompt="🛑 To'xtatish",
#     just_once=True,
#     use_container_width=True,
#     callback=None
# )
#
# # Agar ovoz muvaffaqiyatli yozib bo'lingan bo'lsa
# if audio:
#     with st.spinner("Ovoz tahlil qilinmoqda va tarjima qilinmoqda..."):
#         try:
#             # 1. Audio baytlarni olish
#             audio_bytes = audio['bytes']
#
#             # 2. Pydub orqali audioni standart WAV formatiga o'tkazish
#             audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
#             wav_io = io.BytesIO()
#             audio_segment.export(wav_io, format="wav")
#             wav_io.seek(0)
#
#             # 3. SpeechRecognition formatiga o'tkazish
#             with sr.AudioFile(wav_io) as source:
#                 audio_data = recognizer.record(source)
#
#                 # 4. Ovozni Google API orqali matnga o'girish
#                 text = recognizer.recognize_google(audio_data, language="uz-UZ")
#
#                 if text:
#                     st.audio(audio_bytes, format="audio/wav")  # Ovozni qayta eshitish
#
#                     st.subheader("Siz aytdingiz:")
#                     st.info(text)
#
#                     # 5. Ingliz tiliga tarjima qilish
#                     tarjima = GoogleTranslator(source='uz', target='en').translate(text)
#
#                     st.subheader("Inglizcha tarjimasi:")
#                     st.success(tarjima)
#
#         except sr.UnknownValueError:
#             st.error("Ovozingizni aniqlab bo'lmadi. Iltimos, balandroq va aniqroq gapiring.")
#         except Exception as e:
#             st.error(f"Xatolik yuz berdi: {e}")


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

if audio:
    with st.spinner("Ovozingiz eshitilmoqda va tarjima qilinmoqda..."):
        try:
            audio_bytes = audio['bytes']

            # 1. Baytlarni SpeechRecognition formatiga o'tkazish
            audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)

            # 2. Ovozni o'zbekcha matnga o'girish
            text = recognizer.recognize_google(audio_data, language="uz-UZ")

            if text:
                st.subheader("Siz aytdingiz:")
                st.info(text)

                # 3. Ingliz tiliga tarjima qilish
                tarjima = GoogleTranslator(source='uz', target='en').translate(text)

                st.subheader("Inglizcha tarjimasi:")
                st.success(tarjima)

                # 4. Tarjimani inglizcha OVOZGA aylantirish (TTS)
                tts = gTTS(text=tarjima, lang='en', slow=False)

                # Audio faylni xotirada saqlash
                tts_audio_buffer = io.BytesIO()
                tts.write_to_fp(tts_audio_buffer)
                tts_audio_buffer.seek(0)

                # 5. Ovozli tarjimani pleyerda chiqarish
                st.subheader("🔊 Ovozli tarjimani eshiting:")
                st.audio(tts_audio_buffer, format="audio/mp3")

        except sr.UnknownValueError:
            st.error("Ovozingizni aniqlab bo'lmadi. Iltimos, qaytadan aniqroq gapiring.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")