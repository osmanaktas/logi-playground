"""
Çok Kanallı (WhatsApp + E-Posta + Mobil Uygulama) Belge Tekilleştirme, Sınıflandırma &
Onlarca Soruluk (10-13 Soru) Dinamik Denetim Filtresi Simülatörü.

Normal LLM'lerle her gelen fotoğraf/PDF için yavaş ve maliyetli Markdown (.md) üretmek yerine,
`nace-ai/drex-max` ve `nace-ai/drex-max-finance` ile tek ileri geçişte (0 .md üretimi):
  1. Belgenin sınıfını (`choice`) belirler,
  2. Farklı kanallardan (WhatsApp, E-posta, Mobil) gelen mükerrer kopyaları tekilleştirir (`noul`),
  3. Belge sınıfına özel 10-13 soruluk denetim filtresini aynı anda yanıtlar.

Çalıştırmak için:
    python omnichannel_doc_classifier_sim.py
"""

from __future__ import annotations

import sys

from drex_client import run_omnichannel_doc_classifier_pipeline
from sample_generator import ensure_sample_images

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    ensure_sample_images()

    bundles = [
        (
            "whatsapp_email_pod_dedup",
            "PAKET 1: WHATSAPP + E-POSTA + MOBİL UYGULAMA -> SEVK İRSALİYESİ TEKİLLEŞTİRME & 13 SORULUK POD FİLTRESİ",
        ),
        (
            "email_portal_efatura_dedup",
            "PAKET 2: E-POSTA + WHATSAPP -> TEDARİKÇİ e-FATURA TEKİLLEŞTİRME & 12 SORULUK 3-WAY MATCHING FİLTRESİ",
        ),
        (
            "whatsapp_demurrage_receipt_dedup",
            "PAKET 3: WHATSAPP SÜRÜCÜ HATTI -> KANTAR/OTOYOL FİŞİ TEKİLLEŞTİRME (2025 ARŞİV EŞLEŞMESİ) & 10 SORULUK FRAUD FİLTRESİ",
        ),
    ]

    print("=" * 96)
    print("🗂️ ÇOK KANALLI (WHATSAPP / E-POSTA / MOBİL) BELGE TEKİLLEŞTİRME & ONLARCA SORULUK SINIFLANDIRMA SİMÜLATÖRÜ")
    print("=" * 96)

    for bundle_type, title in bundles:
        print(f"\n▶ {title}")
        print("-" * 96)
        res = run_omnichannel_doc_classifier_pipeline(bundle_type=bundle_type)
        if not res.get("ok"):
            print("❌ Hata:", res)
            continue

        cmp = res["legacy_vs_drex_comparison"]
        print(f"  Model          : {res['model']} | Görsel: {res['image_name']} | Tek Geçişte Sorulan Soru: {res['question_count']} Adet")
        print(f"  ⚡ Drex Süresi : {res['latency_ms']} ms | Girdi Token: {res['usage'].get('input_tokens')} | Maliyet: ${cmp['drex_actual_cost_usd']:.6f}")
        print(
            f"  📉 Eski (.md)  : ~{cmp['legacy_estimated_latency_ms']} ms ({cmp['legacy_estimated_output_tokens']} çıktı token, ~${cmp['legacy_estimated_cost_usd']:.6f}) "
            f"-> KAZANÇ: {cmp['cost_savings_multiplier']} & 0 Markdown Halüsinasyonu!"
        )
        print("  " + "-" * 92)

        for qk, ans in res.get("answers", {}).items():
            if ans["type"] == "noul":
                p = float(ans["noul"]) * 100
                verdict = "EVET (TRUE)" if p >= 50 else "HAYIR (FALSE)"
                print(f"    • [NOUL]   {qk:<42} -> {verdict:<14} (P(True) = %{p:.2f})")
            elif ans["type"] == "choice":
                w = ans["choice"]
                wp = float(ans["probabilities"].get(w, 0)) * 100
                conf = float(ans.get("confidence", 0)) * 100
                print(f"    • [CHOICE] {qk:<42} -> ★ {w} (Olasılık: %{wp:.2f} | Güven: %{conf:.2f})")
            elif ans["type"] == "score":
                sc = float(ans["score"])
                leg = ans.get("legend", {})
                probs = ans.get("probabilities", {})
                top_k = max(probs, key=lambda k: probs[k]) if probs else "0"
                print(
                    f"    • [SCORE]  {qk:<42} -> Skor: {sc:.2f}/{len(leg)-1} "
                    f"('{leg.get(str(top_k), top_k)}' %{float(probs.get(top_k, 0))*100:.2f})"
                )

    print("\n" + "=" * 96)
    print("✅ TÜM ÇOK KANALLI BELGE TEKİLLEŞTİRME & SINIFLANDIRMA SİMÜLASYONLARI TAMAMLANDI")
    print("=" * 96)


if __name__ == "__main__":
    main()
