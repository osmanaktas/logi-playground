"""
Nace.AI Drex Max - Interactive Multimodal Decision Playground (Web UI + API Server).

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
    get_presets,
    make_image_part,
)
from sample_generator import SAMPLES_DIR, ensure_sample_images

load_dotenv(Path(__file__).parent / ".env")

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nace.AI Drex Max — Multimodal Decision Playground</title>
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
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-sky-500/20">
          DX
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg font-bold text-white tracking-tight">Nace.AI Drex Max Playground</h1>
            <span class="text-xs px-2 py-0.5 rounded-full bg-sky-500/15 text-sky-400 border border-sky-500/30 font-medium">27B Multimodal Decision Model</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-medium">System One API</span>
          </div>
          <p class="text-xs text-slate-400">OpenRouter (<code class="text-slate-300">nace-ai/drex-max</code>) • Metin, JSON ve 4 Görsele Kadar Tek İleri Geçişte (Single Forward Pass) Kalibre Olasılık Hesaplama</p>
        </div>
      </div>
      <div class="flex items-center gap-3 text-xs">
        <div id="apiKeyStatus" class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
          API Key kontrol ediliyor...
        </div>
        <a href="https://openrouter.ai/nace-ai/drex-max" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition">
          OpenRouter Sayfası ↗
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 pt-6 space-y-6">
    <!-- Architecture Overview Banner -->
    <section class="glass rounded-2xl p-4 grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
      <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80">
        <div class="text-slate-400 font-medium mb-1">🧠 Mimari & Okuma Kafası</div>
        <div class="text-white font-semibold text-sm">Dense 27B + 255-Way Readout</div>
        <p class="text-slate-400 mt-1">48 Gated DeltaNet + 16 Non-Causal Full-Attention katmanı. Metin üretmez; doğrudan olasılık dağılımı döner.</p>
      </div>
      <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80">
        <div class="text-slate-400 font-medium mb-1">👁️ Görsel Yetenekler (Vision)</div>
        <div class="text-sky-400 font-semibold text-sm">Vision Index: 73.92 / 100</div>
        <p class="text-slate-400 mt-1">InfographicVQA %97.3, KIE (Fatura/Fiş) %92.4, Mind2Web (UI Ajanı) %84.2, CharXiv %80.5. İstek başına 4 görsel.</p>
      </div>
      <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80">
        <div class="text-slate-400 font-medium mb-1">🎯 Soru Tipleri (Typed Questions)</div>
        <div class="text-indigo-400 font-semibold text-sm">noul • choice • score</div>
        <p class="text-slate-400 mt-1"><b>noul:</b> Evet/Hayır olasılığı (0-1)<br/><b>choice:</b> Çoktan seçmeli (255 şık)<br/><b>score:</b> Sıralı ölçek puanlama</p>
      </div>
      <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80">
        <div class="text-slate-400 font-medium mb-1">⚡ Bağlam & Maliyet</div>
        <div class="text-emerald-400 font-semibold text-sm">262K Context • $0.06 / 1M Girdi</div>
        <p class="text-slate-400 mt-1">Çıktı token ücreti $0/1M. JSON parse hatası veya halüsinasyon olmadan deterministik ajan kararları.</p>
      </div>
    </section>

    <!-- Preset Simulation Selector -->
    <section class="glass rounded-2xl p-5">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div>
          <h2 class="text-sm font-bold text-white uppercase tracking-wider">🚀 Hazır Yetenek & Görsel Simülasyon Senaryoları</h2>
          <p class="text-xs text-slate-400">Bir senaryoya tıklayarak görsel ve yapılandırılmış soruları otomatik yükleyip anında test edebilirsiniz.</p>
        </div>
        <button onclick="runAllVisionBenchmarks()" id="btnBatchRun" class="px-3.5 py-2 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 text-xs font-semibold transition">
          ⚡ Tüm Senaryoları Sırayla Simüle Et (Otomatik Test)
        </button>
      </div>
      <div id="presetList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3"></div>
    </section>

    <!-- Main Playground Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left Column: Inputs (State + Images + Questions) -->
      <div class="lg:col-span-7 space-y-6">
        <!-- Model & Endpoint Controls -->
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
              <label class="text-xs font-semibold text-sky-400 uppercase tracking-wider">🖼️ Görsel Girdi Stüdyosu (En Fazla 4 Görsel)</label>
              <button onclick="clearImages()" class="text-xs text-slate-400 hover:text-rose-400">Görselleri Temizle</button>
            </div>
            <p class="text-xs text-slate-400 mb-3">Hazır sentetik test görsellerine tıklayarak ekleyebilir veya bilgisayarınızdan kendi görselinizi (fatura, ekran görüntüsü, grafik, fotoğraf) yükleyebilirsiniz:</p>

            <!-- Built-in Sample Images -->
            <div id="sampleImagesBar" class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-3"></div>

            <!-- Custom Image Upload -->
            <div class="flex items-center gap-3">
              <label class="flex-1 cursor-pointer rounded-xl border border-dashed border-slate-700 hover:border-sky-500 bg-slate-900/60 px-4 py-2.5 text-center text-xs text-slate-300 transition">
                <span>📂 Bilgisayardan Görsel Yükle (PNG, JPEG, WebP) — Çoklu Seçim</span>
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
              <label class="text-xs font-semibold text-slate-300">📄 State (Metin veya JSON Bağlamı)</label>
              <span class="text-[11px] text-slate-400">Görsellerle birlikte üst düzey <code class="text-sky-400">state</code> dizisine eklenir</span>
            </div>
            <textarea id="stateInput" rows="4" class="w-full rounded-xl bg-slate-900 border border-slate-700 p-3 text-xs font-mono text-slate-100 focus:outline-none focus:border-sky-500" placeholder="Metin veya JSON bağlamı girin..."></textarea>
          </div>
        </div>

        <!-- Questions Builder -->
        <div class="glass rounded-2xl p-5 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold text-white">❓ Typed Questions (Yapılandırılmış Sorular)</h3>
              <p class="text-xs text-slate-400">Drex Max tüm soruları tek ileri geçişte (single forward pass) aynı anda yanıtlar.</p>
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
            <button id="btnEvaluate" onclick="submitDecision()" class="flex-1 py-3 px-5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-sky-500/20 transition flex items-center justify-center gap-2">
              <span>🎯 Drex Max Kararını Hesapla (Single Forward Pass)</span>
            </button>
            <button id="btnCompare" onclick="compareModels()" class="py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 font-semibold text-xs transition">
              ⚖️ Drex Max vs Drex Max Finance Karşılaştır
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column: Calibrated Probabilities Output & Code Inspector -->
      <div class="lg:col-span-5 space-y-6">
        <!-- Results Card -->
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
              Soldaki hazır senaryolardan birini seçin veya <b>"Drex Max Kararını Hesapla"</b> butonuna tıklayın.
            </div>
          </div>
        </div>

        <!-- Payload & Code Inspector -->
        <div class="glass rounded-2xl p-5 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider">💻 Ham API Payload & Python / cURL Kodu</h3>
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
    let activeImages = []; // Array of { name, data_url }
    let currentQuestions = {};
    let activeCodeTab = 'response';
    let lastRequestJson = {};
    let lastResponseJson = {};

    async function initApp() {
      const res = await fetch('/api/config');
      appConfig = await res.json();

      // API Key badge
      const keyEl = document.getElementById('apiKeyStatus');
      if (appConfig.has_api_key) {
        keyEl.innerHTML = `<span class="text-emerald-400 font-semibold">● API Key Aktif:</span> <code class="text-slate-400">${appConfig.masked_key}</code>`;
      } else {
        keyEl.innerHTML = `<span class="text-rose-400 font-semibold">● API Key Eksik (.env)</span>`;
      }

      // Models dropdown
      const modelSelect = document.getElementById('modelSelect');
      modelSelect.innerHTML = appConfig.models.map(m =>
        `<option value="${m.id}">${m.name} — $${m.input_price_per_m}/M</option>`
      ).join('');

      // Sample Images bar
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

      // Presets list
      const presetList = document.getElementById('presetList');
      presetList.innerHTML = appConfig.presets.map((p, idx) => `
        <div onclick="loadPreset('${p.id}')" id="preset_${p.id}" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-sky-500/60 transition flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <span class="text-[11px] px-2 py-0.5 rounded-md ${p.sample_images && p.sample_images.length ? 'bg-sky-500/15 text-sky-300 border border-sky-500/30' : 'bg-amber-500/15 text-amber-300 border border-amber-500/30'} font-medium">${p.badge}</span>
              <span class="text-[11px] text-slate-500 font-mono">${Object.keys(p.questions).length} soru</span>
            </div>
            <h4 class="text-xs font-bold text-white mb-1">${p.title}</h4>
            <p class="text-[11px] text-slate-400 line-clamp-3">${p.description}</p>
          </div>
          <div class="mt-2.5 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-sky-400 font-medium">
            <span>Senaryoyu Yükle</span>
            <span>→</span>
          </div>
        </div>
      `).join('');

      // Load first visual preset by default
      if (appConfig.presets.length > 0) {
        loadPreset(appConfig.presets[0].id);
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
        el.classList.remove('ring-2', 'ring-sky-500', 'border-sky-500');
      });
      const card = document.getElementById('preset_' + presetId);
      if (card) card.classList.add('ring-2', 'ring-sky-500');

      document.getElementById('modelSelect').value = preset.model || 'nace-ai/drex-max';

      // Load sample images
      activeImages = [];
      if (preset.sample_images && preset.sample_images.length) {
        for (const imgName of preset.sample_images) {
          if (appConfig.sample_images[imgName]) {
            activeImages.push({ name: imgName, data_url: appConfig.sample_images[imgName] });
          }
        }
      }
      renderActiveImages();

      // Load state
      if (preset.state_json) {
        document.getElementById('stateInput').value = JSON.stringify(preset.state_json, null, 2);
      } else {
        document.getElementById('stateInput').value = preset.state_text || '';
      }

      // Deep copy questions
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
        <div class="relative rounded-xl overflow-hidden border border-sky-500/60 bg-slate-900">
          <img src="${img.data_url}" class="w-full h-24 object-cover cursor-pointer" onclick="openLightbox('${img.name}', '${img.data_url}')" />
          <div class="p-1.5 bg-slate-950/90 flex items-center justify-between text-[11px]">
            <span class="truncate text-sky-300 font-mono">${i + 1}. ${img.name}</span>
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
                <input type="text" value="${key}" onchange="renameQuestionKey('${key}', this.value)" class="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs font-mono text-white font-semibold w-48" />
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

      // For multimodal requests, top-level state is an array of string(s) + image_url parts
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
      // Mask base64 in display preview so it stays readable
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
      btn.innerHTML = `<span>⏳ Drex Max Olasılıkları Hesaplıyor...</span>`;

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

      subtitle.innerHTML = `Model: <code class="text-sky-400">${resp.model || ''}</code> • Sağlayıcı: <b>${resp.provider || 'OpenRouter'}</b>`;
      badges.innerHTML = `
        <span class="px-2.5 py-1 rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 font-mono">${data.client_latency_ms} ms</span>
        <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-mono">${usage.input_tokens || 0} in / ${usage.output_tokens || 0} out tok</span>
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
                ${sorted.map(([opt, p], idx) => {
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
          ? ['nace-ai/drex-max', 'nace-ai/drex-max-finance']
          : ['nace-ai/drex-max', 'nace-ai/drex-max-finance', 'nace-ai/drex-v2.0'];

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
                      <span class="font-mono text-sky-400 font-semibold">${r.model}</span>
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

    async function runAllVisionBenchmarks() {
      const btn = document.getElementById('btnBatchRun');
      const orig = btn.innerHTML;
      btn.disabled = true;
      for (const preset of appConfig.presets) {
        btn.innerHTML = `⏳ Çalıştırılıyor: ${preset.badge}...`;
        loadPreset(preset.id);
        await submitDecision();
        await new Promise(r => setTimeout(r, 900));
      }
      btn.disabled = false;
      btn.innerHTML = orig;
    }

    initApp();
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
            model = body.get("model", "nace-ai/drex-max")
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
            models = body.get("models", ["nace-ai/drex-max", "nace-ai/drex-max-finance"])
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

        self._send_json({"error": "Not found"}, status=404)


def run_server(port: int | None = None) -> None:
    ensure_sample_images()
    listen_port = port or int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("127.0.0.1", listen_port), PlaygroundHandler)
    print("=" * 68)
    print(f"🚀 Nace.AI Drex Max Playground çalışıyor: http://localhost:{listen_port}")
    print("=" * 68)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
        server.server_close()


if __name__ == "__main__":
    run_server()
