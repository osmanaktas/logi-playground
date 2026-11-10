"""
Generates synthetic visual test images for Nace.AI Drex Max multimodal decision testing.
Includes:
1. Invoice / Receipt UI with duplicate charge & action buttons (KIE + UI Navigation)
2. Browser Checkout 504 Error Modal screenshot (Computer Use / Mind2Web)
3. Server Telemetry & Deployment Anomaly Chart (CharXiv / InfographicVQA)
4. Social Media Phishing / Moderation Card (Visual Trust & Safety)
"""

from pathlib import Path
from PIL import Image, ImageDraw

SAMPLES_DIR = Path(__file__).parent / "samples"


def create_invoice_image(path: Path) -> None:
    img = Image.new("RGB", (760, 460), color=(248, 250, 252))
    d = ImageDraw.Draw(img)

    # Header bar
    d.rectangle([20, 20, 740, 88], fill=(15, 23, 42))
    d.text((40, 38), "ACME CLOUD INFRASTRUCTURE  |  INVOICE #INV-2026-8841", fill=(255, 255, 255))
    d.text((40, 60), "Date: 2026-11-10   |   Account: Enterprise-Prod-01   |   Currency: USD", fill=(148, 163, 184))

    # Status badge
    d.rectangle([590, 34, 720, 72], fill=(220, 38, 38))
    d.text((612, 47), "OVERDUE / ALERT", fill=(255, 255, 255))

    # Table box
    d.rectangle([20, 105, 740, 330], outline=(203, 213, 225), width=2, fill=(255, 255, 255))
    d.rectangle([20, 105, 740, 140], fill=(241, 245, 249))
    d.text((40, 117), "LINE ITEM DESCRIPTION", fill=(51, 65, 85))
    d.text((480, 117), "QTY", fill=(51, 65, 85))
    d.text((610, 117), "AMOUNT (USD)", fill=(51, 65, 85))

    # Row 1
    d.text((40, 160), "1. H100 GPU Dedicated Cluster (Monthly Reserved)", fill=(15, 23, 42))
    d.text((485, 160), "1", fill=(15, 23, 42))
    d.text((625, 160), "$4,200.00", fill=(15, 23, 42))
    d.line([35, 190, 725, 190], fill=(226, 232, 240), width=1)

    # Row 2 (Duplicate charge highlighted)
    d.rectangle([28, 198, 732, 238], fill=(254, 242, 242))
    d.text((40, 212), "2. H100 GPU Dedicated Cluster (DUPLICATE BILLING)", fill=(185, 28, 28))
    d.text((485, 212), "1", fill=(185, 28, 28))
    d.text((625, 212), "$4,200.00", fill=(185, 28, 28))
    d.line([35, 246, 725, 246], fill=(226, 232, 240), width=1)

    # Row 3
    d.text((40, 260), "3. Egress Bandwidth & Snapshot Storage (12 TB)", fill=(15, 23, 42))
    d.text((485, 260), "1", fill=(15, 23, 42))
    d.text((632, 260), "$350.00", fill=(15, 23, 42))

    # Total
    d.rectangle([450, 290, 730, 322], fill=(254, 226, 226))
    d.text((465, 300), "TOTAL AMOUNT DUE:  $8,750.00", fill=(153, 27, 27))

    # Action Buttons for UI Agent
    d.text((25, 350), "Finance Agent Action Bar (Select one):", fill=(71, 85, 105))

    d.rectangle([25, 378, 245, 432], fill=(22, 163, 74))
    d.text((55, 399), "[BTN-1] APPROVE & PAY", fill=(255, 255, 255))

    d.rectangle([265, 378, 505, 432], fill=(220, 38, 38))
    d.text((290, 399), "[BTN-2] DISPUTE DUPLICATE", fill=(255, 255, 255))

    d.rectangle([525, 378, 735, 432], fill=(71, 85, 105))
    d.text((555, 399), "[BTN-3] ARCHIVE ONLY", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_checkout_error_image(path: Path) -> None:
    img = Image.new("RGB", (760, 460), color=(241, 245, 249))
    d = ImageDraw.Draw(img)

    # Browser chrome
    d.rectangle([0, 0, 760, 46], fill=(30, 41, 59))
    d.ellipse([16, 15, 30, 29], fill=(239, 68, 68))
    d.ellipse([38, 15, 52, 29], fill=(245, 158, 11))
    d.ellipse([60, 15, 74, 29], fill=(34, 197, 94))
    d.rectangle([100, 10, 660, 36], fill=(51, 65, 85))
    d.text((120, 17), "https://store.example.com/checkout/payment-confirm", fill=(226, 232, 240))

    # Background checkout summary
    d.rectangle([40, 70, 720, 430], fill=(255, 255, 255), outline=(203, 213, 225))
    d.text((65, 90), "Order Summary: 2x Pro Workstation License ($598.00)", fill=(148, 163, 184))
    d.text((65, 115), "Payment Method: Corporate Visa ending in 4419", fill=(148, 163, 184))

    # Dark overlay modal
    d.rectangle([120, 145, 640, 395], fill=(255, 255, 255), outline=(220, 38, 38), width=3)
    d.rectangle([120, 145, 640, 195], fill=(220, 38, 38))
    d.text((145, 164), "ERROR 504: PAYMENT GATEWAY TIMEOUT", fill=(255, 255, 255))

    d.text((145, 215), "Upstream Stripe gateway did not respond within 15,000ms.", fill=(30, 41, 59))
    d.text((145, 240), "Your card has NOT been charged yet. Idempotency Key: ik_99281a", fill=(22, 101, 52))
    d.text((145, 268), "Warning: Do not open a new tab or your session token will expire.", fill=(180, 83, 9))

    # Modal buttons
    d.rectangle([145, 315, 365, 368], fill=(37, 99, 235))
    d.text((170, 336), "RETRY WITH IDEMPOTENCY", fill=(255, 255, 255))

    d.rectangle([390, 315, 615, 368], fill=(226, 232, 240), outline=(148, 163, 184))
    d.text((420, 336), "CANCEL & DELETE CART", fill=(51, 65, 85))

    img.save(path, format="PNG")


def create_telemetry_chart_image(path: Path) -> None:
    img = Image.new("RGB", (760, 460), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Title
    d.text((30, 22), "PROD CLUSTER TELEMETRY  |  CPU & ERROR RATE  (Release v2.4.1 deployed at 14:20)", fill=(248, 250, 252))
    d.text((30, 46), "SLO Threshold: CPU < 80%  |  HTTP 5xx Error Rate < 1.0%", fill=(148, 163, 184))

    # Chart area
    cx0, cy0, cx1, cy1 = 70, 85, 710, 360
    d.rectangle([cx0, cy0, cx1, cy1], fill=(30, 41, 59), outline=(71, 85, 105))

    # Grid lines & Y-axis labels
    for pct, label in [(0, "100%"), (0.2, "80% (SLO)"), (0.5, "50%"), (0.8, "20%"), (1.0, "0%")]:
        y = int(cy0 + pct * (cy1 - cy0))
        color = (239, 68, 68) if pct == 0.2 else (51, 65, 85)
        d.line([cx0, y, cx1, y], fill=color, width=1)
        d.text((15, y - 6), label, fill=(203, 213, 225))

    # Deployment marker at x = 390 (14:20)
    deploy_x = 390
    d.line([deploy_x, cy0, deploy_x, cy1], fill=(250, 204, 21), width=2)
    d.rectangle([deploy_x - 75, cy0 + 8, deploy_x + 85, cy0 + 32], fill=(250, 204, 21))
    d.text((deploy_x - 68, cy0 + 14), "DEPLOY v2.4.1 (14:20)", fill=(15, 23, 42))

    # CPU curve (normal before 14:20, spikes to 98% after 14:20)
    pts = [
        (90, 300), (150, 295), (210, 302), (270, 290), (330, 298), (390, 294),
        (430, 180), (470, 110), (520, 96), (580, 92), (640, 90), (695, 90)
    ]
    d.line(pts, fill=(56, 189, 248), width=4)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(56, 189, 248))

    # Callout box on spike
    d.rectangle([490, 115, 695, 175], fill=(127, 29, 29), outline=(248, 113, 113))
    d.text((502, 125), "ALERT: CPU = 98.4% (BREACH)", fill=(255, 255, 255))
    d.text((502, 148), "HTTP 5xx Rate = 14.2%", fill=(254, 202, 202))

    # X-axis timestamps
    times = [(90, "13:50"), (210, "14:00"), (330, "14:10"), (390, "14:20"), (520, "14:30"), (640, "14:40")]
    for x, t in times:
        d.text((x - 15, cy1 + 12), t, fill=(203, 213, 225))

    # Footer legend
    d.rectangle([30, 405, 730, 442], fill=(30, 41, 59))
    d.text((45, 418), "Automated Canary Gate: Rollback required if CPU > 80% or 5xx > 1% after deploy.", fill=(248, 250, 252))

    img.save(path, format="PNG")


def create_moderation_card_image(path: Path) -> None:
    img = Image.new("RGB", (760, 420), color=(248, 250, 252))
    d = ImageDraw.Draw(img)

    d.rectangle([30, 25, 730, 395], fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    d.ellipse([55, 50, 105, 100], fill=(234, 179, 8))
    d.text((73, 68), "VIP", fill=(255, 255, 255))
    d.text((120, 55), "@Official_Treasury_Airdrop_Support  (Unverified Account - Created 2h ago)", fill=(15, 23, 42))
    d.text((120, 80), "Sponsored Post  |  Reported by 14 users", fill=(220, 38, 38))

    d.rectangle([55, 120, 705, 290], fill=(254, 249, 195), outline=(250, 204, 21), width=2)
    d.text((75, 140), "URGENT SECURITY NOTICE: Your wallet has been selected for a 5.0 ETH refund!", fill=(15, 23, 42))
    d.text((75, 172), "To claim your instant 2x crypto bonus, enter your 12-word recovery seed phrase", fill=(185, 28, 28))
    d.text((75, 200), "and private key at:  http://secure-metamask-claim-verify.xyz/login", fill=(37, 99, 235))
    d.text((75, 238), "Offer expires in 10 minutes! Send 0.1 ETH gas fee to verify ownership.", fill=(15, 23, 42))

    d.text((55, 318), "Trust & Safety Queue Metadata: Category = Financial Scam / Seed Phrase Phishing", fill=(71, 85, 105))
    d.text((55, 345), "Platform Policy #4.2: Immediate ban for seed-phrase solicitation or advance-fee scams.", fill=(71, 85, 105))

    img.save(path, format="PNG")


def ensure_sample_images() -> list[str]:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "invoice_audit.png": create_invoice_image,
        "ui_checkout_error.png": create_checkout_error_image,
        "server_telemetry_chart.png": create_telemetry_chart_image,
        "moderation_card.png": create_moderation_card_image,
    }
    created = []
    for name, fn in files.items():
        target = SAMPLES_DIR / name
        fn(target)
        created.append(str(target))
    return created


if __name__ == "__main__":
    paths = ensure_sample_images()
    print(f"Generated {len(paths)} sample images in {SAMPLES_DIR}:")
    for p in paths:
        print(" -", p)
