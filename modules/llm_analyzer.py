from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Sen deneyimli bir eczacı ve tıp bilgi asistanısın.
Kullanıcıya ilaçlar hakkında bilgi verirsin.
MUTLAKA her cevabın sonuna şu uyarıyı ekle:

⚠️ UYARI: Bu bilgiler genel bilgilendirme amaçlıdır. Tıbbi tavsiye değildir.
Herhangi bir ilaç kullanmadan önce mutlaka doktorunuza veya eczacınıza danışınız.
Kendi kendinize ilaç kullanmayınız.
"""

def analyze_drug(
    drug_name: str,
    active_ingredient: str,
    web_info: str,
    language: str = "tr"
) -> str:
    """
    Groq LLM ile ilaç analizi yap.
    Web bilgisi varsa onu kullansın, yoksa genel bilgiden yorum yapsın.
    """
    prompt = f"""
İlaç Adı: {drug_name}
Etken Madde: {active_ingredient}

Web'den bulunan bilgiler:
{web_info[:3000] if web_info else "Web bilgisi bulunamadı."}

Lütfen şu başlıkları Türkçe olarak kapsamlı şekilde açıkla:

## 💊 İlaç Hakkında Genel Bilgi

## 🎯 Hangi Hastalıklara İyi Gelir (Endikasyonlar)

## ⚗️ Etken Madde ve Etki Mekanizması

## ⚠️ Yan Etkiler
- Yaygın yan etkiler
- Ciddi yan etkiler (varsa)

## 🚫 Kimler Kullanmamalı (Kontrendikasyonlar)

## 💊 Doz Bilgisi (Genel)

## 🔄 Muadil / Eşdeğer İlaçlar
(Aynı etken maddeyi içeren veya benzer etkili ilaçlar)

## 💡 Önemli Notlar

Bilgi bulunamayan bölümlerde etken maddeye göre genel yorumda bulun.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # veya mixtral-8x7b-32768
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM analiz hatası: {str(e)}"


def quick_ingredient_analysis(ingredients_text: str) -> str:
    """
    Sadece etken madde listesinden hızlı analiz.
    Web bilgisi olmadan direkt çalışır.
    """
    prompt = f"""
Aşağıdaki etken madde/ilaç bilgilerini analiz et:

{ingredients_text[:2000]}

Kısa ve net şekilde:
1. Bu maddeler/ilaç ne için kullanılır?
2. Başlıca yan etkileri neler?
3. Kimler dikkatli olmalı?
4. Muadil alternatifleri neler?
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analiz hatası: {str(e)}"
