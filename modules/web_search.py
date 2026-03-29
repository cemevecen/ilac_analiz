from duckduckgo_search import DDGS
import requests
import os

def search_drug_info(drug_name: str) -> str:
    """
    İlaç adına göre web'de arama yapar.
    Önce Türkçe kaynaklarda (ilaçpr.com, vidal.com.tr) arar.
    """
    results_text = ""

    queries = [
        f"{drug_name} ilaç etken madde endikasyon yan etki",
        f"{drug_name} drug active ingredient indication side effects",
        f"{drug_name} site:ilacpr.com OR site:vidal.com.tr",
    ]

    try:
        with DDGS() as ddgs:
            for query in queries[:2]:  # İlk 2 sorgu
                results = list(ddgs.text(query, max_results=3))
                for r in results:
                    results_text += f"\nKaynak: {r.get('href','')}\n"
                    results_text += f"Başlık: {r.get('title','')}\n"
                    results_text += f"Özet: {r.get('body','')}\n"
                    results_text += "-" * 40 + "\n"
    except Exception as e:
        results_text = f"Web arama hatası: {str(e)}"

    return results_text if results_text else "Web'de bilgi bulunamadı."
