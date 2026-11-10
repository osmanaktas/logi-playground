# 🚛 Logi-Playground — Lojistik, Depo (WMS) & Mobil Yük Borsası Çoklu Model Test ve Simülasyon Platformu

**`logi-playground`**, Depo Yönetim Sistemleri (**WMS**), Dijital Navlun / **Mobil Yük Borsası (Freight Exchange)** ve Lojistik Finans operasyonlarında **Karar Modelleri (System-1: `nace-ai/drex-max`, `nace-ai/drex-max-finance`, `nace-ai/drex-v2.0`)** ile **Üretken LLM'lerin (System-2: `gpt-4o-mini`, `gemini-2.5-flash` vb.)** birlikte nasıl çalıştırılacağını test etmek, olasılık/varyasyon analizleri yapmak ve görsel (Vision) yetenekleri simüle etmek için geliştirilmiş kapsamlı bir Python test alanıdır.

---

## 🧠 1. `nace-ai/drex-max` Model İncelemesi ve Kullanım Rehberi

OpenRouter üzerindeki **[`nace-ai/drex-max`](https://openrouter.ai/nace-ai/drex-max)**, Nace.AI tarafından geliştirilen **27 milyar parametreli çok modlu (multimodal) bir karar modelidir (Foundation Decision Model)**.

### 1.1. `nace-ai/drex-max` Klasik LLM'lerden Neden Farklıdır?

Geleneksel sohbet modelleri (`chat/completions`) kelime kelime (token-by-token) metin üretir. Operasyonel yazılımlarda bu durum **JSON parse hatalarına**, **halüsinasyonlara**, **2–5 saniyelik gecikmelere** ve **yüksek çıktı token maliyetine** yol açar.

**`nace-ai/drex-max` ise hiç metin üretmez (`0 output token generation`):**
* **Mimari:** 64 katmanlı yoğun (dense) 27B omurga (**48 Gated DeltaNet** doğrusal dikkat katmanı + her 4 katmanda bir gelen **16 Non-Causal Full-Attention** katmanı) ve sonunda **255-yollu okuma kafası (`255-way readout head`)** bulunur.
* **Tek İleri Geçiş (Single Forward Pass):** Modele bir durum (`state`: metin, JSON veya **4 adede kadar görsel**) ve yapılandırılmış sorular (`questions`) verilir; model tek geçişte her seçenek için **kalibre edilmiş olasılık (`0.0` – `1.0`)** ve **güven (`confidence`)** skoru döndürür.
* **Bağlam Penceresi:** **262,144 token** (262K).
* **Fiyatlandırma:** **$0.06 / 1M girdi token** • **$0.00 / 1M çıktı token**.
* **Benchmark Skorları:**
  * **Public Decision Index 0.4 (Metin):** **`67.52`** (*Tools:* `81.9`, *Language:* `72.2`, *Retrieval:* `68.8`, *Decision Bench v4:* `%94.30`, *JevBench:* `%92.2`)
  * **Public Vision Index (Görsel):** **`73.92`** (*InfographicVQA:* `%97.3`, *KIE CORD+FUNSD Fatura/İrsaliye:* `%92.4`, *Mind2Web UI Navigasyon:* `%84.2`, *CharXiv Grafik:* `%80.5`)

---

### 1.2. `nace-ai/drex-max` API İstek Formatı ve Soru Tipleri (`questions`)

`nace-ai/drex-max`, standart `/api/v1/chat/completions` yerine **OpenRouter Decisions API** veya **TypeSafe System One API** uç noktalarıyla çağrılır:
* `POST https://openrouter.ai/api/alpha/decisions`
* `POST https://openrouter.ai/api/v1/systemone`

İstek gövdesi (`payload`) 3 ana alandan oluşur:
1. **`model`**: `"nace-ai/drex-max"` (veya `"nace-ai/drex-max-finance"`, `"nace-ai/drex-v2.0"`, `"nace-ai/drex-v1.5"`)
2. **`state`**: Değerlendirilecek bağlam:
   * Düz metin (`string`),
   * Yapılandırılmış `JSON` nesnesi (`dict` / `list`),
   * **Görsel (Multimodal) Dizi:** Üst düzey `state` listesi içinde metin ve en fazla 4 adet `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}` öğesi.
3. **`questions`**: İsimlendirilmiş sorulardan oluşan sözlük. Her soru şu **3 tipten** biridir:

| Soru Tipi (`type`) | Ne Sorulur? | Parametreler | Modelin Döndürdüğü Yanıt (`answers`) |
|---|---|---|---|
| **`noul`** | **Evet / Hayır (`True` / `False`)** önermesi | `instructions`: Soru metni<br>*(Opsiyonel)* `criteria`: `{"true": "...", "false": "..."}` | `{"type": "noul", "noul": 0.9984}`<br>*(0 ile 1 arasında "Evet/True" olma olasılığı)* |
| **`choice`** | **Çoktan Seçmeli Sınıflandırma / Yönlendirme** (255 seçeneğe kadar) | `instructions`: Soru metni<br>`criteria`: `{"secenek_a": "Açıklama A", "secenek_b": "Açıklama B"}` | `{"type": "choice", "choice": "secenek_a", "probabilities": {"secenek_a": 0.998, "secenek_b": 0.002}, "confidence": 0.997}` |
| **`score`** | **Sıralı Derecelendirme Ölçeği (Ordinal Rating)** | `instructions`: Soru metni<br>`criteria`: `["Düşük", "Orta", "Yüksek", "Kritik"]` *(Düşükten yükseğe sıralı liste)* | `{"type": "score", "score": 2.91, "legend": {"0": "Düşük", ...}, "probabilities": {"0": 0.001, ...}, "confidence": 0.92}` |

---

### 1.3. `nace-ai/drex-max` Kullanım Örnekleri (Python & cURL)

#### Örnek A: Metin / JSON `state` ile `nace-ai/drex-max` Kullanımı

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

payload = {
    "model": "nace-ai/drex-max",
    "state": {
        "load_id": "YUK-88310",
        "route": "Antalya -> Berlin",
        "required_trailer": "Frigo (-18C)",
        "incoming_chat": "Reis uygulama %8 komisyon kesiyor, ilanı iptal et sıfır beş yüz otuz iki... numaradan ara elden IBAN'a at."
    },
    "questions": {
        "commission_circumvention": {
            "type": "noul",
            "instructions": "Is the carrier trying to bypass platform commission by moving payment off-platform?"
        },
        "moderation_action": {
            "type": "choice",
            "instructions": "Which backend action should execute immediately?",
            "criteria": {
                "block_and_warn": "Block chat message, mask phone number, and send policy warning",
                "deliver_message": "Deliver message to shipper normally"
            }
        },
        "violation_severity": {
            "type": "score",
            "instructions": "Rate the severity of the policy violation.",
            "criteria": ["None", "Low", "High", "Critical Ban"]
        }
    }
}

response = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=30,
)
print(response.json())
```

#### Örnek B: Görsel (Multimodal Vision) `state` ile `nace-ai/drex-max` Kullanımı

`nace-ai/drex-max` modeline görsel göndermek için görsel `base64` data URL (`data:image/png;base64,...`) formatına çevrilir ve **doğrudan üst düzey `state` dizisinin (`list`) içine** yerleştirilir:

```python
import base64
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 1. Görseli Base64 Data URL olarak hazırla
img_bytes = Path("samples/warehouse_damaged_pallet.png").read_bytes()
b64_img = base64.b64encode(img_bytes).decode("utf-8")

