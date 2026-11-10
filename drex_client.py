"""
Nace.AI Drex Max & Drex Max Finance OpenRouter Client,
Preset Simulation Scenarios, 4-Layer Hybrid Pipeline &
Probability / Variation / Gray-Zone Pre-Router Matrix Simulator.
"""

from __future__ import annotations

import base64
import concurrent.futures
import json
import mimetypes
import os
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

ENDPOINTS = {
    "decisions": "https://openrouter.ai/api/alpha/decisions",
    "systemone": "https://openrouter.ai/api/v1/systemone",
    "chat": "https://openrouter.ai/api/v1/chat/completions",
}

SUPPORTED_MODELS = [
    {
        "id": "nace-ai/drex-max-finance",
        "name": "Nace.AI: Drex Max Finance (27B Multimodal - Finans & Lojistik Denetim)",
        "modalities": ["text", "image"],
        "context_length": 262144,
        "input_price_per_m": 0.06,
        "output_price_per_m": 0.00,
        "description": "Finans, fatura/irsaliye 3-Way Matching, hak ediş/demuraj sahteciliği, sigorta rücu ve kredi/faktoring risk skorlaması için özel eğitilmiş 27B multimodal karar modeli.",
    },
    {
        "id": "nace-ai/drex-max",
        "name": "Nace.AI: Drex Max (27B Multimodal - Genel Karar & Vision)",
        "modalities": ["text", "image"],
        "context_length": 262144,
        "input_price_per_m": 0.06,
        "output_price_per_m": 0.00,
        "description": "Flagship 27B multimodal decision model (Decision Index 0.4: 67.52, Vision Index: 73.92). Accepts text, JSON, and up to 4 images.",
    },
    {
        "id": "nace-ai/drex-v2.0",
        "name": "Nace.AI: Drex v2.0 (35B MoE - 3B Active, Text/JSON)",
        "modalities": ["text"],
        "context_length": 131072,
        "input_price_per_m": 0.06,
        "output_price_per_m": 0.00,
        "description": "35B Mixture-of-Experts text/JSON decision model (3B active parameters).",
    },
    {
        "id": "nace-ai/drex-v1.5",
        "name": "Nace.AI: Drex v1.5 (9B Dense, Text/JSON)",
        "modalities": ["text"],
        "context_length": 131072,
        "input_price_per_m": 0.06,
        "output_price_per_m": 0.00,
        "description": "Compact 9B text/JSON decision model for ultra-fast routing and triage.",
    },
]


def encode_image_to_data_url(image_path: str | Path) -> str:
    path = Path(image_path)
    mime, _ = mimetypes.guess_type(str(path))
    if mime not in ("image/png", "image/jpeg", "image/webp"):
        mime = "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def make_image_part(data_url: str) -> dict[str, Any]:
    return {
        "type": "image_url",
        "image_url": {"url": data_url},
    }


def evaluate_decision(
    state: Any,
    questions: dict[str, Any],
    model: str = "nace-ai/drex-max-finance",
    endpoint_type: str = "decisions",
    api_key: str | None = None,
    timeout: int = 45,
) -> dict[str, Any]:
    """
    Sends a structured decision request (`state` + `questions`) to OpenRouter.
    Returns the parsed response along with `client_latency_ms` and `endpoint_url`.
    """
    key = (api_key or os.getenv("OPENROUTER_API_KEY", "")).strip()
    if not key:
        raise ValueError("OPENROUTER_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

    url = ENDPOINTS.get(endpoint_type, ENDPOINTS["decisions"])
    payload = {
        "model": model,
        "state": state,
        "questions": questions,
    }

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/osmanaktas/drex-max-playground",
        "X-Title": "Drex Max Finance & Logistics Playground",
    }

    t0 = time.perf_counter()
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    try:
        data = resp.json()
    except Exception:
        data = {"error": {"message": resp.text, "code": resp.status_code}}

    if resp.status_code >= 400:
        return {
            "ok": False,
            "status_code": resp.status_code,
            "endpoint_url": url,
            "client_latency_ms": elapsed_ms,
            "error": data.get("error", data),
            "request_payload": payload,
        }

    return {
        "ok": True,
        "status_code": resp.status_code,
        "endpoint_url": url,
        "client_latency_ms": elapsed_ms,
        "response": data,
    }


def classify_prerouter_gate(answers: dict[str, Any]) -> dict[str, Any]:
    """
    Implements the System-One Pre-Router / Gatekeeper logic:
    - High confidence & clear probability -> Direct DB execution (Fast Path, $0 LLM cost)
    - Gray-zone probability (0.35..0.68) or low confidence (<0.72) -> Escalate to Reasoning LLM Agent / Human Specialist
    """
    noul_probs = []
    choice_confs = []
    primary_choice = None

    for k, v in answers.items():
        if v.get("type") == "noul":
            noul_probs.append(float(v.get("noul", 0.5)))
        elif v.get("type") == "choice":
            primary_choice = v.get("choice")
            choice_confs.append(float(v.get("confidence", 0.5)))

    in_gray_zone = any(0.32 <= p <= 0.68 for p in noul_probs) or any(c < 0.72 for c in choice_confs)
    avg_conf = round(sum(choice_confs) / len(choice_confs), 4) if choice_confs else 0.85

    if in_gray_zone or (primary_choice and "gray_zone" in primary_choice) or (primary_choice and "escalate" in primary_choice):
        return {
            "gate_route": "GRAY_ZONE_ESCALATE_TO_REASONING_LLM",
            "badge": "⚠️ GRİ ALAN -> ÜST KATMAN LLM AJANI / UZMAN İNCELEMESİ",
            "color": "amber",
            "avg_confidence": avg_conf,
            "primary_choice": primary_choice,
            "explanation": "Olasılık dağılımı sınır/gri bölgede (0.32–0.68) veya çelişkili kanıt içeriyor; dosya derin muhakeme (System-2 Reasoning LLM) ajanına devredildi.",
        }

    if primary_choice and any(w in primary_choice for w in ("approve", "release", "auto_post", "clean")):
        return {
            "gate_route": "FAST_PATH_AUTO_APPROVE_DB",
            "badge": "✅ YEŞİL HAT -> OTOMATİK DB ONAYI (LLM ÇAĞRILMADI)",
            "color": "emerald",
            "avg_confidence": avg_conf,
            "primary_choice": primary_choice,
            "explanation": "Yüksek güven skoruyla tüm kurallar doğrulandı; üst katman LLM tetiklenmeden doğrudan ERP/Veritabanına işlendi.",
        }

    return {
        "gate_route": "FAST_PATH_AUTO_BLOCK_OR_CLAIM",
        "badge": "🛑 KIRMIZI HAT -> OTOMATİK BLOKE / RÜCU / RED (LLM ÇAĞRILMADI)",
        "color": "rose",
        "avg_confidence": avg_conf,
        "primary_choice": primary_choice,
        "explanation": "Yüksek güven skoruyla kural ihlali/anomali tespit edildi; üst katman LLM maliyeti olmadan otomatik bloke/rücu kuyruğuna alındı.",
    }


