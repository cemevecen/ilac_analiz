# 💊 İlaç Analiz Asistanı

Fotoğraf veya kamera ile ilaç kutusunu tara, AI ile detaylı analiz al.

## Özellikler
- 📷 Kamera veya dosya yükleme ile ilaç kutusu okuma
- 🖼️ Gemini Vision ile akıllı görsel analiz
- 🔡 EasyOCR ile yedek metin okuma
- 🌐 DuckDuckGo ile gerçek zamanlı web araması
- 🤖 Groq LLaMA ile hızlı ve detaylı analiz
- 📱 Mobil uyumlu Streamlit arayüzü
- 📄 PDF ve metin raporu indirme

## Kurulum

### 1. Repo'yu klonla
```bash
git clone https://github.com/cemevecen/ilac_analiz.git
cd ilac_analiz
```

### 2. Sanal ortam oluştur
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Bağımlılıkları yükle
```bash
pip install -r requirements.txt
```

### 4. API anahtarlarını ayarla
```bash
cp .env.example .env
# .env dosyasını düzenle, API anahtarlarını gir
```

### 5. Uygulamayı başlat
```bash
streamlit run app.py
```

## API Anahtarları Nereden Alınır?
| Servis | Link | Ücretsiz mi? |
|--------|------|--------------|
| Groq | https://console.groq.com | ✅ Ücretsiz |
| Gemini | https://aistudio.google.com | ✅ Ücretsiz |
| SerpAPI | https://serpapi.com | ⚠️ Sınırlı ücretsiz |

## GitHub'a Deploy
```bash
git add .
git commit -m "İlk commit"
git push origin main
```
Streamlit Cloud: https://share.streamlit.io — repo'yu bağla, .env değişkenlerini Secrets'a gir.

## ⚠️ Yasal Uyarı
Bu uygulama eğitim amaçlıdır. Tıbbi tavsiye vermez.

## 🎓 Bilişim Öğretmeni Python Yapay Zeka Kursü — Görüntü İşleme Projesi
