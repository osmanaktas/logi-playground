"""
Generates synthetic visual test images for Nace.AI Drex Max multimodal decision testing.
Includes 8 visual scenarios:
1-4: General Enterprise (Invoice Audit, Browser 504 Error, Server Telemetry, Moderation Card)
5-8: Warehouse (WMS), Logistics & Mobile Freight Exchange (Mobil Yük Borsası):
  5. logistics_pod_waybill.png    - Sevk İrsaliyesi / POD (Proof of Delivery) with damage reservation note
  6. warehouse_damaged_pallet.png - WMS Dock Inspection: Damaged pallet with ADR Class 3 Hazmat label
  7. mobile_load_board_ui.png     - Mobile Freight Exchange UI: Cold-chain load vs Carrier bid screen
  8. cold_chain_telemetry.png     - Reefer Truck Cold-Chain Temperature Breach & Door Sensor Chart
"""

from pathlib import Path
from PIL import Image, ImageDraw

SAMPLES_DIR = Path(__file__).parent / "samples"


def create_invoice_image(path: Path) -> None:
    img = Image.new("RGB", (760, 460), color=(248, 250, 252))
    d = ImageDraw.Draw(img)

    d.rectangle([20, 20, 740, 88], fill=(15, 23, 42))
    d.text((40, 38), "ACME CLOUD INFRASTRUCTURE  |  INVOICE #INV-2026-8841", fill=(255, 255, 255))
    d.text((40, 60), "Date: 2026-11-10   |   Account: Enterprise-Prod-01   |   Currency: USD", fill=(148, 163, 184))

    d.rectangle([590, 34, 720, 72], fill=(220, 38, 38))
    d.text((612, 47), "OVERDUE / ALERT", fill=(255, 255, 255))

    d.rectangle([20, 105, 740, 330], outline=(203, 213, 225), width=2, fill=(255, 255, 255))
    d.rectangle([20, 105, 740, 140], fill=(241, 245, 249))
    d.text((40, 117), "LINE ITEM DESCRIPTION", fill=(51, 65, 85))
    d.text((480, 117), "QTY", fill=(51, 65, 85))
    d.text((610, 117), "AMOUNT (USD)", fill=(51, 65, 85))

    d.text((40, 160), "1. H100 GPU Dedicated Cluster (Monthly Reserved)", fill=(15, 23, 42))
    d.text((485, 160), "1", fill=(15, 23, 42))
    d.text((625, 160), "$4,200.00", fill=(15, 23, 42))
    d.line([35, 190, 725, 190], fill=(226, 232, 240), width=1)

    d.rectangle([28, 198, 732, 238], fill=(254, 242, 242))
    d.text((40, 212), "2. H100 GPU Dedicated Cluster (DUPLICATE BILLING)", fill=(185, 28, 28))
    d.text((485, 212), "1", fill=(185, 28, 28))
    d.text((625, 212), "$4,200.00", fill=(185, 28, 28))
    d.line([35, 246, 725, 246], fill=(226, 232, 240), width=1)

    d.text((40, 260), "3. Egress Bandwidth & Snapshot Storage (12 TB)", fill=(15, 23, 42))
    d.text((485, 260), "1", fill=(15, 23, 42))
    d.text((632, 260), "$350.00", fill=(15, 23, 42))

    d.rectangle([450, 290, 730, 322], fill=(254, 226, 226))
    d.text((465, 300), "TOTAL AMOUNT DUE:  $8,750.00", fill=(153, 27, 27))

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

    d.rectangle([0, 0, 760, 46], fill=(30, 41, 59))
    d.ellipse([16, 15, 30, 29], fill=(239, 68, 68))
    d.ellipse([38, 15, 52, 29], fill=(245, 158, 11))
    d.ellipse([60, 15, 74, 29], fill=(34, 197, 94))
    d.rectangle([100, 10, 660, 36], fill=(51, 65, 85))
    d.text((120, 17), "https://store.example.com/checkout/payment-confirm", fill=(226, 232, 240))

    d.rectangle([40, 70, 720, 430], fill=(255, 255, 255), outline=(203, 213, 225))
    d.text((65, 90), "Order Summary: 2x Pro Workstation License ($598.00)", fill=(148, 163, 184))
    d.text((65, 115), "Payment Method: Corporate Visa ending in 4419", fill=(148, 163, 184))

    d.rectangle([120, 145, 640, 395], fill=(255, 255, 255), outline=(220, 38, 38), width=3)
    d.rectangle([120, 145, 640, 195], fill=(220, 38, 38))
    d.text((145, 164), "ERROR 504: PAYMENT GATEWAY TIMEOUT", fill=(255, 255, 255))

    d.text((145, 215), "Upstream Stripe gateway did not respond within 15,000ms.", fill=(30, 41, 59))
    d.text((145, 240), "Your card has NOT been charged yet. Idempotency Key: ik_99281a", fill=(22, 101, 52))
    d.text((145, 268), "Warning: Do not open a new tab or your session token will expire.", fill=(180, 83, 9))

    d.rectangle([145, 315, 365, 368], fill=(37, 99, 235))
    d.text((170, 336), "RETRY WITH IDEMPOTENCY", fill=(255, 255, 255))

    d.rectangle([390, 315, 615, 368], fill=(226, 232, 240), outline=(148, 163, 184))
    d.text((420, 336), "CANCEL & DELETE CART", fill=(51, 65, 85))

    img.save(path, format="PNG")