def run_probability_variation_matrix(domain: str = "3way_matching") -> dict[str, Any]:
    """
    Runs 3 controlled variations (Clean / Gray-Zone / Violation-Fraud) in parallel
    on `nace-ai/drex-max-finance` to test how probabilities, scores, and System-One
    Pre-Router gates respond to operational variations in logistics finance.
    """
    if domain == "pod_demurrage_fraud":
        title = "Navlun Hak Ediş, POD & Demuraj (Bekleme) Varyasyon Matrisi"
        questions = {
            "pod_signature_and_stamp_complete": {
                "type": "noul",
                "instructions": "Is the POD delivery document properly signed and stamped by the receiver without missing signatures?",
            },
            "demurrage_claim_valid_per_contract": {
                "type": "noul",
                "instructions": "Is the carrier's extra waiting (demurrage) fee claim clearly valid beyond the 4-hour free waiting window?",
            },
            "receipt_authentic_and_untampered": {
                "type": "noul",
                "instructions": "Are the attached weighbridge/toll receipts authentic, from the current trip date, and free of tampering?",
            },
            "prerouter_payout_action": {
                "type": "choice",
                "instructions": "How should the System-One Pre-Router route this carrier payout request?",
                "criteria": {
                    "auto_release_full_payout": "High-confidence clean POD & valid charges -> Release full payout automatically",
                    "gray_zone_escalate_to_reasoning_agent": "Ambiguous/conflicting GPS vs timestamp or borderline waiting time -> Escalate to System-2 Reasoning Agent",
                    "auto_block_fraud_and_hold_escrow": "Tampered/reused receipt or clear false demurrage claim -> Block payout & flag fraud",
                },
            },
            "anomaly_risk_score": {
                "type": "score",
                "instructions": "Rate the financial fraud / discrepancy risk of this carrier claim.",
                "criteria": ["0 - Clean", "1 - Minor Ambiguity (Gray Zone)", "2 - High Discrepancy", "3 - Severe Receipt Fraud"],
            },
        }
        variations = [
            {
                "id": "var_clean",
                "label": "Varyasyon 1: Yeşil Hat (Tam Uyumlu POD & Doğrulanmış Demuraj)",
                "expected_band": "Otomatik Onay (>0.90 Güven)",
                "state": {
                    "trip_id": "TRIP-2026-801",
                    "contract_free_waiting_hours": 4.0,
                    "gps_verified_waiting_hours": 6.5,
                    "claimed_demurrage_hours": 2.5,
                    "pod_status": "Wet stamp + receiver signature verified cleanly. Zero damage notes.",
                    "toll_receipt_check": "Original e-receipt dated 10.11.2026 matching plate 34 TRK 882, unique hash.",
                },
            },
            {
                "id": "var_gray",
                "label": "Varyasyon 2: Gri Alan (GPS Tünel Kaybı & Silik Kaşe — Kararsız Bölge)",
                "expected_band": "Gri Alan (0.35 - 0.65) -> Üst Katman LLM Ajanı",
                "state": {
                    "trip_id": "TRIP-2026-802",
                    "contract_free_waiting_hours": 4.0,
                    "gps_verified_waiting_hours": "Unclear: 3.8 hours logged before GPS signal dropped inside underground depot dock; driver claims 4.3 hours total.",
                    "claimed_demurrage_hours": 0.5,
                    "pod_status": "Receiver signature is present, but rubber stamp ink is partially faded/smudged on the corner. No damage noted, but unconfirmed whether depot delay was caused by driver arriving 15 mins late or dock congestion.",
                    "toll_receipt_check": "Receipt image is slightly cropped at the bottom margin; date matches trip date.",
                },
            },
            {
                "id": "var_fraud",
                "label": "Varyasyon 3: Kırmızı Hat (Oynanmış 2025 Fişi & Haksız Demuraj)",
                "expected_band": "Kesin Red & Fraud Kuyruğu (>0.90 Güven)",
                "state": {
                    "trip_id": "TRIP-2026-803",
                    "contract_free_waiting_hours": 4.0,
                    "gps_verified_waiting_hours": 0.75,
                    "claimed_demurrage_hours": 6.0,
                    "pod_status": "Receiver wrote '3 pallets crushed' reservation note.",
                    "toll_receipt_check": "CRITICAL ALERT: Uploaded receipt #FIS-2025-11049 is from August 2025, plate 06 XYZ 44 crossed out by hand, hash matches previously paid trip #TRIP-2025-109!",
                },
            },
        ]
    elif domain == "credit_factoring_risk":
        title = "Vadeli Yük Veren & Alt Taşıyıcı Kredi / Faktoring Varyasyon Matrisi"
        questions = {
            "liquidity_and_ratios_healthy": {
                "type": "noul",
                "instructions": "Does the applicant meet healthy liquidity standards (Current Ratio >= 1.20 and low short-term debt)?",
            },
            "clean_check_and_payment_history": {
                "type": "noul",
                "instructions": "Is the applicant free of bounced checks (karşılıksız çek), protested notes, and severe payment delays?",
            },
            "requested_limit_within_policy_cap": {
                "type": "noul",
                "instructions": "Is the requested open-account credit limit within the 10% annual turnover policy cap?",
            },
            "credit_prerouter_decision": {
                "type": "choice",
                "instructions": "Which credit routing action should `drex-max-finance` trigger?",
                "criteria": {
                    "auto_approve_open_account_and_factoring": "Strong financials & clean history -> Auto-approve credit limit in sub-second",
                    "gray_zone_escalate_to_credit_underwriter_llm": "Borderline ratios or seasonal dip with partial collateral -> Route to Senior Credit Agent / Underwriter",
                    "auto_reject_credit_require_cash_escrow": "Bounced checks, insolvent ratios, or excessive limit -> Auto-reject credit & enforce Cash/Escrow",
                },
            },
            "default_risk_level": {
                "type": "score",
                "instructions": "Rate the counterparty default risk.",
                "criteria": ["AAA - Prime", "BBB - Moderate / Watch", "CCC - High Risk", "D - Imminent Default"],
            },
        }
        variations = [
            {
                "id": "var_clean",
                "label": "Varyasyon 1: Yeşil Hat (Kurumsal A+ Firma — Otomatik Kredi Tahsisi)",
                "expected_band": "Otomatik Onay",
                "state": {
                    "company": "Anadolu Endüstriyel Lojistik A.Ş. (14 Yıllık Firma)",
                    "annual_turnover_tl": 180000000,
                    "requested_open_account_limit_tl": 9000000,
                    "limit_to_turnover_ratio_pct": 5.0,
                    "current_ratio": 1.85,
                    "findeks_score": "1820 / 1900 (Prime)",
                    "bounced_checks_last_12m": 0,
                    "avg_payment_delay_days": 0,
                },
            },
            {
                "id": "var_gray",
                "label": "Varyasyon 2: Gri Alan (Sınırda Cari Oran 1.18 & Mevsimsel Gecikme)",
                "expected_band": "Gri Alan -> Kredi Komitesi / Üst Katman LLM",
                "state": {
                    "company": "Ege Tarım Ürünleri Nakliyat Ltd. (3 Yıllık Firma)",
                    "annual_turnover_tl": 40000000,
                    "requested_open_account_limit_tl": 4150000,
                    "limit_to_turnover_ratio_pct": 10.3,
                    "current_ratio": 1.18,
                    "findeks_score": "1390 / 1900 (Medium)",
                    "bounced_checks_last_12m": 0,
                    "avg_payment_delay_days": 9,
                    "notes": "No bounced checks, but Current Ratio (1.18) is slightly below 1.20 threshold and requested limit (10.3%) is right on the 10% cap; company offers 50% partial bank guarantee.",
                },
            },
            {
                "id": "var_fraud",
                "label": "Varyasyon 3: Kırmızı Hat (3 Karşılıksız Çek + Cari Oran 0.68)",
                "expected_band": "Otomatik Red (Sadece Peşin/Escrow)",
                "state": {
                    "company": "Delta İç ve Dış Ticaret Ltd. (4 Aylık Firma)",
                    "annual_turnover_tl": 8200000,
                    "requested_open_account_limit_tl": 3500000,
                    "limit_to_turnover_ratio_pct": 42.6,
                    "current_ratio": 0.68,
                    "findeks_score": "840 / 1900 (High Risk)",
                    "bounced_checks_last_12m": 3,
                    "protested_bills": 2,
                    "avg_payment_delay_days": 48,
                },
            },
        ]
    else:
        # Default: 3-Way Matching (PO - WMS Receiving - e-Invoice)
        title = "Depo Mal Kabul 3-Way Matching (PO – İrsaliye – e-Fatura) Varyasyon Matrisi"
        questions = {
            "quantity_matches_wms_count": {
                "type": "noul",
                "instructions": "Does the invoiced quantity match the actual WMS receiving count?",
            },
            "unit_price_within_2pct_po_tolerance": {
                "type": "noul",
                "instructions": "Is the invoiced unit price within the 2.0% Purchase Order tolerance?",
            },
            "vat_and_withholding_compliant": {
                "type": "noul",
                "instructions": "Are the VAT (20%) and mandatory 2/10 withholding tax (KDV tevkifatı) applied accurately?",
            },
            "erp_prerouter_action": {
                "type": "choice",
                "instructions": "How should `drex-max-finance` route this supplier invoice?",
                "criteria": {
                    "auto_post_to_sap_erp": "All 3-way matching rules pass with high confidence -> Post directly to ERP for payment",
                    "gray_zone_escalate_to_procurement_agent": "Minor borderline price/rounding variance (~1.8%-2.1%) or FX conversion ambiguity -> Escalate to Procurement LLM Agent",
                    "auto_block_and_issue_debit_memo": "Major quantity shortage, price overcharge, or missing tax withholding -> Block invoice & issue debit memo",
                },
            },
            "discrepancy_severity": {
                "type": "score",
                "instructions": "Rate the severity of the 3-way matching discrepancy.",
                "criteria": ["0 - Exact Match", "1 - Minor Tolerance Edge (Gray Zone)", "2 - Material Variance", "3 - Severe Overbilling"],
            },
        }
        variations = [
            {
                "id": "var_clean",
                "label": "Varyasyon 1: Yeşil Hat (PO = WMS = e-Fatura Tam Eşleşme)",
                "expected_band": "Otomatik ERP Onayı (>0.95 Güven)",
                "state": {
                    "po_number": "PO-2026-4401",
                    "po_ordered_qty": 1000,
                    "po_unit_price_tl": 400.00,
                    "po_tolerance_pct": 2.0,
                    "wms_received_good_qty": 1000,
                    "weighbridge_net_kg": 22000,
                    "invoice_billed_qty": 1000,
                    "invoice_unit_price_tl": 400.00,
                    "vat_rate_pct": 20,
                    "withholding_tax_applied": "2/10 KDV Tevkifatı doğru düşülmüştür.",
                },
            },
            {
                "id": "var_gray",
                "label": "Varyasyon 2: Gri Alan (%1.95 Kur/Birim Fiyat Farkı & 4 Palet Nemli Ambalaj)",
                "expected_band": "Gri Alan -> Üst Katman Satınalma LLM Ajanı",
                "state": {
                    "po_number": "PO-2026-4402",
                    "po_ordered_qty": 1000,
                    "po_unit_price_tl": 400.00,
                    "po_tolerance_pct": 2.0,
                    "wms_received_good_qty": 996,
                    "wms_note": "996 pallets intact; 4 pallets have slightly damp outer stretch wrap but inner cartons appear usable (pending QC decision).",
                    "invoice_billed_qty": 1000,
                    "invoice_unit_price_tl": 407.80,
                    "price_variance_note": "+1.95% variance due to Central Bank EUR/TRY daily exchange rate rounding clause on delivery day.",
                    "vat_rate_pct": 20,
                    "withholding_tax_applied": "2/10 KDV Tevkifatı uygulanmış.",
                },
            },
            {
                "id": "var_fraud",
                "label": "Varyasyon 3: Kırmızı Hat (150 Palet Eksik + %16.2 Fiyat Aşımı + Tevkifat Yok)",
                "expected_band": "Otomatik Bloke & Fiyat/Miktar Fark Faturası",
                "state": {
                    "po_number": "PO-2026-4401",
                    "po_ordered_qty": 1000,
                    "po_unit_price_tl": 400.00,
                    "po_tolerance_pct": 2.0,
                    "wms_received_good_qty": 850,
                    "wms_shortage_qty": 150,
                    "weighbridge_net_kg": 18700,
                    "invoice_billed_qty": 1000,
                    "invoice_unit_price_tl": 465.00,
                    "price_variance_pct": "+16.25% unauthorized price hike",
                    "vat_rate_pct": 20,
                    "withholding_tax_applied": "0.00 TL - Zorunlu 2/10 tevkifat uygulanmamış!",
                },
            },
        ]

    def _eval_var(var_item: dict[str, Any]) -> dict[str, Any]:
        res = evaluate_decision(
            state=var_item["state"],
            questions=questions,
            model="nace-ai/drex-max-finance",
        )
        answers = res.get("response", {}).get("answers", {}) if res.get("ok") else {}
        gate = classify_prerouter_gate(answers) if answers else {}
        return {
            "id": var_item["id"],
            "label": var_item["label"],
            "expected_band": var_item["expected_band"],
            "state": var_item["state"],
            "ok": res.get("ok", False),
            "latency_ms": res.get("client_latency_ms", 0),
            "usage": res.get("response", {}).get("usage", {}),
            "answers": answers,
            "prerouter_gate": gate,
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(_eval_var, variations))

    return {
        "ok": True,
        "domain": domain,
        "title": title,
        "model": "nace-ai/drex-max-finance",
        "questions": questions,
        "variations": results,
    }


