"""
CLI Benchmark & Capability Simulator for Nace.AI Drex Max (`nace-ai/drex-max`).
Executes all 6 multimodal (vision) and JSON decision scenarios against OpenRouter
and outputs calibrated probability distributions, confidence scores, and cost metrics.

Usage:
    python cli_demo.py
"""

from __future__ import annotations

import sys
from typing import Any

from drex_client import (
    encode_image_to_data_url,
    evaluate_decision,
    get_presets,
    make_image_part,
)
from sample_generator import SAMPLES_DIR, ensure_sample_images

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_preset_state(preset: dict[str, Any]) -> Any:
    images = preset.get("sample_images", [])
    if not images:
        return preset.get("state_json") or preset.get("state_text", "")

    state_list: list[Any] = []
    if preset.get("state_text"):
        state_list.append(preset["state_text"])
    for img_name in images:
        data_url = encode_image_to_data_url(SAMPLES_DIR / img_name)
        state_list.append(make_image_part(data_url))
    return state_list


def run_all_simulations() -> None:
    ensure_sample_images()
    presets = get_presets()

    print("=" * 82)
    print("🎯 NACE.AI DREX MAX (nace-ai/drex-max) — MULTIMODAL DECISION BENCHMARK SUITE")
    print("=" * 82)

    total_cost = 0.0
    total_tokens = 0

    for idx, preset in enumerate(presets, 1):
        print(f"\n[{idx}/{len(presets)}] {preset['title']}")
        print(f"    Kategori : {preset['category']} | Görseller: {preset.get('sample_images') or 'Yok (JSON)'}")

        state = build_preset_state(preset)
        result = evaluate_decision(
            state=state,
            questions=preset["questions"],
            model=preset.get("model", "nace-ai/drex-max"),
        )

        if not result["ok"]:
            print(f"    ❌ HATA ({result['status_code']}): {result.get('error')}")
            continue

        resp = result["response"]
        usage = resp.get("usage", {})
        cost = float(usage.get("cost", 0.0))
        in_tok = int(usage.get("input_tokens", 0))
        total_cost += cost
        total_tokens += in_tok

        print(
            f"    ⚡ Süre: {result['client_latency_ms']} ms | "
            f"Girdi Token: {in_tok} | Maliyet: ${cost:.6f} | Sağlayıcı: {resp.get('provider')}"
        )
        print("    " + "-" * 74)

        for q_key, ans in resp.get("answers", {}).items():
            q_type = ans.get("type")
            if q_type == "noul":
                prob = float(ans.get("noul", 0.0))
                verdict = "EVET (TRUE)" if prob >= 0.5 else "HAYIR (FALSE)"
                print(f"    • [NOUL]   {q_key:<26} -> {verdict:<14} (P(True) = %{prob * 100:.2f})")
            elif q_type == "choice":
                winner = ans.get("choice")
                probs = ans.get("probabilities", {})
                win_p = float(probs.get(winner, 0.0)) * 100
                conf = float(ans.get("confidence", 0.0)) * 100
                print(
                    f"    • [CHOICE] {q_key:<26} -> {winner:<24} "
                    f"(Olasılık: %{win_p:.2f} | Güven: %{conf:.2f})"
                )
            elif q_type == "score":
                score_val = float(ans.get("score", 0.0))
                legend = ans.get("legend", {})
                probs = ans.get("probabilities", {})
                top_k = max(probs, key=lambda k: probs[k]) if probs else "0"
                top_label = legend.get(str(top_k), top_k)
                top_p = float(probs.get(top_k, 0.0)) * 100
                print(
                    f"    • [SCORE]  {q_key:<26} -> Skor: {score_val:.2f} / {len(legend) - 1} "
                    f"(En Yüksek: '{top_label}' %{top_p:.2f})"
                )

    print("\n" + "=" * 82)
    print(
        f"✅ TÜM SİMÜLASYONLAR TAMAMLANDI | Toplam Girdi Token: {total_tokens} | "
        f"Toplam Maliyet: ${total_cost:.6f}"
    )
    print("=" * 82)


if __name__ == "__main__":
    run_all_simulations()
