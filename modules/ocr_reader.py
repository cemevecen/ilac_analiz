import easyocr
import numpy as np
from PIL import Image
import streamlit as st

@st.cache_resource
def get_ocr_reader():
    """EasyOCR reader'ı bir kez yükle, cache'le."""
    return easyocr.Reader(['tr', 'en'], gpu=False)

def extract_text_from_image(image: Image.Image) -> str:
    """
    PIL Image'dan metin çıkar.
    EasyOCR kullanarak Türkçe + İngilizce destekler.
    """
    try:
        reader = get_ocr_reader()
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0, paragraph=True)
        extracted = " ".join(results).strip()
        return extracted if extracted else ""
    except Exception as e:
        return f"OCR hatası: {str(e)}"
