# 🚛 Logi-Playground — Lojistik Operasyon, Mobil Yük Borsası, Depo (WMS) & Lojistik Finans Dinamik Simülasyon Platformu

**`logi-playground`**, Türkiye ve uluslararası lojistik operasyonlarında **Depo Yönetim Sistemleri (WMS)**, **Mobil Yük Borsası (Freight Exchange)**, **Çok Kanallı (WhatsApp / E-Posta / Mobil) Evrak Otomasyonu** ve **Lojistik Finans (3-Way Matching, Demuraj, Harcırah, Kredi Riski)** süreçlerini uçtan uca simüle etmek, dinamik akış diyagramları kurgulamak ve canlı verilerle test etmek için geliştirilmiş bir **İş Modeli ve Operasyon Simülatörüdür**.

> **💡 Mimari Prensip (Modeller Birer Araçtır):** Bu platform bir model incelemesi değil; gerçek lojistik iş süreçlerinin nasıl otomatize edileceğini gösteren bir operasyon motorudur. Yapay zeka modelleri bu iş modelinde doğru katmana yerleştirilmiş **birer araç** olarak görev yapar:
> * ⚡ **Hızlı Karar, Sınıflandırma & Kural Denetim Araçları (System-1 — `0 Output Token`):**
>   * **[`nace-ai/drex-max`](https://openrouter.ai/nace-ai/drex-max)**: WhatsApp/E-posta belge sınıflandırma, tekilleştirme (deduplication), WMS rampa/palet/ADR kontrolü, uluslararası CMR & yükleme checklist (`#CHK-551`) denetimi ve komisyon atlatma (fraud) kalkanı.
>   * **[`nace-ai/drex-max-finance`](https://openrouter.ai/nace-ai/drex-max-finance)**: Depo mal kabulde 3-Way Matching (PO – İrsaliye – e-Fatura), KDV/Tevkifat denetimi, navlun hak ediş & demuraj (bekleme) suistimali, şoför yol masraf fişleri (mazot, HGS, kantar) harcırah mahsubu, sigorta rücu ve vadeli kredi/faktoring risk skorlaması.
> * 🧠 **Üretken Dil, Çeviri, Yapılandırılmış JSON & Dinamik Senaryo Aracı (System-2 LLM):**
>   * **[`deepseek/deepseek-v4.1-flash-1017`](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017)**:
>     1. **Dinamik Simülasyon Üretimi:** Tek tıkla gerçekçi Türkiye lojistik WhatsApp/E-posta operasyon yazışmaları ve belgeye özel 8–15 adet denetim sorusu (`noul`, `choice`, `score`) sentezleme,
>     2. **Sohbetten Operasyona Dönüştürme (Chat-to-Load & CRM):** WhatsApp yazışmasından **Mobil Yük Borsası İlan JSON'u** ve kartvizit fotoğrafından **CRM Müşteri/VKN Kartı JSON'u** çıkarma,
>     3. **Sınır Ötesi Çeviri (Türkçe ↔ Rusça `Русский язык`):** Sarp / Verkhniy Lars sınır kapısı ve Rusya/BDT koridorunda şoför/gümrük mesajlarını Türkçeye, operasyoncunun Türkçe talimatlarını ise alıcı firma için profesyonel lojistik Rusçasına çevirme,
>     4. **Resmi Tutanak & Mahsup Raporu Yazımı:** System-1 karar modelinin verdiği kesin karara bağlı kalarak depo rampa blokaj tutanağı veya şoför harcırah mahsup tablosu oluşturma.

---

## ⚡ 1. Dinamik Akış & Diyagram Stüdyosu (Visual Flow Builder + `▶ RUN`)

Web arayüzü (`http://localhost:8080`), statik form testleri yerine **dinamik bir operasyon akışı kurgulayıp görsel diyagram üzerinde `▶ RUN SIMULATION` butonuyla çalıştırma** mantığıyla tasarlanmıştır:

```mermaid
flowchart LR
    N1["🌐 DÜĞÜM 1: Çok Kanallı Girdi\n• İnternetten Canlı Belge Arama / URL'den Doğrudan Çekme\n• WhatsApp / E-Posta / Mobil Kamera Görseli"] --> N2["✨ DÜĞÜM 2: DeepSeek V4.1 Flash Sentezleyici\n• Gerçekçi WhatsApp/E-Posta Operasyon Sohbeti Üretimi\n• Belgeye Özel 8-15 Karar Sorusu (noul/choice/score) Üretimi"]
    N2 --> N3["⚡ DÜĞÜM 3: System-1 Karar Filtresi\n(drex-max / drex-max-finance)\nTek İleri Geçişte Kalibre Olasılık & Sınıflandırma"]
    N3 --> N4{"🛡️ DÜĞÜM 4: System-One Gatekeeper\n(Yeşil / Gri / Kırmızı Hat)"}
    N4 -- "🟢 Yeşil / 🔴 Kırmızı / 🟡 Gri" --> N5["🧠 DÜĞÜM 5: DeepSeek V4.1 Flash Operasyon Ajanı\n• Yük Borsası İlan JSON + CRM Kartvizit JSON\n• Türkçe ↔ Rusça CMR/Gümrük Çevirisi\n• Rampa Tutanağı / Harcırah Mahsup Özeti"]
    N5 --> N6["🔒 DÜĞÜM 6: System-1 Çıktı Guardrail & Commit\nHalüsinasyon Kontrolü -> WMS / SAP ERP / Mobil App Onayı"]
```

### 🌐 İnternetten Canlı Belge Arama, Önizleme ve Dosya Yüklemeden Doğrudan URL ile Test Etme
1. **Canlı Web Belge Arama & Önizleme (`🔍 Web'de Ara`):** Arayüz üzerinden `"sevk irsaliyesi ornegi"`, `"cmr belgesi"`, `"e-fatura ornegi"`, `"kantar fisi"`, `"kartvizit"` gibi aramalar yaparak internetteki gerçek belge görsellerini küçük resim önizlemeli olarak listeleyebilirsiniz.
   * Küçük resme tıklayarak **Büyük Önizleme (Lightbox)** açabilir,
   * **`↗ Sekme`** ile görseli yeni sekmede açabilir,
   * **`✕`** butonu ile alakasız görselleri listeden çıkartabilirsiniz.
2. **Doğrudan URL'den Belge Çekme (`🔗 Kullan` / `🔗 URL'den Çek & Bağla`):** Seçtiğiniz veya yapıştırdığınız URL diske kaydedilmeden doğrudan bellekte (`fetch_remote_image_to_data_url`) çekilir, boyutlandırılır ve **[`deepseek/deepseek-v4.1-flash-1017`](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017)** ile okunarak **o belgeye özel karar soruları + WhatsApp operasyon sohbeti otomatik üretilir**.
3. **`▶ AKIŞI ÇALIŞTIR (RUN SIMULATION)`:** Tek tıkla diyagramdaki 6 düğüm sırayla çalışır; her düğümün çalışma süresi (`ms`), olasılık çubukları ve üretilen operasyonel çıktılar canlı olarak gösterilir.

---

## 🎯 2. Lojistik Operasyonlarda Soru Filtresi Mimarisi ve Zengin Soru Bankası (100+ Örnek Soru)

WhatsApp, E-Posta ve Mobil Uygulamadan gelen evrakları ve yazışmaları **normal LLM'lerle `.md` (Markdown) metne dönüştürmek yerine**; belge ve süreç tipine göre hazırlanmış **onlarca yapılandırılmış karar sorusundan (`noul`, `choice`, `score`)** tek bir ileri geçişte (`single forward pass — 0 output token`) geçiriyoruz.

### 2.1. Karar Sorusu Tipleri (`questions` Şeması)

| Soru Tipi (`type`) | Operasyonel Amacı | Parametreler | Döndürülen Kalibre Yanıt (`answers`) |
|---|---|---|---|
| **`noul`** | **Evet / Hayır (`True` / `False`) Kural Denetimi** | `instructions`: Soru metni<br>*(Opsiyonel)* `criteria`: `{"true": "...", "false": "..."}` | `{"type": "noul", "noul": 0.9984}`<br>*(0.0 ile 1.0 arasında "Evet/True" olma olasılığı)* |
| **`choice`** | **Çoktan Seçmeli Belge Sınıflandırma & Mikroservis Yönlendirme** (255 seçeneğe kadar) | `instructions`: Soru metni<br>`criteria`: `{"secenek_a": "Açıklama A", "secenek_b": "Açıklama B"}` | `{"type": "choice", "choice": "secenek_a", "probabilities": {"secenek_a": 0.998, "secenek_b": 0.002}, "confidence": 0.997}` |
| **`score`** | **Sıralı Derecelendirme Ölçeği (Risk / Hasar / Tamlık Skoru)** | `instructions`: Soru metni<br>`criteria`: `["0 - Düşük", "1 - Orta", "2 - Yüksek", "3 - Kritik"]` | `{"type": "score", "score": 2.91, "legend": {"0": "0 - Düşük", ...}, "probabilities": {"0": 0.001, ...}, "confidence": 0.92}` |

---

### 2.2. Süreç ve Belge Sınıflarına Göre Detaylı Soru Şablonları ([`DOCUMENT_QUESTION_TEMPLATES`](file:///C:/Users/Osman/Desktop/llm-test/drex_client.py#L754-L1104))

Aşağıdaki 8 ana lojistik süreç şablonu projede doğrudan tanımlıdır ve kendi operasyonlarınıza göre genişletilebilir:

#### 📦 Şablon 1: Sevk İrsaliyesi / POD (Teslimat Kanıtı) & Çok Kanallı Tekilleştirme Filtresi (15 Soru)
1. `q01_is_valid_pod_waybill` (`noul`): Yüklenen görsel bir sohbet ekran görüntüsü veya fatura değil, resmi bir **Sevk / Taşıma İrsaliyesi (POD)** mi?
2. `q02_is_duplicate_across_channels` (`noul`): Bu irsaliye (`#IRS-2026-90412`, plaka `34 TRK 882`), daha önce Mobil Uygulamadan yüklenen `DOC-CANON-90412` kaydının mükerrer (duplicate) kopyası mı?
3. `q03_image_quality_archivable` (`noul`): Belge fotoğrafında bulanıklık, parlamadan dolayı okunamayan alan veya kesik kenar olmadan yasal arşivlemeye uygun mu?
4. `q04_has_shipper_and_origin` (`noul`): Gönderici firma ünvanı (`Marmara Gıda A.Ş.`), vergi dairesi/VKN ve çıkış deposu açıkça okunuyor mu?
5. `q05_has_consignee_and_destination` (`noul`): Alıcı firma ünvanı (`Anadolu Perakende`) ve teslimat adresi/şehri açıkça okunuyor mu?
6. `q06_has_waybill_date_and_dispatch_date` (`noul`): İrsaliye düzenleme tarihi ve fiili sevk tarihi mevzuata uygun şekilde yazılmış mı?
7. `q07_has_truck_and_trailer_plate` (`noul`): Çekici ve dorse plakası (`34 TRK 882 / 34 DRS 19`) ile sürücü ad-soyad/TCKN bilgisi belgede yer alıyor mu?
8. `q08_has_qr_or_gib_ettn_code` (`noul`): e-İrsaliye ise GİB karekodu (QR) ve ETTN numarası mevcut ve okunaklı mı?
9. `q09_has_receiver_wet_signature` (`noul`): Teslim alan depo yetkilisinin adı, soyadı ve ıslak imzası (`Teslim Alan`) kutusunda mevcut mu?
10. `q10_has_official_company_stamp` (`noul`): Alıcı firmanın resmi şirket kaşesi evrak üzerine basılmış mı?
11. `q11_has_damage_or_shortage_note` (`noul`): Evrak üzerinde el yazısıyla düşülmüş bir **"Hasar / Eksik / İade Şerhi"** (`3 Palet Hasarlı / Koli Ezik`) var mı?
12. `q12_delivered_qty_equals_shipped_qty` (`noul`): Sevk edilen 24 paletin tamamı eksiksiz ve sağlam olarak teslim alınmış mı?
13. `q13_primary_document_class` (`choice`): Belgenin ana sınıfı nedir?
    * `sevk_irsaliyesi_pod`: Sevk İrsaliyesi / Teslimat Kanıtı (POD)
    * `tasima_irsaliyesi`: Nakliyeci Taşıma İrsaliyesi
    * `tedarikci_e_fatura`: Ticari e-Fatura / e-Arşiv Fatura
    * `kantar_tartim_fisi`: Kantar Tartım Fişi
    * `otoyol_kopru_dekontu`: Otoyol / HGS / Köprü Geçiş Fişi
    * `surucu_k1_src_belgesi`: Sürücü SRC / Psikoteknik / K1 Yetki Belgesi
14. `q14_dedup_and_ingestion_action` (`choice`): Çok kanallı belge işleme motoru hangi aksiyonu almalı?
    * `deduplicate_link_to_existing_load_and_hold_escrow`: Yeni `.md` çıkarma yapma; mükerrer kopyayı kanonik kayda bağla ve 3 hasarlı palet nedeniyle Escrow ödemesini bloke tut
    * `auto_approve_pod_and_release_escrow`: Tam imzalı/kaşeli hatasız POD; taşıyıcı hak edişini (`48.500 TL`) serbest bırak
    * `request_retake_or_missing_stamp`: İmza/kaşe eksik veya fotoğraf bulanık; şoföre WhatsApp'tan yeniden yükleme bildirimi gönder
15. `q15_document_completeness_score` (`score`): Belgenin resmi ve hukuki tamlık derecesi:
    * `["0 - Geçersiz / Okunamaz", "1 - Eksik İmza veya Kaşe", "2 - İmzalı Ancak Hasar/Eksik Şerhli", "3 - Tam İmzalı, Kaşeli ve Şerhsiz Temiz POD"]`

---

#### 📑 Şablon 2: Depo Mal Kabul 3-Way Matching (PO – İrsaliye – e-Fatura) & KDV Tevkifat Filtresi (14 Soru)
1. `q01_is_commercial_e_invoice` (`noul`): Birincil belge GİB onaylı resmi bir ticari e-Fatura (`#GIB202600091882`) mı?
2. `q02_has_valid_po_reference` (`noul`): Fatura üzerinde sistemdeki onaylı Satınalma Siparişi (`#PO-2026-4401`) referansı yer alıyor mu?
3. `q03_is_duplicate_invoice_submission` (`noul`): WhatsApp'tan gelen bu fatura görüntüsü, daha önce e-posta veya GİB entegrasyonundan alınan `#GIB202600091882` faturasının mükerreri mi?
4. `q04_supplier_vkn_and_iban_matches_master_data` (`noul`): Faturadaki satıcı VKN ve TR IBAN bilgisi ERP tedarikçi ana verisiyle birebir uyuşuyor mu?
5. `q05_billed_qty_matches_wms_good_count` (`noul`): Faturalanan miktar (`1.000 palet`), WMS depo mal kabul sağlam sayımıyla (`850 palet`) eşleşiyor mu?
6. `q06_unit_price_within_2pct_po_contract` (`noul`): Fatura birim fiyatı (`465 TL`), PO sözleşme birim fiyatının (`400 TL`) `%2.0` tolerans limiti içinde mi?
7. `q07_declared_weight_matches_weighbridge` (`noul`): Faturada beyan edilen brüt/net ağırlık (`22.000 kg`), depo kantar fişi net tartımıyla (`18.700 kg`) uyuşuyor mu?
8. `q08_currency_and_fx_rate_compliant` (`noul`): Dövizli fatura ise kullanılan TCMB kur değeri sözleşmedeki fatura günü döviz alış kuruyla uyumlu mu?
9. `q09_vat_rate_is_correct` (`noul`): Ürün/hizmet grubuna göre uygulanan KDV oranı (`%20`) doğru mu?
10. `q10_mandatory_withholding_tax_applied` (`noul`): Taşıma/lojistik hizmetinde zorunlu `2/10` KDV tevkifatı faturada doğru hesaplanıp düşülmüş mü?
11. `q11_requires_debit_memo_for_shortage` (`noul`): 150 eksik palet ve `+65 TL` birim fiyat farkı için tedarikçiye **Fiyat/Miktar Fark Faturası (Debit Memo / İade Faturası)** kesilmeli mi?
12. `q12_document_classification` (`choice`): Belge paketinin sınıfı nedir? (`e_fatura_ve_kantar_3way_paketi`, `sevk_irsaliyesi_pod`, `fiyat_farki_iade_faturasi`, `personel_masraf_fisi`)
13. `q13_erp_ingestion_workflow` (`choice`): SAP / ERP muhasebe entegrasyonu hangi akışı çalıştırmalı?
    * `dedup_merge_and_block_sap_payment`: Mükerrer eki mevcut faturaya bağla, SAP ödemesini bloke et ve otomatik Debit Memo görevi aç
    * `approve_and_schedule_payment`: 3-Way Matching tam uyumlu; faturayı muhasebeleştir ve ödeme vadesine al
    * `route_to_gray_zone_tax_specialist`: Küçük kur/yuvarlama farkı (`<%2`); finans uzmanına yönlendir
14. `q14_financial_compliance_score` (`score`): Faturanın PO, WMS ve vergi mevzuatına uyumluluk skoru:
    * `["0 - Ağır Fiyat/Miktar/Tevkifat İhlali", "1 - Önemli Uyuşmazlık", "2 - Küçük Yuvarlama Farkı", "3 - %100 Tam Uyumlu 3-Way Match"]`

---

#### 📲 Şablon 3: WhatsApp Sohbetinden Yük İlanı Açma (Chat-to-Load) & Kartvizitten CRM Müşteri Kaydı Filtresi (14 Soru)
1. `q01_is_load_creation_request_in_chat` (`noul`): WhatsApp mesajı gerçek bir yük taşıma talebi / araç arayışı içeriyor mu?
2. `q02_has_origin_and_destination_cities` (`noul`): Yükleme noktası (`Gebze OSB`) ve boşaltma noktası (`Çorlu Fabrika`) açıkça belirtilmiş mi?
3. `q03_has_loading_date_and_time_window` (`noul`): Yükleme tarihi ve saati (`Yarın sabah 08:00`) net olarak verilmiş mi?
4. `q04_has_tonnage_and_pallet_count` (`noul`): Yükün tonajı (`22 ton`) ve palet/kap adedi (`33 Euro Palet`) belirtilmiş mi?
5. `q05_has_cargo_commodity_type` (`noul`): Taşınacak yükün cinsi (`Tekstil Kolisi / Kuru Yük / Paletli Gıda`) belli mi?
6. `q06_has_required_trailer_type` (`noul`): İstenen dorse/araç tipi (`13.60 Tenteli Kayar Perde / Frigo / Açık Kasa / Sal Dorse`) açıkça yazılmış mı?
7. `q07_has_target_freight_price_and_payment_term` (`noul`): Teklif edilen hedef navlun tutarı (`18.000 TL + KDV`) ve ödeme vadesi (`Peşin / 30 Gün Vadeli`) belirtilmiş mi?
8. `q08_attached_image_is_business_card` (`noul`): Sohbete eklenen fotoğraf kurumsal bir **Kartvizit (Business Card)** mi?
9. `q09_business_card_has_person_and_title` (`noul`): Kartvizit üzerinde yetkili kişinin adı-soyadı (`Ahmet Yalçın`) ve ünvanı (`Lojistik ve Tedarik Zinciri Müdürü`) okunuyor mu?
10. `q10_business_card_has_phone_and_email` (`noul`): Mobil telefon (`+90 532 418 92 10`) ve kurumsal e-posta (`ayalcin@trakyatekstil.com.tr`) okunaklı mı?
11. `q11_business_card_has_tax_id_vkn` (`noul`): Fatura/sözleşme için gereken Vergi Dairesi ve VKN (`Çorlu VD / VKN: 8590412881`) kartvizitte yer alıyor mu?
12. `q12_primary_bundle_classification` (`choice`): Bu WhatsApp mesaj ve görsel paketinin sınıfı nedir?
    * `whatsapp_yuk_talebi_ve_crm_kartvizit`: WhatsApp Yük İlanı Talebi + Yeni Müşteri Kartviziti (CRM Lead)
    * `sadece_fiyat_sorma_sohbeti`: Eksik bilgili genel fiyat sorma mesajı
    * `komisyon_atlatma_girisimi`: Platform dışı elden ödeme / komisyon atlatma mesajı
13. `q13_orchestration_action` (`choice`): Hangi hibrit otomasyon akışı tetiklenmeli?
    * `trigger_deepseek_extract_load_and_crm_json`: [`deepseek/deepseek-v4.1-flash-1017`](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017)'yi tetikle; Yük Borsası İlan JSON'u + CRM Müşteri JSON'u çıkar ve WhatsApp teyit mesajı gönder
    * `ask_shipper_for_missing_tonnage_or_trailer`: Eksik dorse/tonaj bilgisini müşteriye WhatsApp'tan otomatik sor
    * `discard_as_irrelevant_chat`: Lojistik dışı sohbet; işlem yapma
14. `q14_commercial_readiness_score` (`score`): Talebin doğrudan ilana ve CRM kaydına dönüşmeye hazırlık puanı:
    * `["0 - Alakasız Sohbet", "1 - Çok Eksik Bilgi", "2 - Küçük Eksik (Saat/Tonaj)", "3 - %100 Eksiksiz Yük İlanı + Doğrulanmış VKN Kartvizit"]`

---

#### 🌍 Şablon 4: Uluslararası CMR Taşıma Senedi, Sarp / Verkhniy Lars Gümrük & Türkçe ↔ Rusça Çeviri Filtresi (13 Soru)
1. `q01_contains_international_cmr_waybill` (`noul`): Görselde uluslararası karayolu taşıma sözleşmesi olan **CMR Belgesi (`#TR-RU-88412`)** yer alıyor mu?
2. `q02_has_exporter_and_importer_details` (`noul`): CMR Hane 1 (Gönderici: `Antalya Sera İhracat A.Ş.`) ve Hane 2 (Alıcı: `OOO Moskva Agro Trade - Moskova`) tam mı?
3. `q03_customs_seal_is_intact` (`noul`): Araç gümrük mührü (`#TR-994810` / T1 Transit Mührü) sağlam ve bozulmamış (`SAĞLAM / пломба цела`) olarak mı raporlanmış?
4. `q04_cmr_box18_has_packaging_reservation` (`noul`): CMR 18. hanede taşıyıcının ambalaj/streç film hasarına dair ihtirazi kaydı (`Повреждена стрейч-пленка на 2 паллетах`) var mı?
5. `q05_cargo_boxes_inside_pallets_are_intact` (`noul`): Dış streç filmdeki yırtığa rağmen palet içindeki ürün kolilerinin `%100` sağlam olduğu belirtilmiş mi?
6. `q06_driver_at_verkhniy_lars_border_queue` (`noul`): Sürücünün paylaştığı konum/durum izinsiz bir rota sapması değil, Sarp / Verkhniy Lars sınır kapısındaki resmi gümrük kuyruğu (~6 saat) mu?
7. `q07_reefer_temperature_maintained_at_border` (`noul`): Sınır kapısında beklerken frigo dorse sıcaklığı hedef değerde (`+3.8°C`) sabit tutuluyor mu?
8. `q08_requires_russian_turkish_llm_translation` (`noul`): Rus şoför/gümrük mesajının Türkçeye ve operasyoncunun cevabının Moskova'daki alıcı için Rusçaya (`Русский язык`) çevrilmesi gerekiyor mu?
9. `q09_cmr_box24_consignee_stamp_pending_arrival` (`noul`): Araç henüz sınır kapısında olduğu için CMR 24. hane (Alıcı Teslim Kaşesi) beklendiği üzere henüz boş mu?
10. `q10_delay_qualifies_as_customs_force_majeure` (`noul`): Sınır kapısı yoğunluğundan kaynaklanan 6 saatlik gecikme sözleşmede gümrük mücbir sebebi sayılarak sürücüye geç kalma cezası kesilmemeli mi?
11. `q11_operational_document_classification` (`choice`): Belge ve operasyon paketinin sınıfı nedir? (`uluslararasi_cmr_ve_gumruk_bildirimi`, `yurtici_sevk_irsaliyesi`, `gumruk_ceza_tutanagi`)
12. `q12_operational_decision_routing` (`choice`): Kontrol kulesi hangi aksiyonu almalı?
    * `approve_customs_wait_and_trigger_deepseek_ru_tr_translation`: Sınır beklemesini onayla, ceza uygulama ve [`deepseek/deepseek-v4.1-flash-1017`](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017) ile Rusça ↔ Türkçe resmi alıcı/sürücü çevirisini üret
    * `open_cmr_cargo_damage_claim`: Ürünler tamamen hasarlı; CMR sigorta hasar dosyası aç
    * `penalize_driver_for_route_deviation`: Sürücüye rota sapma cezası uygula
13. `q13_cross_border_risk_score` (`score`): Sınır geçiş ve yük güvenliği risk seviyesi:
    * `["0 - Sorunsuz Transit", "1 - Normal Sınır Kuyruğu & Hafif Dış Streç Yırtığı", "2 - Gümrük Evrak Eksikliği", "3 - Mühür Kırık / Soğuk Zincir İhlali"]`

---

#### 🏭 Şablon 5: Depo (WMS) Rampa Mal Kabul, Yükleme Checklist (`#CHK-551`), Spanzet, İstif & ADR Kontrol Filtresi (14 Soru)
1. `q01_is_warehouse_dock_checklist_or_pallet_photo` (`noul`): WhatsApp'tan gelen görüntü bir Depo Rampa Yükleme/Mal Kabul Checklist formu veya palet kamera görüntüsü mü?
2. `q02_trailer_floor_clean_dry_and_odor_free` (`noul`): Dorse taban temizliği, kuruluğu ve koku kontrolü (`Madde 1`) uygun mu?
3. `q03_reefer_precooling_target_met` (`noul`): Yükleme öncesi frigo dorse ön soğutma sıcaklığı (`+3.8°C` vs `+4.0°C` hedef) uygun mu?
4. `q04_pallet_and_box_count_matches_asn` (`noul`): Rampada sayılan palet (`26 palet`) ve koli adedi (`640 koli`) ASN / sevk emriyle birebir tutuyor mu?
5. `q05_lashing_straps_spanzet_compliant` (`noul`): Araçta iş güvenliği kuralı gereği zorunlu olan **en az 6 adet Spanzet (gerdirme kayışı)** takılmış mı?
6. `q06_dunnage_airbags_installed` (`noul`): Palet aralarındaki boşluklara devrilmeyi önleyici hava yastığı (dunnage bag) yerleştirilmiş mi?
7. `q07_stretch_film_and_corner_boards_tight` (`noul`): Tüm paletlerin streç filmleri ve köşebentleri gevşeklik olmadan sıkıca sarılmış mı?
8. `q08_pallet_wood_base_intact` (`noul`): Euro paletlerin ahşap takoz ve alt tahtalarında kırık veya çivi çıkıntısı yok mu?
9. `q09_undeclared_adr_hazmat_label_detected` (`noul`): ASN'de "Standart Kuru Gıda" beyan edilmesine rağmen palet üzerinde **ADR Tehlikeli Madde (`UN 1263` Yanıcı / Aşındırıcı)** etiketi var mı?
10. `q10_liquid_chemical_spill_on_dock_floor` (`noul`): Palet altında veya rampa zemininde sıvı/kimyasal sızıntısı görülüyor mu?
11. `q11_barcode_gs1_sscc_label_readable` (`noul`): Palet üzerindeki GS1-128 / SSCC barkod etiketi el terminaliyle okunabilir durumda mı?
12. `q12_wms_dock_action` (`choice`): WMS sistemi bu araç/palet için hangi komutu çalıştırmalı?
    * `hold_truck_at_dock_until_4_straps_and_stretch_fixed`: Aracın rampa çıkışını bloke et; 4 ek spanzet takılana ve arka 2 palet streçlenene kadar çıkış izni verme
    * `quarantine_hazmat_pallet_and_alert_safety_team`: Beyan edilmemiş ADR / sızıntılı paleti yüksek rafa kaldırma; Tehlikeli Madde Karantina alanına al
    * `release_truck_and_print_waybill`: Tüm checklist maddeleri tam; rampa çıkış onayı ver ve e-İrsaliyeyi yazdır
13. `q13_non_compliance_root_cause` (`choice`): Tespit edilen uygunsuzluğun ana kaynağı nedir? (`eksik_spanzet_ve_gevsek_strec`, `beyan_edilmeyen_adr_sizinti`, `eksik_koli_sayimi`, `uygunsuzluk_yok`)
14. `q14_cargo_securing_and_safety_risk_score` (`score`): Yük emniyeti ve depo iş güvenliği risk skoru:
    * `["0 - %100 Güvenli Yükleme", "1 - Hafif Streç Gevşekliği", "2 - Yüksek Risk (Eksik Spanzet 2/6 - Devrilme Tehlikesi)", "3 - Kritik Acil Durum (ADR Kimyasal Sızıntı)"]`

---

#### ⛽ Şablon 6: Şoför WhatsApp Yol Masraf Fişleri (Mazot ÖKC, HGS/Otoyol, Kantar, Yemek) & Sefer Harcırah Mahsup Filtresi (12 Soru)
1. `q01_is_driver_road_expense_submission` (`noul`): Görsel, şoförün sefer sonunda WhatsApp'tan gönderdiği yol masraf fişleri (`Mazot, Otoyol, Kantar, Market`) paketi mi?
2. `q02_fuel_receipt_is_valid_okc_slip` (`noul`): 1. fiş resmi bir akaryakıt istasyonu ÖKC (Ödeme Kaydedici Cihaz) motorin fişi (`Opet Pozantı - 14.260 TL`) mi?
3. `q03_fuel_receipt_plate_matches_active_truck` (`noul`): Akaryakıt fişi üzerindeki plaka (`34 KLM 482`), seferdeki aktif çekici plakasıyla (`34 KLM 482`) birebir aynı mı?
4. `q04_fuel_liters_within_route_consumption_norm` (`noul`): İstanbul–Mersin (`940 km`) rotası için alınan `310 litre` motorin (`32.9 lt / 100 km`), ağır vasıta TIR yakıt tüketim normu (`30–36 lt / 100 km`) içinde mi?
5. `q05_highway_and_weighbridge_receipt_valid` (`noul`): 2. fişteki Kuzey Marmara + Niğde Otoyolu (`1.850 TL`) ve Mersin Liman Kantar (`400 TL`) harcamaları sefer güzergahı ve GPS saatleriyle uyumlu mu?
6. `q06_all_receipts_belong_to_same_truck_plate` (`noul`): Gönderilen **tüm fişler** istisnasız aktif çekici plakasına (`34 KLM 482`) mı ait?
7. `q07_contains_other_vehicle_plate_receipt` (`noul`): 3. fişte aktif çekici yerine **başka bir araca ait plaka (`06 YAB 119`)** mı yer alıyor?
8. `q08_contains_pre_trip_or_out_of_date_receipt` (`noul`): Fişler arasında sefer başlangıç tarihinden (`10.11.2026`) daha eski tarihli (`08.11.2026`) bir fiş var mı?
9. `q09_contains_disallowed_personal_items` (`noul`): Fiş içeriğinde şirket harcırah politikası dışı kişisel market/sigara harcaması (`2.450 TL`) bulunuyor mu?
10. `q10_expense_bundle_classification` (`choice`): Şoför masraf paketinin denetim sonucu nedir?
    * `kismi_onay_akaryakit_otoyol_gecerli_market_fisi_red`: Mazot (`14.260 TL`) + Otoyol/Kantar (`2.250 TL`) Onaylı (`16.510 TL`); Farklı Plakalı Market Fişi (`2.450 TL`) Red
    * `tamami_onayli_sefer_masrafi`: Tüm fişler plaka ve rota uyumlu (`18.960 TL` Tam Onay)
    * `tamami_sahte_red`: Tüm fişler sahte/mükerrer
11. `q11_accounting_reimbursement_action` (`choice`): Ön muhasebe ve harcırah sistemi hangi işlemi yapmalı?
    * `approve_16510_tl_deduct_2450_tl_and_notify_via_deepseek`: `16.510 TL`'yi onayla, `2.450 TL` kişisel/farklı plakalı fişi kes ve [`deepseek/deepseek-v4.1-flash-1017`](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017) ile şoföre kalem kalem WhatsApp mahsup tablosu gönder
    * `pay_full_18960_tl`: Kesintisiz `18.960 TL` öde
12. `q12_expense_policy_violation_score` (`score`): Masraf bildirimindeki politika ihlal derecesi:
    * `["0 - Hatasız Bildirim", "1 - Küçük Belge Eksikliği", "2 - Farklı Plaka / Kişisel Market Fişi (Kesinti & Uyarı)", "3 - Sistematik Yakıt/Fiş Suistimali"]`

---

#### 🕵️ Şablon 7: Navlun Hak Ediş, Demuraj (Bekleme) Talebi & Manipüle Edilmiş Mükerrer Fiş (Fraud) Filtresi (12 Soru)
1. `q01_is_expense_or_toll_receipt` (`noul`): Yüklenen belge ekstra bekleme (demuraj) veya otoyol/kantar geri ödemesi için sunulan bir fiş mi?
2. `q02_is_reused_duplicate_from_old_trip` (`noul`): Bu fiş (`#FIS-2025-11049`), arşiv kayıtlarına göre 2025 yılındaki başka bir seferde (`#TRIP-2025-109`) daha önce kullanılmış mükerrer bir fiş mi?
3. `q03_receipt_date_matches_current_trip` (`noul`): Fiş üzerindeki basılı tarih (`14.08.2025`), aktif sefer tarihiyle (`10.11.2026`) eşleşiyor mu?
4. `q04_plate_number_matches_active_truck` (`noul`): Fişteki orijinal basılı plaka (`06 XYZ 44`), el yazısıyla karalanmadan aktif çekici plakasıyla (`34 ABC 901`) uyuşuyor mu?
5. `q05_shows_visual_tampering_or_crossed_text` (`noul`): Fiş görselinde tükenmez kalemle plaka karalaması veya dijital piksel/font manipülasyonu var mı?
6. `q06_gps_waiting_time_exceeds_4_hours` (`noul`): Mobil uygulama GPS poligon verisine göre gerçek bekleme süresi (`45 dakika`), sözleşmedeki 4 saatlik (`240 dakika`) ücretsiz bekleme muafiyetini aştı mı?
7. `q07_demurrage_claim_has_signed_ramp_time_sheet` (`noul`): Talep edilen `6.500 TL` demuraj için alıcı depo sorumlusunun imzaladığı resmi giriş-çıkış saat tutanağı mevcut mu?
8. `q08_base_freight_pod_is_clean` (`noul`): Seferin ana navlun tutarı (`32.000 TL`) için imzalı ve hasarsız teslimat irsaliyesi (POD) mevcut mu?
9. `q09_document_classification` (`choice`): Belge ve talep sınıfı nedir? (`manipule_edilmis_mukerrer_kantar_otoyol_fisi`, `gecerli_demuraj_ve_otoyol_fisi`, `standart_navlun_faturasi`)
10. `q10_automated_pipeline_action` (`choice`): Hak ediş motoru hangi kararı uygulamalı?
    * `pay_base_32000_tl_only_reject_9300_tl_extras_and_flag_fraud`: `32.000 TL` ana navlunu öde; `6.500 TL` haksız demuraj ve `2.800 TL` sahte fiş talebini (`9.300 TL`) reddet ve Fraud uyarısı aç
    * `approve_all_41300_tl`: Tüm talebi (`41.300 TL`) öde
    * `freeze_entire_carrier_account`: Tüm ödemeleri süresiz dondur
11. `q11_carrier_trust_penalty_action` (`choice`): Taşıyıcı puanına hangi yaptırım uygulanmalı? (`deduct_40_trust_points_and_disable_instant_pay`, `no_penalty`, `permanent_blacklist`)
12. `q12_fraud_confidence_level` (`score`): Evrak manipülasyonu ve çifte faturalama suistimal skoru:
    * `["0 - Geçerli Belge", "1 - Sehven Yanlış Yükleme", "2 - Şüpheli Demuraj Talebi", "3 - Kesinleşmiş 2025 Mükerrer & Plakası Karalanmış Fiş Suistimali"]`

---

#### 🏦 Şablon 8: Vadeli Yük Veren / Alt Taşıyıcı Bilanço, Vergi Levhası, Findeks Çek & Faktoring Kredi Risk Filtresi (12 Soru)
1. `q01_tax_certificate_is_active` (`noul`): Vergi levhası ve Ticaret Sicil kaydına göre firma aktif faaliyette mi?
2. `q02_company_age_meets_minimum_policy` (`noul`): Firmanın kuruluş yaşı vadeli açık hesap için gereken minimum 2 yıl şartını karşılıyor mu?
3. `q03_current_ratio_above_1_20` (`noul`): Bilanço özetindeki **Cari Oran (`Current Ratio = 0.68`)**, kredi politikası alt limiti olan `1.20`'nin üzerinde mi?
4. `q04_debt_to_equity_within_limit` (`noul`): Kısa vadeli banka/piyasa borçlarının özsermayeye oranı güvenli sınırlar içinde mi?
5. `q05_requested_credit_within_15pct_annual_revenue` (`noul`): Talep edilen `4.500.000 TL` açık hesap limiti, firmanın yıllık net cirosunun (`10.550.000 TL`) maksimum `%15`'i (`1.582.500 TL`) sınırının altında mı (`%42.6` talep edilmiş)?
6. `q06_zero_bounced_checks_in_last_12_months` (`noul`): Findeks / KKB çek raporuna göre son 12 ayda arkası yazılmış **karşılıksız çek (`3 adet - 1.450.000 TL`)** sayısı sıfır (`0`) mı?
7. `q07_platform_payment_delay_within_5_days` (`noul`): Firmanın platformdaki geçmiş ortalama ödeme gecikmesi (`18 gün`), maksimum tolerans olan `5 gün` içinde mi?
8. `q08_has_bank_letter_of_guarantee` (`noul`): Firma talep ettiği açık hesap limiti için kesin ve süresiz **Banka Teminat Mektubu (DBS / Teminat)** sunmuş mu?
9. `q09_eligible_for_carrier_early_payout_factoring` (`noul`): Bu yük verenin ilanını taşıyan nakliyecilere platform üzerinden "Erken Ödeme / Faktoring" kullandırılması finansal açıdan güvenli mi?
10. `q10_credit_committee_decision` (`choice`): Kredi ve risk motoru hangi kararı vermeli?
    * `reject_open_account_require_prepayment_or_bank_guarantee`: `4.5M TL` açık hesabı reddet; sadece Peşin Havale, Kredi Kartı Blokesi veya Doğrudan Borçlandırma Sistemi (DBS / Banka Teminat Mektubu) ile ilan açmasına izin ver
    * `approve_capped_credit_limit_1_2m_tl`: Kısmi teminatla `1.200.000 TL` sınırlandırılmış limit onayla
    * `approve_full_4_5m_tl_open_account`: `4.500.000 TL` vadeli açık hesabı onayla
11. `q11_factoring_pricing_tier` (`choice`): Faktoring / erken ödeme risk primi hangi dilimden uygulanmalı? (`blocked_high_default_risk`, `tier_3_high_spread`, `tier_1_prime_rate`)
12. `q12_default_risk_rating` (`score`): 90 gün içinde temerrüde düşme (ödememe) risk derecesi:
    * `["0 - Prime (AAA)", "1 - Düşük Risk", "2 - Orta/Gri Alan Risk", "3 - Çok Yüksek Temerrüt Riski (Karşılıksız Çek & Cari Oran < 1.0)"]`

---

## 💻 3. API İstek Formatı ve Çoklu Soru Kod Örneği (Python)

Görsel (`image_url`) + JSON bağlamını tek bir `state` listesinde birleştirip aynı anda onlarca soruyu (`noul`, `choice`, `score`) sormak için kullanılan standart yapı:

```python
import base64
import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 1. Belge görselini Base64 Data URL'e çevir (veya doğrudan URL'den belleğe çek)
img_b64 = base64.b64encode(Path("samples/whatsapp_load_and_business_card.png").read_bytes()).decode("utf-8")

# 2. Üst düzey `state` dizisine WhatsApp yazışma bağlamını + görseli ekle
payload = {
    "model": "nace-ai/drex-max",
    "state": [
        json.dumps({
            "channel": "WhatsApp Operasyon Grubu",
            "sender": "+90 532 418 92 10",
            "message": "Yarın 08:00 Gebze OSB -> Çorlu 22 ton 33 EP tekstil kolisi, 13.60 Kayar Perde, 18.000 TL + KDV. Kartvizitimi de ekte attım CRM'e kaydedersiniz."
        }, ensure_ascii=False),
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img_b64}"}
        }
    ],
    "questions": {
        "q01_is_load_creation_request": {
            "type": "noul",
            "instructions": "Does the WhatsApp message contain a valid freight shipment request (Gebze OSB -> Çorlu)?"
        },
        "q02_has_tonnage_and_trailer_type": {
            "type": "noul",
            "instructions": "Are both tonnage (22 tons / 33 Euro Pallets) and trailer type (13.60 Tenteli Kayar Perde) specified?"
        },
        "q03_attached_image_is_business_card_with_vkn": {
            "type": "noul",
            "instructions": "Does the attached image show a corporate Business Card containing a valid Turkish Tax ID (VKN: 8590412881)?"
        },
        "q04_orchestration_action": {
            "type": "choice",
            "instructions": "Which hybrid pipeline action should execute?",
            "criteria": {
                "trigger_deepseek_extract_load_and_crm_json": "Trigger DeepSeek V4.1 Flash to extract Load Board JSON + CRM Lead JSON",
                "ask_for_missing_details": "Ask shipper for missing load details",
                "ignore_chat": "Ignore irrelevant chat message"
            }
        },
        "q05_commercial_readiness_score": {
            "type": "score",
            "instructions": "Rate how complete this request is for automated Load Board publishing and CRM onboarding.",
            "criteria": ["0 - Unusable", "1 - Partial", "2 - Minor Missing Field", "3 - 100% Complete Load + Verified VKN Business Card"]
        }
    }
}

resp = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
    json=payload,
    timeout=30,
)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
```

---

## 🔗 4. İş Modelinde Kullanılan Araçlar (OpenRouter Model Bağlantıları)

| Rol / Katman | Model Bağlantısı | Girdi / Çıktı | Kullanım Amacı |
|---|---|---|---|
| **System-1 Genel & Saha Karar Motoru** | **[`nace-ai/drex-max`](https://openrouter.ai/nace-ai/drex-max)** | Metin, JSON, Görsel (4 adede kadar) ➔ `noul`, `choice`, `score` olasılıkları (`0 output token`) | WMS rampa kabul, POD irsaliye, CMR, yük borsası eşleştirme, belge sınıflandırma & tekilleştirme |
| **System-1 Lojistik Finans Karar Motoru** | **[`nace-ai/drex-max-finance`](https://openrouter.ai/nace-ai/drex-max-finance)** | Metin, JSON, Görsel ➔ `noul`, `choice`, `score` olasılıkları (`0 output token`) | 3-Way Matching, e-Fatura KDV/Tevkifat, demuraj & fiş sahteciliği, şoför harcırah mahsubu, kredi/faktoring riski |
| **System-2 Üretken LLM, Çeviri & Senaryo Sentezleyici** | **[`deepseek/deepseek-v4.1-flash-1017`](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017)** | Metin + Görsel (1M Context) ➔ Yapılandırılmış JSON & Çok Dilli Metin | Dinamik WhatsApp sohbet & soru üretimi, Sohbetten Yük/CRM JSON çıkarma, Türkçe ↔ Rusça CMR/Gümrük çevirisi, tutanak yazımı |
| **System-1 Hafif Metin/JSON Karar Motorları** | **[`nace-ai/drex-v2.0`](https://openrouter.ai/nace-ai/drex-v2.0)** / **[`nace-ai/drex-v1.5`](https://openrouter.ai/nace-ai/drex-v1.5)** | Metin, JSON ➔ `noul`, `choice`, `score` | Yüksek hacimli metin/JSON ön filtreleme ve sohbet moderasyonu |

---

## 🧪 5. Projede Yer Alan 17 Hazır Simülasyon Senaryosu

### A. Çok Kanallı Belge & WhatsApp Operasyon Sınıflandırma Senaryoları (5 Adet)
1. 🗂️ **[Çok Kanallı Tekilleştirme + 13 Soru] WhatsApp, E-Posta & Mobil İrsaliye Sınıflandırma** ([`omnichannel_whatsapp_email_bundle.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/omnichannel_whatsapp_email_bundle.png))
2. 📑 **[Çok Kanallı e-Fatura + 12 Soru] E-Posta & WhatsApp Fatura Tekilleştirme ve 3-Way Filtresi** ([`finance_3way_matching.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_3way_matching.png))
3. 📲 **[WhatsApp Operasyon + 12 Soru] Sohbetten Yük İlanı Açma & Kartvizitten CRM Kaydı** ([`whatsapp_load_and_business_card.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/whatsapp_load_and_business_card.png))
4. 🌍 **[Uluslararası CMR + Depo Checklist] TR-RU Sınır Kapısı & Rampa Spanzet Denetimi (11 Soru)** ([`whatsapp_cmr_and_warehouse_checklist.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/whatsapp_cmr_and_warehouse_checklist.png))
5. ⛽ **[Şoför Yol Masraf Fişleri + 9 Soru] Mazot ÖKC, Otoyol, Kantar vs Farklı Plakalı Market Fişi** ([`whatsapp_driver_road_expenses.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/whatsapp_driver_road_expenses.png))

### B. Lojistik Finans (`nace-ai/drex-max-finance`) Senaryoları (5 Adet)
6. 📑 **Depo Mal Kabul Üçlü Eşleştirme (3-Way Matching: PO – İrsaliye – e-Fatura)** ([`finance_3way_matching.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_3way_matching.png))
7. 🕵️ **Navlun Hak Ediş, Demuraj (Bekleme) & Sahte Kantar/Otoyol Fişi Denetimi** ([`finance_demurrage_receipt_fraud.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_demurrage_receipt_fraud.png))
8. ⚖️ **Hasarlı Kargo & Sigorta Rücu (Subrogation) Triyajı (3 Görsel Birden)**
9. 🏦 **Vadeli Yük Veren (Açık Hesap) & Faktoring Kredi Risk Skorlaması** ([`finance_credit_balance_sheet.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/finance_credit_balance_sheet.png))
10. 🧭 **Çoklu Ajan (Multi-Agent) "System One" Ön Yönlendirici (Gri Alan Gatekeeper)**

### C. Depo (WMS), Lojistik & Mobil Yük Borsası (`nace-ai/drex-max`) Senaryoları (5 Adet)
11. 🚚 **Mobil Yük Borsası — Sevk İrsaliyesi (POD) & Escrow Denetimi** ([`logistics_pod_waybill.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/logistics_pod_waybill.png))
12. 🏭 **Depo (WMS) Rampa Kabul — Hasarlı Palet & Beyan Edilmemiş ADR Tespiti** ([`warehouse_damaged_pallet.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/warehouse_damaged_pallet.png))
13. 📱 **Mobil Yük Borsası — İlan Şartları (-18°C Frigo & 5M Sigorta) vs Taşıyıcı Teklifi Kalkanı** ([`mobile_load_board_ui.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/mobile_load_board_ui.png))
14. ❄️ **Soğuk Zincir (Frigo) IoT Telemetri Grafiği & Acil Soğuk Depo Yönlendirmesi** ([`cold_chain_telemetry.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/cold_chain_telemetry.png))
15. 🤖 **Mobil Yük Borsası — LLM Öncesi Sohbet & Komisyon Atlatma (Fraud) Kalkanı** (JSON State)

### D. Genel Kurumsal Senaryolar (2 Adet)
16. 🧾 **Kurumsal Bulut Faturası Mükerrer Kalem Denetimi** ([`invoice_audit.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/invoice_audit.png))
17. 🌐 **Tarayıcı Ajanı (Computer Use) 504 Ödeme Hatası Navigasyonu** ([`ui_checkout_error.png`](file:///C:/Users/Osman/Desktop/llm-test/samples/ui_checkout_error.png))

---

## 🛠️ 6. Kurulum ve Çalıştırma

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. .env dosyasını oluşturun
cp .env.example .env
# OPENROUTER_API_KEY=sk-or-v1-... anahtarınızı ekleyin

# 3. Dinamik Akış & Diyagram Stüdyosu Web Uygulamasını başlatın (http://localhost:8080)
python app.py

# 4. Türkiye WhatsApp/E-Posta Operasyon Karar Anları + DeepSeek V4.1 Flash (TR<->RU Çeviri, Yük & CRM, Rampa Checklist, Yol Fişleri)
python whatsapp_deepseek_ops_sim.py

# 5. Çok Kanallı (WhatsApp + E-Posta + Mobil) Belge Tekilleştirme & 10-13 Soruluk Sınıflandırma Simülatörü
python omnichannel_doc_classifier_sim.py

# 6. Drex Max Finance & Olasılık/Varyasyon (Yeşil/Gri/Kırmızı Hat) Simülatörü
python finance_variations_sim.py

# 7. 4-Katmanlı Hibrit (System-1 Drex Max + System-2 DeepSeek V4.1 Flash) Lojistik Orkestrasyon Simülatörü
python logistics_pipeline_sim.py

# 8. Tüm 17 Görsel & JSON Senaryosunun Benchmark Testi
python cli_demo.py
```
