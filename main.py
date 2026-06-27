# import speech_recognition as sr
# from deep_translator import GoogleTranslator
# from gtts import gTTS
# import os
# import time
#
#
# def ovozli_tarjimon_to_voice():
#     recognizer = sr.Recognizer()
#
#     with sr.Microphone() as source:
#         print("\n=== Jonli Ovozli Tarjimon ===")
#         print("Atrofdagi shovqinlar o'lchanmoqda...")
#         recognizer.adjust_for_ambient_noise(source, duration=1)
#
#         print("\nGapiring (O'zbek tilida)...")
#         audio = recognizer.listen(source)
#         print("Ovoz qayta ishlanmoqda...")
#
#     try:
#         # 1. Ovozni matnga aylantirish
#         matn = recognizer.recognize_google(audio, language="uz-UZ")
#         print(f"\nSiz aytdingiz: {matn}")
#
#         # 2. Ingliz tiliga tarjima qilish
#         tarjima = GoogleTranslator(source='uz', target='en').translate(matn)
#         print(f"Tarjima (Inglizcha): {tarjima}")
#
#         # 3. Tarjimani ovozga aylantirish (Ingliz tilida - 'en')
#         print("Inglizcha talaffuz qilinmoqda...")
#         tts = gTTS(text=tarjima, lang='en', slow=False)
#
#         # Audiofaylni saqlash va chalish
#         audio_fayl = "tarjima.mp3"
#         tts.save(audio_fayl)
#
#         # Operatsion tizimga qarab audioni qo'yish
#         if os.name == 'nt':  # Windows uchun
#             os.system(f"start {audio_fayl}")
#         else:  # Mac yoki Linux uchun
#             os.system(f"open {audio_fayl}" if os.uname().sysname == 'Darwin' else f"xdg-open {audio_fayl}")
#
#     except sr.UnknownValueError:
#         print("Ovozingizni tushuna olmadim.")
#     except sr.RequestError:
#         print("Internetda xatolik.")
#
#
# if __name__ == "__main__":
#     ovozli_tarjimon_to_voice()

