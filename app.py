"""
Nace.AI Drex Max & Drex Max Finance - Interactive Multimodal Decision Playground,
Probability/Variation Lab (System-One Pre-Router) & 4-Layer Logistics Simulator.

Run with:
    python app.py
Then open http://localhost:8080 in your browser.
"""

from __future__ import annotations

import concurrent.futures
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dotenv import load_dotenv

from drex_client import (
    ENDPOINTS,
    SUPPORTED_MODELS,
    encode_image_to_data_url,
    evaluate_decision,
    execute_dynamic_flow_run,
    fetch_remote_image_to_data_url,
    generate_dynamic_simulation_with_deepseek,
    get_presets,
    run_hybrid_logistics_pipeline,
    run_omnichannel_doc_classifier_pipeline,
    run_probability_variation_matrix,
    run_whatsapp_operations_and_deepseek_pipeline,
    search_web_document_images,
)
from sample_generator import SAMPLES_DIR, ensure_sample_images

load_dotenv(Path(__file__).parent / ".env")

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nace.AI Drex Max & Drex Max Finance — Lojistik Finans & WMS Karar Playground</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background-color: #0b0f19; color: #e2e8f0; font-family: Inter, system-ui, -apple-system, sans-serif; }
    .glass { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.65); }
    .prob-bar { transition: width 0.55s cubic-bezier(0.16, 1, 0.3, 1); }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
  </style>
