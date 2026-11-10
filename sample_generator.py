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


def create_omnichannel_bundle_image(path: Path) -> None:
    """Omnichannel document ingestion image: WhatsApp Driver Chat + Email Attachment + Mobile App Duplicate Check."""
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Top Header
    d.rectangle([15, 12, 745, 62], fill=(30, 41, 59), outline=(56, 189, 248))
    d.text((28, 22), "OMNICHANNEL BELGE GIRIS MERKEZI (WHATSAPP + E-POSTA + MOBIL UYGULAMA)", fill=(56, 189, 248))
    d.text((28, 42), "Hedef: Normal LLM ile .md cikarmadan once Tekillestirme (Dedup) + 12 Soruluk Siniflandirma", fill=(203, 213, 225))

    # Column 1: WhatsApp Incoming Message & Forwarded Photo
    d.rectangle([15, 74, 252, 392], fill=(20, 83, 45), outline=(34, 197, 94), width=2)
    d.rectangle([15, 74, 252, 108], fill=(22, 101, 52))
    d.text((26, 85), "1. WHATSAPP (+90 532 ... 88)", fill=(255, 255, 255))

    d.rectangle([25, 118, 242, 235], fill=(255, 255, 255))
    d.text((32, 126), "[FOTO: SEVK IRSALIYESI]", fill=(30, 58, 138))
    d.text((32, 146), "Belge No: #IRS-2026-90412", fill=(185, 28, 28))
    d.text((32, 166), "Plaka   : 34 TRK 882", fill=(15, 23, 42))
    d.text((32, 186), "Alici   : Anadolu Depo (Imzali)", fill=(22, 101, 52))
    d.text((32, 206), "Not     : 3 Palet Hasarli Serhi!", fill=(220, 38, 38))

    d.rectangle([25, 245, 242, 378], fill=(220, 252, 231))
    d.text((32, 255), "Surucu WhatsApp Mesaji:", fill=(20, 83, 45))
    d.text((32, 275), "'Abi teslim evrakini WhatsApp'tan", fill=(15, 23, 42))
    d.text((32, 293), "da atiyorum garanti olsun.", fill=(15, 23, 42))
    d.text((32, 311), "Aksam 18:00'e kadar 48.500 TL", fill=(15, 23, 42))
    d.text((32, 329), "hak edisi cikaralim lutfen.'", fill=(15, 23, 42))
    d.text((32, 355), "Saat: 14:22 | Kanal: WhatsApp API", fill=(71, 85, 105))

    # Column 2: Incoming Email Attachment
    d.rectangle([262, 74, 498, 392], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    d.rectangle([262, 74, 498, 108], fill=(37, 99, 235))
    d.text((274, 85), "2. E-POSTA (operasyon@nakliye)", fill=(255, 255, 255))

    d.text((274, 122), "Konu: Sefer #LOAD-77419 Evraklari", fill=(248, 250, 252))
    d.text((274, 144), "Ek-1: irsaliye_90412_scan.jpg", fill=(56, 189, 248))
    d.text((274, 166), "      (Belge No: #IRS-2026-90412)", fill=(250, 204, 21))
    d.text((274, 190), "Ek-2: kantar_fisi_881.jpg", fill=(56, 189, 248))
    d.text((274, 212), "      (Net Tartim: 18,700 kg)", fill=(203, 213, 225))
    d.line([272, 236, 488, 236], fill=(71, 85, 105))
    d.text((274, 248), "E-Posta Govdesi:", fill=(148, 163, 184))
    d.text((274, 268), "'Merhabalar, 34 TRK 882 plakali", fill=(226, 232, 240))
    d.text((274, 286), "aracimizin Ankara teslimat", fill=(226, 232, 240))
    d.text((274, 304), "irsaliyesi (#IRS-2026-90412) ve", fill=(226, 232, 240))
    d.text((274, 322), "kantar fisi ektedir.'", fill=(226, 232, 240))
    d.text((274, 355), "Saat: 14:25 | Kanal: IMAP/SMTP", fill=(148, 163, 184))

    # Column 3: Existing Mobile App Database State & Deduplication Alert
    d.rectangle([508, 74, 745, 392], fill=(30, 41, 59), outline=(245, 158, 11), width=2)
    d.rectangle([508, 74, 745, 108], fill=(180, 83, 9))
    d.text((520, 85), "3. MEVCUT DB KAYDI (MOBIL APP)", fill=(255, 255, 255))

    d.text((520, 122), "Kayit ID  : DOC-CANON-90412", fill=(250, 204, 21))
    d.text((520, 144), "Yukleyen  : Mobil App (14:10'da)", fill=(248, 250, 252))
    d.text((520, 166), "Belge No  : #IRS-2026-90412", fill=(34, 197, 94))
    d.text((520, 188), "Plaka     : 34 TRK 882", fill=(248, 250, 252))
    d.text((520, 210), "Sefer ID  : #LOAD-77419", fill=(248, 250, 252))

    d.rectangle([518, 235, 735, 378], fill=(127, 29, 29), outline=(248, 113, 113))
    d.text((526, 246), "TEKİLLESTIRME (DEDUP) UYARISI:", fill=(255, 255, 255))
    d.text((526, 270), "- WhatsApp ve E-Posta'dan gelen", fill=(254, 202, 202))
    d.text((526, 288), "  #IRS-2026-90412 irsaliyesi", fill=(254, 202, 202))
    d.text((526, 306), "  14:10'da Mobil App'ten yuklenen", fill=(254, 202, 202))
    d.text((526, 324), "  belgenin MUKERRER kopyasidir!", fill=(250, 204, 21))
    d.text((526, 348), "- Sadece Ek-2 Kantar Fisi YENIDIR.", fill=(34, 197, 94))

    # Bottom Pipeline Decision Buttons
    d.rectangle([15, 405, 250, 464], fill=(220, 38, 38))
    d.text((26, 428), "[1] HEPSINI NORMAL LLM ILE .MD YAP", fill=(255, 255, 255))

    d.rectangle([262, 405, 515, 464], fill=(22, 163, 74))
    d.text((274, 428), "[2] IRSALIYEYI TEKILLESTIR + KANTARI ISLE", fill=(255, 255, 255))

    d.rectangle([528, 405, 745, 464], fill=(71, 85, 105))
    d.text((542, 428), "[3] SPAM OLARAK SIL", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_whatsapp_load_and_business_card_image(path: Path) -> None:
    """
    Generates a visual showing a Turkish WhatsApp logistics chat requesting a load
    (Gebze OSB -> Corlu, 22 Ton, 33 Euro Pallet, 13.60 Kayar Perde) alongside a photo
    of a Logistics Manager's Business Card (Kartvizit) to be added to CRM.
    """
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Top Banner
    d.rectangle([0, 0, 760, 58], fill=(6, 78, 59))
    d.text((20, 14), "WHATSAPP OPERASYON HATTI -> YUK ILANI OLUSTURMA & CRM KARTVIZIT KAYDI", fill=(255, 255, 255))
    d.text((20, 34), "Gonderen: +90 532 418 92 10 | Grup: Trakya-Marmara Tir & Yuk Borsasi", fill=(167, 243, 208))

    # Left Panel: WhatsApp Chat Conversation
    d.rectangle([16, 72, 375, 400], fill=(22, 33, 46), outline=(34, 197, 94), width=2)
    d.rectangle([16, 72, 375, 106], fill=(21, 128, 61))
    d.text((28, 83), "WHATSAPP YAZISMASI (YUK TALEBI)", fill=(255, 255, 255))

    # Incoming bubble 1
    d.rectangle([28, 118, 362, 248], fill=(220, 252, 231))
    d.text((36, 126), "Ahmet Yalcin (Trakya Tekstil) - 10:14", fill=(21, 128, 61))
    d.text((36, 146), "'Selamun aleykum sefim, yarin sabah", fill=(15, 23, 42))
    d.text((36, 164), "08:00 Gebze OSB'den Corlu Fabrika'ya", fill=(15, 23, 42))
    d.text((36, 182), "22 ton, 33 Euro Palet tekstil kolisi", fill=(15, 23, 42))
    d.text((36, 200), "var. 13.60 Tenteli Kayar Perde lazim.", fill=(185, 28, 28))
    d.text((36, 218), "Navlun: 18.000 TL + KDV pesin calisir.'", fill=(21, 128, 61))

    # Incoming bubble 2
    d.rectangle([28, 260, 362, 386], fill=(220, 252, 231))
    d.text((36, 268), "Ahmet Yalcin (Trakya Tekstil) - 10:15", fill=(21, 128, 61))
    d.text((36, 288), "'Bu arada yeni kartvizitimi de ekte", fill=(15, 23, 42))
    d.text((36, 306), "fotograf olarak attim, sizin CRM", fill=(15, 23, 42))
    d.text((36, 324), "sistemine musteri olarak acarsiniz.", fill=(15, 23, 42))
    d.text((36, 342), "Plaka belli olunca WhatsApp'tan atin.'", fill=(15, 23, 42))
    d.text((36, 364), "[EK: kartvizit_ahmet_yalcin.jpg]", fill=(30, 58, 138))

    # Right Panel: Business Card Photo (Kartvizit)
    d.rectangle([390, 72, 744, 400], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    d.rectangle([390, 72, 744, 106], fill=(3, 105, 161))
    d.text((404, 83), "WHATSAPP EKI: KARTVIZIT FOTOGRAFI (CRM)", fill=(255, 255, 255))

    # Business card visual inside right panel
    d.rectangle([408, 125, 726, 335], fill=(248, 250, 252), outline=(148, 163, 184), width=2)
    d.rectangle([408, 125, 422, 335], fill=(14, 116, 144))
    d.text((438, 140), "TRAKYA TEKSTIL SAN. VE TIC. A.S.", fill=(14, 116, 144))
    d.text((438, 160), "Uluslararasi Tekstil & Ihracat Lojistigi", fill=(100, 116, 139))
    d.line([438, 180, 710, 180], fill=(203, 213, 225), width=2)

    d.text((438, 192), "AHMET YALCIN", fill=(15, 23, 42))
    d.text((438, 212), "Lojistik ve Tedarik Zinciri Muduru", fill=(180, 83, 9))
    d.text((438, 240), "Mobil : +90 532 418 92 10", fill=(15, 23, 42))
    d.text((438, 258), "E-Mail: ayalcin@trakyatekstil.com.tr", fill=(30, 58, 138))
    d.text((438, 276), "Adres : Corlu 1. OSB Kuzey Cad. No:14 Tekirdag", fill=(51, 65, 85))
    d.text((438, 294), "Vergi : Corlu VD / VKN: 8590412881", fill=(185, 28, 28))

    d.text((408, 352), "CRM Durumu: Sistemde Kayitli Degil -> Yeni Musteri!", fill=(250, 204, 21))
    d.text((408, 372), "Yuk Borsasi: Gebze->Corlu 13.60 Tenteli Ilani Acilacak", fill=(34, 197, 94))

    # Bottom Action Bar
    d.rectangle([16, 412, 375, 466], fill=(22, 163, 74))
    d.text((28, 432), "[1] YUK ILANI AC + KARTVIZITI CRM'E KAYDET", fill=(255, 255, 255))

    d.rectangle([390, 412, 744, 466], fill=(71, 85, 105))
    d.text((406, 432), "[2] EKSIK BILGI SOR / BEKLEMEYE AL", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_whatsapp_cmr_and_warehouse_checklist_image(path: Path) -> None:
    """
    Generates a dual-panel visual:
    Left: International CMR Waybill (Turkey -> Russia / Moscow via Sarp / Verkhniy Lars) with Russian/Turkish notes.
    Right: Warehouse Receiving/Loading Checklist photo sent via WhatsApp (missing lashing straps / spanzet).
    """
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, 760, 58], fill=(30, 58, 138))
    d.text((20, 14), "ULUSLARARASI CMR BELGESI (TR-RU) & DEPO MAL KABUL / YUKLEME CHECKLIST", fill=(255, 255, 255))
    d.text((20, 34), "Sinir Kapisi: Sarp / Verkhniy Lars | Dil: Turkce <-> Rusca (DeepSeek V4.1 Flash + Drex Max)", fill=(147, 197, 253))

    # Left Panel: International CMR Document
    d.rectangle([16, 72, 375, 402], fill=(255, 255, 255), outline=(220, 38, 38), width=2)
    d.rectangle([16, 72, 375, 106], fill=(185, 28, 28))
    d.text((26, 83), "CMR - ULUSLARARASI TASIMA SENEDI (#TR-RU-88412)", fill=(255, 255, 255))

    d.text((26, 116), "1. Gonderici : Antalya Sera Ihracat A.S. (Turkiye)", fill=(15, 23, 42))
    d.text((26, 136), "2. Alici     : OOO Moskva Agro Trade (Moskova / RF)", fill=(15, 23, 42))
    d.text((26, 156), "3. Bosaltma  : Moskova Food City Terminal #4", fill=(15, 23, 42))
    d.text((26, 176), "6-9. Yuk     : 26 Palet Taze Narenciye (21.400 kg)", fill=(21, 128, 61))
    d.text((26, 196), "16. Tasiyici : Karadeniz Uluslararasi Nakliyat", fill=(15, 23, 42))
    d.text((26, 216), "Plaka & Muhur: 07 TR 992 | Gumruk Muhru: #TR-994810 (SAGLAM)", fill=(30, 58, 138))
    d.line([24, 238, 365, 238], fill=(203, 213, 225))

    d.rectangle([24, 246, 365, 326], fill=(254, 242, 242), outline=(220, 38, 38))
    d.text((32, 254), "18. Tasiyici Ihtirazi Kaydi / Оговорки перевозчика:", fill=(185, 28, 28))
    d.text((32, 274), "- RU: Повреждена стрейч-пленка на 2 паллетах, пломба цела.", fill=(15, 23, 42))
    d.text((32, 294), "- TR: 2 palette dis strec film yirtik, gumruk muhru tam.", fill=(15, 23, 42))
    d.text((26, 338), "24. Alici Kasesi: [HENUZ BOS - ARAC VERKHNIY LARS SINIRDA]", fill=(180, 83, 9))
    d.text((26, 362), "Surucu Konum: Verkhniy Lars Gumruk (Kuyruk: ~6 Saat)", fill=(30, 58, 138))

    # Right Panel: Warehouse Loading/Receiving Checklist Photo from WhatsApp
    d.rectangle([390, 72, 744, 402], fill=(248, 250, 252), outline=(245, 158, 11), width=2)
    d.rectangle([390, 72, 744, 106], fill=(180, 83, 9))
    d.text((402, 83), "DEPO RAMPA YUKLEME / KABUL CHECKLIST (#CHK-551)", fill=(255, 255, 255))

    d.text((402, 118), "Kontrol Kalemi                        Durum", fill=(71, 85, 105))
    d.line([400, 136, 734, 136], fill=(203, 213, 225))
    d.text((402, 146), "[OK] 1. Dorse Taban Temizligi & Koku  : UYGUN", fill=(21, 128, 61))
    d.text((402, 168), "[OK] 2. Frigo On Sogutma (+4.0 C)     : UYGUN (+3.8 C)", fill=(21, 128, 61))
    d.text((402, 190), "[OK] 3. Palet / Koli Sayimi (26 Plt)  : TAM (640 Koli)", fill=(21, 128, 61))
    d.text((402, 212), "[!!] 4. Spanzet & Hava Yastigi Baglama: EKSIK! (2/6 Adet)", fill=(220, 38, 38))
    d.text((402, 234), "[!!] 5. Strech Film & Kosebent        : 2 PALET GEVSEK!", fill=(220, 38, 38))
    d.text((402, 256), "[OK] 6. Gumruk Muhur & T1 Evraki      : TAM (#TR-994810)", fill=(21, 128, 61))

    d.rectangle([402, 284, 732, 388], fill=(254, 243, 199), outline=(217, 119, 6))
    d.text((412, 294), "DEPO VARDIYA AMIRI WHATSAPP NOTU:", fill=(146, 64, 14))
    d.text((412, 314), "'Aracta 6 yerine sadece 2 spanzet takili,", fill=(15, 23, 42))
    d.text((412, 332), "arka 2 palet streci gevsek. 4 spanzet daha", fill=(15, 23, 42))
    d.text((412, 350), "takilmadan rampa cikis onayi vermeyin!'", fill=(185, 28, 28))

    # Action bar
    d.rectangle([16, 414, 375, 466], fill=(37, 99, 235))
    d.text((28, 434), "[1] CMR ONAYLA + RUSCA MUSTERI BILDIRIMI CEVIR", fill=(255, 255, 255))

    d.rectangle([390, 414, 744, 466], fill=(220, 38, 38))
    d.text((404, 434), "[2] SPANZET TAMAMLANANA KADAR ARACI RAMPADA TUT", fill=(255, 255, 255))

    img.save(path, format="PNG")


def create_whatsapp_driver_road_expenses_image(path: Path) -> None:
    """
    Generates a visual showing 3 road expense receipts sent by a truck driver on WhatsApp:
    1. Valid Diesel Fuel Receipt (34 KLM 482 - 14,260 TL)
    2. Valid Highway/HGS Toll Receipt (34 KLM 482 - 1,850 TL)
    3. Invalid/Disallowed Receipt (Different car plate 06 YAB 119 + Personal Market items 2,450 TL)
    """
    img = Image.new("RGB", (760, 480), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, 760, 58], fill=(88, 28, 135))
    d.text((20, 14), "WHATSAPP SOFOR YOL MASRAF FISLERI & HARCIRAH MAHSUP DENETIMI", fill=(255, 255, 255))
    d.text((20, 34), "Sefer: #IST-MRS-409 (Istanbul -> Mersin 940 km) | Aktif Cekici Plakasi: 34 KLM 482", fill=(233, 213, 255))

    # Receipt 1: Fuel OKC Receipt
    d.rectangle([15, 74, 248, 392], fill=(255, 255, 255), outline=(34, 197, 94), width=2)
    d.rectangle([15, 74, 248, 108], fill=(21, 128, 61))
    d.text((25, 85), "FIS 1: AKARYAKIT OKC FISI", fill=(255, 255, 255))
    d.text((25, 122), "Istasyon : Opet Pozanti Tesisleri", fill=(15, 23, 42))
    d.text((25, 144), "Tarih    : 10.11.2026 - 11:40", fill=(15, 23, 42))
    d.text((25, 166), "Plaka    : 34 KLM 482 (ESLESTI)", fill=(21, 128, 61))
    d.text((25, 188), "Urun     : Motorin UltraForce", fill=(15, 23, 42))
    d.text((25, 210), "Miktar   : 310.00 Litre", fill=(15, 23, 42))
    d.text((25, 232), "Tutar    : 14,260.00 TL (%20 KDV)", fill=(30, 58, 138))
    d.text((25, 264), "Norm Kontrolu (940 km):", fill=(71, 85, 105))
    d.text((25, 284), "32.9 lt / 100km -> NORMAL", fill=(21, 128, 61))
    d.rectangle([25, 320, 238, 376], fill=(220, 252, 231))
    d.text((34, 342), "KARAR: ONAYLANDI (14.260 TL)", fill=(21, 128, 61))

    # Receipt 2: Highway / HGS Toll Receipt
    d.rectangle([260, 74, 496, 392], fill=(255, 255, 255), outline=(34, 197, 94), width=2)
    d.rectangle([260, 74, 496, 108], fill=(3, 105, 161))
    d.text((270, 85), "FIS 2: OTOYOL & KANTAR FISI", fill=(255, 255, 255))
    d.text((270, 122), "Guzergah : Kuzey Marmara + Nigde Otoyolu", fill=(15, 23, 42))
    d.text((270, 144), "Tarih    : 10.11.2026", fill=(15, 23, 42))
    d.text((270, 166), "Plaka    : 34 KLM 482 (Sinif-4 TIR)", fill=(21, 128, 61))
    d.text((270, 188), "Otoyol   : 1,850.00 TL", fill=(15, 23, 42))
    d.text((270, 210), "Kantar   : 400.00 TL (Mersin Liman)", fill=(15, 23, 42))
    d.text((270, 232), "Toplam   : 2,250.00 TL", fill=(30, 58, 138))
    d.text((270, 264), "Rota Kontrolu:", fill=(71, 85, 105))
    d.text((270, 284), "GPS Gecis Saati Ile %100 Uyumlu", fill=(21, 128, 61))
    d.rectangle([270, 320, 486, 376], fill=(220, 252, 231))
    d.text((280, 342), "KARAR: ONAYLANDI (2.250 TL)", fill=(21, 128, 61))

    # Receipt 3: Invalid / Mismatched Plate Personal Receipt
    d.rectangle([508, 74, 745, 392], fill=(255, 255, 255), outline=(220, 38, 38), width=3)
    d.rectangle([508, 74, 745, 108], fill=(185, 28, 28))
    d.text((518, 85), "FIS 3: SUPHELI MARKET / YAKIT FISI", fill=(255, 255, 255))
    d.text((518, 122), "Isyeri   : Dinlenme Tesisi Market", fill=(15, 23, 42))
    d.text((518, 144), "Tarih    : 08.11.2026 (SEFER ONCESI!)", fill=(220, 38, 38))
    d.text((518, 166), "Plaka    : 06 YAB 119 (BASKA ARAC!)", fill=(220, 38, 38))
    d.text((518, 188), "Kalemler : Kisisel Market & Sigara", fill=(185, 28, 28))
    d.text((518, 210), "Tutar    : 2,450.00 TL", fill=(220, 38, 38))
    d.text((518, 242), "Politika Ihlali:", fill=(185, 28, 28))
    d.text((518, 262), "1) Plaka 34 KLM 482 degil (06 YAB 119)", fill=(15, 23, 42))
    d.text((518, 282), "2) Sefer disi kisisel harcama", fill=(15, 23, 42))
    d.rectangle([518, 320, 735, 376], fill=(254, 226, 226))
    d.text((526, 342), "KARAR: REDDEDILDI (-2.450 TL KESINTI)", fill=(185, 28, 28))

    # Bottom Summary Bar
    d.rectangle([15, 406, 745, 464], fill=(30, 41, 59), outline=(168, 85, 247))
    d.text((28, 418), "TALEP EDILEN TOPLAM: 18,960 TL | ONAYLANAN (AKARYAKIT+OTOYOL+KANTAR): 16,510 TL | RED: 2,450 TL", fill=(250, 204, 21))
    d.text((28, 440), "SONRAKI ADIM -> DeepSeek V4.1 Flash ile Sofore Kalem Kalem Harcirah Mahsup Mesaji Olustur", fill=(167, 243, 208))

    img.save(path, format="PNG")


def ensure_sample_images() -> list[str]:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "whatsapp_load_and_business_card.png": create_whatsapp_load_and_business_card_image,
        "whatsapp_cmr_and_warehouse_checklist.png": create_whatsapp_cmr_and_warehouse_checklist_image,
        "whatsapp_driver_road_expenses.png": create_whatsapp_driver_road_expenses_image,
        "omnichannel_whatsapp_email_bundle.png": create_omnichannel_bundle_image,
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