def run_hybrid_logistics_pipeline(
    scenario_type: str = "pod_dispute",
    sample_dir: Path | None = None,
    llm_model: str = "openai/gpt-4o-mini",
) -> dict[str, Any]:
    """
    Simulates a production 4-Layer Architecture between Mobile Freight Exchange App,
    System 1 Decision Model (`nace-ai/drex-max-finance` / `nace-ai/drex-max`),
    Backend Rules Engine, and System 2 Generative LLM + Final System 1 Guardrail.
    """
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    sdir = sample_dir or (Path(__file__).parent / "samples")

    if scenario_type == "wms_3way_matching":
        img_url = encode_image_to_data_url(sdir / "finance_3way_matching.png")
        s1_model = "nace-ai/drex-max-finance"
        event_context = {
            "event": "WMS_3WAY_MATCHING_INVOICE_ARRIVAL",
            "po_number": "PO-2026-4401",
            "supplier": "Toros Ambalaj & Palet San. A.Ş.",
            "po_terms": {"qty": 1000, "unit_price_tl": 400.0, "withholding_tax": "2/10"},
            "wms_receiving": {"good_qty": 850, "shortage_qty": 150, "weighbridge_kg": 18700},
            "invoice_claimed": {"billed_qty": 1000, "unit_price_tl": 465.0, "total_tl": 558000.0, "withholding_tax": "None"},
        }
        s1_questions = {
            "quantity_matches_wms": {
                "type": "noul",
                "instructions": "Does the invoiced quantity (1,000 units) match the WMS actual received quantity (850 units)?",
            },
            "unit_price_within_po_limit": {
                "type": "noul",
                "instructions": "Is the invoiced unit price (465 TL) within the 2% tolerance of the PO contract price (400 TL)?",
            },
            "withholding_tax_compliant": {
                "type": "noul",
                "instructions": "Did the supplier apply the mandatory 2/10 VAT withholding tax on the invoice?",
            },
            "erp_accounting_action": {
                "type": "choice",
                "instructions": "Which automated ERP accounting workflow should `drex-max-finance` trigger?",
                "criteria": {
                    "auto_approve_sap_payment": "Post invoice to SAP ERP and schedule payment",
                    "block_invoice_issue_debit_note_for_150_shortage_and_price_diff": "Block payment in SAP, issue Debit Memo for 150 missing pallets & +65 TL unit overcharge, and request corrected tax invoice",
                    "escalate_gray_zone": "Escalate minor rounding difference",
                },
            },
            "financial_discrepancy_severity": {
                "type": "score",
                "instructions": "Rate the financial severity of the 3-way matching discrepancy.",
                "criteria": ["Clean Match", "Minor Variance", "High Discrepancy", "Critical Overbilling & Tax Non-Compliance"],
            },
        }
    elif scenario_type == "wms_hazmat_dock":
        img_url = encode_image_to_data_url(sdir / "warehouse_damaged_pallet.png")
        s1_model = "nace-ai/drex-max"
        event_context = {
            "event": "WMS_INBOUND_DOCK_SCAN",
            "warehouse": "Gebze Ana Lojistik Merkezi - Rampa B4",
            "pallet_id": "PLT-99204",
            "asn_declared_type": "Standart Kuru Gıda (Tehlikesiz)",
            "forklift_operator_note": "Paletin alt kolisi ezik, yerde sıvı sızıntısı var ve üstte kırmızı eşkenar etiket görünüyor.",
        }
        s1_questions = {
            "undeclared_adr_hazmat": {
                "type": "noul",
                "instructions": "Does the pallet image show an ADR Class 3 Flammable hazardous material label despite the ASN declaring non-hazardous goods?",
            },
            "active_liquid_spill": {
                "type": "noul",
                "instructions": "Is there a crushed carton or chemical spill visible at the base of the pallet?",
            },
            "wms_microservice_command": {
                "type": "choice",
                "instructions": "Which automated WMS microservice command must be triggered immediately?",
                "criteria": {
                    "putaway_standard_rack": "Send forklift to Standard High Rack A-12",
                    "quarantine_hazmat_and_dispatch_spill_team": "Block rack putaway, route to Hazmat Quarantine Bunker, and page Spill Response Team",
                    "putaway_cold_storage": "Send to -18C Cold Storage Zone",
                },
            },
            "safety_hazard_level": {
                "type": "score",
                "instructions": "Rate the warehouse occupational safety hazard level.",
                "criteria": ["Safe", "Minor Caution", "High Hazard", "Critical ADR Spill Emergency"],
            },
        }
    elif scenario_type == "load_board_matching":
        img_url = encode_image_to_data_url(sdir / "mobile_load_board_ui.png")
        s1_model = "nace-ai/drex-max"
        event_context = {
            "event": "MOBILE_LOAD_BOARD_CARRIER_BID",
            "load_id": "YUK-2026-551",
            "route": "Antalya -> Berlin",
            "cargo": "18 Ton Donuk Deniz Ürünleri (-18°C Frigo Zorunlu, Değer: 4.2M TL)",
            "carrier_bid": {
                "carrier_name": "Kuzey Lojistik",
                "bid_eur": 3150,
                "vehicle_type": "Standart Tenteli Tır (Frigo Yok)",
                "insurance_limit_tl": 1000000,
                "driver_chat_message": "Abi tenteli araçla gece serin gideriz bir şey olmaz hemen saralım yükü.",
            },
        }
        s1_questions = {
            "equipment_compatible": {
                "type": "noul",
                "instructions": "Does the carrier's vehicle type meet the mandatory -18C Reefer (Frigo) requirement shown on the screen?",
            },
            "insurance_sufficient": {
                "type": "noul",
                "instructions": "Is the carrier's 1,000,000 TL insurance sufficient for the 4,200,000 TL cargo value and 5,000,000 TL minimum requirement?",
            },
            "matching_engine_action": {
                "type": "choice",
                "instructions": "Which action should the Mobile Freight Exchange matching engine take?",
                "criteria": {
                    "auto_accept_bid": "Accept the bid and assign load to Kuzey Lojistik",
                    "hard_reject_incompatible_equipment": "Automatically reject bid due to missing Reefer (-18C) trailer and insufficient insurance limit",
                    "negotiate_price_only": "Send price counter-offer to the tented truck",
                },
            },
            "cargo_loss_risk": {
                "type": "score",
                "instructions": "Rate the risk of total cargo spoilage/loss if this bid is accepted.",
                "criteria": ["Low Risk", "Moderate Risk", "High Risk", "Guaranteed Spoilage & Uninsured Loss"],
            },
        }
    else:
        img_url = encode_image_to_data_url(sdir / "logistics_pod_waybill.png")
        s1_model = "nace-ai/drex-max-finance"
        event_context = {
            "event": "DRIVER_POD_UPLOAD_ESCROW_REQUEST",
            "load_id": "LOAD-77419",
            "driver_name": "Ahmet Yılmaz (34 TRK 882)",
            "escrow_amount_tl": 48500,
            "driver_app_claim": "Teslimatı eksiksiz yaptım, kaşeli imzalı irsaliyeyi yükledim, 48.500 TL hak edişimin hemen hesabıma yatmasını istiyorum.",
        }
        s1_questions = {
            "has_wet_stamp_and_signature": {
                "type": "noul",
                "instructions": "Does the uploaded POD waybill image contain the receiver warehouse stamp and signature?",
            },
            "has_damage_reservation_note": {
                "type": "noul",
                "instructions": "Did the receiving warehouse write a damage reservation note (Hasar Şerhi) stating that 3 pallets were damaged and returned?",
            },
            "escrow_payment_action": {
                "type": "choice",
                "instructions": "Which financial action should the Freight Exchange Escrow microservice execute?",
                "criteria": {
                    "release_full_48500_tl": "Immediately release full 48,500 TL to the driver",
                    "freeze_escrow_and_open_partial_damage_reconciliation": "Hold full automatic payout, freeze disputed damage portion (~14,200 TL), and open damage reconciliation workflow",
                    "reject_unreadable_photo": "Reject photo as blurry/unreadable",
                },
            },
            "dispute_severity": {
                "type": "score",
                "instructions": "Rate the financial and operational severity of this delivery discrepancy.",
                "criteria": ["Clean Delivery (No Dispute)", "Minor Delay", "Partial Cargo Damage Dispute", "Total Load Loss"],
            },
        }

    # --- STEP 1: System 1 (Drex Max / Drex Max Finance) Multimodal Decision ---
    s1_state = [json.dumps(event_context, ensure_ascii=False), make_image_part(img_url)]
    s1_result = evaluate_decision(
        state=s1_state,
        questions=s1_questions,
        model=s1_model,
    )

    if not s1_result["ok"]:
        return {"ok": False, "error": s1_result.get("error")}

    s1_answers = s1_result["response"].get("answers", {})

    # --- STEP 2: Deterministic Backend Microservice Routing ---
    chosen_action = None
    chosen_confidence = 0.0
    for k, v in s1_answers.items():
        if v.get("type") == "choice":
            chosen_action = v.get("choice")
            chosen_confidence = float(v.get("confidence", 0.0))

    backend_execution = {
        "system1_model": s1_model,
        "gate_passed": chosen_confidence >= 0.80,
        "confidence_threshold": 0.80,
        "actual_confidence": round(chosen_confidence, 4),
        "executed_microservice": chosen_action,
        "database_tx": f"TX-{int(time.time())}-COMMITTED",
        "llm_needed_for_user_notification": True,
    }

    # --- STEP 3: System 2 (Generative LLM) Drafts Human Notification Strictly Bound to System 1 ---
    t_llm = time.perf_counter()
    llm_prompt = (
        "Sen Sendicom Mobil Yük Borsası, Finans ve WMS Operasyon Asistanısın.\n"
        "ÖNEMLİ KURAL: Kendin karar verme! Üst katmandaki System-1 Karar Modeli (Drex Max Finance) görseli ve veriyi inceleyerek "
        "kesin ve bağlayıcı kararı verdi. Sadece bu kararı karşı tarafa açıklayan, kısa (3-4 cümle), profesyonel Türkçe bildirim mesajı yaz.\n\n"
        f"Olay Bağlamı: {json.dumps(event_context, ensure_ascii=False)}\n"
        f"System-1 Kesin Karar Çıktısı: {json.dumps(s1_answers, ensure_ascii=False)}\n"
        f"Tetiklenen Mikroservis: {chosen_action}"
    )

    chat_resp = requests.post(
        ENDPOINTS["chat"],
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": llm_model,
            "messages": [{"role": "user", "content": llm_prompt}],
            "temperature": 0.2,
            "max_tokens": 220,
        },
        timeout=30,
    )
    llm_latency_ms = round((time.perf_counter() - t_llm) * 1000, 2)
    llm_text = ""
    if chat_resp.status_code == 200:
        llm_text = (
            chat_resp.json()
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
    else:
        llm_text = f"[System-2 LLM Yanıtı Alınamadı: {chat_resp.status_code}] Karar: {chosen_action}"

    # --- STEP 4: System 1 (Drex Max Finance) Output Guardrail Check ---
    guardrail_state = {
        "mandatory_system1_action": chosen_action,
        "system1_decisions": s1_answers,
        "generated_push_notification_draft": llm_text,
    }
    guardrail_questions = {
        "faithful_to_system1_decision": {
            "type": "noul",
            "instructions": "Does the generated push notification accurately reflect the mandatory_system1_action without contradicting it?",
        },
        "contains_unauthorized_payout_promise": {
            "type": "noul",
            "instructions": "Does the notification falsely promise immediate full unconditional payment or ignore the detected discrepancy?",
        },
        "push_gateway_verdict": {
            "type": "choice",
            "instructions": "Should the mobile push notification gateway deliver this message?",
            "criteria": {
                "deliver_push_notification": "Message is accurate, safe, and aligned with System-1 decision",
                "block_hallucinated_message": "Block message because it contradicts System-1 decision",
            },
        },
    }
    guardrail_result = evaluate_decision(
        state=guardrail_state,
        questions=guardrail_questions,
        model=s1_model,
    )

    return {
        "ok": True,
        "scenario_type": scenario_type,
        "event_context": event_context,
        "step1_system1_vision_decision": {
            "model": s1_model,
            "latency_ms": s1_result["client_latency_ms"],
            "usage": s1_result["response"].get("usage", {}),
            "answers": s1_answers,
        },
        "step2_backend_orchestration": backend_execution,
        "step3_system2_llm_generation": {
            "model": llm_model,
            "latency_ms": llm_latency_ms,
            "generated_notification": llm_text,
        },
        "step4_system1_output_guardrail": {
            "latency_ms": guardrail_result.get("client_latency_ms"),
            "usage": guardrail_result.get("response", {}).get("usage", {}),
            "answers": guardrail_result.get("response", {}).get("answers", {}),
        },
    }


def get_presets() -> list[dict[str, Any]]:
    """Returns built-in Drex Max Finance + Logistics / WMS / Mobile Freight Exchange + Enterprise presets."""
    return [
        # ============================================================================
        # 1. DREX MAX FINANCE — LOJİSTİK FİNANS, 3-WAY MATCHING, DEMURAJ & KREDİ RİSKİ
        # ============================================================================
        {
            "id": "finance_wms_3way_matching",
            "title": "📑 1. [Drex Max Finance] Depo Mal Kabul Üçlü Eşleştirme (3-Way Matching: PO – İrsaliye – e-Fatura)",
            "category": "Drex Max Finance (Lojistik Finans)",
            "badge": "3-Way Matching + Vergi",
            "model": "nace-ai/drex-max-finance",
            "description": (
                "Satınalma Siparişi (#PO-2026-4401), WMS Mal Kabul/Kantar sayımı ve Tedarikçi e-Faturasını (finance_3way_matching.png) "
                "tek geçişte karşılaştırır: 150 palet eksik teslimatı, +%16.25 birim fiyat aşımını ve eksik 2/10 KDV tevkifatını yakalar."
            ),
            "sample_images": ["finance_3way_matching.png"],
            "state_text": (
                "3-Way Matching Kuralı (#FIN-3WM): (1) Fatura miktarı WMS mal kabul sağlam sayımını aşamaz. "
                "(2) Birim fiyat PO sözleşme fiyatını (400 TL) en fazla %2.0 aşabilir. "
                "(3) Lojistik/Palet tedarikinde 2/10 KDV tevkifatı zorunludur."
            ),
            "questions": {
                "invoiced_qty_matches_wms_received": {
                    "type": "noul",
                    "instructions": "Does the invoiced quantity (1,000 units) match the actual WMS received good quantity (850 units)?",
                },
                "unit_price_within_po_tolerance": {
                    "type": "noul",
                    "instructions": "Is the invoiced unit price (465.00 TL) within the 2.0% tolerance of the PO unit price (400.00 TL)?",
                },
                "weighbridge_tonnage_matches_invoice": {
                    "type": "noul",
                    "instructions": "Does the weighbridge net weight (18,700 kg) match the invoice declared weight (22,000 kg)?",
                },
                "withholding_tax_applied_correctly": {
                    "type": "noul",
                    "instructions": "Was the mandatory 2/10 VAT withholding tax (KDV tevkifatı) applied on the supplier e-Invoice?",
                },
                "sap_erp_routing_action": {
                    "type": "choice",
                    "instructions": "Which action should the ERP Accounts Payable automation execute?",
                    "criteria": {
                        "btn_1_auto_approve_sap": "[1] Auto-approve invoice in SAP ERP and release 558,000 TL payment",
                        "btn_2_block_and_issue_debit_memo": "[2] Block invoice, issue Debit Memo for 150 missing pallets & +65 TL price hike, and demand tax-compliant credit note",
                        "btn_3_route_gray_zone": "[3] Route to manual review for minor rounding variance",
                    },
                },
                "audit_risk_rating": {
                    "type": "score",
                    "instructions": "Rate the financial and tax compliance risk of paying this e-Invoice as submitted.",
                    "criteria": ["0 - Compliant", "1 - Minor Rounding", "2 - Material Discrepancy", "3 - Severe Overbilling & Tax Violation"],
                },
            },
        },
        {
            "id": "finance_demurrage_receipt_fraud",
            "title": "🕵️ 2. [Drex Max Finance] Navlun Hak Ediş, Demuraj (Bekleme) & Sahte Kantar/Otoyol Fişi Denetimi",
            "category": "Drex Max Finance (Lojistik Finans)",
            "badge": "Demuraj + Sahte Fiş",
            "model": "nace-ai/drex-max-finance",
            "description": (
                "Sefer sonunda nakliyecinin ekstra 6.500 TL bekleme (demuraj) ve 2.800 TL geçiş ücreti için yüklediği fişi "
                "(finance_demurrage_receipt_fraud.png) GPS verisiyle karşılaştırır: 2025 tarihli mükerrer fişi, üzeri çizili plakayı ve 45 dk'lık gerçek beklemeyi yakalar."
            ),
            "sample_images": ["finance_demurrage_receipt_fraud.png"],
            "state_text": (
                "Navlun Ek Gider Politikası: (1) İlk 4 saat (240 dk) bekleme ücretsizdir; GPS bekleme süresi 4 saati aşmıyorsa demuraj ödenmez. "
                "(2) Yüklenen kantar/otoyol fişinin tarihi ve plakası aktif seferle (#TRIP-2026-772, 34 ABC 901, 10.11.2026) birebir eşleşmelidir."
            ),
            "questions": {
                "demurrage_exceeds_4h_free_window": {
                    "type": "noul",
                    "instructions": "According to the GPS ground truth (45 minutes total waiting), did the carrier exceed the 4-hour (240 min) free waiting window?",
                },
                "receipt_date_and_plate_match_trip": {
                    "type": "noul",
                    "instructions": "Do the receipt date (14.08.2025) and plate (06 XYZ 44 crossed out) match the active trip (10.11.2026, plate 34 ABC 901)?",
                },
                "is_duplicate_or_tampered_receipt": {
                    "type": "noul",
                    "instructions": "Is the uploaded receipt a reused document from a previous 2025 trip with signs of pixel/plate tampering?",
                },
                "settlement_action": {
                    "type": "choice",
                    "instructions": "Which payout decision should `drex-max-finance` trigger?",
                    "criteria": {
                        "pay_full_41300_tl": "[1] Approve and pay full 41,300 TL including demurrage and receipt",
                        "reject_extras_and_flag_carrier_fraud": "[2] Reject 9,300 TL extra claim, flag carrier account for receipt fraud, and hold for audit",
                        "escalate_unclear_gps": "Escalate due to missing GPS data",
                    },
                },
                "fraud_severity_score": {
                    "type": "score",
                    "instructions": "Rate the severity of the document tampering and false demurrage claim.",
                    "criteria": ["Clean Claim", "Accidental Upload Error", "Unjustified Expense Claim", "Intentional Document Tampering & Double-Billing Fraud"],
                },
            },
        },
        {
            "id": "finance_insurance_subrogation_triage",
            "title": "⚖️ 3. [Drex Max Finance] Hasarlı Kargo & Sigorta Rücu (Subrogation / Claim) Triyajı (3 Görsel Birden)",
            "category": "Drex Max Finance (Lojistik Finans)",
            "badge": "3 Görsel + Sigorta Rücu",
            "model": "nace-ai/drex-max-finance",
            "description": (
                "Şerhli Sevk İrsaliyesi (logistics_pod_waybill.png), Rampa Hasarlı/ADR Palet fotoğrafı (warehouse_damaged_pallet.png) ve "
                "Frigo Sıcaklık İhlali grafiğini (cold_chain_telemetry.png) poliçe şartlarıyla birlikte okuyup sorumlu tarafı ve rücu dosyasını belirler."
            ),
            "sample_images": [
                "logistics_pod_waybill.png",
                "warehouse_damaged_pallet.png",
                "cold_chain_telemetry.png",
            ],
            "state_text": (
                "Sigorta Poliçesi & Rücu Kuralları (#CMR-2026): "
                "(1) Taşıma sırasında devrilen/ezilen 3 palet zeytinyağı (Görsel 1) taşıyıcının yük sabitleme (lashing) kusurudur -> Taşıyıcı CMR sigortasına rücu edilir. "
                "(2) Beyan edilmemiş ADR Class 3 yanıcı madde gönderimi (Görsel 2) yük verenin (Shipper) ağır kusurudur -> Yük verene rücu edilir. "
                "(3) Kompresör arızasına rağmen soğuk depoya girmeyip +4.5°C'de yola devam etmek (Görsel 3) taşıyıcı ağır kusurudur."
            ),
            "questions": {
                "pod_confirms_in_transit_damage": {
                    "type": "noul",
                    "instructions": "Does Image 1 (POD waybill) confirm that 3 pallets arrived damaged and were returned with an official reservation note?",
                },
                "shipper_liable_for_undeclared_adr": {
                    "type": "noul",
                    "instructions": "Based on Image 2, is the shipper liable for failing to declare ADR Class 3 flammable goods on the ASN manifest?",
                },
                "cold_chain_breach_proven_by_iot": {
                    "type": "noul",
                    "instructions": "Does Image 3 prove that trailer temperature exceeded the -5C threshold up to +4.5C for 95 minutes?",
                },
                "primary_subrogation_action": {
                    "type": "choice",
                    "instructions": "How should the Insurance Claims & Subrogation engine classify and route this multi-incident file?",
                    "criteria": {
                        "waive_all_claims_pay_everyone": "Close file with no liability and pay full freight",
                        "split_subrogation_carrier_cmr_and_shipper_adr_penalty": "Open CMR Subrogation Claim against Carrier for transit/reefer damage AND issue Undeclared Hazmat Penalty to Shipper",
                        "blame_receiving_warehouse_only": "Assign 100% fault to receiving warehouse dock staff",
                    },
                },
                "claim_complexity_score": {
                    "type": "score",
                    "instructions": "Rate the financial and legal severity of this multi-party insurance claim.",
                    "criteria": ["Minor Scratch", "Standard Single-Party Claim", "High-Value Claim", "Critical Multi-Party Subrogation & Hazmat Breach"],
                },
            },
        },
        {
            "id": "finance_credit_factoring_scoring",
            "title": "🏦 4. [Drex Max Finance] Vadeli Yük Veren (Açık Hesap) & Faktoring Kredi Risk Skorlaması",
            "category": "Drex Max Finance (Lojistik Finans)",
            "badge": "Bilanço + Findeks + Kredi",
            "model": "nace-ai/drex-max-finance",
            "description": (
                "60 gün vadeli 3.500.000 TL açık hesap limiti isteyen firmanın bilanço rasyolarını ve Findeks çek/senet dökümünü "
                "(finance_credit_balance_sheet.png) kredi komitesi kurallarından geçirerek saniyenin altında onay/red olasılığı üretir."
            ),
            "sample_images": ["finance_credit_balance_sheet.png"],
            "state_text": (
                "Kurumsal Kredi & Faktoring Politikası (#CRP-09): "
                "(1) Cari Oran en az 1.20 olmalıdır (1.00 altı otomatik red). "
                "(2) Talep edilen açık hesap limiti yıllık cironun %10'unu aşamaz. "
                "(3) Son 12 ayda karşılıksız çek veya protestolu senedi olan firmalara teminatsız vadeli limit açılamaz; sadece Peşin/Escrow çalışılabilir."
            ),
            "questions": {
                "current_ratio_meets_1_20_minimum": {
                    "type": "noul",
                    "instructions": "Does the applicant's Current Ratio (0.68) meet the minimum policy requirement of 1.20?",
                },
                "requested_limit_under_10pct_turnover": {
                    "type": "noul",
                    "instructions": "Is the requested 3,500,000 TL credit limit under 10% of the company's 8,200,000 TL annual turnover (42.6%)?",
                },
                "has_bounced_checks_or_protested_bills": {
                    "type": "noul",
                    "instructions": "Does the Findeks report show bounced checks (3 checks / 920,000 TL) and protested bills (2 bills)?",
                },
                "credit_committee_verdict": {
                    "type": "choice",
                    "instructions": "Which credit allocation button should `drex-max-finance` select?",
                    "criteria": {
                        "btn_1_approve_3_5m_open_account": "[1] Approve 3,500,000 TL unsecured 60-day open account limit",
                        "btn_2_reject_credit_enforce_cash_escrow": "[2] Reject open-account credit and enforce 100% Cash / Upfront Escrow deposit before posting loads",
                        "btn_3_approve_partial_unsecured": "Approve 2,000,000 TL unsecured limit without collateral",
                    },
                },
                "counterparty_default_risk": {
                    "type": "score",
                    "instructions": "Rate the probability of payment default if unsecured credit is extended to this applicant.",
                    "criteria": ["Low Risk (Prime)", "Moderate Risk", "High Risk", "Extreme Default Risk (Insolvent / Bounced Checks)"],
                },
            },
        },
        {
            "id": "finance_gray_zone_prerouter",
            "title": "🧭 5. [Drex Max Finance] Çoklu Ajan (Multi-Agent) 'System One' Ön Yönlendirici (Gri Alan Gatekeeper)",
            "category": "Drex Max Finance (Lojistik Finans)",
            "badge": "Pre-Router / Gri Alan",
            "model": "nace-ai/drex-max-finance",
            "description": (
                "Python/FastAPI + Celery mimarisinde sınırda kalan (%1.95 kur yuvarlama farkı ve 4 nemli palet içeren) "
                "karmaşık bir mal kabul dosyasını değerlendirir; olasılık dağılımı gri alanda kaldığı için üst katman Reasoning LLM ajanına devreder."
            ),
            "sample_images": [],
            "state_json": {
                "pipeline_stage": "SYSTEM_ONE_PRE_ROUTER_GATEKEEPER",
                "po_number": "PO-2026-4490",
                "contract_terms": {
                    "ordered_pallets": 500,
                    "unit_price_tl": 1000.00,
                    "price_tolerance_pct": 2.0,
                    "fx_clause": "TCMB daily EUR selling rate applies if intraday shift exceeds 1.5%.",
                },
                "wms_receiving_report": {
                    "intact_pallets": 496,
                    "borderline_pallets": 4,
                    "qc_inspector_note": "4 paletin dış streç filminde yağmur nemi var ancak iç karton kutular sağlam görünüyor; üretim müdürü şartlı kabul edebilir veya %15 nefaset kesintisi isteyebilir.",
                },
                "supplier_invoice": {
                    "billed_pallets": 500,
                    "billed_unit_price_tl": 1019.50,
                    "variance_pct": 1.95,
                    "supplier_explanation": "Teslimat günü EUR/TL kur farkı nedeniyle +%1.95 fiyat uyarlaması yapılmıştır.",
                },
            },
            "questions": {
                "is_unambiguous_clean_match": {
                    "type": "noul",
                    "instructions": "Is this a 100% clean, zero-discrepancy delivery that can be auto-paid without any QC or FX clause verification?",
                },
                "is_clear_malicious_fraud": {
                    "type": "noul",
                    "instructions": "Is the supplier committing clear malicious fraud (rather than a borderline FX clause and minor damp stretch wrap issue)?",
                },
                "requires_gray_zone_specialist_or_llm": {
                    "type": "noul",
                    "instructions": "Does this file fall into a gray zone (borderline +1.95% FX price adjustment and 4 conditionally acceptable damp pallets) requiring a System-2 Reasoning Agent or QC specialist?",
                },
                "celery_queue_routing": {
                    "type": "choice",
                    "instructions": "Which Celery task queue should the System-One Pre-Router dispatch this event to?",
                    "criteria": {
                        "fast_path_auto_approve_db": "Fast-Path DB Auto-Approve (No LLM needed)",
                        "fast_path_auto_reject_fraud": "Fast-Path Fraud Block Queue (No LLM needed)",
                        "gray_zone_deep_reasoning_llm_queue": "Gray-Zone Escalation Queue -> Trigger System-2 Reasoning LLM Agent to negotiate conditional acceptance & verify TCMB FX rate",
                    },
                },
                "ambiguity_level": {
                    "type": "score",
                    "instructions": "Rate the level of operational ambiguity / gray-zone complexity in this file.",
                    "criteria": ["0 - Clear Cut", "1 - Slight Nuance", "2 - Moderate Gray Zone", "3 - High Multi-Factor Gray Zone (QC + FX Clause)"],
                },
            },
        },
        # ============================================================================
        # 2. DEPO (WMS), LOJİSTİK & MOBİL YÜK BORSASI OPERASYON SENARYOLARI
        # ============================================================================
        {
            "id": "logistics_pod_escrow",
            "title": "🚚 6. Mobil Yük Borsası: Sevk İrsaliyesi (POD) & Hak Ediş (Escrow) Denetimi",
            "category": "Lojistik & Yük Borsası",
            "badge": "Görsel POD + Escrow",
            "model": "nace-ai/drex-max",
            "description": (
                "Sürücünün mobil uygulamadan yüklediği Sevk İrsaliyesi / POD fotoğrafını (logistics_pod_waybill.png) "
                "inceler; ıslak imza/kaşeyi doğrular ancak '3 Palet Hasarlı / İade' şerhini yakalayarak otomatik ödemeyi bloke eder."
            ),
            "sample_images": ["logistics_pod_waybill.png"],
            "state_text": (
                "Mobil Yük Borsası Escrow Politikası: Teslimat irsaliyesinde (POD) alıcı depo ıslak imzası ve kaşesi tam ise "
                "ve herhangi bir hasar/eksik şerhi YOKSA 48.500 TL hak edişi anında serbest bırak. Hasar şerhi varsa ödemeyi bloke et."
            ),
            "questions": {
                "has_receiver_stamp_and_signature": {
                    "type": "noul",
                    "instructions": "Does the POD waybill image contain the receiver warehouse stamp and signature?",
                },
                "has_damage_reservation_note": {
                    "type": "noul",
                    "instructions": "Is there a damage reservation note (Hasar Şerhi) on the waybill indicating 3 damaged/returned pallets?",
                },
                "escrow_payment_decision": {
                    "type": "choice",
                    "instructions": "Which button/action should the Mobile Freight Exchange escrow engine trigger?",
                    "criteria": {
                        "btn_1_release_full_payment": "[1] Release full 48,500 TL payment immediately",
                        "btn_2_hold_escrow_open_damage_claim": "[2] Hold escrow & open partial damage claim (~14,200 TL deduction)",
                        "btn_3_reject_unreadable": "[3] Reject document as unreadable/blurry",
                    },
                },
                "claim_urgency_score": {
                    "type": "score",
                    "instructions": "Rate the severity of the delivery exception.",
                    "criteria": ["Clean Delivery", "Minor Paperwork Issue", "Partial Cargo Damage Claim", "Total Loss / Fraud"],
                },
            },
        },
        {
            "id": "wms_dock_hazmat_inspection",
            "title": "🏭 7. Depo (WMS) Rampa Kabul: Hasarlı Palet & Beyan Edilmemiş ADR Tespiti",
            "category": "Lojistik & Yük Borsası",
            "badge": "Depo Kamera + ADR",
            "model": "nace-ai/drex-max",
            "description": (
                "Depo rampa kamerasından gelen palet görüntüsünü (warehouse_damaged_pallet.png) inceler; "
                "ASN bildiriminde 'Tehlikesiz' yazmasına rağmen palet üzerindeki 'ADR Class 3 UN 1263 Yanıcı' etiketini ve sızıntıyı yakalar."
            ),
            "sample_images": ["warehouse_damaged_pallet.png"],
            "state_text": (
                "WMS Rampa Kabul Kuralı: Gelen palette ezilme, kimyasal sızıntı veya ASN manifestosunda beyan edilmemiş ADR "
                "tehlikeli madde etiketi varsa standart yüksek rafa (High Rack) kesinlikle kaldırma; ADR Karantina alanına yönlendir."
            ),
            "questions": {
                "undeclared_adr_hazmat_present": {
                    "type": "noul",
                    "instructions": "Does the pallet have a red ADR Class 3 (UN 1263 Flammable) diamond label despite the ASN declaring Non-Hazardous goods?",
                },
                "carton_crushed_or_leaking": {
                    "type": "noul",
                    "instructions": "Does the image show a crushed lower carton and a chemical spill at the base of the pallet?",
                },
                "wms_putaway_routing": {
                    "type": "choice",
                    "instructions": "Which WMS putaway zone button should be selected on the handheld terminal?",
                    "criteria": {
                        "zone_a_standard_rack": "[A] Standard High Rack Putaway",
                        "zone_b_hazmat_quarantine_spill": "[B] Hazmat Quarantine Bunker & Dispatch Spill Team",
                        "zone_c_cold_storage": "[C] Cold Storage (-18C)",
                    },
                },
                "warehouse_risk_score": {
                    "type": "score",
                    "instructions": "Rate the physical safety risk of placing this pallet onto a standard high rack.",
                    "criteria": ["Safe", "Low Risk", "High Risk", "Critical Collapse & Fire Hazard"],
                },
            },
        },
        {
            "id": "mobile_load_board_matching",
            "title": "📱 8. Mobil Yük Borsası: İlan Şartları vs Taşıyıcı Teklifi Uygunluk Kalkanı",
            "category": "Lojistik & Yük Borsası",
            "badge": "Mobil Ekran + Eşleştirme",
            "model": "nace-ai/drex-max",
            "description": (
                "Mobil Yük Borsası eşleştirme ekranını (mobile_load_board_ui.png) okur; -18°C Frigo ve 5M TL sigorta "
                "isteyen donuk gıda ilanına 'Standart Tenteli' araç ve 1M TL sigortayla gelen ucuz teklifi otomatik reddeder."
            ),
            "sample_images": ["mobile_load_board_ui.png"],
            "state_text": (
                "Sendicom Akıllı Eşleştirme Kuralı: Soğuk zincir (-18°C Frigo) gerektiren yüklere tenteli/açık kasa araç tekliflerini "
                "veya emtia değerinin altında sigorta limitine sahip taşıyıcıları fiyata bakmaksızın reddet."
            ),
            "questions": {
                "carrier_has_required_reefer": {
                    "type": "noul",
                    "instructions": "Does the bidding carrier have the mandatory -18C Frigo (Reefer) trailer required by the shipper?",
                },
                "insurance_limit_sufficient": {
                    "type": "noul",
                    "instructions": "Does the carrier's 1,000,000 TL insurance cover the required 5,000,000 TL minimum coverage?",
                },
                "load_board_action": {
                    "type": "choice",
                    "instructions": "Which action button on the Mobile Freight Exchange screen should be triggered?",
                    "criteria": {
                        "btn_1_approve_match": "[1] Approve Bid & Match Carrier",
                        "btn_2_reject_incompatible": "[2] Reject Bid (Equipment & Insurance Mismatch)",
                        "btn_3_price_negotiation_only": "[3] Start Price Negotiation Only",
                    },
                },
                "cargo_spoilage_risk": {
                    "type": "score",
                    "instructions": "Rate the risk of cargo spoilage if this carrier transports the frozen seafood.",
                    "criteria": ["No Risk", "Low Risk", "High Risk", "Certain Spoilage & Uninsured Loss"],
                },
            },
        },
        {
            "id": "cold_chain_iot_vision",
            "title": "❄️ 9. Soğuk Zincir (Frigo) IoT Telemetri Grafiği & Acil Rota Değişikliği",
            "category": "Lojistik & Yük Borsası",
            "badge": "IoT Grafik + Soğuk Zincir",
            "model": "nace-ai/drex-max",
            "description": (
                "Frigo dorse IoT sıcaklık grafiğini (cold_chain_telemetry.png) görsel olarak analiz eder; "
                "03:15'teki kompresör arızası sonrası sıcaklığın +4.5°C'ye çıktığını görerek en yakın soğuk depoya yönlendirir."
            ),
            "sample_images": ["cold_chain_telemetry.png"],
            "state_text": (
                "Soğuk Zincir Operasyon Protokolü: Dorse sıcaklığı -5°C kritik eşiğini 30 dakikadan fazla aşarsa "
                "yükü kurtarmak için aracı derhal en yakın anlaşmalı soğuk hava deposuna (Bolu - 18 km) yönlendir."
            ),
            "questions": {
                "critical_temp_breached": {
                    "type": "noul",
                    "instructions": "Did the trailer temperature rise above the -5C critical threshold for more than 30 minutes after the 03:15 compressor failure?",
                },
                "can_continue_normal_route": {
                    "type": "noul",
                    "instructions": "Is it safe for the truck to continue its long-haul route without stopping at a cold storage facility?",
                },
                "dispatch_automation_action": {
                    "type": "choice",
                    "instructions": "What immediate action should the fleet control tower trigger?",
                    "criteria": {
                        "continue_planned_route": "Continue normal highway route to final destination",
                        "reroute_to_bolu_cold_storage": "Emergency reroute to nearest Cold Storage (Bolu - 18 km) & dispatch backup reefer truck",
                        "ignore_sensor_alert": "Mute IoT alarm and wait 6 hours",
                    },
                },
                "spoilage_urgency": {
                    "type": "score",
                    "instructions": "Rate the urgency of intervention to prevent vaccine/frozen food spoilage.",
                    "criteria": ["Normal", "Watch", "Urgent", "Critical Spoilage Imminent"],
                },
            },
        },
        {
            "id": "llm_router_freight_chat",
            "title": "🤖 10. Mobil Yük Borsası: LLM Öncesi Niyet, Fraud & Araç Çağrısı Yönlendirici (JSON)",
            "category": "Lojistik & Yük Borsası",
            "badge": "System-1 LLM Router",
            "model": "nace-ai/drex-max",
            "description": (
                "Mobil uygulamadaki sohbet/teklif mesajını üretken LLM'e göndermeden önce Drex Max ile milisaniyeler içinde "
                "inceler: Komisyon atlatma (platform dışı IBAN/telefon paylaşımı) ve hangi API aracının çağrılacağını seçer."
            ),
            "sample_images": [],
            "state_json": {
                "app_module": "Sendicom Mobil Yük Borsası - İlan İçi Mesajlaşma",
                "load_id": "YUK-88310",
                "listed_price_tl": 38000,
                "carrier_profile": {
                    "id": "USR-4412",
                    "verified_k1_certificate": True,
                    "completed_trips": 19,
                },
                "incoming_chat_message": (
                    "Reis uygulama üzerinden onaylama %8 komisyon kesiyorlar. Sen ilanı iptal et, "
                    "beni sıfır beş yüz otuz iki dört yüz on bir yirmi iki otuz üç numaradan ara "
                    "elden 35.000 TL nakit IBAN'a at hemen yükleyelim."
                ),
            },
            "questions": {
                "attempts_platform_fee_circumvention": {
                    "type": "noul",
                    "instructions": "Is the user attempting to bypass the platform commission by moving the transaction off-platform?",
                },
                "shares_masked_phone_or_iban": {
                    "type": "noul",
                    "instructions": "Does the message contain a phone number written in words or an off-platform payment solicitation?",
                },
                "orchestrator_next_step": {
                    "type": "choice",
                    "instructions": "Which backend pipeline step should execute before any LLM reply?",
                    "criteria": {
                        "block_message_and_warn_carrier": "Block message delivery, mask contact info, and issue Policy Violation Warning without calling expensive LLM",
                        "forward_to_shipper_normally": "Deliver chat message directly to shipper",
                        "trigger_price_counter_offer_tool": "Call automated price counter-offer API tool",
                    },
                },
                "policy_violation_severity": {
                    "type": "score",
                    "instructions": "Rate the severity of the marketplace policy violation.",
                    "criteria": ["No Violation", "Minor Off-Topic", "Commission Circumvention Attempt", "Severe Fraud / Account Ban"],
                },
            },
        },
        # ============================================================================
        # 3. GENEL KURUMSAL MULTIMODAL SENARYOLAR
        # ============================================================================
        {
            "id": "vision_invoice_audit",
            "title": "🧾 11. Kurumsal Bulut Faturası Denetimi & UI Aksiyonu",
            "category": "Kurumsal & Genel",
            "badge": "Görsel + Finans",
            "model": "nace-ai/drex-max-finance",
            "description": "Bulut faturasındaki (invoice_audit.png) mükerrer H100 GPU kalemini tespit eder ve DISPUTE butonunu seçer.",
            "sample_images": ["invoice_audit.png"],
            "state_text": "Audit policy: Flag any invoice over $5,000 or containing duplicate billing.",
            "questions": {
                "has_duplicate_billing": {
                    "type": "noul",
                    "instructions": "Does the invoice image show a duplicate charge for the H100 GPU cluster?",
                },
                "ui_button_to_click": {
                    "type": "choice",
                    "instructions": "Which UI action button should the finance agent click?",
                    "criteria": {
                        "btn_1_approve": "Click [BTN-1] APPROVE & PAY",
                        "btn_2_dispute": "Click [BTN-2] DISPUTE DUPLICATE",
                        "btn_3_archive": "Click [BTN-3] ARCHIVE ONLY",
                    },
                },
            },
        },
        {
            "id": "vision_browser_agent",
            "title": "🌐 12. Tarayıcı Ajanı (Computer Use) 504 Ödeme Hatası Navigasyonu",
            "category": "Kurumsal & Genel",
            "badge": "Browser Agent",
            "model": "nace-ai/drex-max",
            "description": "504 Gateway Timeout ekran görüntüsünü (ui_checkout_error.png) okuyup idempotent retry aksiyonunu seçer.",
            "sample_images": ["ui_checkout_error.png"],
            "state_text": "Browser Agent Goal: Complete checkout without double-charging the card.",
            "questions": {
                "was_card_charged": {
                    "type": "noul",
                    "instructions": "According to the modal, has the card been charged yet?",
                },
                "next_browser_action": {
                    "type": "choice",
                    "instructions": "Which button should the agent click next?",
                    "criteria": {
                        "click_retry_idempotent": "Click RETRY WITH IDEMPOTENCY",
                        "click_cancel_cart": "Click CANCEL & DELETE CART",
                    },
                },
            },
        },
    ]
