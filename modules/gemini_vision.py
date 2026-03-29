import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv
import json

load_dotenv()

def analyze_image_with_gemini(image: Image.Image) -> dict:
    """
    Gemini Vision Pro ile ilaç kutusunu analiz et.
    OCR + bağlam anlama birlikte yapılır.
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
    Bu görüntüde bir ilaç kutusu/ambalajı var.
    Lütfen şunları çıkar ve JSON formatında döndür:
    {
      "ilac_adi": "...",
      "etken_madde": "...",
      "firma": "...",
      "doz": "...",
      "form": "tablet/şurup/kapsül vb.",
      "tum_metin": "kutudaki tüm yazılar"
    }
    Sadece JSON döndür, açıklama ekleme.
    """

    try:
        response = model.generate_content([prompt, image])
        text = response.text.strip()
        # JSON temizleme
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        return {"hata": str(e), "tum_metin": ""}
