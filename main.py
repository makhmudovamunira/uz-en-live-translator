from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

app = FastAPI()

# Frontend va Backend bir-biri bilan gaplashishi uchun CORS ruxsati
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/translate")
def translate(text: str):
    try:
        # 1. Matnni inglizchaga tarjima qilish
        translated_text = GoogleTranslator(source='uz', target='en').translate(text)

        # 2. Tarjimani audio (mp3) faylga aylantirish
        audio_path = "output.mp3"
        tts = gTTS(text=translated_text, lang='en', slow=False)
        tts.save(audio_path)

        # Frontend'ga tarjima matni va audio faylni yuborish
        return {
            "success": True,
            "original": text,
            "translation": translated_text,
            "audio_url": f"http://127.0.0.1:8000/audio"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/audio")
def get_audio():
    # Audioni frontend chalishi uchun fayl ko'rinishida qaytaramiz
    if os.path.exists("output.mp3"):
        return FileResponse("output.mp3", media_type="audio/mpeg")
    return {"error": "Fayl topilmadi"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)