"""
Nace.AI Drex Max OpenRouter Client, Preset Simulation Scenarios &
System 1 (Drex Max) + System 2 (Generative LLM) Hybrid Logistics Orchestrator.
"""

from __future__ import annotations

import base64
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
        "id": "nace-ai/drex-max",
        "name": "Nace.AI: Drex Max (27B Multimodal)",
        "modalities": ["text", "image"],
        "context_length": 262144,
        "input_price_per_m": 0.06,
        "output_price_per_m": 0.00,
        "description": "Flagship 27B multimodal decision model (Decision Index 0.4: 67.52, Vision Index: 73.92). Accepts text, JSON, and up to 4 images.",
    },
    {
        "id": "nace-ai/drex-max-finance",
        "name": "Nace.AI: Drex Max Finance (27B Multimodal)",
        "modalities": ["text", "image"],
        "context_length": 262144,
        "input_price_per_m": 0.06,
        "output_price_per_m": 0.00,
        "description": "Finance-tuned 27B multimodal decision model built for invoices, waybills, escrow, compliance, and markets.",
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
    model: str = "nace-ai/drex-max",
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
        "X-Title": "Drex Max Multimodal Decision Playground",
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


def run_hybrid_logistics_pipeline(
    scenario_type: str = "pod_dispute",
    sample_dir: Path | None = None,
    llm_model: str = "openai/gpt-4o-mini",
) -> dict[str, Any]:
    """
    Simulates a production 4-Layer Architecture between Mobile Freight Exchange App,
    System 1 Decision Model (`nace-ai/drex-max`), Backend Rules Engine, and
    System 2 Generative LLM (`openai/gpt-4o-mini`) + Final System 1 Guardrail.
    """
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    sdir = sample_dir or (Path(__file__).parent / "samples")

    if scenario_type == "wms_hazmat_dock":
        img_url = encode_image_to_data_url(sdir / "warehouse_damaged_pallet.png")
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
        # Default: POD Waybill & Escrow Payment Release Dispute
        img_url = encode_image_to_data_url(sdir / "logistics_pod_waybill.png")
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

    # --- STEP 1: System 1 (Drex Max) Multimodal Decision ---
    s1_state = [json.dumps(event_context, ensure_ascii=False), make_image_part(img_url)]
    s1_result = evaluate_decision(
        state=s1_state,
        questions=s1_questions,
        model="nace-ai/drex-max",
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
        "Sen Sendicom Mobil Yük Borsası ve WMS Operasyon Asistanısın.\n"
        "ÖNEMLİ KURAL: Kendin karar verme! Üst katmandaki System-1 Karar Modeli (Drex Max) görseli ve veriyi inceleyerek "
        "kesin ve bağlayıcı kararı verdi. Sadece bu kararı sürücüye/operatöre açıklayan, kısa (3-4 cümle), profesyonel Türkçe mobil bildirim mesajı yaz.\n\n"
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

    # --- STEP 4: System 1 (Drex Max) Output Guardrail Check ---
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
            "instructions": "Does the notification falsely promise immediate full unconditional payment or ignore the detected hazard/mismatch?",
        },
        "push_gateway_verdict": {
            "type": "choice",
            "instructions": "Should the mobile push notification gateway deliver this message to the user's phone?",
            "criteria": {
                "deliver_push_notification": "Message is accurate, safe, and aligned with System-1 decision",
                "block_hallucinated_message": "Block message because it contradicts System-1 decision",
            },
        },
    }
    guardrail_result = evaluate_decision(
        state=guardrail_state,
        questions=guardrail_questions,
        model="nace-ai/drex-max",
    )

    return {
        "ok": True,
        "scenario_type": scenario_type,
        "event_context": event_context,
        "step1_system1_vision_decision": {
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
    """Returns built-in Logistics / Warehouse / Mobile Freight Exchange + General Enterprise presets."""
    return [
        # ============================================================================
        # DEPO (WMS), LOJİSTİK & MOBİL YÜK BORSASI SENARYOLARI
        # ============================================================================
        {
            "id": "logistics_pod_escrow",
            "title": "🚚 1. Mobil Yük Borsası: Sevk İrsaliyesi (POD) & Hak Ediş (Escrow) Denetimi",
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
            "title": "🏭 2. Depo (WMS) Rampa Kabul: Hasarlı Palet & Beyan Edilmemiş ADR Tespiti",
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
            "title": "📱 3. Mobil Yük Borsası: İlan Şartları vs Taşıyıcı Teklifi Uygunluk Kalkanı",
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
            "title": "❄️ 4. Soğuk Zincir (Frigo) IoT Telemetri Grafiği & Acil Rota Değişikliği",
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
            "id": "logistics_multi_image_claim",
            "title": "🔗 5. Çoklu Görsel Lojistik Hasar Dosyası (İrsaliye + Depo Kamera Korelasyonu)",
            "category": "Lojistik & Yük Borsası",
            "badge": "2 Görsel: POD + Kamera",
            "model": "nace-ai/drex-max",
            "description": (
                "Drex Max'e hem imzalı Sevk İrsaliyesini (logistics_pod_waybill.png) hem de Rampa Kamera görüntüsünü "
                "(warehouse_damaged_pallet.png) aynı anda verir; belge ile fiziksel hasar kanıtını çapraz doğrular."
            ),
            "sample_images": ["logistics_pod_waybill.png", "warehouse_damaged_pallet.png"],
            "state_text": (
                "Hasar Uzlaştırma Merkezi: Görsel 1 alıcı deponun şerh düştüğü sevk irsaliyesi, Görsel 2 ise rampa kamerasındaki "
                "ezilmiş/sızıntılı palet görüntüsüdür. İki görsel kanıt birbirini doğruluyorsa sigorta hasar dosyasını otomatik aç."
            ),
            "questions": {
                "visual_evidence_corroborates_waybill": {
                    "type": "noul",
                    "instructions": "Does the physical pallet damage/leak in Image 2 corroborate the damage reservation note written on the waybill in Image 1?",
                },
                "driver_claim_of_clean_delivery_valid": {
                    "type": "noul",
                    "instructions": "Is the driver's claim that 'all pallets were delivered intact without any damage' supported by the two images?",
                },
                "claims_department_routing": {
                    "type": "choice",
                    "instructions": "How should the automated claims engine process this shipment?",
                    "criteria": {
                        "approve_clean_delivery": "Close ticket as clean delivery and pay carrier 100%",
                        "open_verified_cargo_damage_claim": "Open verified cargo damage & Hazmat non-compliance claim with visual evidence attached",
                        "request_more_photos": "Reject claim due to lack of visual proof",
                    },
                },
                "evidence_strength": {
                    "type": "score",
                    "instructions": "Rate the strength of the combined visual and documentary evidence.",
                    "criteria": ["Weak / Contradictory", "Moderate", "Strong", "Conclusive Multi-Modal Proof"],
                },
            },
        },
        {
            "id": "llm_router_freight_chat",
            "title": "🤖 6. Mobil Yük Borsası: LLM Öncesi Niyet, Fraud & Araç Çağrısı Yönlendirici (JSON)",
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
        # GENEL KURUMSAL MULTIMODAL & JSON SENARYOLARI
        # ============================================================================
        {
            "id": "vision_invoice_audit",
            "title": "🧾 7. Görsel Fatura Denetimi & Ajan UI Aksiyonu (Vision + Finance)",
            "category": "Kurumsal & Finans",
            "badge": "Görsel + Finans",
            "model": "nace-ai/drex-max",
            "description": (
                "Fatura görselini (invoice_audit.png) doğrudan okur; mükerrer (duplicate) ücretlendirmeyi "
                "tespit eder, ekrandaki hangi UI butonuna tıklanması gerektiğini seçer ve finansal risk skorunu hesaplar."
            ),
            "sample_images": ["invoice_audit.png"],
            "state_text": (
                "Company Audit Policy: Automatically approve cloud infrastructure invoices under $5,000 if all line items are unique. "
                "Immediately dispute and flag any invoice containing duplicate billing or exceeding $5,000."
            ),
            "questions": {
                "has_duplicate_billing": {
                    "type": "noul",
                    "instructions": "Does the invoice image show a duplicate charge for the H100 GPU cluster?",
                },
                "exceeds_auto_pay_limit": {
                    "type": "noul",
                    "instructions": "Is the total amount due on the invoice greater than $5,000?",
                },
                "ui_button_to_click": {
                    "type": "choice",
                    "instructions": "Which UI action button at the bottom of the invoice screen should the finance agent click?",
                    "criteria": {
                        "btn_1_approve": "Click [BTN-1] APPROVE & PAY (green button)",
                        "btn_2_dispute": "Click [BTN-2] DISPUTE DUPLICATE (red button)",
                        "btn_3_archive": "Click [BTN-3] ARCHIVE ONLY (gray button)",
                    },
                },
                "financial_risk_score": {
                    "type": "score",
                    "instructions": "Rate the financial risk of paying this invoice without human intervention.",
                    "criteria": ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"],
                },
            },
        },
        {
            "id": "vision_browser_agent",
            "title": "🌐 8. Tarayıcı Ajanı (Computer Use) UI Navigasyonu (Vision)",
            "category": "Kurumsal & Finans",
            "badge": "Görsel + Browser Agent",
            "model": "nace-ai/drex-max",
            "description": (
                "Bir e-ticaret ödeme sayfasında alınan 504 Gateway Timeout ekran görüntüsünü (ui_checkout_error.png) "
                "inceler; karttan para çekilip çekilmediğini doğrular ve bir sonraki tarayıcı aksiyonunu seçer."
            ),
            "sample_images": ["ui_checkout_error.png"],
            "state_text": (
                "Browser Agent Goal: Complete purchase of 2x Pro Workstation License without double-charging the corporate Visa card "
                "or losing the active session token."
            ),
            "questions": {
                "was_card_charged": {
                    "type": "noul",
                    "instructions": "According to the error modal in the screenshot, has the corporate card been charged yet?",
                },
                "safe_to_open_new_tab": {
                    "type": "noul",
                    "instructions": "Is it safe to open a new browser tab without expiring the session token?",
                },
                "next_browser_action": {
                    "type": "choice",
                    "instructions": "Which action should the browser automation agent execute next?",
                    "criteria": {
                        "click_retry_idempotent": "Click the blue 'RETRY WITH IDEMPOTENCY' button inside the modal",
                        "click_cancel_cart": "Click 'CANCEL & DELETE CART' and abort the order",
                        "open_new_tab": "Open a new browser tab and restart checkout from scratch",
                    },
                },
                "recovery_confidence": {
                    "type": "score",
                    "instructions": "How recoverable is this checkout error without losing the cart?",
                    "criteria": ["Unrecoverable", "Hard to recover", "Likely recoverable", "Easily recoverable via idempotent retry"],
                },
            },
        },
        {
            "id": "vision_telemetry_anomaly",
            "title": "📈 9. Sunucu Telemetri Grafiği & Canary Rollback Kararı (Vision)",
            "category": "Kurumsal & Finans",
            "badge": "Görsel Grafik Analizi",
            "model": "nace-ai/drex-max",
            "description": (
                "Canlı sistem izleme grafiğini (server_telemetry_chart.png) görsel olarak okur; v2.4.1 sürüm geçişi "
                "sonrası CPU ve HTTP 5xx SLO ihlalini tespit ederek otomatik Rollback kararı verir."
            ),
            "sample_images": ["server_telemetry_chart.png"],
            "state_text": (
                "SRE Automated Canary Gate: Evaluate post-deployment telemetry chart for release v2.4.1 deployed at 14:20."
            ),
            "questions": {
                "slo_breached_after_deploy": {
                    "type": "noul",
                    "instructions": "Did CPU usage breach the 80% SLO threshold immediately after the 14:20 deployment of v2.4.1?",
                },
                "trigger_auto_rollback": {
                    "type": "noul",
                    "instructions": "Should the automated canary gate trigger an immediate rollback of release v2.4.1?",
                },
                "incident_action": {
                    "type": "choice",
                    "instructions": "What is the correct SRE automation action based on the chart?",
                    "criteria": {
                        "promote_to_100_percent": "Promote v2.4.1 to 100% production traffic",
                        "wait_and_monitor": "Take no action and wait another 60 minutes",
                        "immediate_rollback": "Rollback v2.4.1 immediately and page on-call engineer",
                    },
                },
                "incident_severity": {
                    "type": "score",
                    "instructions": "Rate the severity of the production anomaly shown in the chart.",
                    "criteria": ["SEV-4 (Minor)", "SEV-3 (Moderate)", "SEV-2 (High)", "SEV-1 (Critical Outage)"],
                },
            },
        },
        {
            "id": "vision_moderation_phishing",
            "title": "🛡️ 10. Görsel İçerik Moderasyonu & Kripto Phishing Tespiti (Vision)",
            "category": "Kurumsal & Finans",
            "badge": "Görsel Güvenlik",
            "model": "nace-ai/drex-max",
            "description": (
                "Sosyal medya paylaşım görselini (moderation_card.png) inceler; seed-phrase oltalama (phishing) "
                "ve ön ödemeli kripto dolandırıcılığını tespit ederek yaptırım kararını puanlar."
            ),
            "sample_images": ["moderation_card.png"],
            "state_text": (
                "Trust & Safety Policy #4.2: Strictly prohibit seed-phrase solicitation, impersonation of financial/crypto support, "
                "and advance-fee giveaway scams."
            ),
            "questions": {
                "solicits_seed_phrase": {
                    "type": "noul",
                    "instructions": "Does the post in the image ask users to enter their 12-word recovery seed phrase or private key?",
                },
                "is_advance_fee_scam": {
                    "type": "noul",
                    "instructions": "Does the post request an upfront ETH gas fee to claim a reward?",
                },
                "enforcement_decision": {
                    "type": "choice",
                    "instructions": "Which moderation enforcement action should be applied?",
                    "criteria": {
                        "approve_post": "Approve post as safe promotional content",
                        "add_warning_label": "Keep post visible with a minor warning label",
                        "ban_account_and_remove": "Immediately remove post, block phishing domain, and ban account",
                    },
                },
                "harm_severity": {
                    "type": "score",
                    "instructions": "Rate the financial harm risk to users if this post remains live.",
                    "criteria": ["Negligible", "Low", "High", "Extreme / Immediate Wallet Drain"],
                },
            },
        },
    ]