# 2. Üst düzey `state` dizisine metin bağlamı + görsel parçasını (`image_url`) ekle
payload = {
    "model": "nace-ai/drex-max",
    "state": [
        "WMS Dock Policy: Isolate any pallet with undeclared ADR Hazmat labels or liquid spills.",
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{b64_img}"}
        }
    ],
    "questions": {
        "undeclared_adr_detected": {
            "type": "noul",
            "instructions": "Does the pallet image show an ADR Class 3 Flammable label?"
        },
        "putaway_routing": {
            "type": "choice",
            "instructions": "Where should the WMS route this pallet?",
            "criteria": {
                "standard_rack": "Standard High Rack A-12",
                "hazmat_quarantine": "Hazmat Quarantine Bunker & Spill Team",
                "cold_storage": "Cold Storage (-18C)"
            }
        },
        "safety_risk": {
            "type": "score",
            "instructions": "Rate the warehouse safety risk.",
            "criteria": ["Safe", "Low", "High", "Critical Emergency"]
        }
    }
}

resp = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
    json=payload,
)
print(resp.json())
```

> **📌 Çoklu Görsel İpucu:** Tek bir istekte **4 adede kadar** `{"type": "image_url", ...}` nesnesini aynı `state` listesine ekleyerek `nace-ai/drex-max` modelinin birden fazla fotoğrafı (örneğin *Sevk İrsaliyesi + Rampa Hasar Fotoğrafı + Sıcaklık Grafiği*) çapraz karşılaştırmasını sağlayabilirsiniz. Projedeki [`drex_client.py`](file:///C:/Users/Osman/Desktop/llm-test/drex_client.py) içindeki `encode_image_to_data_url()` ve `evaluate_decision()` fonksiyonları bu işlemi otomatik yapar.

---

## 🏦 2. `nace-ai/drex-max` vs `nace-ai/drex-max-finance` Karşılaştırması

Bu playground içerisinde her iki modeli tek tıkla yan yana (`⚖️ Karşılaştır` butonuyla) test edebilirsiniz:

| Kriter | `nace-ai/drex-max` | `nace-ai/drex-max-finance` |
|---|---|---|
| **Odak Alanı** | Genel çok modlu karar, tarayıcı/UI ajan navigasyonu, depo kamera (WMS) fiziksel hasar & ADR tespiti, IoT grafik okuma, içerik/sohbet moderasyonu | Finansal belgeler, **3-Way Matching (PO – İrsaliye – e-Fatura)**, KDV/Tevkifat denetimi, navlun hak ediş & demuraj sahteciliği, sigorta rücu (subrogation), bilanço/Findeks kredi ve faktoring risk skorlaması |
| **Parametre & Bağlam** | 27B Dense Multimodal • 262K Context | 27B Dense Multimodal (Finans İnce Ayarlı) • 262K Context |
| **Girdi Modalitesi** | Metin, JSON, Görsel (4 adede kadar) | Metin, JSON, Görsel (Fatura, Dekont, İrsaliye, Bilanço) |
| **Fiyatlandırma** | `$0.06 / 1M` girdi • `$0 / 1M` çıktı | `$0.06 / 1M` girdi • `$0 / 1M` çıktı |

---

## 🏗️ 3. Depo (WMS) ve Mobil Yük Borsasında 4-Katmanlı Mimari (System-1 + System-2)

Uygulamalarınız ile LLM'ler arasında `drex-max` ve `drex-max-finance` şu **4 katmanlı mimariyle** konumlandırılır:

```mermaid
flowchart LR
    A["📱 Mobil Yük Borsası / WMS El Terminali\n(İrsaliye Fotoğrafı, Palet Kamerası, e-Fatura, Teklif JSON)"] --> B["⚡ KATMAN 1: System-1 Karar Motoru\n(drex-max / drex-max-finance)\nnoul | choice | score Olasılık Dağılımı"]
    B --> C{"🛡️ KATMAN 2: System-One Pre-Router Kapısı\n(Güven & Olasılık Eşiği)"}
    C -- "🟢 Yeşil Hat (Güven ≥ %85)" --> D["💾 Doğrudan DB / SAP ERP / Escrow Onayı\n(Üst Katman LLM Çağrılmaz - $0 Ek Maliyet)"]
    C -- "🔴 Kırmızı Hat (Kesin İhlal/Fraud)" --> E["🛑 Otomatik Bloke / Rücu / Fraud Kuyruğu\n(Üst Katman LLM Çağrılmaz)"]
    C -- "🟡 Gri Alan (0.32 ≤ P ≤ 0.68)" --> F["🧠 KATMAN 3: System-2 Muhakeme / Üretken LLM\n(Derin Analiz & Sürücü/Operatör Bildirim Yazımı)"]
    F --> G["🔒 KATMAN 4: System-1 Çıktı Guardrail\n(Drex Max Halüsinasyon & Politika Denetimi)"]
    G --> H["📲 Mobil Uygulama Push Bildirimi"]
