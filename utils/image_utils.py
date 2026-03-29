from PIL import Image
import io

def preprocess_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    """
    OCR için görüntüyü optimize et.
    Boyutu küçült, kontrastı artır.
    """
    # RGB'ye çevir
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Maksimum boyut sınırla
    w, h = image.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        new_size = (int(w * ratio), int(h * ratio))
        image = image.resize(new_size, Image.LANCZOS)

    return image


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    """PIL Image'ı bytes'a çevir."""
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()
