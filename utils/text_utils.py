import re

def clean_ocr_text(text: str) -> str:
    """OCR çıktısındaki gürültüyü temizle."""
    # Çok fazla boşluk
    text = re.sub(r'\s+', ' ', text)
    # Sayı-harf karışıklıkları (OCR sık hatası)
    text = text.replace('0', 'O').replace('1', 'I') if len(text) < 20 else text
    return text.strip()


def extract_drug_name(text: str) -> str:
    """
    Metin içinden en olası ilaç adını çıkar.
    Büyük harfli kelimeler genellikle ilaç adıdır.
    """
    words = text.split()
    # 3 harften uzun büyük harfli kelimeler
    candidates = [w for w in words if w.isupper() and len(w) > 3]
    if candidates:
        return candidates[0]
    # Baş harfi büyük olan ilk kelime
    for w in words:
        if w[0].isupper() and len(w) > 3:
            return w
    return text[:50] if text else "Bilinmiyor"