def create_telemetry_chart_image(path: Path) -> None:
    img = Image.new("RGB", (760, 460), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    d.text((30, 22), "PROD CLUSTER TELEMETRY  |  CPU & ERROR RATE  (Release v2.4.1 deployed at 14:20)", fill=(248, 250, 252))
    d.text((30, 46), "SLO Threshold: CPU < 80%  |  HTTP 5xx Error Rate < 1.0%", fill=(148, 163, 184))

    cx0, cy0, cx1, cy1 = 70, 85, 710, 360
    d.rectangle([cx0, cy0, cx1, cy1], fill=(30, 41, 59), outline=(71, 85, 105))

    for pct, label in [(0, "100%"), (0.2, "80% (SLO)"), (0.5, "50%"), (0.8, "20%"), (1.0, "0%")]:
        y = int(cy0 + pct * (cy1 - cy0))
        color = (239, 68, 68) if pct == 0.2 else (51, 65, 85)
        d.line([cx0, y, cx1, y], fill=color, width=1)
        d.text((15, y - 6), label, fill=(203, 213, 225))

    deploy_x = 390
    d.line([deploy_x, cy0, deploy_x, cy1], fill=(250, 204, 21), width=2)
    d.rectangle([deploy_x - 75, cy0 + 8, deploy_x + 85, cy0 + 32], fill=(250, 204, 21))
    d.text((deploy_x - 68, cy0 + 14), "DEPLOY v2.4.1 (14:20)", fill=(15, 23, 42))

    pts = [
        (90, 300), (150, 295), (210, 302), (270, 290), (330, 298), (390, 294),
        (430, 180), (470, 110), (520, 96), (580, 92), (640, 90), (695, 90)
    ]
    d.line(pts, fill=(56, 189, 248), width=4)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(56, 189, 248))

    d.rectangle([490, 115, 695, 175], fill=(127, 29, 29), outline=(248, 113, 113))
    d.text((502, 125), "ALERT: CPU = 98.4% (BREACH)", fill=(255, 255, 255))
    d.text((502, 148), "HTTP 5xx Rate = 14.2%", fill=(254, 202, 202))

    times = [(90, "13:50"), (210, "14:00"), (330, "14:10"), (390, "14:20"), (520, "14:30"), (640, "14:40")]
    for x, t in times:
        d.text((x - 15, cy1 + 12), t, fill=(203, 213, 225))

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


