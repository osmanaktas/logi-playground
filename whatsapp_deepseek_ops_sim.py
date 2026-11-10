"""
Türkiye Lojistik Operasyonlarında WhatsApp / E-Posta Karar Anları &
DeepSeek V4.1 Flash (`deepseek/deepseek-v4.1-flash-1017`) + Drex Max Hibrit Simülatörü.

Simüle Edilen 4 Gerçek Saha Senaryosu:
1. WhatsApp Sohbetinden Yük İlanı Açma (Chat-to-Load) + Kartvizit Fotoğrafından CRM Müşteri Kaydı
2. Uluslararası CMR (TR-RU), Sarp / Verkhniy Lars Gümrük Kapısı Konum Kararı & Türkçe <-> Rusça Çift Yönlü Operasyon Çevirisi
3. Depo Mal Kabul & Yükleme Checklist (#CHK-551) WhatsApp Rampa Denetimi (Spanzet / İstif Blokajı)
4. Şoför WhatsApp Yol Masraf Fişleri (Mazot ÖKC, Otoyol/HGS, Kantar vs Farklı Plakalı Market Fişi) & Harcırah Mahsubu
"""

from __future__ import annotations

import sys

from drex_client import run_whatsapp_operations_and_deepseek_pipeline
from sample_generator import ensure_sample_images

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    ensure_sample_images()

    print("=" * 98)
    print("🚛 TÜRKİYE LOJİSTİK WHATSAPP/E-POSTA KARAR ANLARI & DEEPSEEK V4.1 FLASH HİBRİT SİMÜLATÖRÜ")
    print("   System-1 Karar & 10-12 Soru Filtresi : nace-ai/drex-max & nace-ai/drex-max-finance")
    print("   System-2 Üretken LLM & TR<->RU Çeviri: deepseek/deepseek-v4.1-flash-1017")
    print("=" * 98)

    workflows = [
        "chat_to_load_and_crm_card",
        "cmr_customs_and_ru_tr_translation",
        "warehouse_whatsapp_checklist",
        "driver_road_expenses_audit",
    ]

    for wf in workflows:
        res = run_whatsapp_operations_and_deepseek_pipeline(workflow_type=wf)
        if not res.get("ok"):
            print(f"\n[HATA] {wf}: {res}")
            continue

        s1 = res["step1_system1_decision"]
        s2 = res["step2_deepseek_llm"]
        s3 = res["step3_system1_guardrail"]

        print(f"\n▶ {res['title']}")
        print("-" * 98)
        print(
            f"  [ADIM 1 - SYSTEM-1 KARAR MODELİ] Model: {s1['model']} | Görsel: {res['image_name']} "
            f"| Soru Sayısı: {s1['question_count']} | Süre: {s1['latency_ms']} ms"
        )
        for q_key, ans in s1.get("answers", {}).items():
            q_type = ans.get("type")
            if q_type == "noul":
                prob = float(ans.get("noul", 0.0)) * 100
                verdict = "EVET (TRUE) " if prob >= 50 else "HAYIR (FALSE)"
                print(f"    • [NOUL]   {q_key:<52} -> {verdict} (P = %{prob:.2f})")
            elif q_type == "choice":
                choice = ans.get("choice")
                conf = float(ans.get("confidence", 0.0)) * 100
                win_p = float((ans.get("probabilities") or {}).get(choice, 0.0)) * 100
                print(f"    • [CHOICE] {q_key:<52} -> ★ {choice} (Olasılık: %{win_p:.2f} | Güven: %{conf:.2f})")
            elif q_type == "score":
                score = float(ans.get("score", 0.0))
                legend = ans.get("legend") or {}
                probs = ans.get("probabilities") or {}
                top_idx = max(probs, key=probs.get) if probs else "0"
                print(f"    • [SCORE]  {q_key:<52} -> Skor: {score:.2f} ('{legend.get(top_idx)}' %{ float(probs.get(top_idx, 0))*100:.2f})")

        print(
            f"\n  [ADIM 2 - SYSTEM-2 DEEPSEEK LLM] Model: {s2['model']} | Süre: {s2['latency_ms']} ms"
        )
        print("  " + "." * 94)
        for line in s2.get("generated_output", "").splitlines():
            print(f"    {line}")
        print("  " + "." * 94)

        g_ans = s3.get("answers", {})
        g_align = float(g_ans.get("aligned_with_system1_decision", {}).get("noul", 0.0)) * 100
        g_choice = g_ans.get("safe_for_external_dispatch", {}).get("choice", "")
        print(
            f"  [ADIM 3 - SYSTEM-1 ÇIKTI GUARDRAIL] ({s3['latency_ms']} ms) "
            f"Karara Sadakat: %{g_align:.2f} | Gönderim Onayı: ★ {g_choice}"
        )

    print("\n" + "=" * 98)
    print("✅ TÜM WHATSAPP / E-POSTA OPERASYON & DEEPSEEK V4.1 FLASH SİMÜLASYONLARI TAMAMLANDI")
    print("=" * 98)


if __name__ == "__main__":
    main()