</head>
<body class="min-h-screen pb-16">
  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-950/90 sticky top-0 z-30 backdrop-blur">
    <div class="max-w-7xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-sky-600 flex items-center justify-center font-bold text-white shadow-lg shadow-emerald-500/20">
          DF
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <h1 class="text-lg font-bold text-white tracking-tight">Logi-Playground — Lojistik Operasyon, Mobil Yük Borsası, Depo (WMS) & Finans Simülatörü</h1>
            <a href="https://openrouter.ai/nace-ai/drex-max-finance" target="_blank" class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-400 border border-emerald-500/30 font-medium">nace-ai/drex-max-finance ↗</a>
            <a href="https://openrouter.ai/nace-ai/drex-max" target="_blank" class="text-xs px-2 py-0.5 rounded-full bg-sky-500/15 hover:bg-sky-500/25 text-sky-400 border border-sky-500/30 font-medium">nace-ai/drex-max ↗</a>
            <a href="https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017" target="_blank" class="text-xs px-2 py-0.5 rounded-full bg-cyan-500/15 hover:bg-cyan-500/25 text-cyan-300 border border-cyan-500/30 font-medium">deepseek/deepseek-v4.1-flash-1017 ↗</a>
          </div>
          <p class="text-xs text-slate-400">Dinamik Akış & Diyagram Stüdyosu (▶ RUN) • İnternetten Canlı Belge Çekme • DeepSeek Otomatik Sohbet/Soru Üretimi • TR↔RU Çeviri • 3-Way Matching</p>
        </div>
      </div>
      <div class="flex items-center gap-2.5 text-xs flex-wrap">
        <div id="apiKeyStatus" class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
          API Key kontrol ediliyor...
        </div>
        <a href="https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017" target="_blank" class="px-3 py-1.5 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 transition font-semibold">
          DeepSeek V4.1 Flash ↗
        </a>
        <a href="https://openrouter.ai/nace-ai/drex-max-finance" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-500/40 text-emerald-300 transition">
          Drex Max Finance ↗
        </a>
        <a href="https://openrouter.ai/nace-ai/drex-max" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition">
          Drex Max ↗
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 pt-6 space-y-6">
    <!-- MASTER STUDIO: Dynamic Flow & Diagram Builder + Web Document Fetch + DeepSeek Chat/Question Synthesis + RUN -->
    <section class="glass rounded-2xl p-6 border-2 border-cyan-500/50 bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950/30 shadow-2xl shadow-cyan-950/30 space-y-5">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-xs font-bold uppercase tracking-wider">⚡ DİNAMİK AKIŞ & DİYAGRAM STÜDYOSU</span>
            <h2 class="text-base font-bold text-white">Lojistik Operasyon + Yük Borsası + Depo (WMS) Uçtan Uca Canlı Akış Tasarımcısı</h2>
          </div>
          <p class="text-xs text-slate-300 mt-1">
            <b>1)</b> İnternetten canlı belge arayın veya doğrudan bir belge URL'si çekin (dosya yüklemeden) •
            <b>2)</b> <a href="https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017" target="_blank" class="text-cyan-400 underline">DeepSeek V4.1 Flash</a> ile gerçekçi WhatsApp/E-posta operasyon sohbeti ve belgeye özel karar soruları üretin •
            <b>3)</b> <b>▶ AKIŞI ÇALIŞTIR (RUN)</b> ile 6 düğümlü diyagramı canlı koşturun!
          </p>
        </div>
        <button onclick="runDynamicFlowSimulation()" id="btnRunDynamicFlow" class="px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-extrabold text-sm shadow-lg shadow-emerald-500/25 transition flex items-center gap-2">
          <span>▶ AKIŞI ÇALIŞTIR (RUN SIMULATION)</span>
        </button>
      </div>

      <!-- Control Bar: Left = Web Document Search & Direct URL Fetch | Right = DeepSeek Chat & Question Synthesizer -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <!-- Box A: Direct Internet Document Search & URL Ingestion -->
        <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-sky-300 uppercase tracking-wider">🌐 1. İnternetten Belge Ara veya Doğrudan URL'den Çek (Yüklemesiz)</span>
            <span id="remoteFetchStatus" class="text-[11px] font-mono text-slate-400">Hazır</span>
          </div>

          <!-- Search Input -->
          <div class="flex flex-wrap gap-2">
            <input id="webDocSearchInput" type="text" value="sevk irsaliyesi ornegi" onkeydown="if(event.key==='Enter') searchWebDocuments()" placeholder="Örn: sevk irsaliyesi ornegi, cmr belgesi, e-fatura, kantar fisi..." class="flex-1 min-w-[180px] rounded-lg bg-slate-950 border border-slate-700 px-3 py-1.5 text-xs text-white focus:outline-none focus:border-sky-500" />
            <button onclick="searchWebDocuments()" class="px-3 py-1.5 rounded-lg bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-500/40 text-xs font-semibold whitespace-nowrap">
              🔍 Web'de Ara
            </button>
            <button onclick="openGoogleImagesTab()" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs whitespace-nowrap" title="Aramayı Google Görseller'de yeni sekmede aç">
              🌐 Google Görseller ↗
            </button>
          </div>

          <!-- Direct URL Paste Input -->
          <div class="flex gap-2">
            <input id="directImageUrlInput" type="text" placeholder="Herhangi bir internet belge/fotoğraf URL'si yapıştırın (https://...)" class="flex-1 rounded-lg bg-slate-950 border border-slate-700 px-3 py-1.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-emerald-500" />
            <button onclick="pullRemoteImageUrl()" class="px-3 py-1.5 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-semibold whitespace-nowrap">
              🔗 URL'den Çek & Bağla
            </button>
          </div>

          <!-- Web Search Results Grid with Image Previews, Open in New Tab & Remove Irrelevant Button -->
          <div id="webSearchResultsGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5 max-h-64 overflow-y-auto pt-1 pr-1"></div>
        </div>

        <!-- Box B: DeepSeek V4.1 Flash Dynamic Chat & Question Generator -->
        <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-cyan-300 uppercase tracking-wider">✨ 2. DeepSeek V4.1 Flash ile Dinamik Sohbet & Soru Filtresi Üret</span>
            <a href="https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017" target="_blank" class="text-[11px] font-mono text-cyan-400 hover:underline">deepseek/deepseek-v4.1-flash-1017 ↗</a>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <select id="dynamicDomainSelect" class="rounded-lg bg-slate-950 border border-slate-700 px-3 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-500">
              <option value="yuk_borsasi_ve_crm">📲 Yük Borsası İlan Açma & CRM Kartvizit</option>
              <option value="cmr_gumruk_ru_tr">🌍 Uluslararası CMR, Sarp/Rusya Gümrük & TR↔RU Çeviri</option>
              <option value="depo_wms_checklist">🏭 Depo (WMS) Rampa Kabul & Yükleme Checklist</option>
              <option value="finans_3way_demuraj">📑 Lojistik Finans 3-Way Matching & Demuraj</option>
              <option value="sofor_konum_masraf">⛽ Şoför Canlı Konum & Yol Masraf Fişleri Mahsubu</option>
            </select>
            <input id="dynamicCustomInstruction" type="text" placeholder="Özel senaryo isteği (örn: Şoför Sarp sınırda, 2 palet ıslak, Rusça çeviri lazım...)" class="rounded-lg bg-slate-950 border border-slate-700 px-3 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-500" />
          </div>

          <div class="flex items-center justify-between gap-2 pt-1">
            <p class="text-[11px] text-slate-400">Seçili belgeyi ve süreci inceleyip otomatik <b>WhatsApp yazışması + 8 karar sorusu</b> üretir:</p>
            <button onclick="generateDynamicScenarioWithDeepSeek()" id="btnGenerateDeepSeekScenario" class="px-3.5 py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-200 border border-cyan-500/40 text-xs font-bold whitespace-nowrap transition">
              ✨ DeepSeek ile Sohbet & Soruları Üret
            </button>
          </div>

          <!-- Preview of Active Chat Transcript -->
          <div id="dynamicChatTranscriptBox" class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 max-h-28 overflow-y-auto text-[11px] space-y-1 text-slate-300">
            <div class="text-slate-500 italic">Henüz dinamik sohbet üretilmedi veya mevcut senaryo aktif. Yukarıdan "✨ DeepSeek ile Sohbet & Soruları Üret" butonuna tıklayabilir veya doğrudan "▶ AKIŞI ÇALIŞTIR" diyebilirsiniz.</div>
          </div>
        </div>
      </div>

      <!-- 6-Node Interactive Visual Pipeline Diagram -->
      <div class="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-white uppercase tracking-wider">📊 Canlı Operasyon Akış Diyagramı (6 Düğümlü Mimari — Çalıştırmak İçin ▶ RUN Butonuna Basın)</span>
          <span id="flowDiagramStatus" class="text-xs font-mono text-emerald-400">● Çalışmaya Hazır</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-2.5" id="visualFlowNodes">
          <div id="fnode_1" class="p-3 rounded-xl bg-slate-900 border border-slate-700 flex flex-col justify-between transition">
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-sky-400 mb-1"><span>DÜĞÜM 1</span><span id="fnode_1_badge">HAZIR</span></div>
              <div class="text-xs font-bold text-white">📥 Çok Kanallı Girdi</div>
              <p class="text-[11px] text-slate-400 mt-1">WhatsApp / E-Posta / Web URL Belgesi</p>
            </div>
            <div id="fnode_1_meta" class="text-[10px] font-mono text-slate-400 mt-2 pt-1.5 border-t border-slate-800">Görsel & Metin Bağlamı</div>
          </div>

          <div id="fnode_2" class="p-3 rounded-xl bg-slate-900 border border-slate-700 flex flex-col justify-between transition">
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-cyan-400 mb-1"><span>DÜĞÜM 2</span><span id="fnode_2_badge">HAZIR</span></div>
              <div class="text-xs font-bold text-white">🎯 Soru Filtresi</div>
              <p class="text-[11px] text-slate-400 mt-1">Belgeye Özel `noul`, `choice`, `score`</p>
            </div>
            <div id="fnode_2_meta" class="text-[10px] font-mono text-slate-400 mt-2 pt-1.5 border-t border-slate-800">Dinamik Soru Şablonu</div>
          </div>

          <div id="fnode_3" class="p-3 rounded-xl bg-slate-900 border border-slate-700 flex flex-col justify-between transition">
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-emerald-400 mb-1"><span>DÜĞÜM 3</span><span id="fnode_3_badge">SYSTEM-1</span></div>
              <div class="text-xs font-bold text-white">⚡ Drex Max Karar</div>
              <p class="text-[11px] text-slate-400 mt-1">Tek Geçişte Kalibre Olasılık (0 Token)</p>
            </div>
            <div id="fnode_3_meta" class="text-[10px] font-mono text-slate-400 mt-2 pt-1.5 border-t border-slate-800">nace-ai/drex-max-finance</div>
          </div>

          <div id="fnode_4" class="p-3 rounded-xl bg-slate-900 border border-slate-700 flex flex-col justify-between transition">
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-amber-400 mb-1"><span>DÜĞÜM 4</span><span id="fnode_4_badge">PRE-ROUTER</span></div>
              <div class="text-xs font-bold text-white">🛡️ Gatekeeper Kapısı</div>
              <p class="text-[11px] text-slate-400 mt-1">Yeşil Onay / Gri Alan / Kırmızı Bloke</p>
            </div>
            <div id="fnode_4_meta" class="text-[10px] font-mono text-slate-400 mt-2 pt-1.5 border-t border-slate-800">Olasılık Eşik Denetimi</div>
          </div>

          <div id="fnode_5" class="p-3 rounded-xl bg-slate-900 border border-slate-700 flex flex-col justify-between transition">
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-cyan-300 mb-1"><span>DÜĞÜM 5</span><span id="fnode_5_badge">SYSTEM-2 LLM</span></div>
              <div class="text-xs font-bold text-white">🧠 DeepSeek V4.1 Flash</div>
              <p class="text-[11px] text-slate-400 mt-1">İlan/CRM JSON, TR↔RU Çeviri, Tutanak</p>
            </div>
            <div id="fnode_5_meta" class="text-[10px] font-mono text-slate-400 mt-2 pt-1.5 border-t border-slate-800">deepseek-v4.1-flash-1017</div>
          </div>

          <div id="fnode_6" class="p-3 rounded-xl bg-slate-900 border border-slate-700 flex flex-col justify-between transition">
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-fuchsia-400 mb-1"><span>DÜĞÜM 6</span><span id="fnode_6_badge">GUARDRAIL</span></div>
              <div class="text-xs font-bold text-white">🔒 Çıktı Denetimi & DB</div>
              <p class="text-[11px] text-slate-400 mt-1">WMS / Yük Borsası / SAP ERP Commit</p>
            </div>
            <div id="fnode_6_meta" class="text-[10px] font-mono text-slate-400 mt-2 pt-1.5 border-t border-slate-800">Halüsinasyon Kalkanı</div>
          </div>
        </div>

        <!-- Output of the Dynamic Flow Run -->
        <div id="dynamicFlowRunOutput" class="hidden pt-3 border-t border-slate-800"></div>
      </div>
    </section>
    <!-- LAB 1: Probability, Variation & Gray-Zone Pre-Router Matrix (drex-max-finance) -->
    <section class="glass rounded-2xl p-5 border-emerald-500/40">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold">OLASILIK & VARYASYON LABORATUVARI</span>
            <h2 class="text-base font-bold text-white">🎛️ Drex Max Finance: Olasılık Dağılımı, Varyasyon & "System One" Ön Yönlendirici (Pre-Router) Matrisi</h2>
          </div>
          <p class="text-xs text-slate-400 mt-1">
            Aynı operasyonel kural setine karşı <b>3 farklı varyasyonu (Yeşil Hat: Tam Uyumlu / Gri Alan: Sınırda & Çelişkili / Kırmızı Hat: Sahtecilik & İhlal)</b> paralel koşturur.
            Rutin evrakların %85-90'ını doğrudan DB'ye yazarken, yalnızca <b>Gri Alan (0.32–0.68 olasılık bandı)</b> dosyalarını üst katman Reasoning LLM ajanına devreder.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
        <button onclick="runVariationMatrix('3way_matching')" class="p-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-emerald-500 text-left transition">
          <div class="text-xs font-bold text-emerald-400 mb-1">📑 Varyasyon Testi 1: Depo 3-Way Matching (PO – İrsaliye – e-Fatura)</div>
          <p class="text-[11px] text-slate-400">Tam Eşleşme vs +%1.95 Kur Yuvarlama & 4 Nemli Palet (Gri Alan) vs 150 Eksik Palet & +%16.2 Fiyat Aşımı varyasyonlarını karşılaştırır.</p>
        </button>
        <button onclick="runVariationMatrix('pod_demurrage_fraud')" class="p-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-amber-500 text-left transition">
          <div class="text-xs font-bold text-amber-400 mb-1">🕵️ Varyasyon Testi 2: Navlun Hak Ediş, POD & Demuraj / Sahte Fiş</div>
          <p class="text-[11px] text-slate-400">Temiz POD vs GPS Tünel Kaybı & Silik Kaşe (Gri Alan) vs 2025 Tarihli Oynanmış Kantar Fişi varyasyonlarını karşılaştırır.</p>
        </button>
        <button onclick="runVariationMatrix('credit_factoring_risk')" class="p-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-sky-500 text-left transition">
          <div class="text-xs font-bold text-sky-400 mb-1">🏦 Varyasyon Testi 3: Vadeli Yük Veren & Faktoring Kredi Risk</div>
          <p class="text-[11px] text-slate-400">Kurumsal Prime Firma vs Sınırda Cari Oran 1.18 & Kısmi Teminat (Gri Alan) vs 3 Karşılıksız Çek & Cari Oran 0.68 varyasyonlarını karşılaştırır.</p>
        </button>
      </div>

      <div id="variationMatrixOutput" class="hidden"></div>
    </section>

    <!-- LAB 2: 4-Layer Hybrid Logistics Pipeline Simulator -->
    <section class="glass rounded-2xl p-5 border-sky-500/40">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-bold">4-KATMANLI HİBRİT MİMARİ</span>
            <h2 class="text-base font-bold text-white">🚛 Mobil Yük Borsası, Finans & WMS: System-1 (Drex Max Finance) + System-2 (LLM) Orkestrasyonu</h2>
          </div>
          <p class="text-xs text-slate-400 mt-1">
            <b>Katman 1 (Drex Max / Finance):</b> Görsel + JSON durumunu puanlar ➔
            <b>Katman 2 (Mikroservis):</b> Güven ≥ %80 ise ERP/Escrow işlemini tetikler ➔
            <b>Katman 3 (Üretken LLM):</b> Bildirimi yazar ➔
            <b>Katman 4 (Drex Max Guardrail):</b> LLM mesajını denetler.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-3 mb-4">
        <button onclick="runHybridPipeline('wms_3way_matching')" class="p-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-emerald-500 text-left transition">
          <div class="text-xs font-bold text-emerald-400 mb-1">📑 Akış A: [Drex Max Finance] 3-Way Matching</div>
          <p class="text-[11px] text-slate-400">PO + WMS + e-Fatura görselini inceleyip 150 eksik palet ve +%16 fiyat farkı için SAP blokajı ve tedarikçi ihtarı üretir.</p>
        </button>
        <button onclick="runHybridPipeline('pod_dispute')" class="p-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-sky-500 text-left transition">
          <div class="text-xs font-bold text-sky-400 mb-1">📄 Akış B: [Drex Max Finance] POD & Escrow Bloke</div>
          <p class="text-[11px] text-slate-400">Sevk irsaliyesindeki "3 Palet Hasarlı" şerhini yakalar, 48.500 TL ödemeyi bloke eder ve sürücü bildirimini üretir.</p>
        </button>
        <button onclick="runHybridPipeline('wms_hazmat_dock')" class="p-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-amber-500 text-left transition">
          <div class="text-xs font-bold text-amber-400 mb-1">🏭 Akış C: WMS Rampa — Beyan Edilmemiş ADR</div>
          <p class="text-[11px] text-slate-400">Rampa kamerasındaki UN 1263 Yanıcı ADR etiketini ve sızıntıyı tespit eder, yüksek rafa kaldırmayı engelleyip karantina emri verir.</p>
        </button>
        <button onclick="runHybridPipeline('load_board_matching')" class="p-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-indigo-500 text-left transition">
          <div class="text-xs font-bold text-indigo-400 mb-1">📱 Akış D: Yük Borsası — Frigo & Sigorta Kalkanı</div>
          <p class="text-[11px] text-slate-400">-18°C Donuk Deniz Ürünleri ilanına "Tenteli Araç" ve yetersiz sigortayla gelen teklifi reddeder.</p>
        </button>
      </div>

      <div id="hybridPipelineOutput" class="hidden"></div>
    </section>

    <!-- NEW: Omnichannel Document Deduplication & 10-13 Question Classification Filter Section -->
    <section class="glass rounded-2xl p-5 border border-fuchsia-500/30 bg-gradient-to-br from-slate-900/95 via-fuchsia-950/20 to-slate-900/95">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 rounded bg-fuchsia-500/20 text-fuchsia-300 border border-fuchsia-500/40 text-[10px] font-bold uppercase tracking-wider">YENİ • OMNICHANNEL BELGE MOTORU</span>
            <h2 class="text-sm font-bold text-white uppercase tracking-wider">🗂️ Çok Kanallı (WhatsApp + E-Posta + Mobil) Belge Tekilleştirme & 10-13 Soruluk Sınıflandırma Filtresi</h2>
          </div>
          <p class="text-xs text-slate-300 mt-1">
            WhatsApp, E-Posta ve Mobil Yük Borsası'ndan gelen evrakları <b>normal LLM ile <code>.md</code> (Markdown) metne dönüştürmek yerine</b>;
            tek bir <code>forward pass</code> içinde <b>(1) Kross-kanal tekilleştirme (deduplication)</b> yapar, <b>(2) Belge sınıfını belirler</b> ve <b>(3) Belge tipine özel 10-13 denetim sorusunu</b> aynı anda yanıtlar (<code>0 output token</code>).
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
        <button onclick="runOmnichannelClassify('whatsapp_email_pod_dedup')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-fuchsia-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-fuchsia-300">📲 Paket 1: WhatsApp + E-Posta + Mobil POD Tekilleştirme</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-fuchsia-500/20 text-fuchsia-300 font-mono">13 SORU</span>
          </div>
          <p class="text-[11px] text-slate-400">Aynı sefere (#IST-ANK-88421) ait 3 kanaldan gelen mükerrer Sevk İrsaliyesi + Kantar Fişi görsellerini tekilleştirir ve 13 soruluk POD denetiminden geçirir.</p>
        </button>

        <button onclick="runOmnichannelClassify('email_portal_efatura_dedup')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-emerald-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-emerald-300">📧 Paket 2: E-Posta + GİB + WhatsApp e-Fatura Tekilleştirme</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">12 SORU</span>
          </div>
          <p class="text-[11px] text-slate-400">E-posta PDF'i, GİB Portal ve WhatsApp'tan gelen #GIB2026000009481 faturasını tekilleştirir ve 12 soruluk 3-Way Matching denetiminden geçirir.</p>
        </button>

        <button onclick="runOmnichannelClassify('whatsapp_demurrage_receipt_dedup')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-amber-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-amber-300">🧾 Paket 3: WhatsApp + Mobil Demuraj & Fiş Fraud Filtresi</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono">10 SORU</span>
          </div>
          <p class="text-[11px] text-slate-400">WhatsApp ve Mobil Uygulamadan çifte gönderilen 11.400 TL bekleme faturası ve otoyol fişini tekilleştirir ve 10 soruluk suistimal filtresinden geçirir.</p>
        </button>
      </div>

      <div id="omnichannelOutput" class="hidden"></div>
    </section>

    <!-- NEW: Turkish WhatsApp/Email Operational Decision Moments + DeepSeek V4.1 Flash Hybrid Section -->
    <section class="glass rounded-2xl p-5 border border-cyan-500/30 bg-gradient-to-br from-slate-900/95 via-cyan-950/20 to-slate-900/95">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-[10px] font-bold uppercase tracking-wider">YENİ • TÜRKİYE SAHA OPERASYONLARI + DEEPSEEK V4.1 FLASH</span>
            <h2 class="text-sm font-bold text-white uppercase tracking-wider">💬 WhatsApp & E-Posta Operasyon Karar Anları (Yük Açma, CRM Kartvizit, TR↔RU CMR Çevirisi, Depo Checklist & Yol Masraf Fişleri)</h2>
          </div>
          <p class="text-xs text-slate-300 mt-1">
            <b>Adım 1 (System-1 <code>drex-max</code> / <code>drex-max-finance</code>):</b> Görseli ve WhatsApp yazışmasını 9–12 soruluk filtreden geçirerek milisaniyeler içinde karar verir.
            <b>Adım 2 (System-2 <code>deepseek/deepseek-v4.1-flash-1017</code>):</b> Sadece LLM'in gerçekten gerektiği yerde (<i>Sohbetten Yük JSON'u + Kartvizitten CRM kaydı çıkarma, Türkçe ↔ Rusça CMR/Gümrük çevirisi, Depo Rampa Tutanak yazımı ve Şoför Harcırah Mahsup tablosu</i>) devreye girer.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        <button onclick="runWhatsappDeepseekOps('chat_to_load_and_crm_card')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-cyan-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-cyan-300">📲 1. WhatsApp Sohbetten Yük + CRM Kartvizit</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono">12 SORU + JSON</span>
          </div>
          <p class="text-[11px] text-slate-400">'Gebze OSB -> Çorlu 22t 33 EP 13.60 Kayar Perde' mesajını ve Lojistik Müdürü Kartvizit fotoğrafını denetler; DeepSeek ile İlan JSON + CRM Müşteri Kartı üretir.</p>
        </button>

        <button onclick="runWhatsappDeepseekOps('cmr_customs_and_ru_tr_translation')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-sky-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-sky-300">🌍 2. CMR (TR-RU) & Sınır Kapısı + TR↔RU Çeviri</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 font-mono">11 SORU + RU/TR</span>
          </div>
          <p class="text-[11px] text-slate-400">Verkhniy Lars sınır kapısındaki tırın CMR 18. hane şerhini ve gümrük mührünü denetler; DeepSeek ile Rusça -> Türkçe ve Türkçe -> Rusça resmi alıcı bildirimi çevirir.</p>
        </button>

        <button onclick="runWhatsappDeepseekOps('warehouse_whatsapp_checklist')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-amber-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-amber-300">🏭 3. Depo Rampa Checklist (#CHK-551) Blokajı</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono">11 SORU + WMS</span>
          </div>
          <p class="text-[11px] text-slate-400">WhatsApp'tan gelen rampa yükleme checklist fotoğrafında eksik spanzeti (2/6) yakalar; aracın çıkışını bloke edip vardiya amiri talimatını üretir.</p>
        </button>

        <button onclick="runWhatsappDeepseekOps('driver_road_expenses_audit')" class="p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-emerald-500 text-left transition">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-emerald-300">⛽ 4. Şoför Yol Masraf Fişleri & Harcırah Mahsubu</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">9 SORU + MAHSUP</span>
          </div>
          <p class="text-[11px] text-slate-400">34 KLM 482 plakalı mazot (14.260 TL) ve otoyol (2.250 TL) fişini onaylar; 06 YAB 119 plakalı kişisel market fişini (-2.450 TL) kesip şoför mahsup tablosunu yazar.</p>
        </button>
      </div>

      <div id="whatsappDeepseekOutput" class="hidden"></div>
    </section>

    <!-- Preset Simulation Selector with Category Filter -->
    <section class="glass rounded-2xl p-5">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <h2 class="text-sm font-bold text-white uppercase tracking-wider">🎯 Tekil Karar Senaryoları (17 Hazır Görsel & JSON Simülasyon)</h2>
          <p class="text-xs text-slate-400">Bir senaryoya tıklayarak görseli, modeli ve yapılandırılmış soruları (`noul`, `choice`, `score`) yükleyin.</p>
        </div>
        <div class="flex flex-wrap items-center gap-2 text-xs">
          <button onclick="filterCategory('Belge Sınıflandırma & Tekilleştirme')" id="cat_omnichannel" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">🗂️ Belge & WhatsApp Sınıflandırma (5)</button>
          <button onclick="filterCategory('Drex Max Finance (Lojistik Finans)')" id="cat_finance" class="px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold">🏦 Drex Max Finance (Lojistik Finans) (5)</button>
          <button onclick="filterCategory('Lojistik & Yük Borsası')" id="cat_logistics" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">🚛 Lojistik, Depo & Yük Borsası (5)</button>
          <button onclick="filterCategory('Kurumsal & Genel')" id="cat_enterprise" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">🏢 Kurumsal & Genel (2)</button>
          <button onclick="filterCategory('all')" id="cat_all" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">Tümü (17)</button>
        </div>
      </div>
      <div id="presetList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3"></div>
    </section>

    <!-- Main Playground Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left Column: Inputs (State + Images + Questions) -->
      <div class="lg:col-span-7 space-y-6">
        <div class="glass rounded-2xl p-5 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Model Seçimi</label>
              <select id="modelSelect" class="w-full rounded-xl bg-slate-900 border border-slate-700 px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"></select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">OpenRouter Protokol Endpoint'i</label>
              <select id="endpointSelect" class="w-full rounded-xl bg-slate-900 border border-slate-700 px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500">
                <option value="decisions">POST /api/alpha/decisions (OpenRouter Decisions API)</option>
                <option value="systemone">POST /api/v1/systemone (TypeSafe System One API)</option>
              </select>
            </div>
          </div>

          <!-- Visual Input Studio -->
          <div class="pt-2 border-t border-slate-800">
            <div class="flex items-center justify-between mb-2">
              <label class="text-xs font-semibold text-sky-400 uppercase tracking-wider">🖼️ Görsel Girdi Stüdyosu (11 Hazır Görsel + Özel Yükleme — En Fazla 4 Görsel)</label>
              <button onclick="clearImages()" class="text-xs text-slate-400 hover:text-rose-400">Görselleri Temizle</button>
            </div>

            <!-- Built-in Sample Images -->
            <div id="sampleImagesBar" class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-3"></div>

            <!-- Custom Image Upload -->
            <div class="flex items-center gap-3">
              <label class="flex-1 cursor-pointer rounded-xl border border-dashed border-slate-700 hover:border-sky-500 bg-slate-900/60 px-4 py-2.5 text-center text-xs text-slate-300 transition">
                <span>📂 Bilgisayardan e-Fatura / İrsaliye / Kantar Fişi / Palet Fotoğrafı Yükle (PNG, JPEG, WebP)</span>
                <input type="file" id="customImageInput" accept="image/png,image/jpeg,image/webp" multiple class="hidden" onchange="handleCustomImageUpload(event)" />
              </label>
            </div>

            <!-- Active Attached Images Preview -->
            <div id="activeImagesContainer" class="mt-3 hidden">
              <div class="text-xs text-slate-400 mb-1.5">İsteğe Eklenen Aktif Görseller (<span id="activeImageCount">0</span>/4):</div>
              <div id="activeImagesList" class="grid grid-cols-2 sm:grid-cols-4 gap-2.5"></div>
            </div>
          </div>

          <!-- State Text / JSON Input -->
          <div class="pt-2 border-t border-slate-800">
            <div class="flex items-center justify-between mb-1.5">
              <label class="text-xs font-semibold text-slate-300">📄 State (Metin veya JSON Operasyon / Sözleşme Bağlamı)</label>
              <span class="text-[11px] text-slate-400">Görsellerle birlikte üst düzey <code class="text-sky-400">state</code> dizisine eklenir</span>
            </div>
            <textarea id="stateInput" rows="4" class="w-full rounded-xl bg-slate-900 border border-slate-700 p-3 text-xs font-mono text-slate-100 focus:outline-none focus:border-sky-500" placeholder="Metin veya JSON bağlamı girin..."></textarea>
          </div>
        </div>

        <!-- Questions Builder -->
        <div class="glass rounded-2xl p-5 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold text-white">❓ Typed Questions (Yapılandırılmış Denetim & Karar Soruları)</h3>
              <p class="text-xs text-slate-400">Drex Max Finance tüm kontrol sorularını tek ileri geçişte aynı anda yanıtlar.</p>
            </div>
            <div class="flex items-center gap-1.5 text-xs">
              <button onclick="addQuestion('noul')" class="px-2.5 py-1.5 rounded-lg bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 font-medium">+ Noul (Evet/Hayır)</button>
              <button onclick="addQuestion('choice')" class="px-2.5 py-1.5 rounded-lg bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 font-medium">+ Choice (Seçenek)</button>
              <button onclick="addQuestion('score')" class="px-2.5 py-1.5 rounded-lg bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 font-medium">+ Score (Derece)</button>
            </div>
          </div>

          <div id="questionsList" class="space-y-3"></div>

          <!-- Action Buttons -->
          <div class="pt-3 border-t border-slate-800 flex flex-wrap items-center gap-3">
            <button id="btnEvaluate" onclick="submitDecision()" class="flex-1 py-3 px-5 rounded-xl bg-gradient-to-r from-emerald-500 to-sky-600 hover:from-emerald-400 hover:to-sky-500 text-white font-bold text-sm shadow-lg shadow-emerald-500/20 transition flex items-center justify-center gap-2">
              <span>🎯 Kararı & Olasılıkları Hesapla (Single Forward Pass)</span>
            </button>
            <button id="btnCompare" onclick="compareModels()" class="py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 font-semibold text-xs transition">
              ⚖️ Drex Max Finance vs Drex Max Karşılaştır
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column: Calibrated Probabilities Output & Code Inspector -->
      <div class="lg:col-span-5 space-y-6">
        <div class="glass rounded-2xl p-5 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider">📊 Kalibre Olasılık & Karar Çıktısı</h2>
              <p id="resultSubtitle" class="text-xs text-slate-400">Henüz bir karar isteği çalıştırılmadı.</p>
            </div>
            <div id="telemetryBadges" class="flex items-center gap-2 text-xs"></div>
          </div>

          <div id="resultsContainer" class="space-y-4 text-sm">
            <div class="p-8 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl">
              Soldaki hazır senaryolardan birini seçin veya <b>"Kararı & Olasılıkları Hesapla"</b> butonuna tıklayın.
            </div>
          </div>
        </div>

        <!-- Payload & Code Inspector -->
        <div class="glass rounded-2xl p-5 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider">💻 Ham API Payload & Python Kodu</h3>
            <div class="flex gap-1 text-xs">
              <button onclick="switchCodeTab('response')" id="tab_response" class="px-2.5 py-1 rounded bg-sky-500/20 text-sky-300 font-medium">API Yanıtı</button>
              <button onclick="switchCodeTab('request')" id="tab_request" class="px-2.5 py-1 rounded bg-slate-800 text-slate-400">İstek JSON</button>
              <button onclick="switchCodeTab('python')" id="tab_python" class="px-2.5 py-1 rounded bg-slate-800 text-slate-400">Python Kodu</button>
            </div>
          </div>
          <pre id="codeInspector" class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300 overflow-x-auto max-h-96"></pre>
        </div>
      </div>
    </div>
  </main>

  <!-- Image Lightbox Modal -->
  <div id="lightboxModal" class="fixed inset-0 bg-black/80 z-50 hidden items-center justify-center p-4" onclick="closeLightbox()">
    <div class="max-w-4xl w-full bg-slate-900 border border-slate-700 rounded-2xl p-4" onclick="event.stopPropagation()">
      <div class="flex justify-between items-center mb-3">
        <span id="lightboxTitle" class="text-sm font-bold text-white">Görsel Önizleme</span>
        <button onclick="closeLightbox()" class="text-slate-400 hover:text-white text-sm">✕ Kapat</button>
      </div>
      <img id="lightboxImg" src="" class="w-full rounded-xl border border-slate-800" />
    </div>
  </div>

  <script>
    let appConfig = { models: [], presets: [], sample_images: {} };
    let activeCategory = 'Drex Max Finance (Lojistik Finans)';
    let activeImages = [];
    let currentQuestions = {};
    let activeCodeTab = 'response';
    let lastRequestJson = {};
    let lastResponseJson = {};

    async function initApp() {
      const res = await fetch('/api/config');
      appConfig = await res.json();

      const keyEl = document.getElementById('apiKeyStatus');
      if (appConfig.has_api_key) {
        keyEl.innerHTML = `<span class="text-emerald-400 font-semibold">● API Key Aktif:</span> <code class="text-slate-400">${appConfig.masked_key}</code>`;
      } else {
        keyEl.innerHTML = `<span class="text-rose-400 font-semibold">● API Key Eksik (.env)</span>`;
      }

      const modelSelect = document.getElementById('modelSelect');
      modelSelect.innerHTML = appConfig.models.map(m =>
        `<option value="${m.id}">${m.name} — $${m.input_price_per_m}/M</option>`
      ).join('');

      const sampleBar = document.getElementById('sampleImagesBar');
      sampleBar.innerHTML = Object.entries(appConfig.sample_images).map(([name, dataUrl]) => `
        <div class="group relative rounded-xl overflow-hidden border border-slate-700 bg-slate-900 hover:border-sky-500 transition">
          <img src="${dataUrl}" class="w-full h-20 object-cover cursor-pointer" onclick="openLightbox('${name}', '${dataUrl}')" title="Büyütmek için tıklayın" />
          <div class="p-1.5 flex items-center justify-between bg-slate-950/90 text-[11px]">
            <span class="truncate text-slate-300 font-mono" title="${name}">${name}</span>
            <button onclick="toggleSampleImage('${name}')" class="px-2 py-0.5 rounded bg-sky-500/20 hover:bg-sky-500/40 text-sky-300 font-semibold">+ Ekle</button>
          </div>
        </div>
      `).join('');

      renderPresets();
      if (appConfig.presets.length > 0) {
        loadPreset(appConfig.presets[0].id);
      }
    }

    function filterCategory(cat) {
      activeCategory = cat;
      const map = {
        'Belge Sınıflandırma & Tekilleştirme': 'cat_omnichannel',
        'Drex Max Finance (Lojistik Finans)': 'cat_finance',
        'Lojistik & Yük Borsası': 'cat_logistics',
        'Kurumsal & Genel': 'cat_enterprise',
        'all': 'cat_all'
      };
      Object.entries(map).forEach(([k, id]) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (k === cat) {
          el.className = 'px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold';
        } else {
          el.className = 'px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700';
        }
      });
      renderPresets();
    }

    function renderPresets() {
      const presetList = document.getElementById('presetList');
      const filtered = activeCategory === 'all'
        ? appConfig.presets
        : appConfig.presets.filter(p => p.category === activeCategory);

      presetList.innerHTML = filtered.map(p => {
        const isFinance = p.model === 'nace-ai/drex-max-finance';
        return `
          <div onclick="loadPreset('${p.id}')" id="preset_${p.id}" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-emerald-500/60 transition flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between gap-2 mb-1.5">
                <span class="text-[11px] px-2 py-0.5 rounded-md ${isFinance ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30' : 'bg-sky-500/15 text-sky-300 border border-sky-500/30'} font-medium">${p.badge}</span>
                <span class="text-[10px] text-slate-400 font-mono">${p.model.replace('nace-ai/', '')}</span>
              </div>
              <h4 class="text-xs font-bold text-white mb-1">${p.title}</h4>
              <p class="text-[11px] text-slate-400 line-clamp-3">${p.description}</p>
            </div>
            <div class="mt-2.5 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-emerald-400 font-medium">
              <span>Senaryoyu Yükle (${Object.keys(p.questions).length} kontrol sorusu)</span>
              <span>→</span>
            </div>
          </div>
        `;
      }).join('');
    }

    async function runVariationMatrix(domain) {
      const out = document.getElementById('variationMatrixOutput');
      out.classList.remove('hidden');
      out.innerHTML = `<div class="p-4 rounded-xl bg-slate-900 border border-emerald-500/40 text-xs text-emerald-300 animate-pulse">⏳ <code>nace-ai/drex-max-finance</code> üzerinde 3 Varyasyon (Yeşil Hat / Gri Alan / Kırmızı Hat) paralel koşturuluyor...</div>`;

      try {
        const res = await fetch('/api/variation_matrix', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ domain })
        });
        const data = await res.json();
        lastResponseJson = data;
        switchCodeTab('response');

        out.innerHTML = `
          <div class="pt-3 border-t border-slate-800 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white">${data.title} — <code class="text-emerald-400">${data.model}</code></span>
              <span class="text-[11px] text-slate-400">3 Varyasyon Paralel Karşılaştırması</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              ${(data.variations || []).map(v => {
                const g = v.prerouter_gate || {};
                const borderCol = g.color === 'emerald' ? 'border-emerald-500/50' : (g.color === 'amber' ? 'border-amber-500/50' : 'border-rose-500/50');
                const badgeBg = g.color === 'emerald' ? 'bg-emerald-500/20 text-emerald-300' : (g.color === 'amber' ? 'bg-amber-500/20 text-amber-300' : 'bg-rose-500/20 text-rose-300');
                return `
                  <div class="p-4 rounded-xl bg-slate-950 border ${borderCol} space-y-2.5 text-xs">
                    <div class="flex items-center justify-between gap-2">
                      <span class="font-bold text-white">${v.label}</span>
                      <span class="text-[10px] font-mono text-slate-400">${v.latency_ms} ms</span>
                    </div>
                    <div class="px-2.5 py-1.5 rounded-lg ${badgeBg} font-bold text-[11px]">
                      ${g.badge || ''}
                    </div>
                    <p class="text-[11px] text-slate-400">${g.explanation || ''}</p>
                    <div class="space-y-1.5 pt-2 border-t border-slate-800/80 font-mono text-[11px]">
                      ${Object.entries(v.answers || {}).map(([qk, ans]) => {
                        if (ans.type === 'noul') {
                          const p = (Number(ans.noul) * 100).toFixed(1);
                          return `<div class="flex justify-between"><span class="text-slate-400">${qk}:</span><b class="${p >= 50 ? 'text-emerald-400' : 'text-rose-400'}">%${p}</b></div>`;
                        }
                        if (ans.type === 'choice') {
                          const wp = ((ans.probabilities || {})[ans.choice] * 100 || 0).toFixed(1);
                          return `<div class="pt-1"><span class="text-slate-400">${qk}:</span><br/><b class="text-sky-300">★ ${ans.choice} (%${wp})</b></div>`;
                        }
                        if (ans.type === 'score') {
                          return `<div class="flex justify-between"><span class="text-slate-400">${qk}:</span><b class="text-amber-300">Skor: ${Number(ans.score).toFixed(2)}</b></div>`;
                        }
                        return '';
                      }).join('')}
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      } catch (e) {
        out.innerHTML = `<div class="text-xs text-rose-400">Hata: ${e.message}</div>`;
      }
    }

    async function runHybridPipeline(scenarioType) {
      const out = document.getElementById('hybridPipelineOutput');
      out.classList.remove('hidden');
      out.innerHTML = `<div class="p-4 rounded-xl bg-slate-900 border border-sky-500/40 text-xs text-sky-300 animate-pulse">⏳ 4-Katmanlı Hibrit Akış Çalıştırılıyor: (1) Drex Max Finance Görsel Analiz ➔ (2) Mikroservis Eşiği ➔ (3) System-2 LLM Bildirimi ➔ (4) Drex Max Çıktı Guardrail...</div>`;

      try {
        const res = await fetch('/api/hybrid_pipeline', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ scenario_type: scenarioType })
        });
        const data = await res.json();
        if (!data.ok) {
          out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950 border border-rose-500 text-xs text-rose-200">${JSON.stringify(data.error)}</div>`;
          return;
        }
        const s1 = data.step1_system1_vision_decision;
        const s2 = data.step2_backend_orchestration;
        const s3 = data.step3_system2_llm_generation;
        const s4 = data.step4_system1_output_guardrail;

        out.innerHTML = `
          <div class="grid grid-cols-1 md:grid-cols-4 gap-3 pt-2 border-t border-slate-800 text-xs">
            <div class="p-3.5 rounded-xl bg-slate-950 border border-sky-500/40 space-y-1.5">
              <div class="font-bold text-sky-400">1️⃣ System-1 (${s1.model || 'Drex Max'})</div>
              <div class="text-[11px] text-slate-400 font-mono">Süre: ${s1.latency_ms} ms | $${Number(s1.usage.cost || 0).toFixed(6)}</div>
              <div class="space-y-1 pt-1">
                ${Object.entries(s1.answers).map(([k, v]) => {
                  if (v.type === 'noul') return `<div class="font-mono text-[11px]"><span class="text-slate-400">${k}:</span> <b class="text-white">%${(v.noul*100).toFixed(1)}</b></div>`;
                  if (v.type === 'choice') return `<div class="font-mono text-[11px]"><span class="text-slate-400">${k}:</span> <b class="text-sky-300">${v.choice}</b></div>`;
                  return `<div class="font-mono text-[11px]"><span class="text-slate-400">${k}:</span> <b class="text-amber-300">${Number(v.score).toFixed(2)}</b></div>`;
                }).join('')}
              </div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-indigo-500/40 space-y-1.5">
              <div class="font-bold text-indigo-400">2️⃣ Backend Mikroservis Kapısı</div>
              <div class="text-[11px] text-slate-400 font-mono">Eşik: ≥%80 | Gerçekleşen: %${(s2.actual_confidence*100).toFixed(2)}</div>
              <div class="p-2 rounded bg-indigo-950/40 border border-indigo-500/30 font-mono text-[11px] text-indigo-200">
                ⚡ ${s2.executed_microservice}
              </div>
              <div class="text-[11px] text-emerald-400 font-mono">✓ DB Kaydı: ${s2.database_tx}</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-amber-500/40 space-y-1.5">
              <div class="font-bold text-amber-400">3️⃣ System-2: Üretken LLM Bildirimi</div>
              <div class="text-[11px] text-slate-400 font-mono">${s3.model} (${s3.latency_ms} ms)</div>
              <p class="text-[11px] text-slate-200 italic bg-slate-900 p-2 rounded border border-slate-800">"${s3.generated_notification}"</p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-emerald-500/40 space-y-1.5">
              <div class="font-bold text-emerald-400">4️⃣ System-1: Çıktı Guardrail Denetimi</div>
              <div class="text-[11px] text-slate-400 font-mono">Süre: ${s4.latency_ms} ms</div>
              <div class="space-y-1 pt-1">
                ${Object.entries(s4.answers || {}).map(([k, v]) => {
                  if (v.type === 'noul') return `<div class="font-mono text-[11px]"><span class="text-slate-400">${k}:</span> <b class="text-white">%${(v.noul*100).toFixed(1)}</b></div>`;
                  if (v.type === 'choice') return `<div class="font-mono text-[11px]"><span class="text-slate-400">Karar:</span> <b class="text-emerald-300">✓ ${v.choice}</b></div>`;
                  return '';
                }).join('')}
              </div>
            </div>
          </div>
        `;
      } catch (err) {
        out.innerHTML = `<div class="text-xs text-rose-400">Hata: ${err.message}</div>`;
      }
    }

    function openLightbox(title, url) {
      document.getElementById('lightboxTitle').textContent = title;
      document.getElementById('lightboxImg').src = url;
      const modal = document.getElementById('lightboxModal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeLightbox() {
      const modal = document.getElementById('lightboxModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function loadPreset(presetId) {
      const preset = appConfig.presets.find(p => p.id === presetId);
      if (!preset) return;

      document.querySelectorAll('[id^="preset_"]').forEach(el => {
        el.classList.remove('ring-2', 'ring-emerald-500', 'border-emerald-500');
      });
      const card = document.getElementById('preset_' + presetId);
      if (card) card.classList.add('ring-2', 'ring-emerald-500');

      document.getElementById('modelSelect').value = preset.model || 'nace-ai/drex-max-finance';

      activeImages = [];
      if (preset.sample_images && preset.sample_images.length) {
        for (const imgName of preset.sample_images) {
          if (appConfig.sample_images[imgName]) {
            activeImages.push({ name: imgName, data_url: appConfig.sample_images[imgName] });
          }
        }
      }
      renderActiveImages();

      if (preset.state_json) {
        document.getElementById('stateInput').value = JSON.stringify(preset.state_json, null, 2);
      } else {
        document.getElementById('stateInput').value = preset.state_text || '';
      }

      currentQuestions = JSON.parse(JSON.stringify(preset.questions));
      renderQuestions();
      updatePreviewPayload();
    }

    function toggleSampleImage(name) {
      const idx = activeImages.findIndex(x => x.name === name);
      if (idx >= 0) {
        activeImages.splice(idx, 1);
      } else {
        if (activeImages.length >= 4) {
          alert('Drex Max istek başına en fazla 4 görsel kabul etmektedir.');
          return;
        }
        activeImages.push({ name, data_url: appConfig.sample_images[name] });
      }
      renderActiveImages();
      updatePreviewPayload();
    }

    function clearImages() {
      activeImages = [];
      renderActiveImages();
      updatePreviewPayload();
    }

    function handleCustomImageUpload(event) {
      const files = Array.from(event.target.files || []);
      for (const file of files) {
        if (activeImages.length >= 4) {
          alert('En fazla 4 görsel ekleyebilirsiniz.');
          break;
        }
        const reader = new FileReader();
        reader.onload = (e) => {
          activeImages.push({ name: file.name, data_url: e.target.result });
          renderActiveImages();
          updatePreviewPayload();
        };
        reader.readAsDataURL(file);
      }
      event.target.value = '';
    }

    function renderActiveImages() {
      const container = document.getElementById('activeImagesContainer');
      const list = document.getElementById('activeImagesList');
      document.getElementById('activeImageCount').textContent = activeImages.length;

      if (activeImages.length === 0) {
        container.classList.add('hidden');
        list.innerHTML = '';
        return;
      }
      container.classList.remove('hidden');
      list.innerHTML = activeImages.map((img, i) => `
        <div class="relative rounded-xl overflow-hidden border border-emerald-500/60 bg-slate-900">
          <img src="${img.data_url}" class="w-full h-24 object-cover cursor-pointer" onclick="openLightbox('${img.name}', '${img.data_url}')" />
          <div class="p-1.5 bg-slate-950/90 flex items-center justify-between text-[11px]">
            <span class="truncate text-emerald-300 font-mono">${i + 1}. ${img.name}</span>
            <button onclick="removeActiveImage(${i})" class="text-rose-400 hover:text-rose-300 font-bold px-1">✕</button>
          </div>
        </div>
      `).join('');
    }

    function removeActiveImage(index) {
      activeImages.splice(index, 1);
      renderActiveImages();
      updatePreviewPayload();
    }

    function renderQuestions() {
      const container = document.getElementById('questionsList');
      const entries = Object.entries(currentQuestions);
      if (entries.length === 0) {
        container.innerHTML = `<div class="text-xs text-slate-500 p-4 border border-dashed border-slate-800 rounded-xl text-center">En az bir soru ekleyin.</div>`;
        return;
      }

      container.innerHTML = entries.map(([key, q]) => {
        const badgeColor = q.type === 'noul' ? 'emerald' : (q.type === 'choice' ? 'sky' : 'amber');
        let criteriaHtml = '';
        if (q.type === 'choice') {
          const critText = Object.entries(q.criteria || {}).map(([k, v]) => `${k}: ${v || ''}`).join('\n');
          criteriaHtml = `
            <div class="mt-2">
              <label class="block text-[11px] text-slate-400 mb-1">Seçenekler (Her satıra <code>anahtar: açıklama</code>):</label>
              <textarea onchange="updateChoiceCriteria('${key}', this.value)" rows="3" class="w-full rounded-lg bg-slate-950 border border-slate-800 p-2 text-xs font-mono text-slate-200">${critText}</textarea>
            </div>
          `;
        } else if (q.type === 'score') {
          const levels = (q.criteria || []).join(', ');
          criteriaHtml = `
            <div class="mt-2">
              <label class="block text-[11px] text-slate-400 mb-1">Sıralı Ölçek Seviyeleri (Virgülle ayırın, düşükten yükseğe):</label>
              <input type="text" value="${levels}" onchange="updateScoreCriteria('${key}', this.value)" class="w-full rounded-lg bg-slate-950 border border-slate-800 p-2 text-xs font-mono text-slate-200" />
            </div>
          `;
        }

        return `
          <div class="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-2 flex-1">
                <span class="text-[11px] px-2 py-0.5 rounded bg-${badgeColor}-500/15 text-${badgeColor}-300 border border-${badgeColor}-500/30 font-mono uppercase">${q.type}</span>
                <input type="text" value="${key}" onchange="renameQuestionKey('${key}', this.value)" class="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs font-mono text-white font-semibold w-56" />
              </div>
              <button onclick="deleteQuestion('${key}')" class="text-xs text-slate-500 hover:text-rose-400">Sil ✕</button>
            </div>
            <div>
              <input type="text" value="${(q.instructions || '').replace(/"/g, '&quot;')}" onchange="updateQuestionInstructions('${key}', this.value)" class="w-full rounded-lg bg-slate-950 border border-slate-800 p-2 text-xs text-slate-200" placeholder="Soru yönergesi (instructions)..." />
            </div>
            ${criteriaHtml}
          </div>
        `;
      }).join('');
    }

    function renameQuestionKey(oldKey, newKey) {
      newKey = newKey.trim().replace(/\s+/g, '_');
      if (!newKey || newKey === oldKey) return;
      const updated = {};
      for (const [k, v] of Object.entries(currentQuestions)) {
        updated[k === oldKey ? newKey : k] = v;
      }
      currentQuestions = updated;
      renderQuestions();
      updatePreviewPayload();
    }

    function updateQuestionInstructions(key, val) {
      if (currentQuestions[key]) {
        currentQuestions[key].instructions = val;
        updatePreviewPayload();
      }
    }

    function updateChoiceCriteria(key, text) {
      const map = {};
      text.split('\n').forEach(line => {
        const trimmed = line.trim();
        if (!trimmed) return;
        const colonIdx = trimmed.indexOf(':');
        if (colonIdx > 0) {
          const k = trimmed.slice(0, colonIdx).trim();
          const v = trimmed.slice(colonIdx + 1).trim();
          map[k] = v;
        } else {
          map[trimmed] = trimmed;
        }
      });
      currentQuestions[key].criteria = map;
      updatePreviewPayload();
    }

    function updateScoreCriteria(key, text) {
      currentQuestions[key].criteria = text.split(',').map(s => s.trim()).filter(Boolean);
      updatePreviewPayload();
    }

    function deleteQuestion(key) {
      delete currentQuestions[key];
      renderQuestions();
      updatePreviewPayload();
    }

    function addQuestion(type) {
      const id = `${type}_q${Object.keys(currentQuestions).length + 1}`;
      if (type === 'noul') {
        currentQuestions[id] = { type: 'noul', instructions: 'Is this condition satisfied?' };
      } else if (type === 'choice') {
        currentQuestions[id] = {
          type: 'choice',
          instructions: 'Which option fits best?',
          criteria: { option_a: 'First option description', option_b: 'Second option description' }
        };
      } else {
        currentQuestions[id] = {
          type: 'score',
          instructions: 'Rate the severity level.',
          criteria: ['Low', 'Medium', 'High', 'Critical']
        };
      }
      renderQuestions();
      updatePreviewPayload();
    }

    function buildStatePayload() {
      const rawText = document.getElementById('stateInput').value.trim();
      let parsedState = rawText;
      if ((rawText.startsWith('{') && rawText.endsWith('}')) || (rawText.startsWith('[') && rawText.endsWith(']'))) {
        try { parsedState = JSON.parse(rawText); } catch (e) {}
      }

      if (activeImages.length === 0) {
        return parsedState;
      }

      const arr = [];
      if (rawText) {
        arr.push(typeof parsedState === 'string' ? parsedState : JSON.stringify(parsedState));
      }
      for (const img of activeImages) {
        arr.push({
          type: 'image_url',
          image_url: { url: img.data_url }
        });
      }
      return arr;
    }

    function updatePreviewPayload() {
      const model = document.getElementById('modelSelect').value;
      const state = buildStatePayload();
      const displayState = Array.isArray(state)
        ? state.map(item => (item && item.type === 'image_url')
            ? { type: 'image_url', image_url: { url: item.image_url.url.slice(0, 42) + '...[BASE64_IMAGE]' } }
            : item)
        : state;

      lastRequestJson = { model, state: displayState, questions: currentQuestions };
      if (activeCodeTab !== 'response') {
        renderCodeInspector();
      }
    }

    function switchCodeTab(tab) {
      activeCodeTab = tab;
      ['response', 'request', 'python'].forEach(t => {
        const btn = document.getElementById('tab_' + t);
        if (t === tab) {
          btn.className = 'px-2.5 py-1 rounded bg-sky-500/20 text-sky-300 font-medium';
        } else {
          btn.className = 'px-2.5 py-1 rounded bg-slate-800 text-slate-400';
        }
      });
      renderCodeInspector();
    }

    function renderCodeInspector() {
      const el = document.getElementById('codeInspector');
      const endpointType = document.getElementById('endpointSelect').value;
      const url = endpointType === 'systemone'
        ? 'https://openrouter.ai/api/v1/systemone'
        : 'https://openrouter.ai/api/alpha/decisions';

      if (activeCodeTab === 'response') {
        el.textContent = Object.keys(lastResponseJson).length
          ? JSON.stringify(lastResponseJson, null, 2)
          : '// Henüz API yanıtı yok.';
      } else if (activeCodeTab === 'request') {
        updatePreviewPayload();
        el.textContent = JSON.stringify(lastRequestJson, null, 2);
      } else if (activeCodeTab === 'python') {
        updatePreviewPayload();
        el.textContent = `import os, requests\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\npayload = ${JSON.stringify(lastRequestJson, null, 2)}\n\nresponse = requests.post(\n    "${url}",\n    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},\n    json=payload\n)\nprint(response.json())`;
      }
    }

    async function submitDecision() {
      const btn = document.getElementById('btnEvaluate');
      const origHtml = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `<span>⏳ Olasılık Dağılımı Hesaplanıyor...</span>`;

      try {
        const model = document.getElementById('modelSelect').value;
        const endpoint_type = document.getElementById('endpointSelect').value;
        const state = buildStatePayload();
        updatePreviewPayload();

        const res = await fetch('/api/evaluate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ model, endpoint_type, state, questions: currentQuestions })
        });
        const data = await res.json();
        lastResponseJson = data;
        switchCodeTab('response');
        renderDecisionResult(data);
      } catch (err) {
        alert('Hata: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = origHtml;
      }
    }

    function renderDecisionResult(data) {
      const container = document.getElementById('resultsContainer');
      const badges = document.getElementById('telemetryBadges');
      const subtitle = document.getElementById('resultSubtitle');

      if (!data.ok) {
        subtitle.textContent = `Hata Kodu: ${data.status_code}`;
        container.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-rose-200 text-xs font-mono whitespace-pre-wrap">${JSON.stringify(data.error, null, 2)}</div>`;
        return;
      }

      const resp = data.response || {};
      const usage = resp.usage || {};
      const costStr = usage.cost !== undefined ? `$${Number(usage.cost).toFixed(6)}` : '$0.0000';

      subtitle.innerHTML = `Model: <code class="text-emerald-400">${resp.model || ''}</code> • Sağlayıcı: <b>${resp.provider || 'OpenRouter'}</b>`;
      badges.innerHTML = `
        <span class="px-2.5 py-1 rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 font-mono">${data.client_latency_ms} ms</span>
        <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-mono">${usage.input_tokens || 0} in tok</span>
        <span class="px-2.5 py-1 rounded-lg bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 font-mono">${costStr}</span>
      `;

      const answers = resp.answers || {};
      container.innerHTML = Object.entries(answers).map(([qKey, ans]) => {
        const qDef = currentQuestions[qKey] || {};
        const instr = qDef.instructions || '';

        if (ans.type === 'noul') {
          const probTrue = Number(ans.noul || 0);
          const pctTrue = (probTrue * 100).toFixed(2);
          const pctFalse = ((1 - probTrue) * 100).toFixed(2);
          const isYes = probTrue >= 0.5;
          return `
            <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2.5">
              <div class="flex items-center justify-between gap-2">
                <div>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-300 font-mono uppercase mr-1.5">NOUL (EVET/HAYIR)</span>
                  <span class="font-bold text-white font-mono text-xs">${qKey}</span>
                </div>
                <span class="px-2.5 py-1 rounded-lg text-xs font-bold ${isYes ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'}">
                  ${isYes ? '✓ EVET (TRUE)' : '✕ HAYIR (FALSE)'} — %${isYes ? pctTrue : pctFalse}
                </span>
              </div>
              <p class="text-xs text-slate-400">${instr}</p>
              <div class="space-y-1.5 pt-1">
                <div class="flex justify-between text-xs font-mono">
                  <span class="text-emerald-400">True (Evet): %${pctTrue}</span>
                  <span class="text-rose-400">False (Hayır): %${pctFalse}</span>
                </div>
                <div class="w-full h-3 rounded-full bg-rose-950 overflow-hidden flex">
                  <div class="prob-bar h-full bg-gradient-to-r from-emerald-500 to-teal-400" style="width: ${pctTrue}%"></div>
                </div>
              </div>
            </div>
          `;
        }

        if (ans.type === 'choice') {
          const probs = ans.probabilities || {};
          const conf = ans.confidence !== undefined ? (Number(ans.confidence) * 100).toFixed(1) : null;
          const sorted = Object.entries(probs).sort((a, b) => b[1] - a[1]);
          return `
            <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2.5">
              <div class="flex items-center justify-between gap-2">
                <div>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/15 text-sky-300 font-mono uppercase mr-1.5">CHOICE</span>
                  <span class="font-bold text-white font-mono text-xs">${qKey}</span>
                </div>
                <div class="flex items-center gap-2">
                  ${conf ? `<span class="text-[11px] text-slate-400 font-mono">Güven: %${conf}</span>` : ''}
                  <span class="px-2.5 py-1 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-bold font-mono">★ ${ans.choice}</span>
                </div>
              </div>
              <p class="text-xs text-slate-400">${instr}</p>
              <div class="space-y-2 pt-1">
                ${sorted.map(([opt, p]) => {
                  const pct = (Number(p) * 100).toFixed(2);
                  const isWinner = opt === ans.choice;
                  return `
                    <div>
                      <div class="flex justify-between text-xs mb-1">
                        <span class="font-mono ${isWinner ? 'text-sky-300 font-bold' : 'text-slate-400'}">${isWinner ? '▶ ' : ''}${opt}</span>
                        <span class="font-mono ${isWinner ? 'text-white font-bold' : 'text-slate-400'}">%${pct}</span>
                      </div>
                      <div class="w-full h-2.5 rounded-full bg-slate-950 overflow-hidden">
                        <div class="prob-bar h-full ${isWinner ? 'bg-gradient-to-r from-sky-500 to-indigo-500' : 'bg-slate-700'}" style="width: ${Math.max(Number(pct), 1)}%"></div>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          `;
        }

        if (ans.type === 'score') {
          const legend = ans.legend || {};
          const probs = ans.probabilities || {};
          const conf = ans.confidence !== undefined ? (Number(ans.confidence) * 100).toFixed(1) : null;
          const keys = Object.keys(legend);
          const maxScore = Math.max(keys.length - 1, 1);
          const rawScore = Number(ans.score || 0);
          return `
            <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2.5">
              <div class="flex items-center justify-between gap-2">
                <div>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/15 text-amber-300 font-mono uppercase mr-1.5">SCORE (ÖLÇEK)</span>
                  <span class="font-bold text-white font-mono text-xs">${qKey}</span>
                </div>
                <div class="flex items-center gap-2">
                  ${conf ? `<span class="text-[11px] text-slate-400 font-mono">Güven: %${conf}</span>` : ''}
                  <span class="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-bold font-mono">Skor: ${rawScore.toFixed(2)} / ${maxScore}</span>
                </div>
              </div>
              <p class="text-xs text-slate-400">${instr}</p>
              <div class="space-y-2 pt-1">
                ${keys.map(k => {
                  const label = legend[k];
                  const p = Number(probs[k] || 0);
                  const pct = (p * 100).toFixed(2);
                  return `
                    <div>
                      <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-300 font-mono">[${k}] ${label}</span>
                        <span class="text-amber-300 font-mono font-semibold">%${pct}</span>
                      </div>
                      <div class="w-full h-2.5 rounded-full bg-slate-950 overflow-hidden">
                        <div class="prob-bar h-full bg-gradient-to-r from-amber-500 to-orange-500" style="width: ${Math.max(Number(pct), 1)}%"></div>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          `;
        }

        return `<pre class="text-xs font-mono">${JSON.stringify(ans, null, 2)}</pre>`;
      }).join('');
    }

    async function compareModels() {
      const btn = document.getElementById('btnCompare');
      const orig = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '⏳ Modeller Karşılaştırılıyor...';

      try {
        const state = buildStatePayload();
        const models = activeImages.length > 0
          ? ['nace-ai/drex-max-finance', 'nace-ai/drex-max']
          : ['nace-ai/drex-max-finance', 'nace-ai/drex-max', 'nace-ai/drex-v2.0'];

        const res = await fetch('/api/compare', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ models, state, questions: currentQuestions })
        });
        const data = await res.json();
        lastResponseJson = data;
        switchCodeTab('response');
        renderComparisonResults(data.results || []);
      } catch (e) {
        alert('Karşılaştırma hatası: ' + e.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = orig;
      }
    }

    function renderComparisonResults(results) {
      const container = document.getElementById('resultsContainer');
      document.getElementById('resultSubtitle').textContent = `${results.length} Nace.AI Modeli Yan Yana Karşılaştırıldı`;
      document.getElementById('telemetryBadges').innerHTML = '';

      const qKeys = Object.keys(currentQuestions);
      container.innerHTML = qKeys.map(qKey => {
        const qDef = currentQuestions[qKey];
        return `
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-3">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white font-mono text-xs">${qKey} (${qDef.type.toUpperCase()})</span>
            </div>
            <p class="text-xs text-slate-400">${qDef.instructions}</p>
            <div class="space-y-2">
              ${results.map(r => {
                if (!r.ok) {
                  return `<div class="text-xs text-rose-400 font-mono">${r.model}: Hata (${r.status_code})</div>`;
                }
                const ans = (r.response.answers || {})[qKey] || {};
                let summary = '';
                if (ans.type === 'noul') {
                  summary = `Evet Olasılığı: %${(Number(ans.noul) * 100).toFixed(2)}`;
                } else if (ans.type === 'choice') {
                  const winProb = ((ans.probabilities || {})[ans.choice] || 0) * 100;
                  summary = `Seçim: ${ans.choice} (%${winProb.toFixed(2)})`;
                } else if (ans.type === 'score') {
                  summary = `Skor: ${Number(ans.score).toFixed(2)}`;
                }
                return `
                  <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
                    <div>
                      <span class="font-mono text-emerald-400 font-semibold">${r.model}</span>
                      <span class="text-slate-500 ml-2">(${r.client_latency_ms} ms)</span>
                    </div>
                    <span class="font-mono text-white font-bold">${summary}</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');
    }

    async function runOmnichannelClassify(bundleType) {
      const out = document.getElementById('omnichannelOutput');
      out.classList.remove('hidden');
      out.innerHTML = `<div class="p-4 rounded-xl bg-slate-900 border border-fuchsia-500/40 text-xs text-fuchsia-300 animate-pulse">⏳ Çok kanallı belgeler tekilleştiriliyor, sınıflandırılıyor ve 10-13 soruluk denetim filtresinden geçiriliyor...</div>`;

      try {
        const res = await fetch('/api/omnichannel_classify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ bundle_type: bundleType })
        });
        const data = await res.json();
        lastResponseJson = data;
        switchCodeTab('response');

        if (!data.ok) {
          out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-xs text-rose-200 font-mono">${JSON.stringify(data, null, 2)}</div>`;
          return;
        }

        const comp = data.legacy_vs_drex_comparison || {};
        const answers = data.answers || {};
        const questionsDef = data.questions || {};
        const incoming = (data.channel_metadata || {}).incoming_sources || [];

        let chosenClass = '';
        let chosenAction = '';
        Object.entries(answers).forEach(([k, ans]) => {
          if (ans.type === 'choice') {
            if (k.includes('class')) chosenClass = ans.choice;
            else chosenAction = ans.choice;
          }
        });

        const incomingRows = incoming.map(f => `
          <div class="p-2.5 rounded-lg bg-slate-950/90 border border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
            <div>
              <span class="px-2 py-0.5 rounded bg-fuchsia-500/15 text-fuchsia-300 font-mono text-[10px] mr-1.5">${f.channel}</span>
              <span class="font-mono text-white font-semibold">${f.attachment || f.doc_no || f.subject || ''}</span>
            </div>
            <div class="text-[11px] text-slate-400 font-mono">${f.message || f.subject || ('Canonical: ' + (f.canonical_id || ''))} • ${f.received_at || ''}</div>
          </div>
        `).join('');

        const questionCards = Object.entries(answers).map(([qKey, r]) => {
          const qInstr = (questionsDef[qKey] || {}).instructions || '';
          let valBadge = '';
          if (r.type === 'noul') {
            const p = Number(r.noul || 0) * 100;
            const isYes = p >= 50;
            valBadge = `<span class="px-2 py-0.5 rounded font-mono text-[11px] font-bold ${isYes ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'}">${isYes ? 'EVET' : 'HAYIR'} (%${p.toFixed(1)})</span>`;
          } else if (r.type === 'choice') {
            const winProb = ((r.probabilities || {})[r.choice] || 0) * 100;
            valBadge = `<span class="px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30 font-mono text-[11px] font-bold">★ ${r.choice} (%${winProb.toFixed(1)})</span>`;
          } else if (r.type === 'score') {
            valBadge = `<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-mono text-[11px] font-bold">Skor: ${Number(r.score || 0).toFixed(2)}</span>`;
          }
          return `
            <div class="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 flex flex-col justify-between gap-1.5">
              <div class="flex items-center justify-between gap-2">
                <span class="font-mono text-[11px] text-fuchsia-300 font-bold">${qKey}</span>
                ${valBadge}
              </div>
              <p class="text-[11px] text-slate-400 leading-snug">${qInstr}</p>
            </div>
          `;
        }).join('');

        out.innerHTML = `
          <div class="space-y-4 pt-2 border-t border-slate-800">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 class="text-xs font-bold text-white uppercase tracking-wider">Paket: ${data.bundle_type} (${data.image_name})</h3>
                <p class="text-[11px] text-slate-400">Model: <code class="text-fuchsia-300">${data.model}</code> • Toplam Süre: <b>${data.latency_ms} ms</b> • Girdi: <b>${data.usage?.input_tokens || 0} token</b> • Çıktı: <b>0 .md token</b></p>
              </div>
              <span class="px-3 py-1 rounded-lg border bg-fuchsia-500/20 text-fuchsia-300 border-fuchsia-500/40 text-xs font-bold font-mono">
                AKSİYON: ${chosenAction}
              </span>
            </div>

            <!-- Architecture Comparison Banner -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div class="p-3 rounded-xl bg-rose-950/25 border border-rose-500/30">
                <div class="font-bold text-rose-300 mb-1">❌ Klasik Mimari (Normal LLM ile .md Markdown Çıkarma)</div>
                <p class="text-[11px] text-slate-300">${comp.legacy_workflow || ''}</p>
                <div class="mt-1.5 text-[11px] text-rose-300 font-mono">Süre: ~${comp.legacy_estimated_latency_ms} ms • Çıktı: ${comp.legacy_estimated_output_tokens} tok • Maliyet: $${comp.legacy_estimated_cost_usd}</div>
              </div>
              <div class="p-3 rounded-xl bg-emerald-950/25 border border-emerald-500/30">
                <div class="font-bold text-emerald-300 mb-1">✅ Yeni Mimari (${comp.cost_savings_multiplier || ''})</div>
                <p class="text-[11px] text-slate-300">${comp.drex_workflow || ''}</p>
                <div class="mt-1.5 text-[11px] text-emerald-300 font-mono">Gerçek Süre: ${comp.drex_actual_latency_ms} ms • Çıktı: 0 tok • Maliyet: $${Number(comp.drex_actual_cost_usd || 0).toFixed(6)}</div>
              </div>
            </div>

            <!-- Incoming Multi-Channel Files & Deduplication Status -->
            <div class="p-3.5 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
              <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
                <span class="font-bold text-white">📥 Kanallardan Gelen Dosyalar & Tekilleştirme (Deduplication) Sonucu</span>
                <div class="flex flex-wrap items-center gap-2 font-mono text-[11px]">
                  <span class="px-2 py-0.5 rounded bg-fuchsia-500/20 text-fuchsia-300">Tespit Edilen Sınıf: ${chosenClass}</span>
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Soru Sayısı: ${data.question_count} Adet</span>
                </div>
              </div>
              <div class="space-y-1.5">${incomingRows}</div>
            </div>

            <!-- 10-13 Question Filter Matrix -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-fuchsia-300 uppercase tracking-wider">🔍 Belge Sınıfına Özel ${data.question_count} Soruluk Karar Filtresi Sonuçları (Tek Forward Pass)</div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5">
                ${questionCards}
              </div>
            </div>
          </div>
        `;
      } catch (err) {
        out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-xs text-rose-200">Hata: ${err.message}</div>`;
      }
    }

    async function runWhatsappDeepseekOps(workflowType) {
      const out = document.getElementById('whatsappDeepseekOutput');
      out.classList.remove('hidden');
      out.innerHTML = `<div class="p-4 rounded-xl bg-slate-900 border border-cyan-500/40 text-xs text-cyan-300 animate-pulse">⏳ Adım 1: Drex Max (System-1) görsel ve WhatsApp bağlamını 9-12 soruluk filtreden geçiriyor... Ardından Adım 2: DeepSeek V4.1 Flash (deepseek/deepseek-v4.1-flash-1017) yapılandırılmış JSON / TR↔RU çeviri / mahsup tablosunu üretiyor...</div>`;

      try {
        const res = await fetch('/api/whatsapp_deepseek_ops', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ workflow_type: workflowType })
        });
        const data = await res.json();
        lastResponseJson = data;
        switchCodeTab('response');

        if (!data.ok) {
          out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-xs text-rose-200 font-mono">${JSON.stringify(data, null, 2)}</div>`;
          return;
        }

        const s1 = data.step1_system1_decision || {};
        const s2 = data.step2_deepseek_llm || {};
        const s3 = data.step3_system1_guardrail || {};
        const answers = s1.answers || {};
        const qDefs = s1.questions || {};
        const imgUrl = appConfig.sample_images[data.image_name] || '';

        const qCards = Object.entries(answers).map(([qKey, r]) => {
          const instr = (qDefs[qKey] || {}).instructions || '';
          let badge = '';
          if (r.type === 'noul') {
            const p = Number(r.noul || 0) * 100;
            const isYes = p >= 50;
            badge = `<span class="px-2 py-0.5 rounded font-mono text-[11px] font-bold ${isYes ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'}">${isYes ? 'EVET' : 'HAYIR'} (%${p.toFixed(1)})</span>`;
          } else if (r.type === 'choice') {
            const winP = ((r.probabilities || {})[r.choice] || 0) * 100;
            badge = `<span class="px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30 font-mono text-[11px] font-bold">★ ${r.choice} (%${winP.toFixed(1)})</span>`;
          } else if (r.type === 'score') {
            badge = `<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-mono text-[11px] font-bold">Skor: ${Number(r.score || 0).toFixed(2)}</span>`;
          }
          return `
            <div class="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 flex flex-col justify-between gap-1">
              <div class="flex items-center justify-between gap-2">
                <span class="font-mono text-[11px] text-cyan-300 font-bold">${qKey}</span>
                ${badge}
              </div>
              <p class="text-[11px] text-slate-400 leading-snug">${instr}</p>
            </div>
          `;
        }).join('');

        const guardChoice = s3.answers?.safe_for_external_dispatch?.choice || 'approve_and_dispatch';
        const guardProb = Number(s3.answers?.aligned_with_system1_decision?.noul || 0) * 100;

        out.innerHTML = `
          <div class="space-y-4 pt-3 border-t border-slate-800">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 class="text-xs font-bold text-white uppercase tracking-wider">${data.title}</h3>
                <p class="text-[11px] text-slate-400">
                  System-1: <code class="text-emerald-400">${s1.model}</code> (${s1.latency_ms} ms, ${s1.question_count} soru) •
                  System-2 LLM: <code class="text-cyan-400">${s2.model}</code> (${s2.latency_ms} ms) •
                  Guardrail: <code class="text-fuchsia-400">%${guardProb.toFixed(1)} Uyum (${guardChoice})</code>
                </p>
              </div>
              ${imgUrl ? `<button onclick="openLightbox('${data.image_name}', '${imgUrl}')" class="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 text-xs font-semibold">🖼️ Saha Görselini Büyüt (${data.image_name})</button>` : ''}
            </div>

            <!-- Step 1: System-1 Decision Filter -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-emerald-300 uppercase tracking-wider">⚡ Adım 1: System-1 (${s1.model}) — ${s1.question_count} Soruluk Karar & Sınıflandırma Filtresi (0 Çıktı Token)</div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5">
                ${qCards}
              </div>
            </div>

            <!-- Step 2: DeepSeek V4.1 Flash Output -->
            <div class="p-4 rounded-xl bg-slate-950/90 border border-cyan-500/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-cyan-300 uppercase tracking-wider">🧠 Adım 2: System-2 (${s2.model}) — Üretilen Yapılandırılmış JSON / TR↔RU Çeviri / Operasyon Çıktısı</span>
                <span class="text-[11px] font-mono text-slate-400">${s2.latency_ms} ms</span>
              </div>
              <pre class="text-xs text-slate-200 font-mono whitespace-pre-wrap leading-relaxed overflow-x-auto max-h-96 p-3 rounded-lg bg-slate-900 border border-slate-800">${(s2.generated_output || '').replace(/</g, '&lt;')}</pre>
            </div>
          </div>
        `;
      } catch (err) {
        out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-xs text-rose-200">Hata: ${err.message}</div>`;
      }
    }

    let dynamicChatTranscript = [];
    let webSearchItems = [];

    function openGoogleImagesTab() {
      const q = document.getElementById('webDocSearchInput').value || 'sevk irsaliyesi ornegi';
      window.open('https://www.google.com/search?tbm=isch&q=' + encodeURIComponent(q), '_blank');
    }

    function renderWebSearchGrid() {
      const grid = document.getElementById('webSearchResultsGrid');
      const status = document.getElementById('remoteFetchStatus');
      status.textContent = `${webSearchItems.length} görsel listeleniyor (Önizlemek için resme tıklayın, alakasızları ✕ ile çıkarın)`;

      if (webSearchItems.length === 0) {
        grid.innerHTML = `<div class="col-span-full text-center text-xs text-slate-500 py-4">Listede görsel kalmadı. Yeni bir arama yapabilirsiniz.</div>`;
        return;
      }

      grid.innerHTML = webSearchItems.map((item, idx) => {
        const safeUrl = (item.url || '').replace(/'/g, "\\'");
        const safeTitle = (item.title || 'Belge Görseli').replace(/'/g, "\\'");
        return `
          <div class="group relative rounded-xl overflow-hidden bg-slate-950 border border-slate-800 hover:border-sky-500 transition flex flex-col justify-between text-[10px]">
            <!-- Remove Irrelevant Image Button (Top Right) -->
            <button onclick="removeWebSearchItem(${idx})" title="Alakasız görseli listeden çıkar" class="absolute top-1 right-1 z-10 w-5 h-5 rounded-full bg-rose-950/90 hover:bg-rose-600 text-rose-200 hover:text-white border border-rose-500/50 flex items-center justify-center font-bold text-[10px] shadow">
              ✕
            </button>

            <!-- Thumbnail Image Preview (Click to enlarge in Lightbox) -->
            <div class="relative w-full h-24 bg-slate-900 overflow-hidden cursor-pointer" onclick="openLightbox('${safeTitle}', '${safeUrl}')" title="Büyük önizleme için tıklayın">
              <img src="${item.url}" referrerpolicy="no-referrer" onerror="this.closest('.group').style.display='none'" class="w-full h-full object-cover group-hover:scale-105 transition duration-200" />
              <span class="absolute bottom-1 left-1 px-1.5 py-0.5 rounded bg-slate-950/80 text-[9px] text-slate-300 font-mono">🔍 Önizle</span>
            </div>

            <!-- Title, Source & Action Buttons -->
            <div class="p-1.5 space-y-1">
              <div class="font-semibold text-slate-200 truncate" title="${item.title}">${item.title}</div>
              <div class="text-[9px] text-slate-500 truncate">${item.source || ''}</div>
              <div class="flex items-center gap-1 pt-0.5">
                <button onclick="pullSpecificRemoteUrl('${safeUrl}', '${safeTitle}')" class="flex-1 px-1.5 py-1 rounded bg-sky-500/20 hover:bg-sky-500/40 text-sky-300 border border-sky-500/30 font-bold text-center">
                  🔗 Kullan
                </button>
                <a href="${item.url}" target="_blank" rel="noopener noreferrer" title="Görseli yeni sekmede aç" class="px-1.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-semibold">
                  ↗ Sekme
                </a>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function removeWebSearchItem(idx) {
      webSearchItems.splice(idx, 1);
      renderWebSearchGrid();
    }

    async function searchWebDocuments() {
      const q = document.getElementById('webDocSearchInput').value || 'sevk irsaliyesi ornegi';
      const status = document.getElementById('remoteFetchStatus');
      status.textContent = '🔍 Web\'de görsel aranıyor...';
      try {
        const res = await fetch('/api/web_image_search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q })
        });
        const data = await res.json();
        webSearchItems = data.results || [];
        renderWebSearchGrid();
      } catch (e) {
        status.textContent = 'Arama hatası';
      }
    }

    async function pullSpecificRemoteUrl(url, title) {
      document.getElementById('directImageUrlInput').value = url;
      await pullRemoteImageUrl(title);
    }

    async function pullRemoteImageUrl(customLabel) {
      const url = document.getElementById('directImageUrlInput').value.trim();
      if (!url) {
        alert('Lütfen önce bir görsel URL\'si girin veya arama sonuçlarından seçin.');
        return;
      }
      const status = document.getElementById('remoteFetchStatus');
      status.innerHTML = `<span class="text-amber-300 animate-pulse">⏳ URL'den belleğe çekiliyor...</span>`;
      try {
        const res = await fetch('/api/fetch_remote_image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_url: url })
        });
        const data = await res.json();
        if (!data.ok) {
          status.innerHTML = `<span class="text-rose-400">✕ ${data.error}</span>`;
          return;
        }
        activeImages = [{
          name: customLabel || ('WebURL_' + url.split('/').pop().slice(0, 24)),
          data_url: data.data_url
        }];
        renderActiveImages();
        updatePreviewPayload();
        status.innerHTML = `<span class="text-emerald-400">✓ Çekildi (${data.width}x${data.height}, ${data.size_kb} KB, ${data.fetch_latency_ms} ms)</span>`;
        document.getElementById('fnode_1_meta').textContent = `Web URL (${data.size_kb} KB) Bağlandı`;
        document.getElementById('fnode_1_badge').textContent = 'WEB URL AKTİF';
      } catch (e) {
        status.innerHTML = `<span class="text-rose-400">Hata: ${e.message}</span>`;
      }
    }

    async function generateDynamicScenarioWithDeepSeek() {
      const btn = document.getElementById('btnGenerateDeepSeekScenario');
      const orig = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '⏳ DeepSeek Sohbet & Soruları Üretiyor...';

      const chatBox = document.getElementById('dynamicChatTranscriptBox');
      chatBox.innerHTML = `<div class="text-cyan-300 animate-pulse">⏳ DeepSeek V4.1 Flash (deepseek/deepseek-v4.1-flash-1017) seçili görseli ve süreç alanını inceleyerek gerçekçi WhatsApp yazışması ve 8 adet karar sorusu sentezliyor...</div>`;

      try {
        const domain = document.getElementById('dynamicDomainSelect').value;
        const custom_instruction = document.getElementById('dynamicCustomInstruction').value;
        const image_data_url = activeImages.length > 0 ? activeImages[0].data_url : null;

        const res = await fetch('/api/generate_dynamic_sim', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ domain, custom_instruction, image_data_url })
        });
        const data = await res.json();
        if (!data.ok) {
          chatBox.innerHTML = `<div class="text-rose-400">${data.error}</div>`;
          return;
        }

        const sc = data.scenario || {};
        dynamicChatTranscript = sc.whatsapp_chat_transcript || [];
        if (sc.recommended_drex_model) {
          document.getElementById('modelSelect').value = sc.recommended_drex_model;
        }
        if (sc.state_summary) {
          document.getElementById('stateInput').value = sc.state_summary;
        }
        if (sc.questions && Object.keys(sc.questions).length > 0) {
          currentQuestions = sc.questions;
          renderQuestions();
        }
        updatePreviewPayload();

        chatBox.innerHTML = dynamicChatTranscript.map(m => `
          <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
            <span class="font-bold text-emerald-400">[${m.channel || 'WhatsApp'} • ${m.time || ''}] ${m.sender}:</span>
            <span class="text-slate-200 ml-1">${m.message}</span>
          </div>
        `).join('');

        document.getElementById('fnode_1_meta').textContent = `${dynamicChatTranscript.length} Mesaj + ${activeImages.length} Görsel`;
        document.getElementById('fnode_2_meta').textContent = `${Object.keys(currentQuestions).length} Dinamik Soru Hazır`;
        document.getElementById('fnode_2_badge').textContent = `${data.latency_ms} ms`;
        document.getElementById('flowDiagramStatus').innerHTML = `<span class="text-cyan-300">✨ DeepSeek Senaryosu Hazır — Şimdi "▶ AKIŞI ÇALIŞTIR" butonuna basın!</span>`;
      } catch (e) {
        chatBox.innerHTML = `<div class="text-rose-400">Hata: ${e.message}</div>`;
      } finally {
        btn.disabled = false;
        btn.innerHTML = orig;
      }
    }

    async function runDynamicFlowSimulation() {
      const btn = document.getElementById('btnRunDynamicFlow');
      const orig = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span>⏳ 6 DÜĞÜMLÜ AKIŞ ÇALIŞIYOR...</span>';

      const out = document.getElementById('dynamicFlowRunOutput');
      out.classList.remove('hidden');
      out.innerHTML = `<div class="p-4 rounded-xl bg-slate-900 border border-cyan-500/40 text-xs text-cyan-300 animate-pulse">⏳ Düğüm 1..6 sırayla çalıştırılıyor: Drex Max olasılık dağılımı hesaplanıyor ve DeepSeek V4.1 Flash operasyon çıktısı üretiliyor...</div>`;

      // Highlight nodes as running
      for (let i = 1; i <= 6; i++) {
        const el = document.getElementById('fnode_' + i);
        if (el) el.className = 'p-3 rounded-xl bg-slate-900/90 border-2 border-cyan-500/60 flex flex-col justify-between transition animate-pulse';
      }

      try {
        const drex_model = document.getElementById('modelSelect').value;
        const state_text = document.getElementById('stateInput').value;
        const images = activeImages.map(x => x.data_url);

        const res = await fetch('/api/run_dynamic_flow', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            drex_model,
            llm_model: 'deepseek/deepseek-v4.1-flash-1017',
            state_text,
            chat_transcript: dynamicChatTranscript,
            questions: currentQuestions,
            images
          })
        });
        const data = await res.json();
        lastResponseJson = data;
        switchCodeTab('response');

        if (!data.ok) {
          out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-xs text-rose-200 font-mono">${JSON.stringify(data, null, 2)}</div>`;
          return;
        }

        const nodes = data.nodes || {};
        // Update visual node cards
        const setNodeDone = (idx, badgeText, metaText, borderCls) => {
          const el = document.getElementById('fnode_' + idx);
          if (el) el.className = `p-3 rounded-xl bg-slate-900 border-2 ${borderCls} flex flex-col justify-between transition`;
          const b = document.getElementById(`fnode_${idx}_badge`);
          if (b) b.textContent = badgeText;
          const m = document.getElementById(`fnode_${idx}_meta`);
          if (m) m.textContent = metaText;
        };

        setNodeDone(1, '✓ TAMAM', `${nodes.node1_ingestion.image_count} Görsel, ${nodes.node1_ingestion.chat_messages_count} Mesaj`, 'border-sky-500/70');
        setNodeDone(2, '✓ TAMAM', `${nodes.node2_question_filter.question_count} Karar Sorusu`, 'border-cyan-500/70');
        setNodeDone(3, `${nodes.node3_system1_drex.latency_ms} ms`, nodes.node3_system1_drex.model, 'border-emerald-500/70');
        setNodeDone(4, `Güven %${(nodes.node4_gatekeeper.confidence*100).toFixed(1)}`, nodes.node4_gatekeeper.label, 'border-amber-500/70');
        setNodeDone(5, `${nodes.node5_deepseek_llm.latency_ms} ms`, nodes.node5_deepseek_llm.model, 'border-cyan-400/70');
        const gChoice = nodes.node6_guardrail_commit.answers?.final_commit_verdict?.choice || 'commit_and_dispatch';
        setNodeDone(6, `${nodes.node6_guardrail_commit.latency_ms} ms`, gChoice, 'border-fuchsia-500/70');

        document.getElementById('flowDiagramStatus').innerHTML = `<span class="text-emerald-400 font-bold">✓ 6 Düğüm Başarıyla Çalıştırıldı (${nodes.node4_gatekeeper.label})</span>`;

        // Also update the main right-side decision probability panel
        if (data.raw_decision_response) {
          renderDecisionResult(data.raw_decision_response);
        }

        // Render rich flow execution summary right inside the studio
        const s1Answers = nodes.node3_system1_drex.answers || {};
        const qSummaryCards = Object.entries(s1Answers).map(([qk, r]) => {
          let badge = '';
          if (r.type === 'noul') {
            const p = Number(r.noul || 0) * 100;
            badge = `<span class="px-2 py-0.5 rounded font-mono text-[11px] font-bold ${p >= 50 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}">${p >= 50 ? 'EVET' : 'HAYIR'} (%${p.toFixed(1)})</span>`;
          } else if (r.type === 'choice') {
            const wp = ((r.probabilities || {})[r.choice] || 0) * 100;
            badge = `<span class="px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 font-mono text-[11px] font-bold">★ ${r.choice} (%${wp.toFixed(1)})</span>`;
          } else if (r.type === 'score') {
            badge = `<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-[11px] font-bold">Skor: ${Number(r.score || 0).toFixed(2)}</span>`;
          }
          return `
            <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between gap-2 text-xs">
              <span class="font-mono text-slate-200 truncate" title="${qk}">${qk}</span>
              ${badge}
            </div>
          `;
        }).join('');

        out.innerHTML = `
          <div class="space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="text-xs font-bold text-emerald-300 uppercase tracking-wider">
                ⚡ Düğüm 3 & 4 Çıktısı: System-1 (${nodes.node3_system1_drex.model}) Olasılık Kararları & Gatekeeper Yönlendirmesi
              </div>
              <span class="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold font-mono">
                ${nodes.node4_gatekeeper.label}
              </span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
              ${qSummaryCards}
            </div>
            <div class="p-4 rounded-xl bg-slate-900/95 border border-cyan-500/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-cyan-300 uppercase tracking-wider">🧠 Düğüm 5 & 6 Çıktısı: DeepSeek V4.1 Flash Operasyon Ajanı + Guardrail (${gChoice})</span>
                <span class="text-[11px] font-mono text-slate-400">DeepSeek: ${nodes.node5_deepseek_llm.latency_ms} ms • Guardrail: ${nodes.node6_guardrail_commit.latency_ms} ms</span>
              </div>
              <pre class="text-xs text-slate-200 font-mono whitespace-pre-wrap leading-relaxed max-h-80 overflow-y-auto p-3 rounded-lg bg-slate-950 border border-slate-800">${(nodes.node5_deepseek_llm.output || '').replace(/</g, '&lt;')}</pre>
            </div>
          </div>
        `;
      } catch (e) {
        out.innerHTML = `<div class="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-xs text-rose-200">Hata: ${e.message}</div>`;
      } finally {
        btn.disabled = false;
        btn.innerHTML = orig;
      }
    }

    initApp();
    searchWebDocuments();
  </script>