def create_logistics_pod_waybill_image(path: Path) -> None:
    """Sevk İrsaliyesi / POD (Proof of Delivery) document with wet stamp + damage reservation note."""
    img = Image.new("RGB", (760, 480), color=(241, 245, 249))
    d = ImageDraw.Draw(img)

    # Document sheet
    d.rectangle([25, 18, 735, 385], fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    d.rectangle([25, 18, 735, 76], fill=(30, 58, 138))
    d.text((45, 30), "SEVK IRSALIYESI / PROOF OF DELIVERY (POD)  |  BELGE NO: #IRS-2026-90412", fill=(255, 255, 255))
    d.text((45, 52), "Gonderici: Marmara Gida A.S. (Gebze Depo)  ->  Alici: Anadolu Perakende Dagitim (Ankara)", fill=(191, 219, 254))

    # Shipment metadata
    d.text((45, 92), "Plaka / Dorse : 34 TRK 882 / 34 DRS 19", fill=(15, 23, 42))
    d.text((420, 92), "Yuk Borsasi Ilan ID : #LOAD-77419", fill=(15, 23, 42))
    d.text((45, 116), "Sevk Edilen   : 24 Euro Palet (Endustriyel Zeytinyagi Tenekeleri)", fill=(15, 23, 42))
    d.text((420, 116), "Hak Edis (Escrow)   : 48,500.00 TL", fill=(22, 101, 52))
    d.line([40, 140, 720, 140], fill=(203, 213, 225), width=2)

    # Delivery table
    d.text((45, 152), "KALEM", fill=(71, 85, 105))
    d.text((310, 152), "SEVK ADEDI", fill=(71, 85, 105))
    d.text((450, 152), "TESLIM ALINAN", fill=(71, 85, 105))
    d.text((590, 152), "DURUM", fill=(71, 85, 105))

    d.text((45, 178), "Euro Palet - 5L Zeytinyagi Kolisi", fill=(15, 23, 42))
    d.text((325, 178), "24 Palet", fill=(15, 23, 42))
    d.text((465, 178), "21 Palet Saglam", fill=(15, 23, 42))
    d.text((590, 178), "3 PALET HASARLI!", fill=(220, 38, 38))

    # Red Damage Reservation Box (Hasar Şerhi)
    d.rectangle([45, 212, 475, 365], fill=(254, 242, 242), outline=(220, 38, 38), width=2)
    d.text((60, 224), "ALICI DEPO TESLIMAT SERHI (DAMAGE RESERVATION NOTE):", fill=(185, 28, 28))
    d.text((60, 250), "- Rampa kabulde 3 paletin devrilmis ve tenekelerin", fill=(153, 27, 27))
    d.text((60, 272), "  delinmis oldugu tespit edildi (yag sizintisi mevcut).", fill=(153, 27, 27))
    d.text((60, 298), "- 3 Palet (Hasar Tutari: ~14,200 TL) TUTANAKLA IADE", fill=(185, 28, 28))
    d.text((60, 320), "  EDILDI. Sadece 21 palet teslim alinmistir.", fill=(185, 28, 28))
    d.text((60, 342), "- Hasar fotograflari WMS sistemine eklendi.", fill=(100, 116, 139))

    # Wet Stamp & Receiver Signature Box
    d.rectangle([495, 212, 715, 365], fill=(248, 250, 252), outline=(37, 99, 235), width=2)
    d.text((515, 224), "ALICI DEPO KASE & ISLAK IMZA", fill=(30, 58, 138))
    d.ellipse([530, 252, 680, 332], outline=(37, 99, 235), width=2)
    d.text((552, 275), "ANADOLU DEPO", fill=(37, 99, 235))
    d.text((545, 295), "TESLIM ALINDI - IMZA", fill=(37, 99, 235))
    d.text((515, 342), "Imza: [M. Demir - Rampa Sefi]", fill=(15, 23, 42))

    # Mobile App Escrow Action Buttons
    d.rectangle([25, 398, 245, 460], fill=(22, 163, 74))
    d.text((42, 422), "[1] TAM ODEMEYI SERBEST BIRAK", fill=(255, 255, 255))

    d.rectangle([265, 398, 515, 460], fill=(217, 119, 6))
    d.text((280, 422), "[2] ESCROW BLOKE & HASAR DOSYASI", fill=(255, 255, 255))

    d.rectangle([535, 398, 735, 460], fill=(71, 85, 105))
    d.text((552, 422), "[3] BELGE OKUNAKSIZ (RED)", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_warehouse_damaged_pallet_image(path: Path) -> None:
    """WMS Dock Inspection camera feed showing a damaged/leaning pallet with ADR Class 3 Hazmat diamond."""
    img = Image.new("RGB", (760, 480), color=(30, 41, 59))
    d = ImageDraw.Draw(img)

    # Top WMS Camera HUD
    d.rectangle([0, 0, 760, 54], fill=(15, 23, 42))
    d.text((20, 12), "WMS DOCK CAMERA #04 (INBOUND GATE B)  |  SCAN: PALLET-ID #PLT-99204", fill=(56, 189, 248))
    d.text((20, 32), "ASN Manifest: Declared as 'Standard Dry Goods (Non-Hazardous)'  |  Weight: 640 kg", fill=(203, 213, 225))

    # Warehouse floor & pallet drawing
    d.rectangle([30, 70, 460, 385], fill=(51, 65, 85), outline=(100, 116, 139), width=2)
    d.rectangle([30, 340, 460, 385], fill=(71, 85, 105))  # concrete floor

    # Wooden Euro Pallet base
    d.rectangle([90, 315, 400, 340], fill=(180, 83, 9), outline=(120, 53, 15), width=2)
    d.text((195, 322), "EUR EPAL PALLET", fill=(255, 255, 255))

    # Bottom crushed box + leaking puddle
    d.polygon([(95, 315), (395, 315), (410, 235), (115, 245)], fill=(217, 119, 6), outline=(239, 68, 68), width=3)
    d.text((130, 268), "CRUSHED CARTON / LEAKING DRUM", fill=(255, 255, 255))
    d.text((130, 290), "STRETCH FILM TORN - LEANING 18 DEG", fill=(254, 202, 202))
    d.ellipse([320, 342, 445, 378], fill=(220, 38, 38))
    d.text((335, 354), "CHEMICAL SPILL!", fill=(255, 255, 255))

    # Upper carton with big red ADR Class 3 Flammable Diamond
    d.rectangle([115, 100, 385, 235], fill=(202, 138, 4), outline=(250, 204, 21), width=2)
    # Red diamond
    d.polygon([(250, 110), (325, 168), (250, 225), (175, 168)], fill=(220, 38, 38), outline=(255, 255, 255), width=3)
    d.text((205, 152), "ADR CLASS 3", fill=(255, 255, 255))
    d.text((200, 172), "UN 1263 FLAMMABLE", fill=(255, 255, 255))

    # Right panel: WMS Rule Summary
    d.rectangle([480, 70, 735, 385], fill=(15, 23, 42), outline=(71, 85, 105), width=2)
    d.text((498, 88), "WMS PUTAWAY POLICY:", fill=(56, 189, 248))
    d.text((498, 118), "1. Undeclared ADR / Hazmat", fill=(248, 250, 252))
    d.text((498, 138), "   -> Isolate in HAZMAT BUNKER", fill=(250, 204, 21))
    d.text((498, 170), "2. Chemical Spill / Crushed", fill=(248, 250, 252))
    d.text((498, 190), "   -> Trigger Spill Containment", fill=(248, 113, 113))
    d.text((498, 210), "   -> Do NOT put on high rack!", fill=(248, 113, 113))
    d.text((498, 250), "3. Declared vs Actual:", fill=(248, 250, 252))
    d.text((498, 272), "   ASN says Non-Hazardous,", fill=(203, 213, 225))
    d.text((498, 292), "   Visual shows UN 1263 Class 3!", fill=(239, 68, 68))

    # Bottom WMS Terminal Buttons
    d.rectangle([30, 405, 250, 462], fill=(22, 163, 74))
    d.text((48, 428), "[A] STANDARD RACK PUTAWAY", fill=(255, 255, 255))

    d.rectangle([270, 405, 510, 462], fill=(220, 38, 38))
    d.text((285, 428), "[B] HAZMAT QUARANTINE & SPILL TEAM", fill=(255, 255, 255))

    d.rectangle([530, 405, 735, 462], fill=(37, 99, 235))
    d.text((550, 428), "[C] COLD STORAGE (-18C)", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_mobile_load_board_ui_image(path: Path) -> None:
    """Mobile Freight Exchange (Mobil Yük Borsası) screen comparing Load Requirements vs Carrier Bid."""
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Top Mobile App Header
    d.rectangle([20, 15, 740, 68], fill=(30, 41, 59), outline=(56, 189, 248))
    d.text((40, 34), "SENDICOM MOBIL YUK BORSASI  |  AKILLI ESLESTIRME & TEKLIF KALKANI", fill=(56, 189, 248))
    d.text((545, 34), "Ilan: #YUK-2026-551", fill=(255, 255, 255))

    # Left Card: Shipper Load Requirement (Yük İlanı Şartları)
    d.rectangle([20, 82, 370, 380], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    d.rectangle([20, 82, 370, 120], fill=(37, 99, 235))
    d.text((38, 95), "YUK VEREN ILAN SARTLARI (SHIPPER)", fill=(255, 255, 255))

    d.text((38, 138), "Rota       : Antalya -> Berlin (2,450 km)", fill=(248, 250, 252))
    d.text((38, 166), "Yuk Cinsi  : Donuk Deniz Urunleri (18 Ton)", fill=(248, 250, 252))
    d.text((38, 194), "Zorunlu Tip: FRIGO DORSE (-18°C Sabit)", fill=(56, 189, 248))
    d.text((38, 222), "Emtia Deger: 4,200,000 TL (Yuksek Deger)", fill=(250, 204, 21))
    d.text((38, 250), "Min Sigorta: En az 5,000,000 TL CMR/Emtia", fill=(250, 204, 21))
    d.text((38, 278), "ADR Durumu : Yok (Gida Soguk Zincir)", fill=(203, 213, 225))
    d.text((38, 306), "Hedef Navlun: 3,400 EUR", fill=(34, 197, 94))

    # Right Card: Incoming Carrier Bid (Taşıyıcı Teklifi)
    d.rectangle([390, 82, 740, 380], fill=(30, 41, 59), outline=(220, 38, 38), width=2)
    d.rectangle([390, 82, 740, 120], fill=(185, 28, 28))
    d.text((408, 95), "GELEN TASIYICI TEKLIFI (CARRIER BID)", fill=(255, 255, 255))

    d.text((408, 138), "Tasiyici   : Kuzey Lojistik (Puan: 4.1 / 5)", fill=(248, 250, 252))
    d.text((408, 166), "Teklif     : 3,150 EUR (Ucuz Teklif)", fill=(34, 197, 94))
    d.rectangle([402, 188, 728, 216], fill=(127, 29, 29))
    d.text((408, 196), "Arac Tipi  : STANDART TENTELI (FRIGO YOK!)", fill=(254, 202, 202))
    d.rectangle([402, 220, 728, 248], fill=(127, 29, 29))
    d.text((408, 228), "Sigorta Lim: 1,000,000 TL (YETERSIZ LIMIT!)", fill=(254, 202, 202))
    d.text((408, 260), "GPS Konum  : Antalya Hal (Dogrulandi)", fill=(203, 213, 225))
    d.text((408, 288), "Sürücü Notu: 'Abi tenteli aracla gece serin", fill=(250, 204, 21))
    d.text((408, 308), "              gideriz bir sey olmaz hemen saralim'", fill=(250, 204, 21))

    # Action Buttons
    d.rectangle([20, 400, 245, 460], fill=(22, 163, 74))
    d.text((38, 424), "[1] TEKLIFI ONAYLA (ESLESME)", fill=(255, 255, 255))

    d.rectangle([265, 400, 515, 460], fill=(220, 38, 38))
    d.text((280, 424), "[2] REDDET (FRIGO & SIGORTA UYUMSUZ)", fill=(255, 255, 255))

    d.rectangle([535, 400, 740, 460], fill=(37, 99, 235))
    d.text((552, 424), "[3] SADECE FIYAT PAZARLIGI", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_cold_chain_telemetry_image(path: Path) -> None:
    """Reefer truck cold-chain temperature breach chart (-18C target spiking to +4.5C)."""
    img = Image.new("RGB", (760, 460), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    d.text((30, 20), "FRIGO DORSE IOT SENSOR TELEMETRISI  |  PLAKA: 34 FRG 404  |  YUK: DONUK ASI & GIDA", fill=(248, 250, 252))
    d.text((30, 44), "Zorunlu Sicaklik Araligi: -20°C ile -15°C arasi  |  Kritik Bozulma Esigi: > -5°C", fill=(56, 189, 248))

    cx0, cy0, cx1, cy1 = 80, 80, 715, 355
    d.rectangle([cx0, cy0, cx1, cy1], fill=(30, 41, 59), outline=(71, 85, 105))

    # Y-axis temperature lines
    levels = [
        (0.10, "+5°C (BOZULMA!)", (239, 68, 68)),
        (0.35, "-5°C (KRITIK ESIK)", (245, 158, 11)),
        (0.60, "-15°C (UST LIMIT)", (56, 189, 248)),
        (0.75, "-18°C (HEDEF)", (34, 197, 94)),
        (0.90, "-22°C", (71, 85, 105)),
    ]
    for pct, label, col in levels:
        y = int(cy0 + pct * (cy1 - cy0))
        d.line([cx0, y, cx1, y], fill=col, width=1)
        d.text((10, y - 6), label, fill=col)

    # Event marker: Compressor failure + Door left open at 03:15
    evt_x = 370
    d.line([evt_x, cy0, evt_x, cy1], fill=(250, 204, 21), width=2)
    d.rectangle([evt_x - 95, cy0 + 8, evt_x + 115, cy0 + 32], fill=(250, 204, 21))
    d.text((evt_x - 88, cy0 + 14), "03:15 KOMPRESOR ARIZASI!", fill=(15, 23, 42))

    # Temperature curve
    pts = [
        (95, 286), (160, 284), (225, 288), (290, 285), (370, 286),
        (420, 210), (475, 155), (535, 118), (600, 108), (685, 104)
    ]
    d.line(pts, fill=(248, 113, 113), width=4)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(248, 113, 113))

    # Alert box
    d.rectangle([485, 125, 700, 195], fill=(127, 29, 29), outline=(248, 113, 113), width=2)
    d.text((498, 135), "ALARM: DORSE SICAKLIGI +4.5°C!", fill=(255, 255, 255))
    d.text((498, 155), "Sure: 95 Dakikadir > -5°C uzerinde", fill=(254, 202, 202))
    d.text((498, 175), "En Yakin Soguk Depo: 18 km (Bolu)", fill=(250, 204, 21))

    d.rectangle([30, 395, 730, 442], fill=(30, 41, 59))
    d.text((45, 412), "Soguk Zincir Protokolu: Sicaklik > -5°C'yi 30 dk asarsa surucuyu en yakin soguk depoya yonlendir.", fill=(248, 250, 252))

    img.save(path, format="PNG")


def ensure_sample_images() -> list[str]:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "logistics_pod_waybill.png": create_logistics_pod_waybill_image,
        "warehouse_damaged_pallet.png": create_warehouse_damaged_pallet_image,
        "mobile_load_board_ui.png": create_mobile_load_board_ui_image,
        "cold_chain_telemetry.png": create_cold_chain_telemetry_image,
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
