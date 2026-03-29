import streamlit as st
from PIL import Image
import io
import os
from dotenv import load_dotenv

from modules.ocr_reader import extract_text_from_image
from modules.gemini_vision import analyze_image_with_gemini
from modules.web_search import search_drug_info
from modules.llm_analyzer import analyze_drug, quick_ingredient_analysis
from modules.report_generator import generate_pdf_report
from utils.image_utils import preprocess_image
from utils.text_utils import clean_ocr_text, extract_drug_name

load_dotenv()

# ── Sayfa ayarları ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💊 İlaç Analiz Asistanı",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Özel CSS (mobil uyum) ────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { max-width: 800px; margin: 0 auto; }
    .warning-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        font-weight: bold;
    }
    .result-box {
        background: #f0f7ff;
        border-left: 4px solid #0066cc;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    @media (max-width: 600px) {
        .stButton > button { width: 100% !important; }
        h1 { font-size: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ── Başlık ───────────────────────────────────────────────────────────────────
st.title("💊 İlaç Analiz Asistanı")
st.caption("Fotoğraf çek veya yükle → İlaç hakkında her şeyi öğren")

# ── Uyarı Bandı ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="warning-box">
⚠️ Bu uygulama yalnızca bilgilendirme amaçlıdır.
Tıbbi tavsiye niteliği taşımaz. İlaç kullanmadan önce
mutlaka doktorunuza veya eczacınıza danışınız.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Görsel Giriş ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    camera_photo = st.camera_input("📷 Kamera ile Çek")

with col2:
    uploaded_file = st.file_uploader(
        "📁 Dosya Yükle",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        help="İlaç kutusunun net fotoğrafını yükleyin"
    )

# Aktif görseli belirle
image_source = camera_photo or uploaded_file
image = None

if image_source:
    image = Image.open(io.BytesIO(image_source.getvalue()))
    image = preprocess_image(image)
    st.image(image, caption="Yüklenen Görsel", use_container_width=True)

st.divider()

# ── Manuel Giriş (alternatif) ─────────────────────────────────────────────
with st.expander("✍️ Manuel ilaç adı gir (görsel yoksa)"):
    manual_drug = st.text_input("İlaç adı veya etken madde", placeholder="örn: Aspirin, İbuprofen, Parasetamol...")

# ── Analiz Başlat ────────────────────────────────────────────────────────────
analyze_btn = st.button(
    "🔍 Analiz Et",
    type="primary",
    use_container_width=True,
    disabled=(image is None and not manual_drug)
)

# ── Analiz Süreci ────────────────────────────────────────────────────────────
if analyze_btn:
    drug_name = ""
    active_ingredient = ""
    gemini_data = {}

    with st.status("🔄 Analiz yapılıyor...", expanded=True) as status:

        # ADIM 1: Görsel analiz
        if image:
            st.write("🖼️ Görsel analiz ediliyor (Gemini Vision)...")
            try:
                gemini_data = analyze_image_with_gemini(image)
                drug_name = gemini_data.get("ilac_adi", "")
                active_ingredient = gemini_data.get("etken_madde", "")
                st.write(f"✅ İlaç tespit edildi: **{drug_name}**")
            except Exception:
                st.write("⚠️ Gemini hatası, OCR deneniyor...")

            # Gemini başarısızsa OCR dene
            if not drug_name:
                st.write("🔡 OCR ile metin okunuyor...")
                raw_text = extract_text_from_image(image)
                cleaned = clean_ocr_text(raw_text)
                drug_name = extract_drug_name(cleaned)
                active_ingredient = cleaned
                st.write(f"✅ Metin okundu: {cleaned[:100]}...")

        elif manual_drug:
            drug_name = manual_drug
            active_ingredient = manual_drug

        # ADIM 2: Web araması
        st.write(f"🌐 '{drug_name}' internette aranıyor...")
        web_info = search_drug_info(drug_name)
        if "bulunamadı" in web_info or not web_info.strip():
            st.write("⚠️ İnternet bilgisi sınırlı, etken maddeye göre yorum yapılacak.")
        else:
            st.write("✅ Web bilgisi bulundu.")

        # ADIM 3: LLM Analizi
        st.write("🤖 Groq LLM ile detaylı analiz yapılıyor...")
        if drug_name:
            analysis = analyze_drug(drug_name, active_ingredient, web_info)
        else:
            analysis = quick_ingredient_analysis(active_ingredient)

        status.update(label="✅ Analiz tamamlandı!", state="complete")

    # ── Sonuçlar ────────────────────────────────────────────────────────────
    st.divider()
    st.subheader(f"📋 {drug_name} - Analiz Sonucu")

    # Gemini'den gelen yapısal bilgi
    if gemini_data and "hata" not in gemini_data:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("İlaç Adı", gemini_data.get("ilac_adi", "-"))
        with col_b:
            st.metric("Etken Madde", gemini_data.get("etken_madde", "-"))
        with col_c:
            st.metric("Form", gemini_data.get("form", "-"))

    # Ana analiz metni
    st.markdown(analysis)

    # ── Uyarı (tekrar) ──────────────────────────────────────────────────────
    st.error(
        "🏥 ÖNEMLI UYARI: Bu analiz yapay zeka tarafından oluşturulmuştur. "
        "Tıbbi teşhis veya tedavi tavsiyesi değildir. "
        "İlaç kullanımı için mutlaka doktorunuza danışınız.",
        icon="⚠️"
    )

    # ── İndirme Seçenekleri ─────────────────────────────────────────────────
    st.divider()
    st.subheader("📥 Raporu İndir")
    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        st.download_button(
            label="📄 PDF İndir",
            data=generate_pdf_report(drug_name, analysis),
            file_name=f"ilac_raporu_{drug_name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with dl_col2:
        st.download_button(
            label="📝 Metin İndir",
            data=analysis.encode("utf-8"),
            file_name=f"ilac_raporu_{drug_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("💡 Powered by Groq LLaMA · Google Gemini · EasyOCR · Streamlit")
st.caption("🎓 Bilişim Öğretmeni Python Yapay Zeka Kursü — Görüntü İşleme Projesi")