```

---

## 🧪 4. Projede Yer Alan 12 Simülasyon Senaryosu ve Varyasyon Laboratuvarı

### A. `nace-ai/drex-max-finance` Lojistik Finans Senaryoları (5 Adet)
1. 📑 **Depo Mal Kabul Üçlü Eşleştirme (3-Way Matching: PO – İrsaliye – e-Fatura)** ([`finance_3way_matching.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_3way_matching.png)): 150 palet eksik teslimatı, `+%16.25` birim fiyat aşımını ve eksik `2/10` KDV tevkifatını tek geçişte yakalar.
2. 🕵️ **Navlun Hak Ediş, Demuraj (Bekleme) & Sahte Kantar/Otoyol Fişi Denetimi** ([`finance_demurrage_receipt_fraud.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_demurrage_receipt_fraud.png)): 45 dk'lık gerçek GPS beklemesine rağmen istenen 6.500 TL demurajı ve 2025 tarihli, plakası çizilmiş mükerrer fişi yakalar.
3. ⚖️ **Hasarlı Kargo & Sigorta Rücu (Subrogation) Triyajı (3 Görsel Birden)**: İrsaliye + Rampa ADR/Hasar fotoğrafı + Frigo IoT grafiğini birlikte değerlendirip kusuru Taşıyıcı CMR Sigortası ve Yük Veren ADR Cezası olarak paylaştırır.
4. 🏦 **Vadeli Yük Veren (Açık Hesap) & Faktoring Kredi Risk Skorlaması** ([`finance_credit_balance_sheet.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_credit_balance_sheet.png)): Cari oran (`0.68`), ciro/limit oranı (`%42.6`) ve 3 karşılıksız çeki okuyarak vadeli açık hesabı reddeder.
5. 🧭 **Çoklu Ajan (Multi-Agent) "System One" Ön Yönlendirici (Gri Alan Gatekeeper)**: `+%1.95` kur yuvarlama farkı ve 4 nemli palet içeren sınır vakayı tespit edip `gray_zone_deep_reasoning_llm_queue` kuyruğuna yönlendirir.

