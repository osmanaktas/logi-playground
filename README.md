# 🎯 Nace.AI Drex Max — Multimodal Decision Playground (`nace-ai/drex-max`)

OpenRouter üzerinde yayınlanan **[Nace.AI: Drex Max (`nace-ai/drex-max`)](https://openrouter.ai/nace-ai/drex-max)** karar modelinin (Decision Model) metin, yapılandırılmış JSON ve çoklu görsel (Multimodal Vision) yeteneklerini simüle etmek ve test etmek için geliştirilmiş interaktif Python Playground uygulaması.

---

## 🧠 `nace-ai/drex-max` Model İncelemesi

**Drex Max**, geleneksel sohbet/metin üretim (chat completion) LLM'lerinden tamamen farklı bir mimariye sahiptir:

| Özellik | Detay |
|---|---|
| **Model Türü** | Çok Modlu Karar Modeli (*Multimodal Foundation Decision Model*) |
| **Parametre & Mimari** | **27B Dense** (64 Katman: 48 *Gated DeltaNet* doğrusal dikkat + 16 *Non-Causal Full-Attention* katmanı + **255-yollu Readout Head**) |
| **Girdi Modaliteleri** | Metin (`string`), Yapılandırılmış `JSON` nesnesi/dizisi ve **Görsel** (İstek başına **4 görsele kadar** `PNG`, `JPEG`, `WebP`) |
| **Çıktı Modalitesi** | `decisions` — **Metin üretmez (0 token generation)**. Tek ileri geçişte (*single forward pass*) her seçenek için **kalibre edilmiş olasılık dağılımı** ve **güven (`confidence`)** döner. |
| **Soru Tipleri** | 1. **`noul`**: Evet/Hayır önermesi (`0.0` – `1.0` arası `true` olasılığı)<br>2. **`choice`**: Çoktan seçmeli karar (255 seçeneğe kadar olasılık dağılımı)<br>3. **`score`**: Sıralı derecelendirme ölçeği (beklenen değer skoru + seviye olasılıkları) |
| **Bağlam Penceresi** | **262,144 token** (262K) |
| **Fiyatlandırma** | **$0.06 / 1M girdi token** • **$0.00 / 1M çıktı token** (%50 indirimli lansman fiyatı) |
| **Benchmark Skorları** | • **Decision Index 0.4 (Metin):** `67.52` (Tools: `81.9`, Language: `72.2`, Retrieval: `68.8`)<br>• **Public Vision Index:** `73.92` (InfographicVQA: `%97.3`, KIE CORD+FUNSD: `%92.4`, Mind2Web UI: `%84.2`, CharXiv: `%80.5`)<br>• **Decision Bench v4:** `%94.30` • **JevBench:** `%92.2` |
| **API Protokolü** | `POST https://openrouter.ai/api/alpha/decisions` ve `POST https://openrouter.ai/api/v1/systemone` (*TypeSafe System One* uyumlu) |

> ⚠️ **Önemli Fark:** Drex Max standart `/api/v1/chat/completions` uç noktasıyla çağrılmaz; `state` ve `questions` alanlarından oluşan **Decisions / System One** şemasıyla çağrılır.

---

## 🚀 Özellikler & Simülasyon Senaryoları

Bu test alanında **6 hazır simülasyon senaryosu** (4 tekli görsel, 1 çoklu görsel korelasyon, 1 yapılandırılmış JSON) ve **Özel Soru/Görsel Stüdyosu** yer alır:

1. 🧾 **Görsel Fatura Denetimi & Ajan UI Aksiyonu (`samples/invoice_audit.png`)**: Fatura görselindeki mükerrer (duplicate) H100 GPU kalemini tespit eder ve ekrandaki hangi UI butonuna (`[BTN-2] DISPUTE DUPLICATE`) tıklanması gerektiğini `%99.9+` güvenle seçer.
2. 🌐 **Tarayıcı Ajanı (Computer Use) UI Navigasyonu (`samples/ui_checkout_error.png`)**: E-ticaret ödeme ekranındaki `504 Gateway Timeout` hata penceresini okur, karttan çekim yapılmadığını doğrular ve `RETRY WITH IDEMPOTENCY` butonunu seçer.
3. 📈 **Sunucu Telemetri Grafiği & Canary Rollback Kararı (`samples/server_telemetry_chart.png`)**: `v2.4.1` dağıtımı sonrası CPU'nun `%98.4`'e fırladığı grafiği görsel olarak okuyup otomatik Rollback kararı verir.
4. 🛡️ **Görsel İçerik Moderasyonu & Kripto Phishing Tespiti (`samples/moderation_card.png`)**: Görseldeki 12 kelimelik seed-phrase oltalama (phishing) ve ETH gas ücreti dolandırıcılığını yakalar.
5. ⚖️ **Çoklu Görsel Korelasyon Analizi (`ui_checkout_error.png` + `server_telemetry_chart.png`)**: Aynı istekte iki görseli birden değerlendirerek müşteri ekranındaki 504 hatası ile sunucu CPU sıçraması arasındaki nedenselliği doğrular.
6. 🎫 **Yapılandırılmış JSON Destek & SLA Triyajı**: Kurumsal SAML SSO kilitlenme bildirimini milisaniyeler içinde doğru mühendislik kuyruğuna (`iam_sso_security`) ve `P1 - Blocker` önceliğine yönlendirir.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2. `.env` Dosyasını Yapılandırın

`.env.example` dosyasını `.env` olarak kopyalayın ve OpenRouter API anahtarınızı ekleyin:

```env
OPENROUTER_API_KEY=sk-or-v1-...
```

### 3. İnteraktif Web Playground'u Başlatın

```bash
python app.py
```

Tarayıcınızda **`http://localhost:8080`** adresini açın.
- Hazır görsel senaryoları tek tıkla çalıştırabilir,
- Bilgisayarınızdan kendi görsellerinizi (최대 4 adet) yükleyebilir,
- `noul`, `choice` ve `score` tipinde dinamik sorular ekleyebilir,
- **`nace-ai/drex-max` vs `nace-ai/drex-max-finance`** modellerini yan yana karşılaştırabilirsiniz.

### 4. Terminal Üzerinden Tüm Benchmark Simülasyonlarını Koşturun

```bash
python cli_demo.py
```
