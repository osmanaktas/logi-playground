"""
Nace.AI Drex Max OpenRouter Client & Preset Simulation Scenarios.

Drex Max (`nace-ai/drex-max`) is a 27B multimodal decision model (262K context)
with a 255-way readout head. Instead of generating text token-by-token, it evaluates
a given `state` (text, JSON, or up to 4 images) and typed `questions` (`noul`, `choice`,
`score`) in a single forward pass, returning calibrated probabilities and confidence scores.
"""

from __future__ import annotations

import base64
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
        "description": "Finance-tuned 27B multimodal decision model built for invoices, receipts, banking, compliance, credit, and markets.",
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


def get_presets() -> list[dict[str, Any]]:
    """Returns built-in multimodal (vision) and text/JSON simulation presets."""
    return [
        {
            "id": "vision_invoice_audit",
            "title": "🧾 1. Görsel Fatura Denetimi & Ajan UI Aksiyonu (Vision + Finance)",
            "category": "Multimodal Vision",
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
            "title": "🌐 2. Tarayıcı Ajanı (Computer Use) UI Navigasyonu (Vision)",
            "category": "Multimodal Vision",
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
            "title": "📈 3. Sunucu Telemetri Grafiği & Canary Rollback Kararı (Vision)",
            "category": "Multimodal Vision",
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
            "title": "🛡️ 4. Görsel İçerik Moderasyonu & Kripto Phishing Tespiti (Vision)",
            "category": "Multimodal Vision",
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
        {
            "id": "multi_image_correlation",
            "title": "⚖️ 5. Çoklu Görsel Korelasyon Analizi (Multi-Image Vision State)",
            "category": "Multimodal Vision",
            "badge": "2 Görsel Birden",
            "model": "nace-ai/drex-max",
            "description": (
                "Drex Max'in tek istekte 4 görsele kadar analiz yeteneğini simüle eder: Hem ödeme hatası ekranını "
                "(ui_checkout_error.png) hem de sunucu telemetri grafiğini (server_telemetry_chart.png) aynı anda değerlendirir."
            ),
            "sample_images": ["ui_checkout_error.png", "server_telemetry_chart.png"],
            "state_text": (
                "Incident Correlation Context: Image 1 is the customer's checkout browser screen showing a 504 Gateway Timeout. "
                "Image 2 is our backend cluster telemetry chart showing CPU spiking to 98.4% and HTTP 5xx rate jumping to 14.2% right after Deploy v2.4.1."
            ),
            "questions": {
                "are_incidents_correlated": {
                    "type": "noul",
                    "instructions": "Does the backend telemetry spike in Image 2 explain the 504 Gateway Timeout seen by the user in Image 1?",
                },
                "root_cause_department": {
                    "type": "choice",
                    "instructions": "Which engineering group should own the root-cause remediation?",
                    "criteria": {
                        "release_sre_team": "Backend Release & SRE Team (rollback v2.4.1 causing 98.4% CPU & 5xx timeouts)",
                        "frontend_css_team": "Frontend UI/CSS Styling Team",
                        "customer_card_issuer": "Customer's Corporate Visa Bank",
                    },
                },
                "systemic_impact_score": {
                    "type": "score",
                    "instructions": "How systemic is this issue across the platform?",
                    "criteria": ["Isolated single user", "Minor glitch", "Major service degradation", "Platform-wide checkout outage"],
                },
            },
        },
        {
            "id": "json_support_triage",
            "title": "🎫 6. Yapılandırılmış JSON Destek & SLA Triyajı (Text / JSON State)",
            "category": "Text / JSON Decision",
            "badge": "JSON State",
            "model": "nace-ai/drex-max",
            "description": (
                "Görsel olmadan saf yapılandırılmış JSON verisi üzerinde milisaniyeler içinde departman yönlendirmesi, "
                "SLA ihlal riski ve iade talebi sınıflandırması yapar."
            ),
            "sample_images": [],
            "state_json": {
                "customer": {
                    "tier": "Enterprise Platinum",
                    "arr_usd": 145000,
                    "sla_response_minutes": 15,
                },
                "ticket": {
                    "subject": "Production SSO SAML Assertion Failure after certificate rotation",
                    "body": "All 450 of our engineers are locked out of the dashboard since 09:00 UTC. SAML response returns InvalidSignature. Need immediate hotfix or cert rollback!",
                    "attachments": ["saml_trace.xml"],
                },
            },
            "questions": {
                "is_production_lockout": {
                    "type": "noul",
                    "instructions": "Are the customer's users completely locked out of production?",
                },
                "asking_for_refund": {
                    "type": "noul",
                    "instructions": "Is the customer asking for a monetary refund in this ticket?",
                },
                "routing_queue": {
                    "type": "choice",
                    "instructions": "Which specialized engineering queue should receive this ticket?",
                    "criteria": {
                        "iam_sso_security": "Identity, SAML SSO, Authentication, and Certificate Management",
                        "billing_invoicing": "Invoices, subscriptions, and refunds",
                        "data_warehouse": "Analytics exports and SQL reporting",
                        "general_tier1": "Password resets for free-tier users",
                    },
                },
                "sla_priority": {
                    "type": "score",
                    "instructions": "Rate the SLA priority level for this ticket.",
                    "criteria": ["P4 - Low", "P3 - Normal", "P2 - High", "P1 - Blocker (Immediate Page)"],
                },
            },
        },
    ]
