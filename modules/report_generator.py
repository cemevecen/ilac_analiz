from fpdf import FPDF
from datetime import datetime
from pathlib import Path
import unicodedata


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

    return ""


def _normalize_pdf_text(text: str) -> str:
    """Core PDF font fallback icin Turkce karakterleri ASCII'ye indirger."""
    translation_table = str.maketrans({
        "ç": "c",
        "Ç": "C",
        "ğ": "g",
        "Ğ": "G",
        "ı": "i",
        "İ": "I",
        "ö": "o",
        "Ö": "O",
        "ş": "s",
        "Ş": "S",
        "ü": "u",
        "Ü": "U",
        "â": "a",
        "Â": "A",
        "î": "i",
        "Î": "I",
        "û": "u",
        "Û": "U",
        "⚠": "",
        "️": "",
        "💊": "",
        "🎯": "",
        "⚗": "",
        "🚫": "",
        "🔄": "",
        "💡": "",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "\u00a0": " ",
    })
    normalized = text.translate(translation_table)
    normalized = unicodedata.normalize("NFKD", normalized)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned_lines = [" ".join(line.split()) for line in normalized.splitlines()]
    return "\n".join(cleaned_lines)


def _configure_pdf_font(pdf: FPDF) -> tuple[str, bool]:
    """Unicode font varsa onu, yoksa core Helvetica'yi kullan."""
    font_path = _find_unicode_font()
    if font_path:
        pdf.add_font("UnicodeFont", "", font_path)
        return "UnicodeFont", False
    return "Helvetica", True


def _pdf_safe_text(text: str, ascii_only: bool) -> str:
    return _normalize_pdf_text(text) if ascii_only else text

def generate_pdf_report(drug_name: str, analysis_text: str) -> bytes:
    """
    Analiz sonucunu PDF olarak oluştur ve bytes döndür.
    """
    pdf = FPDF()
    pdf.add_page()

    # Unicode font yoksa core font ile bozulmadan devam et.
    font_name, ascii_only = _configure_pdf_font(pdf)
    safe_drug_name = _pdf_safe_text(drug_name, ascii_only)

    # Başlık
    pdf.set_font(font_name, size=16)
    pdf.cell(0, 12, _pdf_safe_text(f"Ilac Analiz Raporu: {safe_drug_name}", ascii_only), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font(font_name, size=10)
    pdf.cell(0, 8, _pdf_safe_text(f"Olusturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ascii_only), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    # Uyarı kutusu
    pdf.set_fill_color(255, 243, 205)
    pdf.set_font(font_name, size=10)
    pdf.multi_cell(0, 8,
        _pdf_safe_text(
            "ONEMLI UYARI: BU RAPOR BILGILENDIRME AMACLIDIR. TIBBI TAVSIYE DEGILDIR. "
            "ILAC KULLANMADAN ONCE DOKTORUNUZA DANISINIZ.",
            ascii_only,
        ),
        fill=True)
    pdf.ln(5)

    # Analiz içeriği
    pdf.set_font(font_name, size=11)
    # Markdown başlıklarını temizle
    clean_text = analysis_text.replace("##", "").replace("**", "").replace("*", "")
    pdf.multi_cell(0, 7, _pdf_safe_text(clean_text, ascii_only))

    # PDF'i bytes olarak döndür
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)
