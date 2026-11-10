"""
Depo (WMS), Lojistik & Mobil Yük Borsası için 4-Katmanlı Hibrit Mimari Simülatörü:
  Katman 1 (System 1 - Drex Max): Görsel + JSON durumunu tek ileri geçişte (0 metin üretimi) puanlar.
  Katman 2 (Backend Mikroservis Kapısı): Güven eşiği (Confidence >= 0.80) ile deterministik DB/ERP işlemini tetikler.
  Katman 3 (System 2 - Üretken LLM): Sadece insan bildirimi/özeti gerekiyorsa System-1 kararına sadık metin üretir.
  Katman 4 (System 1 - Çıktı Guardrail): Üretilen bildirimi müşteriye/sürücüye göndermeden önce halüsinasyon kontrolünden geçirir.

Çalıştırmak için:
    python logistics_pipeline_sim.py
"""

from __future__ import annotations

import json
import sys

from drex_client import run_hybrid_logistics_pipeline
from sample_generator import ensure_sample_images

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    ensure_sample_images()

    scenarios = [
        ("pod_dispute", "SENARYO A: MOBİL YÜK BORSASI — SEVK İRSALİYESİ (POD) HASAR ŞERHİ & ESCROW BLOKE HATTI"),
        ("wms_hazmat_dock", "SENARYO B: DEPO (WMS) RAMPA KABUL — BEYAN EDİLMEMİŞ ADR & KİMYASAL SIZINTI KARANTİNA HATTI"),
        ("load_board_matching", "SENARYO C: MOBİL YÜK BORSASI — SOĞUK ZİNCİR (-18°C) & SİGORTA UYUMSUZ TEKLİF ENGELLEME HATTI"),
    ]

    print("=" * 88)
    print("🚛 DEPO, LOJİSTİK & MOBİL YÜK BORSASI: SYSTEM-1 (DREX MAX) + SYSTEM-2 (LLM) ORKESTRASYONU")
    print("=" * 88)

    for code, title in scenarios:
        print(f"\n▶ {title}")
        print("-" * 88)
        res = run_hybrid_logistics_pipeline(scenario_type=code)
        if not res.get("ok"):
            print("❌ Hata:", res.get("error"))
            continue

        s1 = res["step1_system1_vision_decision"]
        s2 = res["step2_backend_orchestration"]
        s3 = res["step3_system2_llm_generation"]
        s4 = res["step4_system1_output_guardrail"]

        print(f"  [KATMAN 1 — System-1 Drex Max Görsel+JSON Kararı] ({s1['latency_ms']} ms | Maliyet: ${s1['usage'].get('cost', 0):.6f})")
        for k, ans in s1["answers"].items():
            if ans["type"] == "noul":
                print(f"     • {k}: P(True) = %{float(ans['noul']) * 100:.2f}")
            elif ans["type"] == "choice":
                print(f"     • {k}: ★ {ans['choice']} (Güven: %{float(ans.get('confidence', 0)) * 100:.2f})")
            elif ans["type"] == "score":
                print(f"     • {k}: Skor = {float(ans['score']):.2f}")

        print(f"\n  [KATMAN 2 — Uygulama / Mikroservis Kapısı (Deterministik Eşik >= %80)]")
        print(f"     • Güven Eşiği Geçildi mi? : {s2['gate_passed']} (Gerçekleşen Güven: %{s2['actual_confidence'] * 100:.2f})")
        print(f"     • Çağrılan Mikroservis    : {s2['executed_microservice']}")
        print(f"     • Veritabanı İşlem Kaydı  : {s2['database_tx']}")

        print(f"\n  [KATMAN 3 — System-2 Üretken LLM ({s3['model']}) Sürücü/Operatör Bildirim Taslağı] ({s3['latency_ms']} ms)")
        print(f"     \"{s3['generated_notification']}\"")

        print(f"\n  [KATMAN 4 — System-1 Drex Max Çıktı Denetimi (Hallucination & Policy Guardrail)] ({s4['latency_ms']} ms)")
        for k, ans in s4["answers"].items():
            if ans["type"] == "noul":
                print(f"     • {k}: P(True) = %{float(ans['noul']) * 100:.2f}")
            elif ans["type"] == "choice":
                print(f"     • {k}: ★ {ans['choice']} (Güven: %{float(ans.get('confidence', 0)) * 100:.2f})")

    print("\n" + "=" * 88)
    print("✅ 4-KATMANLI HİBRİT LOJİSTİK & YÜK BORSASI SİMÜLASYONU TAMAMLANDI")
    print("=" * 88)


if __name__ == "__main__":
    main()
