from fpdf import FPDF
import io
from datetime import datetime

def generate_pdf_report(drug_name: str, analysis_text: str) -> bytes:
    """
    Analiz sonucunu PDF olarak oluştur ve bytes döndür.
    """
    pdf = FPDF()
    pdf.add_page()

    # Türkçe karakter desteği için font
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)

    # Başlık
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 12, f"İlaç Analiz Raporu: {drug_name}", ln=True, align="C")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 8, f"Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align="C")
    pdf.ln(5)

    # Uyarı kutusu
    pdf.set_fill_color(255, 243, 205)
    pdf.set_font("DejaVu", "B", 10)
    pdf.multi_cell(0, 8,
        "⚠️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR. TIBBİ TAVSİYE DEĞİLDİR. "
        "İLAÇ KULLANMADAN ÖNCE DOKTORUNUZA DANIŞINIZ.",
        fill=True)
    pdf.ln(5)

    # Analiz içeriği
    pdf.set_font("DejaVu", "", 11)
    # Markdown başlıklarını temizle
    clean_text = analysis_text.replace("##", "").replace("**", "").replace("*", "")
    pdf.multi_cell(0, 7, clean_text)

    # PDF'i bytes olarak döndür
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)