### B. `nace-ai/drex-max` Depo (WMS), Lojistik & Mobil Yük Borsası Senaryoları (5 Adet)
6. 🚚 **Mobil Yük Borsası — Sevk İrsaliyesi (POD) & Escrow Denetimi** ([`logistics_pod_waybill.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/logistics_pod_waybill.png))
7. 🏭 **Depo (WMS) Rampa Kabul — Hasarlı Palet & Beyan Edilmemiş ADR Tespiti** ([`warehouse_damaged_pallet.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/warehouse_damaged_pallet.png))
8. 📱 **Mobil Yük Borsası — İlan Şartları (-18°C Frigo & 5M Sigorta) vs Taşıyıcı Teklifi Kalkanı** ([`mobile_load_board_ui.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/mobile_load_board_ui.png))
9. ❄️ **Soğuk Zincir (Frigo) IoT Telemetri Grafiği & Acil Soğuk Depo Yönlendirmesi** ([`cold_chain_telemetry.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/cold_chain_telemetry.png))
10. 🤖 **Mobil Yük Borsası — LLM Öncesi Sohbet & Komisyon Atlatma (Fraud) Kalkanı** (JSON State)

### C. Genel Kurumsal Senaryolar (2 Adet)
11. 🧾 **Kurumsal Bulut Faturası Mükerrer Kalem Denetimi** ([`invoice_audit.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/invoice_audit.png))
12. 🌐 **Tarayıcı Ajanı (Computer Use) 504 Ödeme Hatası Navigasyonu** ([`ui_checkout_error.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/ui_checkout_error.png))

---

## 🛠️ 5. Kurulum ve Çalıştırma

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. .env dosyasını oluşturun
cp .env.example .env
# OPENROUTER_API_KEY=sk-or-v1-... anahtarınızı ekleyin

# 3. İnteraktif Web Playground'u başlatın (http://localhost:8080)
python app.py

# 4. Drex Max Finance & Olasılık/Varyasyon (Yeşil/Gri/Kırmızı Hat) Simülatörü
python finance_variations_sim.py

# 5. 4-Katmanlı Hibrit (System-1 Drex Max + System-2 LLM) Lojistik Orkestrasyon Simülatörü
python logistics_pipeline_sim.py

# 6. Tüm 12 Görsel & JSON Senaryosunun Benchmark Testi
python cli_demo.py
```
