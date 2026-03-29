from fpdf import FPDF
from datetime import datetime
from pathlib import Path


def _find_unicode_font() -> str:
    """Türkçe karakterleri destekleyen mevcut bir TTF font yolu döndür."""
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/DejaVuSans.ttf",
    ]

    for font_path in font_candidates:
        if Path(font_path).exists():
            return font_path

    raise FileNotFoundError(
        "PDF icin uygun bir Unicode font bulunamadi. "
        "Sistemde DejaVu Sans veya Arial Unicode yuklu olmali."
    )

def generate_pdf_report(drug_name: str, analysis_text: str) -> bytes:
    """
    Analiz sonucunu PDF olarak oluştur ve bytes döndür.
    """
    pdf = FPDF()
    pdf.add_page()

    # Türkçe karakter desteği için sistemdeki uygun Unicode fontu kullan.
    font_path = _find_unicode_font()
    pdf.add_font("UnicodeFont", "", font_path)

    # Başlık
    pdf.set_font("UnicodeFont", size=16)
    pdf.cell(0, 12, f"İlaç Analiz Raporu: {drug_name}", ln=True, align="C")
    pdf.set_font("UnicodeFont", size=10)
    pdf.cell(0, 8, f"Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align="C")
    pdf.ln(5)

    # Uyarı kutusu
    pdf.set_fill_color(255, 243, 205)
    pdf.set_font("UnicodeFont", size=10)
    pdf.multi_cell(0, 8,
        "ONEMLI UYARI: BU RAPOR BILGILENDIRME AMACLIDIR. TIBBI TAVSIYE DEGILDIR. "
        "İLAÇ KULLANMADAN ÖNCE DOKTORUNUZA DANIŞINIZ.",
        fill=True)
    pdf.ln(5)

    # Analiz içeriği
    pdf.set_font("UnicodeFont", size=11)
    # Markdown başlıklarını temizle
    clean_text = analysis_text.replace("##", "").replace("**", "").replace("*", "")
    pdf.multi_cell(0, 7, clean_text)

    # PDF'i bytes olarak döndür
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)
