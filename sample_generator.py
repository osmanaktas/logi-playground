"""
Generates synthetic visual test images for Nace.AI Drex Max & Drex Max Finance multimodal decision testing.
Includes 11 visual scenarios across:
- Drex Max Finance (3-Way Matching e-Fatura/Kantar, Demurrage & Tampered Toll/Fuel Receipt, Carrier/Shipper Credit & Factoring Card)
- Logistics, Warehouse (WMS) & Mobile Freight Exchange (POD Waybill, Damaged ADR Pallet, Load Board Matching UI, Cold-Chain IoT Chart)
- General Enterprise (Cloud Invoice, Browser 504 Error, Server Telemetry, Moderation Card)
"""

from pathlib import Path
from PIL import Image, ImageDraw

SAMPLES_DIR = Path(__file__).parent / "samples"


def create_finance_3way_matching_image(path: Path) -> None:
    """Visual scan showing side-by-side e-Fatura + Weighbridge (Kantar) & WMS Receiving Slip for 3-Way Matching."""
    img = Image.new("RGB", (760, 480), color=(241, 245, 249))
    d = ImageDraw.Draw(img)

    # Top Header
    d.rectangle([15, 12, 745, 62], fill=(15, 23, 42))
    d.text((30, 22), "WMS 3-WAY MATCHING (UCLU ESLESTIRME)  |  PO #PO-2026-4401 vs IRSALIYE vs e-FATURA", fill=(56, 189, 248))
    d.text((30, 42), "Model: nace-ai/drex-max-finance  |  Tolerans Kurali: Fiyat Farki <= %2.0, Miktar = WMS Sayimi", fill=(203, 213, 225))

    # Left Document: Supplier e-Invoice (Tedarikçi e-Faturası)
    d.rectangle([15, 74, 375, 390], fill=(255, 255, 255), outline=(220, 38, 38), width=2)
    d.rectangle([15, 74, 375, 110], fill=(185, 28, 28))
    d.text((28, 86), "TEDARIKCI e-FATURA #GIB202600091882", fill=(255, 255, 255))

    d.text((28, 124), "Tedarikci  : Toros Ambalaj & Palet San. A.S.", fill=(15, 23, 42))
    d.text((28, 148), "Ref PO No  : #PO-2026-4401", fill=(15, 23, 42))
    d.line([25, 170, 365, 170], fill=(203, 213, 225), width=1)

    d.text((28, 182), "Faturalanan Miktar : 1,000 Adet Euro Palet", fill=(185, 28, 28))
    d.text((28, 206), "Fatura Birim Fiyat : 465.00 TL / Adet (+%16.2!)", fill=(185, 28, 28))
    d.text((28, 230), "Beyan Tonaj        : 22,000 kg", fill=(15, 23, 42))
    d.text((28, 254), "Ara Toplam         : 465,000.00 TL", fill=(15, 23, 42))
    d.text((28, 278), "KDV (%20)          :  93,000.00 TL", fill=(15, 23, 42))
    d.rectangle([25, 298, 365, 326], fill=(254, 242, 242))
    d.text((32, 306), "KDV Tevkifati      : 0.00 TL (TEVKIFAT EKSİK!)", fill=(185, 28, 28))
    d.rectangle([25, 336, 365, 374], fill=(254, 226, 226))
    d.text((32, 349), "GENEL TOPLAM       : 558,000.00 TL", fill=(153, 27, 27))

    # Right Document: Purchase Order + WMS Receiving & Weighbridge Slip
    d.rectangle([390, 74, 745, 390], fill=(255, 255, 255), outline=(37, 99, 235), width=2)
    d.rectangle([390, 74, 745, 110], fill=(30, 58, 138))
    d.text((405, 86), "ONAYLI PO + WMS MAL KABUL & KANTAR FISI", fill=(255, 255, 255))

    d.text((405, 124), "1. SATINALMA SIPARISI (#PO-2026-4401):", fill=(30, 58, 138))
    d.text((405, 146), "   - Siparis Adedi     : 1,000 Adet", fill=(15, 23, 42))
    d.text((405, 166), "   - Sozlesme B. Fiyat : 400.00 TL (Max %2 Tol.)", fill=(22, 101, 52))
    d.text((405, 186), "   - Zorunlu Tevkifat  : 2/10 KDV Tevkifati", fill=(22, 101, 52))

    d.line([400, 208, 735, 208], fill=(203, 213, 225), width=1)
    d.text((405, 220), "2. WMS RAMPA MAL KABUL & KANTAR (#KNT-881):", fill=(30, 58, 138))
    d.rectangle([400, 242, 735, 294], fill=(254, 249, 195), outline=(234, 179, 8))
    d.text((412, 250), "WMS Fiili Sayim : 850 Adet Saglam (150 EKSIK!)", fill=(180, 83, 9))
    d.text((412, 272), "Kantar Net Tartim: 18,700 kg (Faturadan -3.3t az)", fill=(180, 83, 9))

    d.text((405, 310), "3. MUHASEBE UYUSMAZLIK OZETI:", fill=(185, 28, 28))
    d.text((405, 332), "   - 150 Adet eksik teslimata ragmen tam fatura!", fill=(185, 28, 28))
    d.text((405, 352), "   - Birim fiyat 400 TL yerine 465 TL (+%16.25)!", fill=(185, 28, 28))

    # ERP Action Bar
    d.rectangle([15, 405, 245, 464], fill=(22, 163, 74))
    d.text((32, 428), "[1] SAP ERP OTOMATIK ONAYLA", fill=(255, 255, 255))

    d.rectangle([260, 405, 515, 464], fill=(220, 38, 38))
    d.text((275, 428), "[2] BLOKE ET & FIYAT/MIKTAR FARK FATURASI", fill=(255, 255, 255))

    d.rectangle([530, 405, 745, 464], fill=(217, 119, 6))
    d.text((545, 428), "[3] GRI ALAN -> UZMAN MUHASEBE", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_finance_demurrage_receipt_fraud_image(path: Path) -> None:
    """Visual scan of Carrier Demurrage (Bekleme) & Toll/Weighbridge receipt showing plate/date tampering."""
    img = Image.new("RGB", (760, 480), color=(241, 245, 249))
    d = ImageDraw.Draw(img)

    d.rectangle([15, 12, 745, 62], fill=(15, 23, 42))
    d.text((30, 22), "NAVLUN HAK EDIS & EK GIDER (DEMURAJ / KANTAR FISI) SAHTECILIK DENETIMI", fill=(250, 204, 21))
    d.text((30, 42), "Model: nace-ai/drex-max-finance  |  Sefer: #TRIP-2026-772  |  Aktif Plaka: 34 ABC 901", fill=(203, 213, 225))

    # Left: Uploaded Toll & Weighbridge Receipt with Tampered Plate & Old Date
    d.rectangle([15, 75, 375, 390], fill=(255, 255, 255), outline=(220, 38, 38), width=2)
    d.rectangle([15, 75, 375, 110], fill=(185, 28, 28))
    d.text((28, 87), "YUKLENEN KANTAR & OTOYOL DEKONTU (SUPHELI)", fill=(255, 255, 255))

    d.text((28, 128), "Belge No        : #FIS-2025-11049 (GECMIS YIL!)", fill=(185, 28, 28))
    d.rectangle([25, 150, 365, 180], fill=(254, 242, 242))
    d.text((32, 159), "Fis Tarihi      : 14.08.2025 (SEFER: 10.11.2026!)", fill=(185, 28, 28))
    d.rectangle([25, 186, 365, 216], fill=(254, 242, 242))
    d.text((32, 195), "Fisteki Plaka   : 06 XYZ 44 (ÜZERİ ÇİZİLİP YAZILMIŞ)", fill=(185, 28, 28))
    d.text((28, 230), "Talep Edilen    : 6,500 TL Demuraj + 2,800 TL Gecis", fill=(15, 23, 42))
    d.text((28, 256), "Belge Hash Kontrol: DAHA ONCE #TRIP-2025-109'DA", fill=(185, 28, 28))
    d.text((28, 276), "                    KULLANILMIS MUKERRER DEKONT!", fill=(185, 28, 28))

    d.rectangle([25, 305, 365, 372], fill=(254, 249, 195), outline=(234, 179, 8))
    d.text((35, 316), "Gorsel Adli Analiz (Forensic Check):", fill=(146, 64, 14))
    d.text((35, 336), "- Tutar hanesinde farkli font / piksel oynama var", fill=(146, 64, 14))
    d.text((35, 354), "- GPS kaydina gore arac bekleme suresi sadece 45 dk", fill=(146, 64, 14))

    # Right: Contract & GPS Telemetry Ground Truth
    d.rectangle([390, 75, 745, 390], fill=(255, 255, 255), outline=(71, 85, 105), width=2)
    d.rectangle([390, 75, 745, 110], fill=(30, 41, 59))
    d.text((405, 87), "TASIMA SOZLESMESI & GPS GERCEK VERISI", fill=(255, 255, 255))

    d.text((405, 128), "Sefer ID        : #TRIP-2026-772", fill=(15, 23, 42))
    d.text((405, 152), "Sozlesme Plakasi: 34 ABC 901", fill=(22, 101, 52))
    d.text((405, 176), "Sefer Tarihi    : 10.11.2026", fill=(22, 101, 52))
    d.text((405, 200), "Ana Navlun      : 32,000.00 TL (POD Imzali-Temiz)", fill=(22, 101, 52))
    d.line([400, 222, 735, 222], fill=(203, 213, 225))
    d.text((405, 236), "DEMURAJ (BEKLEME) SOZLESME KURALI:", fill=(30, 58, 138))
    d.text((405, 258), "- Ilk 4 saat (240 dk) bekleme ucretsizdir.", fill=(15, 23, 42))
    d.text((405, 280), "- GPS Giris: 10:00 | Cikis: 10:45 (Toplam: 45 dk!)", fill=(185, 28, 28))
    d.text((405, 304), "- Sonuc: Demuraj hakki DOĞMAMIŞTIR (0 TL).", fill=(185, 28, 28))
    d.text((405, 334), "- Sahte/Eski fis yukleme -> Fraud Inceleme Kuyrugu", fill=(185, 28, 28))

    # Action Buttons
    d.rectangle([15, 405, 245, 464], fill=(22, 163, 74))
    d.text((30, 428), "[1] TUM TALEBI ODE (41,300 TL)", fill=(255, 255, 255))

    d.rectangle([260, 405, 515, 464], fill=(220, 38, 38))
    d.text((272, 428), "[2] EK GIDERI REDDET & FRAUD BAYRAGI", fill=(255, 255, 255))

    d.rectangle([530, 405, 745, 464], fill=(37, 99, 235))
    d.text((545, 428), "[3] SADECE ANA NAVLUNU ODE", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_finance_credit_balance_sheet_image(path: Path) -> None:
    """Visual Financial Summary & Findeks/Credit Risk Card for Shipper Open-Account & Carrier Factoring."""
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    d.rectangle([15, 12, 745, 62], fill=(30, 41, 59), outline=(56, 189, 248))
    d.text((30, 22), "VADELI YUK VEREN (ACIK HESAP) & FAKTORING RISK SKORLAMA KARTI", fill=(56, 189, 248))
    d.text((30, 42), "Model: nace-ai/drex-max-finance  |  Basvuru: 60 Gun Vadeli 3,500,000 TL Acik Hesap Limiti", fill=(203, 213, 225))

    # Left: Financial Statements & Balance Sheet Ratios
    d.rectangle([15, 75, 375, 390], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    d.rectangle([15, 75, 375, 110], fill=(37, 99, 235))
    d.text((28, 87), "BILANCO, VERGI LEVHASI & FINANSAL RASYOLAR", fill=(255, 255, 255))

    d.text((28, 126), "Firma Unvani   : Delta Ic ve Dis Ticaret Ltd.", fill=(248, 250, 252))
    d.text((28, 150), "Kurulus Tarihi : 4 Ay Once (Yeni Kurulmus Firma)", fill=(250, 204, 21))
    d.text((28, 174), "Yillik Ciro    : 8,200,000 TL", fill=(248, 250, 252))
    d.text((28, 198), "Ozkaynaklar    :   450,000 TL (Dusuk Sermaye)", fill=(248, 113, 113))
    d.text((28, 222), "Kisa V. Borclar: 6,800,000 TL", fill=(248, 113, 113))
    d.rectangle([25, 244, 365, 274], fill=(127, 29, 29))
    d.text((32, 253), "Cari Oran      : 0.68 (Politika Alt Siniri >= 1.20!)", fill=(254, 202, 202))
    d.rectangle([25, 280, 365, 310], fill=(127, 29, 29))
    d.text((32, 289), "Talep / Ciro   : %42.6 (Politika Tavani Max %10!)", fill=(254, 202, 202))
    d.text((28, 326), "Teminat Mektubu: YOK (Teminatsiz Acik Hesap)", fill=(250, 204, 21))

    # Right: Findeks, Check & Payment History
    d.rectangle([390, 75, 745, 390], fill=(30, 41, 59), outline=(220, 38, 38), width=2)
    d.rectangle([390, 75, 745, 110], fill=(185, 28, 28))
    d.text((405, 87), "FINDEKS CEK / SENET & ODEME PERFORMANSI", fill=(255, 255, 255))

    d.text((405, 126), "Kurumsal Kredi Notu : 840 / 1900 (YUKSEK RISK)", fill=(248, 113, 113))
    d.rectangle([400, 148, 735, 182], fill=(127, 29, 29))
    d.text((410, 159), "Son 6 Ay Karsiliksiz Cek : 3 Adet (Toplam 920,000 TL)", fill=(255, 255, 255))
    d.text((405, 196), "Protestolu Senet    : 2 Adet (Aktif İcra Takibi Var)", fill=(248, 113, 113))
    d.text((405, 222), "Ortalama Gecikme    : +48 Gun Vade Asimi", fill=(250, 204, 21))

    d.line([400, 246, 735, 246], fill=(71, 85, 105))
    d.text((405, 260), "KREDI KOMITESI POLITIKA KURALI (#CRP-09):", fill=(56, 189, 248))
    d.text((405, 284), "1. Karsiliksiz cek veya Cari Oran < 1.0 olan firmaya", fill=(203, 213, 225))
    d.text((405, 304), "   teminatsiz vadeli acik hesap KESINLIKLE acilamaz.", fill=(203, 213, 225))
    d.text((405, 326), "2. Sadece Pesin/Escrow veya Kesin Banka Teminat", fill=(34, 197, 94))
    d.text((405, 346), "   Mektubu ile yuk ilani acmasina izin verilir.", fill=(34, 197, 94))

    # Action Buttons
    d.rectangle([15, 405, 245, 464], fill=(22, 163, 74))
    d.text((28, 428), "[1] 3.5M TL ACIK HESAP ONAYLA", fill=(255, 255, 255))

    d.rectangle([260, 405, 515, 464], fill=(220, 38, 38))
    d.text((272, 428), "[2] VADELI REDDET (PESIN / ESCROW ZORUNLU)", fill=(255, 255, 255))

    d.rectangle([530, 405, 745, 464], fill=(37, 99, 235))
    d.text((542, 428), "[3] BANKA TEMINAT MEKTUBU ISTE", fill=(255, 255, 255))

    img.save(path, format="PNG")


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
    img = Image.new("RGB", (760, 480), color=(241, 245, 249))
    d = ImageDraw.Draw(img)

    d.rectangle([25, 18, 735, 385], fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    d.rectangle([25, 18, 735, 76], fill=(30, 58, 138))
    d.text((45, 30), "SEVK IRSALIYESI / PROOF OF DELIVERY (POD)  |  BELGE NO: #IRS-2026-90412", fill=(255, 255, 255))
    d.text((45, 52), "Gonderici: Marmara Gida A.S. (Gebze Depo)  ->  Alici: Anadolu Perakende Dagitim (Ankara)", fill=(191, 219, 254))

    d.text((45, 92), "Plaka / Dorse : 34 TRK 882 / 34 DRS 19", fill=(15, 23, 42))
    d.text((420, 92), "Yuk Borsasi Ilan ID : #LOAD-77419", fill=(15, 23, 42))
    d.text((45, 116), "Sevk Edilen   : 24 Euro Palet (Endustriyel Zeytinyagi Tenekeleri)", fill=(15, 23, 42))
    d.text((420, 116), "Hak Edis (Escrow)   : 48,500.00 TL", fill=(22, 101, 52))
    d.line([40, 140, 720, 140], fill=(203, 213, 225), width=2)

    d.text((45, 152), "KALEM", fill=(71, 85, 105))
    d.text((310, 152), "SEVK ADEDI", fill=(71, 85, 105))
    d.text((450, 152), "TESLIM ALINAN", fill=(71, 85, 105))
    d.text((590, 152), "DURUM", fill=(71, 85, 105))

    d.text((45, 178), "Euro Palet - 5L Zeytinyagi Kolisi", fill=(15, 23, 42))
    d.text((325, 178), "24 Palet", fill=(15, 23, 42))
    d.text((465, 178), "21 Palet Saglam", fill=(15, 23, 42))
    d.text((590, 178), "3 PALET HASARLI!", fill=(220, 38, 38))

    d.rectangle([45, 212, 475, 365], fill=(254, 242, 242), outline=(220, 38, 38), width=2)
    d.text((60, 224), "ALICI DEPO TESLIMAT SERHI (DAMAGE RESERVATION NOTE):", fill=(185, 28, 28))
    d.text((60, 250), "- Rampa kabulde 3 paletin devrilmis ve tenekelerin", fill=(153, 27, 27))
    d.text((60, 272), "  delinmis oldugu tespit edildi (yag sizintisi mevcut).", fill=(153, 27, 27))
    d.text((60, 298), "- 3 Palet (Hasar Tutari: ~14,200 TL) TUTANAKLA IADE", fill=(185, 28, 28))
    d.text((60, 320), "  EDILDI. Sadece 21 palet teslim alinmistir.", fill=(185, 28, 28))
    d.text((60, 342), "- Hasar fotograflari WMS sistemine eklendi.", fill=(100, 116, 139))

    d.rectangle([495, 212, 715, 365], fill=(248, 250, 252), outline=(37, 99, 235), width=2)
    d.text((515, 224), "ALICI DEPO KASE & ISLAK IMZA", fill=(30, 58, 138))
    d.ellipse([530, 252, 680, 332], outline=(37, 99, 235), width=2)
    d.text((552, 275), "ANADOLU DEPO", fill=(37, 99, 235))
    d.text((545, 295), "TESLIM ALINDI - IMZA", fill=(37, 99, 235))
    d.text((515, 342), "Imza: [M. Demir - Rampa Sefi]", fill=(15, 23, 42))

    d.rectangle([25, 398, 245, 460], fill=(22, 163, 74))
    d.text((42, 422), "[1] TAM ODEMEYI SERBEST BIRAK", fill=(255, 255, 255))

    d.rectangle([265, 398, 515, 460], fill=(217, 119, 6))
    d.text((280, 422), "[2] ESCROW BLOKE & HASAR DOSYASI", fill=(255, 255, 255))

    d.rectangle([535, 398, 735, 460], fill=(71, 85, 105))
    d.text((552, 422), "[3] BELGE OKUNAKSIZ (RED)", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_warehouse_damaged_pallet_image(path: Path) -> None:
    img = Image.new("RGB", (760, 480), color=(30, 41, 59))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 760, 54], fill=(15, 23, 42))
    d.text((20, 12), "WMS DOCK CAMERA #04 (INBOUND GATE B)  |  SCAN: PALLET-ID #PLT-99204", fill=(56, 189, 248))
    d.text((20, 32), "ASN Manifest: Declared as 'Standard Dry Goods (Non-Hazardous)'  |  Weight: 640 kg", fill=(203, 213, 225))

    d.rectangle([30, 70, 460, 385], fill=(51, 65, 85), outline=(100, 116, 139), width=2)
    d.rectangle([30, 340, 460, 385], fill=(71, 85, 105))

    d.rectangle([90, 315, 400, 340], fill=(180, 83, 9), outline=(120, 53, 15), width=2)
    d.text((195, 322), "EUR EPAL PALLET", fill=(255, 255, 255))

    d.polygon([(95, 315), (395, 315), (410, 235), (115, 245)], fill=(217, 119, 6), outline=(239, 68, 68), width=3)
    d.text((130, 268), "CRUSHED CARTON / LEAKING DRUM", fill=(255, 255, 255))
    d.text((130, 290), "STRETCH FILM TORN - LEANING 18 DEG", fill=(254, 202, 202))
    d.ellipse([320, 342, 445, 378], fill=(220, 38, 38))
    d.text((335, 354), "CHEMICAL SPILL!", fill=(255, 255, 255))

    d.rectangle([115, 100, 385, 235], fill=(202, 138, 4), outline=(250, 204, 21), width=2)
    d.polygon([(250, 110), (325, 168), (250, 225), (175, 168)], fill=(220, 38, 38), outline=(255, 255, 255), width=3)
    d.text((205, 152), "ADR CLASS 3", fill=(255, 255, 255))
    d.text((200, 172), "UN 1263 FLAMMABLE", fill=(255, 255, 255))

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

    d.rectangle([30, 405, 250, 462], fill=(22, 163, 74))
    d.text((48, 428), "[A] STANDARD RACK PUTAWAY", fill=(255, 255, 255))

    d.rectangle([270, 405, 510, 462], fill=(220, 38, 38))
    d.text((285, 428), "[B] HAZMAT QUARANTINE & SPILL TEAM", fill=(255, 255, 255))

    d.rectangle([530, 405, 735, 462], fill=(37, 99, 235))
    d.text((550, 428), "[C] COLD STORAGE (-18C)", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_mobile_load_board_ui_image(path: Path) -> None:
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    d.rectangle([20, 15, 740, 68], fill=(30, 41, 59), outline=(56, 189, 248))
    d.text((40, 34), "SENDICOM MOBIL YUK BORSASI  |  AKILLI ESLESTIRME & TEKLIF KALKANI", fill=(56, 189, 248))
    d.text((545, 34), "Ilan: #YUK-2026-551", fill=(255, 255, 255))

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

    d.rectangle([20, 400, 245, 460], fill=(22, 163, 74))
    d.text((38, 424), "[1] TEKLIFI ONAYLA (ESLESME)", fill=(255, 255, 255))

    d.rectangle([265, 400, 515, 460], fill=(220, 38, 38))
    d.text((280, 424), "[2] REDDET (FRIGO & SIGORTA UYUMSUZ)", fill=(255, 255, 255))

    d.rectangle([535, 400, 740, 460], fill=(37, 99, 235))
    d.text((552, 424), "[3] SADECE FIYAT PAZARLIGI", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_cold_chain_telemetry_image(path: Path) -> None:
    img = Image.new("RGB", (760, 460), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    d.text((30, 20), "FRIGO DORSE IOT SENSOR TELEMETRISI  |  PLAKA: 34 FRG 404  |  YUK: DONUK ASI & GIDA", fill=(248, 250, 252))
    d.text((30, 44), "Zorunlu Sicaklik Araligi: -20°C ile -15°C arasi  |  Kritik Bozulma Esigi: > -5°C", fill=(56, 189, 248))

    cx0, cy0, cx1, cy1 = 80, 80, 715, 355
    d.rectangle([cx0, cy0, cx1, cy1], fill=(30, 41, 59), outline=(71, 85, 105))

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

    evt_x = 370
    d.line([evt_x, cy0, evt_x, cy1], fill=(250, 204, 21), width=2)
    d.rectangle([evt_x - 95, cy0 + 8, evt_x + 115, cy0 + 32], fill=(250, 204, 21))
    d.text((evt_x - 88, cy0 + 14), "03:15 KOMPRESOR ARIZASI!", fill=(15, 23, 42))

    pts = [
        (95, 286), (160, 284), (225, 288), (290, 285), (370, 286),
        (420, 210), (475, 155), (535, 118), (600, 108), (685, 104)
    ]
    d.line(pts, fill=(248, 113, 113), width=4)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(248, 113, 113))

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
        "finance_3way_matching.png": create_finance_3way_matching_image,
        "finance_demurrage_receipt_fraud.png": create_finance_demurrage_receipt_fraud_image,
        "finance_credit_balance_sheet.png": create_finance_credit_balance_sheet_image,
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
