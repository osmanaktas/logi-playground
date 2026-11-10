# 🎯 Nace.AI Drex Max & Drex Max Finance — Lojistik Finans, WMS & Mobil Yük Borsası Karar Playground

OpenRouter üzerinde yayınlanan **[`nace-ai/drex-max-finance`](https://openrouter.ai/nace-ai/drex-max-finance)** ve **[`nace-ai/drex-max`](https://openrouter.ai/nace-ai/drex-max)** çok modlu karar modellerinin **Depo Yönetim Sistemleri (WMS)**, **Lojistik Finans (3-Way Matching, Demuraj, Sigorta Rücu, Kredi/Faktoring)** ve **Mobil Yük Borsası** operasyonlarında nasıl konumlandırılacağını, olasılık/varyasyon matrislerini ve **System-1 + System-2** orkestrasyonunu simüle eden Python Playground paketi.

---

## 🏦 1. `nace-ai/drex-max-finance` Lojistik Operasyonlarda Ne İşe Yarar?

Depo yönetim sistemleri (WMS) ve dijital navlun pazar yeri operasyonlarında evrak trafiği hem **görsel (irsaliye, kantar fişi, e-Fatura, hasar fotoğrafı)** hem de **yapılandırılmış veri (PO JSON, GPS telemetri, Findeks/Bilanço)** içerir. **`nace-ai/drex-max-finance`** tek bir ileri geçişte (*single forward pass*, 0 metin üretimi) bu iki dünyayı birleştirir:

| # | Operasyon Alanı | Görsel & Yapılandırılmış Girdi (`state`) | Tek Geçişte Yanıtlanan Sorular (`questions`) |
|---|---|---|---|
| **1** | **Depo Mal Kabulde Üçlü Eşleştirme (3-Way Matching: PO – İrsaliye – e-Fatura)** | [`finance_3way_matching.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_3way_matching.png) + PO & WMS Sayım JSON | • Fatura adedi (1.000) WMS sağlam sayımıyla (850) uyuşuyor mu?<br>• Birim fiyat (465 TL) PO toleransını (%2) aşıyor mu?<br>• Kantar net tartımı (18.7t) fatura tonajıyla (22t) uyumlu mu?<br>• Zorunlu 2/10 KDV tevkifatı uygulanmış mı? |
| **2** | **Navlun Pazar Yerinde Hak Ediş, POD, Demuraj & Sahte Fiş Denetimi** | [`finance_demurrage_receipt_fraud.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_demurrage_receipt_fraud.png) + GPS Bekleme Kaydı | • GPS bekleme süresi (45 dk) 4 saatlik ücretsiz demuraj süresini aşıyor mu?<br>• Kantar/otoyol fişindeki tarih (`2025`) ve üzeri çizili plaka aktif seferle uyumlu mu?<br>• Fiş daha önce başka bir seferde kullanılmış mükerrer belge mi? |
| **3** | **Hasarlı Kargo & Sigorta Rücu (Subrogation / Claim) Triyajı** | **3 Görsel Birden:** [`logistics_pod_waybill.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/logistics_pod_waybill.png) + [`warehouse_damaged_pallet.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/warehouse_damaged_pallet.png) + [`cold_chain_telemetry.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/cold_chain_telemetry.png) | • İrsaliyedeki 3 palet hasar şerhi taşıma kusuru mu?<br>• Beyan edilmemiş ADR Class 3 yanıcı etiket yük veren (Shipper) kusuru mu?<br>• Frigo sıcaklık ihlali (+4.5°C) IoT grafiğiyle kanıtlandı mı?<br>• Kime rücu edilmeli? |
| **4** | **Vadeli Yük Veren (Açık Hesap) & Alt Taşıyıcı Kredi / Faktoring Risk Skorlaması** | [`finance_credit_balance_sheet.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_credit_balance_sheet.png) + Findeks Çek/Senet Özeti | • Cari oran (`0.68`) minimum `1.20` politikasını karşılıyor mu?<br>• Talep edilen 3.5M TL limit yıllık cironun `%10` tavanı içinde mi (`%42.6`)?<br>• Son 6 ayda karşılıksız çek (3 adet) veya protestolu senet var mı? |
| **5** | **Çoklu Ajan (Multi-Agent) Mimaride "System One" Ön Yönlendirici (Pre-Router / Gri Alan)** | Python/FastAPI + Celery Görev Kuyruğu JSON | • **Yeşil Hat (`Confidence >= 0.85`):** Doğrudan ERP/DB'ye yaz (LLM çağrılmaz).<br>• **Gri Alan (`0.32 <= P <= 0.68`):** +%1.95 kur farkı ve 4 nemli palet gibi sınırda kalan dosyaları **System-2 Reasoning LLM** ajanına devret.<br>• **Kırmızı Hat:** Kesin sahtecilik/ihlal dosyalarını otomatik bloke et. |

---

## 🎛️ 2. Olasılık, Varyasyon & Gri Alan (Pre-Router) Test Laboratuvarı

[`finance_variations_sim.py`](file:///C:/Users/Osman/Desktop/llm-test/finance_variations_sim.py) ve Web arayüzündeki **Olasılık & Varyasyon Laboratuvarı**, aynı operasyonel kural setine karşı **3 farklı varyasyonu** paralel koşturarak `drex-max-finance` modelinin olasılık dağılımlarını nasıl değiştirdiğini test eder:

1. **Varyasyon 1 — Yeşil Hat (Tam Uyumlu):** Tüm `noul` kontrolleri `> %99`, `choice` güveni `> %99` ➔ **Üst katman LLM tetiklenmeden doğrudan DB/SAP onayı.**
2. **Varyasyon 2 — Gri Alan (Sınırda / Çelişkili Kanıt):** Örneğin `%2.0` tolerans sınırında `+%1.95` TCMB kur farkı + `4 adet dış streci nemli ama içi sağlam palet` veya `GPS tünel kaybı nedeniyle doğrulanamayan 4.3 saat bekleme` ➔ Model `gray_zone_escalate_to_reasoning_agent` seçerek dosyayı **System-2 Muhakeme LLM Ajanına / Uzman Kuyruğuna** aktarır.
3. **Varyasyon 3 — Kırmızı Hat (Kesin İhlal / Fraud):** `150 eksik palet`, `2025 tarihli oynanmış fiş` veya `3 karşılıksız çek` ➔ **Üst katman LLM maliyeti olmadan otomatik bloke ve rücu/fraud kaydı.**

---

## 🛠️ 3. Çalıştırma Komutları

```bash
# 1. İnteraktif Web Playground (Varyasyon Laboratuvarı + 4-Katmanlı Hibrit Akış + 12 Senaryo)
python app.py
# Tarayıcıda açın: http://localhost:8080

# 2. Drex Max Finance (5 Finans Senaryosu + 3x3 Olasılık/Varyasyon Matrisi)
python finance_variations_sim.py

# 3. 4-Katmanlı Hibrit Lojistik & Mobil Yük Borsası Orkestrasyon Simülasyonu
python logistics_pipeline_sim.py

# 4. Tüm 12 Görsel & JSON Senaryosunun Benchmark Testi
python cli_demo.py
```