</body>
</html>
"""


class PlaygroundHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        print(f"[DrexPlayground] {self.address_string()} - {format % args}")

    def _send_json(self, payload: Any, status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_html(self, html: str, status: int = 200) -> None:
        raw = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html(HTML_PAGE)
            return

        if parsed.path == "/api/config":
            ensure_sample_images()
            sample_images = {}
            for img_path in sorted(SAMPLES_DIR.glob("*.png")):
                sample_images[img_path.name] = encode_image_to_data_url(img_path)

            key = os.getenv("OPENROUTER_API_KEY", "").strip()
            masked = f"{key[:12]}...{key[-6:]}" if len(key) > 20 else ("Tanımlı" if key else "")

            self._send_json(
                {
                    "has_api_key": bool(key),
                    "masked_key": masked,
                    "models": SUPPORTED_MODELS,
                    "endpoints": ENDPOINTS,
                    "presets": get_presets(),
                    "sample_images": sample_images,
                }
            )
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if parsed.path == "/api/evaluate":
            model = body.get("model", "nace-ai/drex-max-finance")
            endpoint_type = body.get("endpoint_type", "decisions")
            state = body.get("state", "")
            questions = body.get("questions", {})
            result = evaluate_decision(
                state=state,
                questions=questions,
                model=model,
                endpoint_type=endpoint_type,
            )
            self._send_json(result)
            return

        if parsed.path == "/api/compare":
            models = body.get("models", ["nace-ai/drex-max-finance", "nace-ai/drex-max"])
            state = body.get("state", "")
            questions = body.get("questions", {})

            def _call(m: str) -> dict[str, Any]:
                res = evaluate_decision(state=state, questions=questions, model=m)
                res["model"] = m
                return res

            with concurrent.futures.ThreadPoolExecutor(max_workers=len(models)) as pool:
                results = list(pool.map(_call, models))

            self._send_json({"ok": True, "results": results})
            return

        if parsed.path == "/api/hybrid_pipeline":
            scenario_type = body.get("scenario_type", "wms_3way_matching")
            result = run_hybrid_logistics_pipeline(scenario_type=scenario_type)
            self._send_json(result)
            return

        if parsed.path == "/api/variation_matrix":
            domain = body.get("domain", "3way_matching")
            result = run_probability_variation_matrix(domain=domain)
            self._send_json(result)
            return

        if parsed.path == "/api/omnichannel_classify":
            bundle_type = body.get("bundle_type", "whatsapp_email_pod_dedup")
            result = run_omnichannel_doc_classifier_pipeline(bundle_type=bundle_type)
            self._send_json(result)
            return

        if parsed.path == "/api/whatsapp_deepseek_ops":
            workflow_type = body.get("workflow_type", "chat_to_load_and_crm_card")
            result = run_whatsapp_operations_and_deepseek_pipeline(workflow_type=workflow_type)
            self._send_json(result)
            return

        if parsed.path == "/api/web_image_search":
            query = body.get("query", "CMR irsaliye fatura")
            result = search_web_document_images(query=query)
            self._send_json(result)
            return

        if parsed.path == "/api/fetch_remote_image":
            image_url = body.get("image_url", "")
            result = fetch_remote_image_to_data_url(image_url=image_url)
            self._send_json(result)
            return

        if parsed.path == "/api/generate_dynamic_sim":
            domain = body.get("domain", "yuk_borsasi_ve_crm")
            custom_instruction = body.get("custom_instruction", "")
            image_data_url = body.get("image_data_url")
            result = generate_dynamic_simulation_with_deepseek(
                domain=domain,
                custom_instruction=custom_instruction,
                image_data_url=image_data_url,
            )
            self._send_json(result)
            return

        if parsed.path == "/api/run_dynamic_flow":
            result = execute_dynamic_flow_run(body)
            self._send_json(result)
            return

        self._send_json({"error": "Not found"}, status=404)


def run_server(port: int | None = None) -> None:
    ensure_sample_images()
    listen_port = port or int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("127.0.0.1", listen_port), PlaygroundHandler)
    print("=" * 68)
    print(f"🚀 Nace.AI Drex Max & Finance Playground çalışıyor: http://localhost:{listen_port}")
    print("=" * 68)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
        server.server_close()


if __name__ == "__main__":
    run_server()
