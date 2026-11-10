"""
Nace.AI Drex Max Finance (`nace-ai/drex-max-finance`) — Lojistik Finans,
3-Way Matching, Demuraj/Sahte Fiş, Sigorta Rücu, Kredi Risk &
Olasılık / Varyasyon (Yeşil Hat - Gri Alan - Kırmızı Hat Pre-Router) Simülatörü.

Çalıştırmak için:
    python finance_variations_sim.py
"""

from __future__ import annotations

import sys
from typing import Any

from drex_client import (
    encode_image_to_data_url,
    evaluate_decision,
    get_presets,
    make_image_part,
    run_probability_variation_matrix,
)
from sample_generator import SAMPLES_DIR, ensure_sample_images

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_state(preset: dict[str, Any]) -> Any:
    images = preset.get("sample_images", [])
    if not images:
        return preset.get("state_json") or preset.get("state_text", "")
    arr: list[Any] = []
    if preset.get("state_text"):
        arr.append(preset["state_text"])
    for img_name in images:
        arr.append(make_image_part(encode_image_to_data_url(SAMPLES_DIR / img_name)))
    return arr


def main() -> None:
    ensure_sample_images()
    finance_presets = [
        p for p in get_presets() if p["category"] == "Drex Max Finance (Lojistik Finans)"
    ]

    print("=" * 92)
    print("🏦 BÖLÜM 1: NACE.AI DREX MAX FINANCE (`nace-ai/drex-max-finance`) — 5 LOJİSTİK FİNANS SENARYOSU")
    print("=" * 92)

    for idx, preset in enumerate(finance_presets, 1):
        print(f"\n[{idx}/{len(finance_presets)}] {preset['title']}")
        print(f"    Model: {preset['model']} | Görseller: {preset.get('sample_images') or 'JSON State'}")
        res = evaluate_decision(
            state=build_state(preset),
            questions=preset["questions"],
            model=preset["model"],
        )
        if not res["ok"]:
            print("    ❌ Hata:", res.get("error"))
            continue

        resp = res["response"]
        usage = resp.get("usage", {})
        print(
            f"    ⚡ Süre: {res['client_latency_ms']} ms | "
            f"Token: {usage.get('input_tokens', 0)} in | Maliyet: ${float(usage.get('cost', 0)):.6f}"
        )
        print("    " + "-" * 84)
        for qk, ans in resp.get("answers", {}).items():
            if ans["type"] == "noul":
                p = float(ans["noul"]) * 100
                verdict = "EVET (TRUE)" if p >= 50 else "HAYIR (FALSE)"
                print(f"    • [NOUL]   {qk:<36} -> {verdict:<14} (P(True) = %{p:.2f})")
            elif ans["type"] == "choice":
                w = ans["choice"]
                wp = float(ans["probabilities"].get(w, 0)) * 100
                conf = float(ans.get("confidence", 0)) * 100
                print(f"    • [CHOICE] {qk:<36} -> ★ {w} (Olasılık: %{wp:.2f} | Güven: %{conf:.2f})")
            elif ans["type"] == "score":
                sc = float(ans["score"])
                leg = ans.get("legend", {})
                probs = ans.get("probabilities", {})
                top_k = max(probs, key=lambda k: probs[k]) if probs else "0"
                print(
                    f"    • [SCORE]  {qk:<36} -> Skor: {sc:.2f}/{len(leg)-1} "
                    f"(En Yüksek: '{leg.get(str(top_k), top_k)}' %{float(probs.get(top_k, 0))*100:.2f})"
                )

    print("\n\n" + "=" * 92)
    print("🎛️ BÖLÜM 2: OLASILIK, VARYASYON & SYSTEM-ONE PRE-ROUTER (YEŞİL HAT / GRİ ALAN / KIRMIZI HAT) MATRİSİ")
    print("=" * 92)

    for domain in ["3way_matching", "pod_demurrage_fraud", "credit_factoring_risk"]:
        matrix = run_probability_variation_matrix(domain=domain)
        print(f"\n▶ ALAN: {matrix['title']} (Model: {matrix['model']})")
        print("-" * 92)
        for var in matrix["variations"]:
            gate = var.get("prerouter_gate", {})
            print(f"  🔹 {var['label']} ({var['latency_ms']} ms)")
            print(f"     Pre-Router Kapısı : {gate.get('badge')} (Ort. Güven: %{gate.get('avg_confidence', 0)*100:.2f})")
            print(f"     Açıklama          : {gate.get('explanation')}")
            for qk, ans in var.get("answers", {}).items():
                if ans["type"] == "noul":
                    print(f"       - {qk}: P(True) = %{float(ans['noul'])*100:.2f}")
                elif ans["type"] == "choice":
                    w = ans["choice"]
                    wp = float(ans["probabilities"].get(w, 0)) * 100
                    print(f"       - {qk}: ★ {w} (%{wp:.2f})")
                elif ans["type"] == "score":
                    print(f"       - {qk}: Skor = {float(ans['score']):.2f}")

    print("\n" + "=" * 92)
    print("✅ TÜM DREX MAX FINANCE VE OLASILIK VARYASYON SİMÜLASYONLARI TAMAMLANDI")
    print("=" * 92)


if __name__ == "__main__":
    main()
