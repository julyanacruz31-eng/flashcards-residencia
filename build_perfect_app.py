import json

with open("app_data_clean.json", "r", encoding="utf-8") as f:
    app_data = json.load(f)

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>MedFlashcards ✨ • Residência Médica</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Firebase (login Google + Firestore para salvar o progresso na nuvem) -->
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore-compat.js"></script>

  <!-- FontAwesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  
  <!-- Tailwind CSS CDN (opcional, com fallback inline robusto) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    if (typeof tailwind !== 'undefined') {
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              rosewater: {
                50: '#fff5f7',
                100: '#ffe4e8',
                200: '#fecdd6',
                300: '#fda4b4',
                400: '#fb718b',
                500: '#f43f68',
                600: '#e11d48',
                900: '#881337'
              }
            }
          }
        }
      }
    }
  </script>

  <!-- CSS COMPLETO E AUTÔNOMO (Garante visual perfeito em qualquer celular/tablet) -->
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: rgba(244, 63, 104, 0.15);
    }
    
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #fff5f8 0%, #fff9fb 50%, #fdf2f8 100%);
      color: #374151;
      min-height: 100vh;
      line-height: 1.5;
      padding-bottom: 90px; /* espaço para o bottom player e créditos */
      touch-action: manipulation;
    }

    button, input, select, textarea {
      font-family: inherit;
      touch-action: manipulation;
    }

    /* Utilitários base */
    .hidden { display: none !important; }

    /* Modal Overlay (Garantido 100% fechado por padrão) */
    .modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      align-items: center;
      justify-content: center;
      padding: 16px;
    }
    .modal-overlay.active {
      display: flex !important;
    }

    /* Glassmorphism Rosinha */
    .glass-card {
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(254, 205, 214, 0.7);
      box-shadow: 0 8px 24px -4px rgba(244, 114, 182, 0.08);
      border-radius: 20px;
    }

    .glass-header {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(254, 205, 214, 0.8);
    }

    /* Abas Principais Grandes e Toque Amigável */
    .main-tab-btn {
      flex: 1;
      min-height: 42px;
      padding: 6px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
      user-select: none;
      -webkit-user-select: none;
      white-space: nowrap;
    }

    .main-tab-btn.active {
      background: linear-gradient(135deg, #ffffff 0%, #fff1f4 100%);
      color: #e11d48;
      border-color: #fda4b4;
      box-shadow: 0 4px 12px rgba(244, 63, 104, 0.12);
    }

    .main-tab-btn.inactive {
      background: transparent;
      color: #64748b;
    }

    .main-tab-btn.inactive:hover, .main-tab-btn.inactive:active {
      background: rgba(255, 241, 244, 0.6);
      color: #334155;
    }

    /* Pílulas de Filtro */
    .filter-pill {
      min-height: 32px;
      padding: 5px 12px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
      -webkit-user-select: none;
      flex-shrink: 0;
    }

    .filter-pill.active {
      background: #e11d48;
      color: #ffffff;
      box-shadow: 0 3px 8px rgba(225, 29, 72, 0.25);
    }

    .filter-pill.inactive {
      background: #ffffff;
      color: #475569;
      border: 1px solid #fecdd6;
    }

    .filter-pill.inactive:active {
      background: #ffe4e8;
    }

    /* FLASHCARD 3D E SUPORTE SAFARI / WEBKIT */
    .flashcard-wrapper {
      perspective: 1200px;
      -webkit-perspective: 1200px;
      width: 100%;
      min-height: 410px;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      position: relative;
    }

    .flashcard-inner {
      position: relative;
      width: 100%;
      min-height: 410px;
      border-radius: 24px;
      transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
      box-shadow: 0 12px 32px -6px rgba(244, 63, 104, 0.12);
    }

    .flashcard-inner.is-flipped {
      transform: rotateY(180deg);
      -webkit-transform: rotateY(180deg);
    }

    .card-face {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border-radius: 24px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      background: #ffffff;
      border: 1.5px solid #fecdd6;
      overflow-y: auto;
    }

    .card-front {
      z-index: 2;
      transform: rotateY(0deg);
      -webkit-transform: rotateY(0deg);
    }

    .card-back {
      transform: rotateY(180deg);
      -webkit-transform: rotateY(180deg);
      background: linear-gradient(145deg, #fff5f7 0%, #ffffff 50%, #fff1f4 100%);
      border-color: #fda4b4;
    }

    /* Fallback extra de visibilidade se 3D estiver desativado no celular */
    .flashcard-inner.is-flipped .card-front {
      pointer-events: none;
    }

    /* Botões de Ação do Flashcard */
    .fc-action-btn {
      min-height: 44px;
      padding: 10px 16px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
      -webkit-user-select: none;
    }

    .fc-action-btn:active {
      transform: scale(0.97);
    }

    /* Scrollbar Suave */
    .custom-scroll::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scroll::-webkit-scrollbar-thumb {
      background: #fbcfe8;
      border-radius: 9999px;
    }

    /* Animação do Mini Player */
    @keyframes pulse-wave {
      0%, 100% { height: 6px; }
      50% { height: 18px; }
    }
    .wave-bar {
      animation: pulse-wave 1s ease-in-out infinite;
    }
  </style>
</head>
<body class="custom-scroll selection:bg-pink-200 selection:text-pink-900">

  <!-- ==========================================
       HEADER FIXO E COMPACTO (Foco Mobile/Tablet)
       ========================================== -->
  <header class="glass-header sticky top-0 z-40 shadow-sm">
    <div class="max-w-4xl mx-auto px-4 py-2.5 flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-rose-400 via-pink-400 to-rose-500 flex items-center justify-center text-white text-lg shadow-md shadow-pink-200">
          <span>🩺</span>
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h1 class="font-serif font-bold text-lg text-rose-800 leading-tight">
              MedFlashcards <span class="text-xs font-sans font-bold text-pink-500">✨</span>
            </h1>
            <span class="px-2 py-0.5 text-[9px] font-extrabold uppercase bg-pink-100 text-rose-700 border border-pink-200 rounded-full">
              Residência Médica
            </span>
          </div>
          <p class="text-[11px] text-rose-500 font-medium">
            Rumo à Residência dos Sonhos 🌸
          </p>
        </div>
      </div>

      <!-- Ações do Topo -->
      <div class="flex items-center gap-2">
        <button id="cloudBtn" onclick="cloudButtonClick()" class="hidden h-9 px-3 rounded-xl bg-white text-slate-700 border border-pink-200 flex items-center gap-1.5 text-xs font-bold hover:bg-pink-50 transition active:scale-95" title="Salvar progresso na nuvem">
          <i id="cloudIcon" class="fa-brands fa-google text-[12px]"></i>
          <span id="cloudLabel">Entrar</span>
        </button>
        <button onclick="openModal('exportModal')" class="w-9 h-9 rounded-xl bg-pink-50 text-rose-600 border border-pink-200 flex items-center justify-center text-xs font-bold hover:bg-pink-100 transition active:scale-95" title="Backup">
          <i class="fa-solid fa-cloud-arrow-down"></i>
        </button>
        <button onclick="openModal('addModal')" class="h-9 px-3.5 rounded-xl bg-gradient-to-r from-rose-500 to-pink-500 text-white flex items-center gap-1.5 text-xs font-bold shadow-md shadow-pink-200 hover:opacity-95 transition active:scale-95">
          <i class="fa-solid fa-plus text-[11px]"></i>
          <span>Adicionar</span>
        </button>
      </div>
    </div>

    <!-- BARRA DE NAVEGAÇÃO DE ABAS PRINCIPAIS (Toque Fácil) -->
    <div class="bg-rose-50/70 border-t border-rose-100 px-3 py-1.5">
      <div class="max-w-4xl mx-auto flex items-center justify-between gap-1.5">
        <button onclick="switchTab('tabelas')" id="tabBtn-tabelas" class="main-tab-btn active">
          <span>📋 Tabelas</span> <span class="text-[10px] bg-rose-100 text-rose-700 font-extrabold px-1.5 py-0.5 rounded-full" id="badgeCount-tabelas">169</span>
        </button>
        <button onclick="switchTab('flashcards')" id="tabBtn-flashcards" class="main-tab-btn inactive">
          <span>🗂️ Cards</span> <span class="text-[10px] bg-pink-100 text-rose-700 font-extrabold px-1.5 py-0.5 rounded-full" id="badgeCount-flashcards">204</span>
        </button>
        <button onclick="switchTab('geral')" id="tabBtn-geral" class="main-tab-btn inactive">
          <span>🎯 Já Caiu</span> <span class="text-[10px] bg-pink-100 text-rose-700 font-extrabold px-1.5 py-0.5 rounded-full" id="badgeCount-geral">8</span>
        </button>
      </div>
    </div>
  </header>

  <!-- ==========================================
       CONTEÚDO PRINCIPAL
       ========================================== -->
  <main class="max-w-4xl mx-auto px-4 py-4 w-full">

    <!-- FILTRO DE GRANDES ÁREAS (Comum a todas as abas) -->
    <div class="mb-4">
      <div class="flex items-center gap-1.5 overflow-x-auto custom-scroll pb-1">
        <span class="text-rose-500 font-extrabold text-[11px] mr-1 shrink-0 flex items-center gap-1">
          <i class="fa-solid fa-filter text-[10px]"></i> Área:
        </span>
        <button onclick="setAreaFilter('todas')" class="filter-pill active" data-area="todas">Todas</button>
        <button onclick="setAreaFilter('clinica')" class="filter-pill inactive" data-area="clinica">Clínica / Cardio</button>
        <button onclick="setAreaFilter('cirurgia')" class="filter-pill inactive" data-area="cirurgia">Cirurgia Geral</button>
        <button onclick="setAreaFilter('pediatria')" class="filter-pill inactive" data-area="pediatria">Pediatria</button>
        <button onclick="setAreaFilter('go')" class="filter-pill inactive" data-area="go">Ginecologia & Obstetrícia</button>
        <button onclick="setAreaFilter('preventiva')" class="filter-pill inactive" data-area="preventiva">Preventiva</button>
      </div>
    </div>

    <!-- ==========================================
         ABA 1: TABELAS DE REVISÃO
         ========================================== -->
    <section id="view-tabelas" class="tab-view block space-y-4">
      <!-- Subfiltro por tipo de tabela -->
      <div class="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-rose-200">
        <div class="flex items-center gap-1.5 overflow-x-auto custom-scroll pb-1">
          <button onclick="setCategoryFilter('todas')" class="filter-pill active" data-cat="todas">Todas as Tabelas</button>
          <button onclick="setCategoryFilter('eponimos')" class="filter-pill inactive" data-cat="eponimos">Epônimos</button>
          <button onclick="setCategoryFilter('triades')" class="filter-pill inactive" data-cat="triades">Tríades & Pêntades</button>
          <button onclick="setCategoryFilter('doencas')" class="filter-pill inactive" data-cat="doencas">Doenças (Epidemio + Tto)</button>
        </div>
        <div class="text-[11px] font-bold text-rose-500 shrink-0" id="tableItemCount">169 itens</div>
      </div>

      <!-- Container dos Itens da Tabela -->
      <div id="tablesContainer" class="space-y-3.5">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>

    <!-- ==========================================
         ABA 2: FLASHCARDS INTERATIVOS (MODO FIXAÇÃO)
         ========================================== -->
    <section id="view-flashcards" class="tab-view hidden space-y-3.5">
      <div class="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-rose-200">
        <div class="flex items-center gap-2">
          <span class="text-sm">🗂️</span>
          <div>
            <h2 class="text-xs font-bold uppercase tracking-wider text-rose-800">Trilha & Cronograma SRS</h2>
            <p class="text-[10px] text-rose-500">Revisão espaçada inteligente • Acerto aumenta o intervalo</p>
          </div>
        </div>
        <div class="flex items-center gap-1.5">
          <button onclick="openTrailModal()" class="px-2.5 py-1 rounded-xl bg-white hover:bg-rose-50 text-rose-700 border border-rose-200 text-[11px] font-bold flex items-center gap-1 shadow-xs transition active:scale-95">
            <span>🗺️ Índice</span>
          </button>
          <button onclick="openModal('tipsModal')" class="px-2.5 py-1 rounded-xl bg-pink-50 hover:bg-pink-100 text-rose-700 border border-pink-200 text-[11px] font-bold flex items-center gap-1 transition active:scale-95">
            <span>🧠 Técnicas</span>
          </button>
          <div class="text-right pl-1">
            <div class="text-xs font-mono font-bold text-rose-600" id="flashcardCounter">Card 1 de 133</div>
            <div class="text-[10px] text-slate-500 font-semibold" id="flashcardScore">🌸 0 hoje</div>
          </div>
        </div>
      </div>

      <!-- Painel de Cronograma SRS e Previsão 7 Dias -->
      <div id="srsDashboard" class="glass-card p-3 space-y-2.5">
        <!-- Renderizado dinamicamente via JS -->
      </div>

      <!-- Modos de Estudo e Trilhas por Especialidade -->
      <div id="fcControls" class="space-y-2">
        <!-- Renderizado dinamicamente via JS -->
      </div>

      <!-- Card Interativo e Controles -->
      <div id="flashcardSection" class="w-full max-w-lg mx-auto">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>

    <!-- ==========================================
         ABA 3: JÁ CAIU NA MACKENZIE (Bancas)
         ========================================== -->
    <section id="view-geral" class="tab-view hidden space-y-4">
      <div class="flex items-center justify-between pb-2 border-b border-rose-200">
        <div class="flex items-center gap-2">
          <span class="text-sm">🎯</span>
          <div>
            <h2 class="text-xs font-bold uppercase tracking-wider text-rose-800">Padrões & Pegadinhas da Bancas na Geral</h2>
            <p class="text-[10px] text-rose-500">O que a banca repete e os detalhes decisivos de prova</p>
          </div>
        </div>
        <div class="text-[11px] font-bold text-rose-500" id="mackCount">8 tópicos</div>
      </div>

      <div id="mackContainer" class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>

  </main>

  <!-- ==========================================
       BOTTOM MINI AUDIO PLAYER (Fixo no Rodapé)
       ========================================== -->
  <div id="bottomAudioPlayer" class="fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-lg border-t border-rose-200 shadow-2xl px-4 py-2.5 transition-transform duration-300 translate-y-full">
    <div class="max-w-4xl mx-auto flex items-center justify-between gap-3">
      
      <!-- Info do Áudio -->
      <div class="flex items-center gap-2.5 min-w-0 flex-1">
        <div class="w-9 h-9 rounded-xl bg-pink-100 text-rose-600 flex items-center justify-center shrink-0 border border-pink-200">
          <div id="playerWave" class="hidden flex items-end gap-0.5 h-4">
            <span class="w-1 bg-pink-500 rounded-full wave-bar" style="animation-delay: 0.1s"></span>
            <span class="w-1 bg-rose-500 rounded-full wave-bar" style="animation-delay: 0.3s"></span>
            <span class="w-1 bg-purple-500 rounded-full wave-bar" style="animation-delay: 0.2s"></span>
          </div>
          <i id="playerStaticIcon" class="fa-solid fa-headphones text-xs"></i>
        </div>
        <div class="min-w-0">
          <p id="audioPlayerTitle" class="text-xs font-bold text-slate-800 truncate">Macete em Áudio</p>
          <div class="flex items-center gap-2 text-[10px] text-rose-500">
            <span id="audioCurrentTime" class="font-mono">1.7x</span>
            <span>•</span>
            <button onclick="openScriptModal()" class="text-rose-700 underline font-semibold">Ver Texto & Pular</button>
          </div>
        </div>
      </div>

      <!-- Controles de Áudio -->
      <div class="flex items-center gap-1.5">
        <button onclick="audioSkip(-1)" class="w-8 h-8 rounded-xl bg-rose-50 hover:bg-pink-100 text-slate-600 flex items-center justify-center text-xs transition active:scale-95" title="Frase Anterior">
          <i class="fa-solid fa-backward-step"></i>
        </button>

        <button id="audioPlayBtn" onclick="toggleAudio()" class="w-10 h-10 rounded-2xl bg-gradient-to-r from-rose-500 to-pink-500 text-white flex items-center justify-center text-sm shadow-md shadow-pink-200 transition active:scale-95">
          <i id="audioPlayIcon" class="fa-solid fa-play"></i>
        </button>

        <button onclick="audioSkip(1)" class="w-8 h-8 rounded-xl bg-rose-50 hover:bg-pink-100 text-slate-600 flex items-center justify-center text-xs transition active:scale-95" title="Próxima Frase">
          <i class="fa-solid fa-forward-step"></i>
        </button>

        <button onclick="cycleSpeed()" id="speedBadge" class="px-2 py-1 rounded-xl bg-pink-100 text-pink-700 font-mono font-bold text-[11px] border border-pink-200">
          1.7x ⭐
        </button>

        <button onclick="closeAudioPlayer()" class="w-7 h-7 rounded-lg text-slate-400 hover:text-rose-600 flex items-center justify-center text-xs transition ml-0.5">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

    </div>
  </div>

  <!-- ==========================================
       MODAL: VER TEXTO DO ÁUDIO
       ========================================== -->
  <div id="scriptModal" class="modal-overlay" style="display: none;">
    <div class="bg-white border border-pink-200 rounded-3xl w-full max-w-lg max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
      <div class="p-4 border-b border-rose-100 flex items-center justify-between bg-pink-50/60">
        <div class="flex items-center gap-2">
          <span>🎙️</span>
          <h3 class="text-sm font-bold text-slate-800">Roteiro do Áudio • Clique para pular</h3>
        </div>
        <button onclick="closeModal('scriptModal')" class="text-slate-400 hover:text-rose-600 p-1">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div id="scriptParagraphsContainer" class="p-4 overflow-y-auto space-y-2 text-xs leading-relaxed custom-scroll flex-1">
        <!-- Preenchido via JS -->
      </div>
      <div class="p-3 border-t border-rose-100 bg-rose-50/40 text-[11px] text-rose-600 text-center font-medium">
        Toque em qualquer frase para o áudio começar dali ✨
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: ADICIONAR NOVO ITEM
       ========================================== -->
  <div id="addModal" class="modal-overlay" style="display: none;">
    <div class="bg-white border border-pink-200 rounded-3xl w-full max-w-lg max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
      <div class="p-4 border-b border-rose-100 flex items-center justify-between bg-gradient-to-r from-pink-50 to-rose-50">
        <div class="flex items-center gap-2">
          <span class="text-base">🎀</span>
          <h3 class="text-sm font-bold text-slate-800">Adicionar ao MedFlashcards</h3>
        </div>
        <button onclick="closeModal('addModal')" class="text-slate-400 hover:text-rose-600 p-1">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Abas de Tipo de Inserção -->
      <div class="flex border-b border-rose-100 px-4 pt-2 gap-2 text-xs font-bold overflow-x-auto no-scrollbar">
        <button onclick="setAddType('tabela')" id="addType-tabela" class="py-1.5 px-3 border-b-2 border-rose-500 text-rose-600">📋 Na Tabela</button>
        <button onclick="setAddType('flashcard')" id="addType-flashcard" class="py-1.5 px-3 text-slate-400 hover:text-slate-700">🗂️ Flashcard</button>
        <button onclick="setAddType('geral')" id="addType-geral" class="py-1.5 px-3 text-slate-400 hover:text-slate-700">🎯 Já Caiu Mack</button>
        <button onclick="setAddType('raw')" id="addType-raw" class="py-1.5 px-3 text-slate-400 hover:text-slate-700">📝 Colar Texto Solto</button>
      </div>

      <!-- Form Body -->
      <div class="p-4 overflow-y-auto space-y-3 text-xs flex-1 custom-scroll">
        <div class="grid grid-cols-2 gap-2.5" id="field-area-cat">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Grande Área</label>
            <select id="inputArea" class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300">
              <option value="clinica">Clínica Médica / Cardio</option>
              <option value="cirurgia">Cirurgia Geral</option>
              <option value="pediatria">Pediatria</option>
              <option value="go">Ginecologia & Obstetrícia</option>
              <option value="preventiva">Medicina Preventiva</option>
            </select>
          </div>
          <div id="field-cat-container">
            <label class="block font-bold text-slate-700 mb-1">Tipo de Tabela</label>
            <select id="inputCat" class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300">
              <option value="eponimos">Epônimo</option>
              <option value="triades">Tríade / Pêntade</option>
              <option value="doencas">Doença (Epidemio + Tto)</option>
            </select>
          </div>
        </div>

        <!-- Form Tabela -->
        <div id="form-tabela" class="space-y-2.5">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Nome do Epônimo / Doença / Tríade</label>
            <input type="text" id="tabName" placeholder="Ex: Tríade de Beck ou Técnica de Lichtenstein..." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300">
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Definição / Achados / Epidemiologia</label>
            <textarea id="tabCol1" rows="2" placeholder="Ex: Hipotensão + Bulhas hipofonéticas + Turgência jugular..." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Diagnóstico & Conduta Terapêutica</label>
            <textarea id="tabCol2" rows="2" placeholder="Ex: Pericardiocentese de alívio imediata..." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Macete em Áudio (Lido a 1.7x)</label>
            <textarea id="tabAudio" rows="2" placeholder="Texto explicativo para ser lido em áudio..." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
        </div>

        <!-- Form Flashcard -->
        <div id="form-flashcard" class="space-y-2.5 hidden">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Frente do Cartão (Pergunta)</label>
            <textarea id="fcFront" rows="2" placeholder="Ex: Qual o antibiótico de escolha para celulite estreptocócica?" class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Verso do Cartão (Resposta Direta)</label>
            <textarea id="fcBack" rows="2" placeholder="Ex: Cefazolina ou Oxacilina IV; Cefalexina VO." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Macete Falado em Áudio</label>
            <textarea id="fcAudio" rows="2" placeholder="Explicação falada para fixação rápida..." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
        </div>

        <!-- Form Já Caiu Geral -->
        <div id="form-geral" class="space-y-2.5 hidden">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Tema / Assunto Cobrado</label>
            <input type="text" id="mackTitle" placeholder="Ex: SHU pós-STEC" class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300">
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Pegadinha / Como a banca cobra</label>
            <textarea id="mackTip" rows="3" placeholder="Ex: Antibiótico é contraindicado por risco de liberação maciça de toxina Shiga..." class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300"></textarea>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Ano / Prova (Ex: Geral 2024, ENARE 2025)</label>
            <input type="text" id="mackYear" placeholder="Ex: Geral 2024 / Bancas" class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300">
          </div>
        </div>

        <!-- Form Colar Texto Solto -->
        <div id="form-raw" class="space-y-2.5 hidden">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Cole aqui notas, tabelas ou resumos soltos</label>
            <textarea id="rawText" rows="6" placeholder="Pode colar qualquer anotação bruta. O app salva e eu posso estruturar tudo para você aqui no chat!" class="w-full bg-rose-50/50 border border-rose-200 rounded-xl p-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-pink-300 custom-scroll"></textarea>
          </div>
        </div>
      </div>

      <!-- Form Footer -->
      <div class="p-3 border-t border-rose-100 flex items-center justify-end gap-2 bg-white">
        <button onclick="closeModal('addModal')" class="px-3.5 py-2 rounded-xl text-slate-400 hover:text-slate-600 text-xs font-bold">Cancelar</button>
        <button onclick="submitNewItem()" class="px-5 py-2 rounded-xl bg-gradient-to-r from-rose-500 to-pink-500 text-white font-bold text-xs shadow-md shadow-pink-200 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-solid fa-check"></i> Salvar no App
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: BACKUP E SINCRONIZAÇÃO
       ========================================== -->
  <div id="exportModal" class="modal-overlay" style="display: none;">
    <div class="bg-white border border-pink-200 rounded-3xl w-full max-w-sm flex flex-col shadow-2xl overflow-hidden">
      <div class="p-4 border-b border-rose-100 flex items-center justify-between bg-pink-50/60">
        <div class="flex items-center gap-2">
          <span>☁️</span>
          <h3 class="text-xs font-bold text-slate-800">Sincronização & Backup</h3>
        </div>
        <button onclick="closeModal('exportModal')" class="text-slate-400 hover:text-rose-600 p-1">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="p-4 space-y-3 text-xs">
        <p class="text-slate-600 leading-relaxed">
          Para transferir entre o notebook, celular e tablet:
        </p>

        <div class="space-y-2">
          <button onclick="exportData()" class="w-full py-2.5 px-4 rounded-xl bg-pink-100 text-pink-700 font-bold hover:bg-pink-200 transition flex items-center justify-center gap-2 active:scale-95">
            <i class="fa-solid fa-download"></i> Baixar Arquivo JSON
          </button>
          
          <label class="w-full py-2.5 px-4 rounded-xl border border-dashed border-rose-300 text-rose-600 font-bold hover:bg-rose-50 transition flex items-center justify-center gap-2 cursor-pointer active:scale-95">
            <i class="fa-solid fa-upload"></i> Restaurar no Celular
            <input type="file" id="importFileInput" onchange="importData(event)" class="hidden" accept=".json">
          </label>
        </div>

        <p class="text-[11px] text-rose-400 text-center pt-1">
          ✨ Se preferir, é só me mandar qualquer novo assunto aqui no chat que eu integro diretamente no código!
        </p>
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: ÍNDICE SEQUENCIAL DA TRILHA
       ========================================== -->
  <div id="trailModal" class="modal-overlay" style="display: none;">
    <div class="bg-white border border-pink-200 rounded-3xl w-full max-w-lg max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
      <div class="p-4 border-b border-rose-100 flex items-center justify-between bg-pink-50/60">
        <div class="flex items-center gap-2">
          <span>🗺️</span>
          <div>
            <h3 class="text-xs font-bold text-slate-800">Índice Sequencial da Trilha</h3>
            <p class="text-[10px] text-rose-500">Toque em qualquer card para ir direto para ele</p>
          </div>
        </div>
        <button onclick="closeModal('trailModal')" class="text-slate-400 hover:text-rose-600 p-1">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div id="trailModalList" class="p-3 overflow-y-auto custom-scroll space-y-1.5 text-xs">
        <!-- Renderizado via JS -->
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: TÉCNICAS DE MEMORIZAÇÃO ATIVA
       ========================================== -->
  <div id="tipsModal" class="modal-overlay" style="display: none;">
    <div class="bg-white border border-pink-200 rounded-3xl w-full max-w-md max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
      <div class="p-4 border-b border-rose-100 flex items-center justify-between bg-pink-50/60">
        <div class="flex items-center gap-2">
          <span>🧠</span>
          <h3 class="text-xs font-bold text-slate-800">Como Decorar Tudo Mais Rápido</h3>
        </div>
        <button onclick="closeModal('tipsModal')" class="text-slate-400 hover:text-rose-600 p-1">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div class="p-4 overflow-y-auto custom-scroll space-y-3 text-xs text-slate-700 leading-relaxed">
        <div class="bg-rose-50/70 p-3 rounded-2xl border border-rose-100">
          <div class="font-bold text-rose-800 mb-1">1. 📅 Repetição Espaçada (SRS)</div>
          <p>Não revise tudo todo dia! Se você acertou fácil, o app empurra o card para <b>3, 7, 15, 30 dias</b>. Se errou, ele volta em <b>5 minutos</b> na mesma sessão e reaparece amanhã.</p>
        </div>
        <div class="bg-pink-50/70 p-3 rounded-2xl border border-pink-100">
          <div class="font-bold text-rose-800 mb-1">2. 💡 Pista Ativa (Antes de Virar)</div>
          <p>Travou na pergunta? Não vire direto! Clique em <b>"💡 Quero uma dica"</b> na frente do card. Forçar o cérebro a lembrar com uma pista cria sinapses muito mais fortes do que apenas ler a resposta.</p>
        </div>
        <div class="bg-amber-50/70 p-3 rounded-2xl border border-amber-100">
          <div class="font-bold text-amber-900 mb-1">3. 🔗 Ancoragem pelo "Porquê"</div>
          <p>Sempre leia o bloco <b>💡 Por que? / Fisiopatologia</b> no verso. Quando você entende a lógica física (ex: a albumina é grande e fica presa na peneira), você deduz o número na prova mesmo se der branco.</p>
        </div>
        <div class="bg-emerald-50/70 p-3 rounded-2xl border border-emerald-100">
          <div class="font-bold text-emerald-900 mb-1">4. 🗣️ Regra dos 15 Segundos + Áudio 1.7x</div>
          <p>Responda <b>em voz alta</b> em até 15s antes de virar. Se errar, clique em <b>"🔊 Ouvir 1.7x"</b> no verso para fixar pela via auditiva também.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- ==========================================
       SCRIPT PRINCIPAL 100% BLINDADO E UNIVERSAL
       ========================================== -->
  <script>
    // ESTADO INICIAL
    var appState = """ + json.dumps(app_data, ensure_ascii=False) + """;

    var activeTab = 'tabelas';
    var activeArea = 'todas';
    var activeCategory = 'todas';
    var currentFlashcardIndex = 0;
    var isFlipped = false;
    var showHint = false;
    var fcDraftAnswers = {};
    var clozeMode = false;
    var fcStudyMode = 'schedule'; // 'schedule' | 'mixed' | 'sequential' | 'hard'
    var shuffleSeed = Date.now();
    var trailPinnedId = null; // card aberto pela Trilha, exibido mesmo se agendado para depois
    var fcSpecialty = 'todas';
    var fcSubtopic = 'todos';
    var srsData = {};
    var srsStats = { reviewedToday: 0, newToday: 0, lastReviewDate: '', examDate: 0 };
    var addModalType = 'tabela';
    var flashcardScores = { correct: 0, review: 0 };

    // Player de Áudio
    var currentSpeed = 1.7;
    var isPlaying = false;
    var currentSpeechText = "";
    var speechUtterance = null;
    var speechChunks = [];
    var currentChunkIndex = 0;
    var selectedVoice = null;
    var voicesList = [];

    // INICIALIZAÇÃO SEGURA
    window.addEventListener('DOMContentLoaded', function() {
      try { loadState(); } catch(e) { console.warn('loadState err', e); }
      try { initCloud(); } catch(e) { console.warn('initCloud err', e); }
      try { initSpeech(); } catch(e) { console.warn('initSpeech err', e); }
      try { updateBadges(); } catch(e) {}
      try { renderCurrentTab(); } catch(e) { console.error('render err', e); }
    });

    function getTodayStr() {
      var d = new Date();
      return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    }

    function loadState() {
      try {
        var stored = localStorage.getItem('dermatomack_data_v5');
        if (stored) {
          var parsed = JSON.parse(stored);
          if (parsed.flashcards && parsed.flashcards.length > 0) {
            var existingIds = {};
            for (var i = 0; i < appState.flashcards.length; i++) existingIds[appState.flashcards[i].id] = true;
            for (var j = 0; j < parsed.flashcards.length; j++) {
              if (!existingIds[parsed.flashcards[j].id]) appState.flashcards.push(parsed.flashcards[j]);
            }
          }
          if (parsed.tables && parsed.tables.length > 0) {
            var existingTIds = {};
            for (var ti = 0; ti < appState.tables.length; ti++) existingTIds[appState.tables[ti].id] = true;
            for (var tj = 0; tj < parsed.tables.length; tj++) {
              if (!existingTIds[parsed.tables[tj].id]) appState.tables.push(parsed.tables[tj]);
            }
          }
          if (parsed.geral && parsed.geral.length > 0) appState.geral = parsed.geral;
        }
        var srsRaw = localStorage.getItem('medflashcards_srs_v1');
        if (srsRaw) {
          var srsParsed = JSON.parse(srsRaw);
          if (srsParsed.srsData) srsData = srsParsed.srsData;
          if (srsParsed.srsStats) srsStats = srsParsed.srsStats;
        }
        var today = getTodayStr();
        if (srsStats.lastReviewDate !== today) {
          srsStats.reviewedToday = 0;
          srsStats.newToday = 0;
          srsStats.lastReviewDate = today;
        }
        if (!srsStats.examDate) {
          srsStats.examDate = getStartOfDay(37);
          saveSRS();
        }
      } catch (e) {
        console.warn('Storage read restricted:', e);
      }
    }

    function writeLocalSRS() {
      try {
        srsStats.lastReviewDate = getTodayStr();
        localStorage.setItem('medflashcards_srs_v1', JSON.stringify({
          srsData: srsData,
          srsStats: srsStats
        }));
      } catch (e) {
        console.warn('SRS write restricted:', e);
      }
    }

    function saveSRS() {
      writeLocalSRS();
      scheduleCloudPush();
    }

    // ==========================================
    // NUVEM: login Google + Firestore (users/{uid})
    // O progresso continua salvo no navegador (funciona offline) e, com login,
    // também na nuvem. Em cada card vale a avaliação mais recente (lastReview),
    // então estudar em dois aparelhos não apaga nada.
    // ==========================================
    var firebaseConfig = {
      apiKey: "AIzaSyB0kzjfZJ3VRHZXLnDB3NNyGWQ9CkU9lj0",
      authDomain: "medflashcards.firebaseapp.com",
      projectId: "medflashcards",
      storageBucket: "medflashcards.firebasestorage.app",
      messagingSenderId: "274560630804",
      appId: "1:274560630804:web:a5566e360f6936ff86a701"
    };
    var cloud = { auth: null, db: null, user: null, unsub: null, pushTimer: null, status: 'off' };

    function initCloud() {
      if (typeof firebase === 'undefined') { setCloudStatus('unavailable'); return; }
      try {
        if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
        cloud.auth = firebase.auth();
        cloud.db = firebase.firestore();
        setCloudStatus('off');
        cloud.auth.onAuthStateChanged(function(user) {
          cloud.user = user;
          if (cloud.unsub) { cloud.unsub(); cloud.unsub = null; }
          if (user) {
            setCloudStatus('syncing');
            startCloudListener();
          } else {
            setCloudStatus('off');
          }
        });
        document.addEventListener('visibilitychange', function() {
          if (document.visibilityState === 'hidden') flushCloudPush();
        });
      } catch (e) {
        console.warn('cloud init', e);
        setCloudStatus('error');
      }
    }

    function cloudDocRef() {
      return cloud.db.collection('users').doc(cloud.user.uid);
    }

    // Junta o progresso da nuvem no local. Retorna true se algo local mudou.
    function mergeRemoteSRS(remote) {
      var changed = false;
      var rData = (remote && remote.srsData) || {};
      for (var id in rData) {
        if (!rData.hasOwnProperty(id)) continue;
        var r = rData[id], l = srsData[id];
        if (!l || (r.lastReview || 0) > (l.lastReview || 0)) { srsData[id] = r; changed = true; }
      }
      var rs = remote && remote.srsStats;
      if (rs) {
        var rSet = rs.examSetAt || 0, lSet = srsStats.examSetAt || 0;
        var takeExam = rs.examDate && (rSet > lSet || (rSet === lSet && !lSet && rs.examDate !== srsStats.examDate));
        if (takeExam) { srsStats.examDate = rs.examDate; srsStats.examSetAt = rs.examSetAt || 0; changed = true; }
        var today = getTodayStr();
        if (rs.lastReviewDate === today) {
          if (srsStats.lastReviewDate !== today) {
            srsStats.reviewedToday = rs.reviewedToday || 0; srsStats.newToday = rs.newToday || 0; changed = true;
          } else {
            if ((rs.reviewedToday || 0) > (srsStats.reviewedToday || 0)) { srsStats.reviewedToday = rs.reviewedToday; changed = true; }
            if ((rs.newToday || 0) > (srsStats.newToday || 0)) { srsStats.newToday = rs.newToday; changed = true; }
          }
        }
      }
      return changed;
    }

    // A nuvem está atrás do local? (card faltando/mais antigo ou estatística diferente)
    function cloudNeedsPush(remote) {
      if (!remote) return Object.keys(srsData).length > 0 || !!srsStats.examSetAt;
      var rData = remote.srsData || {};
      for (var id in srsData) {
        if (!srsData.hasOwnProperty(id)) continue;
        if (!rData[id] || (srsData[id].lastReview || 0) > (rData[id].lastReview || 0)) return true;
      }
      var rs = remote.srsStats || {};
      return rs.examDate !== srsStats.examDate || (rs.reviewedToday || 0) !== (srsStats.reviewedToday || 0) || rs.lastReviewDate !== srsStats.lastReviewDate;
    }

    function startCloudListener() {
      cloud.unsub = cloudDocRef().onSnapshot(function(snap) {
        if (snap.metadata.hasPendingWrites) return;
        var remote = snap.exists ? snap.data() : null;
        if (mergeRemoteSRS(remote)) {
          writeLocalSRS();
          if (!(activeTab === 'flashcards' && isFlipped)) { try { renderCurrentTab(); } catch (e) {} }
        }
        if (cloudNeedsPush(remote)) pushCloudNow();
        else setCloudStatus('ok');
      }, function(err) {
        console.warn('cloud listen', err);
        setCloudStatus('error');
      });
    }

    function scheduleCloudPush() {
      if (!cloud.user || !cloud.db) return;
      setCloudStatus('syncing');
      if (cloud.pushTimer) clearTimeout(cloud.pushTimer);
      cloud.pushTimer = setTimeout(pushCloudNow, 1200);
    }

    function flushCloudPush() {
      if (cloud.pushTimer) pushCloudNow();
    }

    function pushCloudNow() {
      if (cloud.pushTimer) { clearTimeout(cloud.pushTimer); cloud.pushTimer = null; }
      if (!cloud.user || !cloud.db) return;
      cloudDocRef().set({
        srsData: srsData,
        srsStats: srsStats,
        updatedAt: firebase.firestore.FieldValue.serverTimestamp()
      }).then(function() {
        setCloudStatus('ok');
      }).catch(function(err) {
        console.warn('cloud push', err);
        setCloudStatus('error');
      });
    }

    function setCloudStatus(status) {
      cloud.status = status;
      var btn = document.getElementById('cloudBtn');
      var icon = document.getElementById('cloudIcon');
      var label = document.getElementById('cloudLabel');
      if (!btn || !icon || !label) return;
      if (status === 'unavailable') { btn.classList.add('hidden'); return; }
      btn.classList.remove('hidden');
      var first = (cloud.user && (cloud.user.displayName || cloud.user.email) || '').split(' ')[0];
      if (status === 'off') {
        icon.className = 'fa-brands fa-google text-[12px]';
        label.innerText = 'Entrar';
        btn.title = 'Entrar com Google para salvar o progresso na nuvem';
      } else if (status === 'syncing') {
        icon.className = 'fa-solid fa-rotate fa-spin text-[12px] text-sky-500';
        label.innerText = first || 'Salvando';
        btn.title = 'Sincronizando com a nuvem...';
      } else if (status === 'ok') {
        icon.className = 'fa-solid fa-cloud text-[12px] text-emerald-500';
        label.innerText = first || 'Na nuvem';
        btn.title = 'Progresso salvo na nuvem' + (cloud.user && cloud.user.email ? ' (' + cloud.user.email + ')' : '');
      } else {
        icon.className = 'fa-solid fa-triangle-exclamation text-[12px] text-amber-500';
        label.innerText = 'Offline';
        btn.title = 'Sem conexão com a nuvem. O progresso fica salvo neste aparelho e sobe quando voltar.';
      }
    }

    function cloudButtonClick() {
      if (!cloud.auth) return;
      if (!cloud.user) {
        var provider = new firebase.auth.GoogleAuthProvider();
        provider.setCustomParameters({ prompt: 'select_account' });
        cloud.auth.signInWithPopup(provider).catch(function(err) {
          if (err && (err.code === 'auth/popup-closed-by-user' || err.code === 'auth/cancelled-popup-request')) return;
          console.warn('login', err);
          alert('Não foi possível entrar com Google' + (err && err.code ? ' (' + err.code + ')' : '') + '. Se o navegador bloqueou a janela, permita pop-ups para este site e tente de novo.');
        });
        return;
      }
      if (cloud.status === 'error') { setCloudStatus('syncing'); pushCloudNow(); return; }
      var who = cloud.user.email || cloud.user.displayName || 'sua conta';
      if (confirm('Progresso salvo na nuvem em ' + who + '.\\n\\nDeseja sair desta conta? (o progresso continua neste aparelho e na nuvem)')) {
        flushCloudPush();
        cloud.auth.signOut();
      }
    }

    function saveState() {
      try {
        localStorage.setItem('dermatomack_data_v5', JSON.stringify(appState));
      } catch (e) {
        console.warn('Storage write restricted:', e);
      }
      saveSRS();
      updateBadges();
      renderCurrentTab();
    }

    function updateBadges() {
      var bTab = document.getElementById('badgeCount-tabelas');
      var bFc = document.getElementById('badgeCount-flashcards');
      var bMack = document.getElementById('badgeCount-geral');
      if (bTab) bTab.innerText = appState.tables ? appState.tables.length : 0;
      if (bFc) bFc.innerText = appState.flashcards ? appState.flashcards.length : 0;
      if (bMack) bMack.innerText = appState.geral ? appState.geral.length : 0;
    }

    // ==========================================
    // NAVEGAÇÃO DE ABAS (100% GARANTIDA POR STYLE.DISPLAY)
    // ==========================================
    function switchTab(tabId) {
      activeTab = tabId;

      // Esconde todas as abas
      var tabs = ['tabelas', 'flashcards', 'geral'];
      for (var i = 0; i < tabs.length; i++) {
        var t = tabs[i];
        var view = document.getElementById('view-' + t);
        var btn = document.getElementById('tabBtn-' + t);
        if (view) {
          view.style.display = (t === tabId) ? 'block' : 'none';
          if (t === tabId) view.classList.remove('hidden');
          else view.classList.add('hidden');
        }
        if (btn) {
          if (t === tabId) {
            btn.className = "main-tab-btn active";
          } else {
            btn.className = "main-tab-btn inactive";
          }
        }
      }

      renderCurrentTab();
      try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch(e) {}
    }

    function setAreaFilter(area) {
      activeArea = area;
      var btns = document.querySelectorAll('.filter-pill[data-area]');
      for (var i = 0; i < btns.length; i++) {
        var b = btns[i];
        if (b.getAttribute('data-area') === area) {
          b.className = "filter-pill active";
        } else {
          b.className = "filter-pill inactive";
        }
      }
      currentFlashcardIndex = 0;
      isFlipped = false;
      renderCurrentTab();
    }

    function setCategoryFilter(cat) {
      activeCategory = cat;
      var btns = document.querySelectorAll('.filter-pill[data-cat]');
      for (var i = 0; i < btns.length; i++) {
        var b = btns[i];
        if (b.getAttribute('data-cat') === cat) {
          b.className = "filter-pill active";
        } else {
          b.className = "filter-pill inactive";
        }
      }
      renderTables();
    }

    function renderCurrentTab() {
      if (activeTab === 'tabelas') renderTables();
      else if (activeTab === 'flashcards') renderFlashcards();
      else if (activeTab === 'geral') renderGeral();
    }

    // ==========================================
    // RENDER: TABELAS
    // ==========================================
    function renderTables() {
      var container = document.getElementById('tablesContainer');
      var countEl = document.getElementById('tableItemCount');
      if (!container) return;

      var filtered = appState.tables.filter(function(item) {
        var matchArea = activeArea === 'todas' || item.area === activeArea;
        var matchCat = activeCategory === 'todas' || item.cat === activeCategory;
        return matchArea && matchCat;
      });

      if (countEl) countEl.innerText = filtered.length + " itens";

      if (filtered.length === 0) {
        container.innerHTML = '<div class="glass-card p-6 text-center space-y-2 border border-pink-200">' +
          '<div class="text-2xl">📋</div>' +
          '<h3 class="font-bold text-sm text-slate-800">Nenhum item encontrado nesta área</h3>' +
          '<p class="text-xs text-rose-500">Mude o filtro acima ou clique em "+ Adicionar".</p>' +
        '</div>';
        return;
      }

      var html = '';
      for (var i = 0; i < filtered.length; i++) {
        var item = filtered[i];
        var audioBtn = '';
        if (item.audioText) {
          audioBtn = '<button onclick="playItemAudioByIndex(' + item.id + ', \\'table\\')" class="px-2.5 py-1 rounded-xl bg-pink-100 text-rose-700 hover:bg-pink-200 text-xs font-bold flex items-center gap-1.5 transition active:scale-95 shrink-0">' +
            '<i class="fa-solid fa-volume-high text-[11px]"></i>' +
            '<span>Ouvir 1.7x</span>' +
          '</button>';
        }

        html += '<div class="glass-card p-4 sm:p-5 space-y-2.5 transition">' +
          '<div class="flex items-center justify-between gap-2">' +
            '<div class="flex items-center gap-1.5 flex-wrap">' +
              '<span class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-pink-50 text-rose-700 border border-pink-200">' +
                getAreaLabel(item.area) +
              '</span>' +
              '<span class="text-[10px] font-bold text-slate-400">• ' + getCatLabel(item.cat) + '</span>' +
            '</div>' +
            audioBtn +
          '</div>' +
          '<h3 class="font-bold text-sm sm:text-base text-slate-800 leading-snug">' + escapeText(item.name) + '</h3>' +
          '<div class="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs pt-1">' +
            '<div class="bg-rose-50/50 p-3 rounded-xl border border-rose-100/80">' +
              '<span class="font-bold text-rose-600 block mb-1">Definição & Achados:</span>' +
              '<p class="text-slate-600 leading-relaxed">' + (item.col1 || '-') + '</p>' +
            '</div>' +
            '<div class="bg-pink-50/50 p-3 rounded-xl border border-pink-100/80">' +
              '<span class="font-bold text-pink-700 block mb-1">Diagnóstico & Conduta:</span>' +
              '<p class="text-slate-600 leading-relaxed">' + (item.col2 || '-') + '</p>' +
            '</div>' +
          '</div>' +
        '</div>';
      }
      container.innerHTML = html;
    }

    // ==========================================
    // MOTOR DE REPETIÇÃO ESPAÇADA (SRS) & TRILHA SEQUENCIAL
    // ==========================================
    function getStartOfDay(offsetDays) {
      var d = new Date();
      d.setHours(0, 0, 0, 0);
      d.setDate(d.getDate() + (offsetDays || 0));
      return d.getTime();
    }

    function getDaysRemaining() {
      var target = srsStats.examDate || getStartOfDay(37);
      var diff = Math.ceil((target - getStartOfDay(0)) / (24 * 60 * 60 * 1000));
      return Math.max(1, diff);
    }

    function clampIntervalToExam(days) {
      var rem = getDaysRemaining();
      if (rem <= 3) return 1;
      var maxAllowed = Math.max(1, rem - 2);
      return Math.min(days, maxAllowed);
    }

    function adjustExamDays() {
      var cur = getDaysRemaining();
      var input = prompt('Quantos dias faltam para a sua prova? (Cronograma ajusta o teto dos intervalos automaticamente)', cur);
      if (input === null) return;
      var num = parseInt(input, 10);
      if (!isNaN(num) && num >= 1 && num <= 365) {
        srsStats.examDate = getStartOfDay(num);
        srsStats.examSetAt = Date.now();
        saveSRS();
        renderFlashcards();
      }
    }

    function getCardSRS(id) {
      return srsData[id] || { reps: 0, interval: 0, ease: 2.5, due: 0, lapses: 0, lastReview: 0, state: 'new' };
    }

    function computeNextIntervalDays(s, quality) {
      if (quality === 0) return 0;
      if (quality === 1) return 1;
      if (quality === 2) {
        var raw = 1;
        if (s.reps === 0) raw = 1;
        else if (s.reps === 1) raw = 3;
        else if (s.reps === 2) raw = 6;
        else if (s.reps === 3) raw = 12;
        else raw = Math.min(20, Math.round((s.interval || 12) * 1.6));
        return clampIntervalToExam(raw);
      }
      if (quality === 3) {
        var rawEasy = 3;
        if (s.reps === 0) rawEasy = 3;
        else if (s.reps === 1) rawEasy = 7;
        else rawEasy = Math.min(22, Math.max(7, Math.round((s.interval || 6) * 1.8)));
        return clampIntervalToExam(rawEasy);
      }
      return 1;
    }

    function previewNextInterval(cardId, quality) {
      var s = getCardSRS(cardId);
      if (quality === 0) return '5 min';
      var iv = computeNextIntervalDays(s, quality);
      return iv + (iv === 1 ? ' dia' : ' dias');
    }

    function getBaseFilteredFlashcards() {
      return appState.flashcards.filter(function(fc) {
        var matchTop = true;
        if (activeArea !== 'todas') {
          if (activeArea === 'clinica') {
            matchTop = (fc.area === 'clinica' || fc.area === 'cardiologia' || fc.area === 'pneumologia' || fc.area === 'gastroenterologia' || fc.area === 'endocrinologia' || fc.area === 'reumatologia' || fc.area === 'hematologia');
          } else {
            matchTop = fc.area === activeArea;
          }
        }
        var matchSpec = (fcSpecialty === 'todas' || fc.area === fcSpecialty);
        var matchSub = (fcSubtopic === 'todos' || fc.cat === fcSubtopic);
        return matchTop && matchSpec && matchSub;
      });
    }

    function seededRand(seed) {
      var x = Math.sin(seed++) * 10000;
      return x - Math.floor(x);
    }

    function interleaveBySpecialty(list) {
      if (!list || list.length <= 1) return list ? list.slice() : [];
      var buckets = {};
      var keys = [];
      for (var i = 0; i < list.length; i++) {
        var k = list[i].area || 'geral';
        if (!buckets[k]) { buckets[k] = []; keys.push(k); }
        buckets[k].push(list[i]);
      }
      // Ordem estável: cada card/especialidade recebe uma chave fixa derivada da semente,
      // assim tirar um card da fila (ex.: avaliado como Fácil) não embaralha os demais.
      var s = shuffleSeed || 1;
      function keyHash(str) {
        var h = 0;
        for (var c = 0; c < str.length; c++) h = (h * 31 + str.charCodeAt(c)) | 0;
        return h;
      }
      for (var ki = 0; ki < keys.length; ki++) {
        buckets[keys[ki]].sort(function(a, b) {
          return seededRand(s + a.id * 7919) - seededRand(s + b.id * 7919);
        });
      }
      keys.sort(function(a, b) {
        return seededRand(s + keyHash(a)) - seededRand(s + keyHash(b));
      });
      var result = [];
      var added = true;
      while (added) {
        added = false;
        for (var p = 0; p < keys.length; p++) {
          var b = buckets[keys[p]];
          if (b.length > 0) {
            result.push(b.shift());
            added = true;
          }
        }
      }
      return result;
    }

    function reshuffleCards() {
      shuffleSeed = Date.now();
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function getStudyQueue() {
      var allBase = getBaseFilteredFlashcards();
      var now = Date.now();
      var endOfToday = getStartOfDay(1) - 1;

      // Card já avaliado e agendado para um dia futuro (ex.: Fácil -> 3 dias) não aparece
      // em nenhum modo até a data dele. Exceção: o card aberto pela Trilha (trailPinnedId).
      var base = allBase.filter(function(fc) {
        if (fc.id === trailPinnedId) return true;
        var s = getCardSRS(fc.id);
        return s.state === 'new' || s.due <= endOfToday;
      });

      if (fcStudyMode === 'mixed') {
        return interleaveBySpecialty(base);
      }
      if (fcStudyMode === 'sequential') {
        return base.slice().sort(function(a, b) { return a.id - b.id; });
      }
      if (fcStudyMode === 'hard') {
        return base.filter(function(fc) {
          var s = getCardSRS(fc.id);
          return s.lapses > 0 || (s.state === 'learning' && s.interval <= 1);
        }).sort(function(a, b) {
          return getCardSRS(b.id).lapses - getCardSRS(a.id).lapses;
        });
      }
      // Modo 'schedule' (Cronograma de Hoje):
      // 1) Vencidos prontos AGORA (due <= now) -> 2) Novos -> 3) Erros recentes aguardando intervalo (now < due <= endOfToday)
      var readyDueList = [];
      var waitingRelearnList = [];
      var newList = [];
      for (var i = 0; i < base.length; i++) {
        var fc = base[i];
        var s = getCardSRS(fc.id);
        if (s.state === 'new') {
          newList.push(fc);
        } else if (s.due <= now) {
          readyDueList.push(fc);
        } else if (s.due <= endOfToday) {
          waitingRelearnList.push(fc);
        }
      }
      readyDueList.sort(function(a, b) {
        return getCardSRS(a.id).due - getCardSRS(b.id).due;
      });
      waitingRelearnList.sort(function(a, b) {
        return getCardSRS(a.id).due - getCardSRS(b.id).due;
      });
      return interleaveBySpecialty(readyDueList)
        .concat(interleaveBySpecialty(newList))
        .concat(waitingRelearnList);
    }

    function renderSRSDashboard(baseCards) {
      var dash = document.getElementById('srsDashboard');
      if (!dash) return;
      var endOfToday = getStartOfDay(1) - 1;
      var dueToday = 0, newCount = 0, learningCount = 0, masteredCount = 0, hardCount = 0;
      var forecast = [0, 0, 0, 0, 0, 0, 0];

      for (var i = 0; i < baseCards.length; i++) {
        var s = getCardSRS(baseCards[i].id);
        if (s.lapses > 0) hardCount++;
        if (s.state === 'new') {
          newCount++;
          forecast[0]++;
        } else {
          if (s.due <= endOfToday) dueToday++;
          if (s.interval >= 7) masteredCount++;
          else learningCount++;

          for (var d = 0; d < 7; d++) {
            var dStart = (d === 0) ? 0 : getStartOfDay(d);
            var dEnd = getStartOfDay(d + 1) - 1;
            if (s.due >= dStart && s.due <= dEnd) {
              forecast[d]++;
              break;
            }
          }
        }
      }

      var dayLabels = ['Hoje', 'Amanhã', '+2d', '+3d', '+4d', '+5d', '+6d'];
      var forecastHtml = '';
      for (var f = 0; f < 7; f++) {
        var isToday = (f === 0);
        forecastHtml += '<div class="flex-1 text-center py-1 px-0.5 rounded-lg ' + (isToday ? 'bg-rose-100/80 border border-rose-200' : 'bg-white/70 border border-pink-100') + '">' +
          '<div class="text-[9px] font-bold ' + (isToday ? 'text-rose-700' : 'text-slate-400') + '">' + dayLabels[f] + '</div>' +
          '<div class="text-[11px] font-extrabold ' + (forecast[f] > 0 ? 'text-rose-600' : 'text-slate-300') + '">' + forecast[f] + '</div>' +
        '</div>';
      }

      var daysLeft = getDaysRemaining();
      var studyDaysLeft = Math.max(1, daysLeft - 4);
      var dailyNewGoal = newCount > 0 ? Math.max(5, Math.ceil(newCount / studyDaysLeft)) : 0;

      dash.innerHTML =
        '<div class="flex items-center justify-between bg-gradient-to-r from-rose-500 to-pink-500 text-white rounded-xl px-3 py-2 shadow-xs">' +
          '<div class="flex items-center gap-2">' +
            '<span class="text-sm">⏳</span>' +
            '<div>' +
              '<div class="text-[11px] font-extrabold leading-tight">Faltam ' + daysLeft + ' dias para a Prova</div>' +
              '<div class="text-[10px] text-rose-100">Meta de hoje: ' + (dueToday + dailyNewGoal) + ' cards (' + dueToday + ' rev + ' + dailyNewGoal + ' novos) • Nenhum card passa do prazo!</div>' +
            '</div>' +
          '</div>' +
          '<button onclick="adjustExamDays()" class="px-2 py-1 rounded-lg bg-white/20 hover:bg-white/30 text-[10px] font-bold shrink-0 transition">⚙️ Prazo</button>' +
        '</div>' +
        '<div class="grid grid-cols-4 gap-1.5 text-center">' +
          '<div class="bg-rose-50/80 border border-rose-100 rounded-xl py-1.5 px-1">' +
            '<div class="text-[10px] font-bold text-rose-600">📅 P/ Hoje</div>' +
            '<div class="text-sm font-extrabold text-rose-800">' + (dueToday + newCount) + '</div>' +
          '</div>' +
          '<div class="bg-amber-50/80 border border-amber-100 rounded-xl py-1.5 px-1">' +
            '<div class="text-[10px] font-bold text-amber-700">🔥 Difíceis</div>' +
            '<div class="text-sm font-extrabold text-amber-900">' + hardCount + '</div>' +
          '</div>' +
          '<div class="bg-pink-50/80 border border-pink-100 rounded-xl py-1.5 px-1">' +
            '<div class="text-[10px] font-bold text-pink-600">🌱 Fixando</div>' +
            '<div class="text-sm font-extrabold text-pink-800">' + learningCount + '</div>' +
          '</div>' +
          '<div class="bg-emerald-50/80 border border-emerald-100 rounded-xl py-1.5 px-1">' +
            '<div class="text-[10px] font-bold text-emerald-700">🏆 Dominados</div>' +
            '<div class="text-sm font-extrabold text-emerald-900">' + masteredCount + '</div>' +
          '</div>' +
        '</div>' +
        '<div>' +
          '<div class="flex items-center justify-between text-[10px] font-bold text-slate-500 mb-1">' +
            '<span>📆 Previsão de Revisões (7 dias)</span>' +
            '<span class="text-rose-500">✅ ' + srsStats.reviewedToday + ' revisados hoje</span>' +
          '</div>' +
          '<div class="flex items-center gap-1">' + forecastHtml + '</div>' +
        '</div>';
    }

    function renderFCControls() {
      var ctrl = document.getElementById('fcControls');
      if (!ctrl) return;

      var modes = [
        { id: 'schedule', label: '📅 Cronograma (Hoje)' },
        { id: 'mixed', label: '🎲 Misturado' },
        { id: 'sequential', label: '📖 Sequencial (1→N)' },
        { id: 'hard', label: '🔥 Pontos Fracos' }
      ];
      var modeHtml = '';
      for (var m = 0; m < modes.length; m++) {
        var active = (fcStudyMode === modes[m].id);
        modeHtml += '<button onclick="setFCStudyMode(\\'' + modes[m].id + '\\')" class="filter-pill ' + (active ? 'active' : 'inactive') + '">' + modes[m].label + '</button>';
      }
      if (fcStudyMode === 'mixed' || fcStudyMode === 'schedule') {
        modeHtml += '<button onclick="reshuffleCards()" class="filter-pill bg-pink-50 text-rose-700 border border-pink-200 hover:bg-pink-100" title="Gerar nova mistura de especialidades">🔀 Misturar</button>';
      }

      var specs = [
        { id: 'todas', label: 'Todas' },
        { id: 'cardiologia', label: '❤️ Cardio' },
        { id: 'pneumologia', label: '🫁 Pneumo' },
        { id: 'gastroenterologia', label: '🩺 Gastro' },
        { id: 'endocrinologia', label: '🦋 Endocrino' },
        { id: 'reumatologia', label: '🦴 Reumato' },
        { id: 'hematologia', label: '🩸 Hemato' }
      ];
      var specHtml = '';
      for (var s = 0; s < specs.length; s++) {
        var sActive = (fcSpecialty === specs[s].id);
        specHtml += '<button onclick="setFCSpecialty(\\'' + specs[s].id + '\\')" class="filter-pill ' + (sActive ? 'active' : 'inactive') + '">' + specs[s].label + '</button>';
      }

      // Subtópicos dinâmicos da especialidade selecionada
      var subMap = {};
      for (var i = 0; i < appState.flashcards.length; i++) {
        var fc = appState.flashcards[i];
        if ((fcSpecialty === 'todas' || fc.area === fcSpecialty) && fc.cat) {
          subMap[fc.cat] = true;
        }
      }
      var subs = Object.keys(subMap);
      var subHtml = '';
      if (subs.length > 0) {
        subHtml += '<button onclick="setFCSubtopic(\\'todos\\')" class="filter-pill ' + (fcSubtopic === 'todos' ? 'active' : 'inactive') + '">Todos os Temas</button>';
        for (var k = 0; k < subs.length; k++) {
          var subId = subs[k];
          subHtml += '<button onclick="setFCSubtopic(\\'' + subId + '\\')" class="filter-pill ' + (fcSubtopic === subId ? 'active' : 'inactive') + '">' + getCatLabel(subId) + '</button>';
        }
      }

      ctrl.innerHTML =
        '<div class="flex items-center gap-1.5 overflow-x-auto custom-scroll pb-0.5">' + modeHtml + '</div>' +
        '<div class="flex items-center gap-1.5 overflow-x-auto custom-scroll pb-0.5">' + specHtml + '</div>' +
        (subHtml ? '<div class="flex items-center gap-1.5 overflow-x-auto custom-scroll pb-0.5">' + subHtml + '</div>' : '');
    }

    function setFCStudyMode(mode) {
      fcStudyMode = mode;
      trailPinnedId = null;
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function setFCSpecialty(spec) {
      fcSpecialty = spec;
      fcSubtopic = 'todos';
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function setFCSubtopic(sub) {
      fcSubtopic = sub;
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function buildSmartHint(card) {
      var topic = card.name ? ('Tema: ' + card.name) : 'Dica rápida';
      var raw = card.audioText || card.back || '';
      var clean = raw.replace(/[⏱️💡🔗⚠️•📌🎯]/g, '').trim();
      var words = clean.split(/\\s+/);
      var clue = '';
      if (words.length > 4) {
        clue = words.slice(0, 6).join(' ') + '...';
      } else {
        clue = clean;
      }
      return { topic: topic, clue: clue };
    }

    function formatCardBack(text) {
      if (!text) return '';
      var lines = String(text).split(/\\r?\\n/);
      var out = '';
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        if (!line) continue;
        var escaped = escapeText(line);
        if (line.indexOf('💡') === 0 || line.indexOf('🔗') === 0) {
          out += '<div class="bg-amber-50/90 border border-amber-200 rounded-xl px-2.5 py-1.5 text-left text-xs text-amber-950 font-semibold leading-relaxed">' + escaped + '</div>';
        } else if (line.indexOf('⚠️') === 0) {
          out += '<div class="bg-rose-100/80 border border-rose-200 rounded-xl px-2.5 py-1.5 text-left text-xs text-rose-900 font-semibold leading-relaxed">' + escaped + '</div>';
        } else if (line.indexOf('•') === 0 || line.indexOf('-') === 0 || /^\\d+\\./.test(line)) {
          out += '<div class="text-left text-xs sm:text-sm text-slate-700 font-medium leading-relaxed pl-1">' + escaped + '</div>';
        } else {
          out += '<div class="text-sm sm:text-base font-bold text-rose-700 leading-snug">' + escaped + '</div>';
        }
      }
      return out;
    }

    function toggleHint(e) {
      if (e) e.stopPropagation();
      showHint = !showHint;
      renderFlashcards();
    }

    function renderFlashcards() {
      var section = document.getElementById('flashcardSection');
      var counter = document.getElementById('flashcardCounter');
      var scoreEl = document.getElementById('flashcardScore');
      if (!section) return;

      var baseCards = getBaseFilteredFlashcards();
      renderSRSDashboard(baseCards);
      renderFCControls();

      var filtered = getStudyQueue();

      if (scoreEl) {
        scoreEl.innerText = "🌸 " + srsStats.reviewedToday + " revisados hoje";
      }

      if (filtered.length === 0) {
        if (counter) counter.innerText = "0 de 0";
        var emptyTitle = (fcStudyMode === 'schedule') ? '🎉 Meta de Hoje Concluída!' : (fcStudyMode === 'hard' ? '✨ Nenhum ponto fraco pendente!' : 'Nenhum flashcard neste filtro');
        var allScheduled = baseCards.length > 0;
        if (fcStudyMode !== 'schedule' && fcStudyMode !== 'hard' && allScheduled) emptyTitle = '🎉 Tudo em dia neste filtro!';
        var emptyDesc = (fcStudyMode === 'schedule')
          ? 'Você zerou todas as revisões programadas para hoje neste módulo!'
          : (allScheduled
            ? 'Todos os cards deste filtro já estão agendados para os próximos dias. Eles voltam sozinhos na data certa (veja a Trilha).'
            : 'Mude o filtro ou volte para o modo Sequencial para revisar toda a trilha.');
        section.innerHTML = '<div class="glass-card p-6 text-center space-y-3 border border-pink-200">' +
          '<div class="text-3xl">' + (fcStudyMode === 'schedule' ? '🏆' : '🗂️') + '</div>' +
          '<h3 class="font-bold text-sm text-slate-800">' + emptyTitle + '</h3>' +
          '<p class="text-xs text-rose-500">' + emptyDesc + '</p>' +
          '<button onclick="setFCStudyMode(\\'sequential\\')" class="px-4 py-2 rounded-xl bg-gradient-to-r from-rose-500 to-pink-500 text-white text-xs font-bold shadow-sm transition active:scale-95">📖 Estudar em Ordem Sequencial</button>' +
        '</div>';
        return;
      }

      if (currentFlashcardIndex >= filtered.length) currentFlashcardIndex = 0;
      var current = filtered[currentFlashcardIndex];
      var srs = getCardSRS(current.id);
      if (counter) counter.innerText = "Card " + (currentFlashcardIndex + 1) + " de " + filtered.length + " (#" + current.id + ")";

      var statusBadge = '';
      if (srs.state === 'new') statusBadge = '<span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200">🆕 Novo</span>';
      else if (srs.lapses > 0 && srs.interval <= 1) statusBadge = '<span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">🔥 Rever (' + srs.lapses + 'x)</span>';
      else if (srs.interval >= 7) statusBadge = '<span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">🏆 ' + srs.interval + 'd</span>';
      else statusBadge = '<span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-pink-50 text-rose-700 border border-pink-200">🌱 ' + srs.interval + 'd</span>';

      var hintData = buildSmartHint(current);
      var hintBox = showHint
        ? '<div onclick="event.stopPropagation()" class="mt-2 bg-amber-50/90 border border-amber-200 rounded-xl p-2.5 text-left space-y-0.5">' +
            '<div class="text-[10px] font-extrabold text-amber-800 uppercase">' + escapeText(hintData.topic) + '</div>' +
            '<div class="text-xs text-amber-900 font-medium">💡 Pista: ' + escapeText(hintData.clue) + '</div>' +
          '</div>'
        : '';

      var flippedClass = isFlipped ? " is-flipped" : "";

      var html = '<div class="space-y-3">' +
        '<!-- Cartão 3D Interativo -->' +
        '<div class="flashcard-wrapper" onclick="flipFlashcard()">' +
          '<div id="flashcardInner" class="flashcard-inner' + flippedClass + '">' +

            '<!-- FRENTE -->' +
            '<div class="card-face card-front">' +
              '<div class="flex items-center justify-between gap-1.5 flex-wrap">' +
                '<div class="flex items-center gap-1.5">' +
                  '<span class="text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full bg-pink-50 text-rose-700 border border-pink-200">' +
                    getAreaLabel(current.area) +
                  '</span>' +
                  statusBadge +
                '</div>' +
                '<button onclick="toggleHint(event)" class="px-2.5 py-1 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 text-[11px] font-bold transition active:scale-95">' +
                  (showHint ? '🙈 Ocultar Dica' : '💡 Quero uma dica') +
                '</button>' +
              '</div>' +
              '<div class="text-center my-auto px-2 py-3">' +
                '<p class="text-base sm:text-lg font-bold text-slate-800 leading-snug">' + escapeText(current.front) + '</p>' +
                hintBox +
              '</div>' +
              '<div class="text-[11px] text-center text-rose-400 font-medium bg-rose-50/50 py-1.5 px-3 rounded-xl border border-rose-100">' +
                'Toque no card para conferir a resposta e o porquê ✨' +
              '</div>' +
            '</div>' +

            '<!-- VERSO -->' +
            '<div class="card-face card-back">' +
              '<div class="flex items-center justify-between gap-2 pb-1">' +
                '<span class="text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-700">' +
                  escapeText(current.name || 'Resposta & Macete') +
                '</span>' +
                (current.audioText ?
                  '<button onclick="event.stopPropagation(); playCurrentFCAudio()" class="px-2.5 py-1 rounded-xl bg-rose-100 hover:bg-rose-200 text-rose-800 text-xs font-bold flex items-center gap-1.5 transition active:scale-95 shrink-0">' +
                    '<i class="fa-solid fa-volume-high"></i> Ouvir 1.7x' +
                  '</button>' : '') +
              '</div>' +
              '<div class="my-auto px-1 py-2 space-y-2">' +
                formatCardBack(current.back) +
                (current.audioText ? '<p class="text-[11px] text-slate-600 italic bg-white/80 p-2 rounded-xl border border-pink-100 leading-relaxed text-left">🎧 "' + escapeText(current.audioText) + '"</p>' : '') +
              '</div>' +
              '<div class="text-[10px] text-center text-rose-400 font-medium pt-1">' +
                'Avalie abaixo para agendar a próxima revisão 📅' +
              '</div>' +
            '</div>' +

          '</div>' +
        '</div>' +

        '<!-- Rascunho Ativo (Active Recall) -->' +
        '<div class="glass-card p-3 border border-pink-200/80 bg-white/95 space-y-1.5">' +
          '<div class="flex items-center justify-between">' +
            '<label for="fcScratchpad" class="text-[11px] font-extrabold text-rose-700 flex items-center gap-1.5">' +
              '<span>✍️ Meu Rascunho</span>' +
              '<span class="text-[10px] font-medium text-slate-400">(para raciocinar e conferir depois)</span>' +
            '</label>' +
            '<button type="button" onclick="clearFCDraft(' + current.id + ')" class="text-[10px] font-bold text-rose-400 hover:text-rose-600 px-1.5 py-0.5 rounded-lg hover:bg-rose-50 transition">Limpar</button>' +
          '</div>' +
          '<textarea id="fcScratchpad" rows="2" oninput="saveFCDraft(' + current.id + ', this.value)" placeholder="Escreva aqui o que você lembra antes de virar o card..." class="w-full rounded-xl border border-pink-200 bg-rose-50/30 px-3 py-2 text-xs sm:text-sm text-slate-800 placeholder:text-rose-300 focus:outline-none focus:ring-2 focus:ring-rose-300 focus:bg-white resize-y leading-relaxed">' + escapeText(fcDraftAnswers[current.id] || '') + '</textarea>' +
        '</div>' +

        '<!-- Botão Explícito de Virar -->' +
        '<div class="flex items-center gap-2">' +
          '<button onclick="prevFlashcard(' + filtered.length + ')" class="px-3 py-2.5 rounded-xl bg-white hover:bg-rose-50 text-slate-600 text-xs font-bold border border-rose-200 transition active:scale-95"><i class="fa-solid fa-arrow-left"></i></button>' +
          '<button onclick="flipFlashcard()" class="flex-1 py-2.5 rounded-xl bg-pink-50 hover:bg-pink-100 text-rose-700 text-xs font-bold border border-pink-200 transition active:scale-98 flex items-center justify-center gap-2">' +
            '<i class="fa-solid fa-arrows-rotate"></i>' +
            '<span>' + (isFlipped ? 'Voltar para a Pergunta' : 'Mostrar Resposta & Macete') + '</span>' +
          '</button>' +
          '<button onclick="nextFlashcard(' + filtered.length + ')" class="px-3 py-2.5 rounded-xl bg-white hover:bg-rose-50 text-slate-600 text-xs font-bold border border-rose-200 transition active:scale-95"><i class="fa-solid fa-arrow-right"></i></button>' +
        '</div>' +

        '<!-- Botões de Repetição Espaçada (SRS) com Intervalo Dinâmico -->' +
        '<div class="grid grid-cols-4 gap-1.5 pt-0.5">' +
          '<button onclick="rateCard(' + current.id + ', 0)" class="fc-action-btn flex-col !gap-0.5 !py-2 !px-1 bg-rose-50 hover:bg-rose-100 text-rose-800 border border-rose-200 shadow-xs">' +
            '<span class="text-xs font-extrabold">❌ Errei</span>' +
            '<span class="text-[10px] font-semibold text-rose-600">' + previewNextInterval(current.id, 0) + '</span>' +
          '</button>' +
          '<button onclick="rateCard(' + current.id + ', 1)" class="fc-action-btn flex-col !gap-0.5 !py-2 !px-1 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 shadow-xs">' +
            '<span class="text-xs font-extrabold">😅 Difícil</span>' +
            '<span class="text-[10px] font-semibold text-amber-600">' + previewNextInterval(current.id, 1) + '</span>' +
          '</button>' +
          '<button onclick="rateCard(' + current.id + ', 2)" class="fc-action-btn flex-col !gap-0.5 !py-2 !px-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 shadow-xs">' +
            '<span class="text-xs font-extrabold">🌸 Acertei</span>' +
            '<span class="text-[10px] font-semibold text-emerald-600">' + previewNextInterval(current.id, 2) + '</span>' +
          '</button>' +
          '<button onclick="rateCard(' + current.id + ', 3)" class="fc-action-btn flex-col !gap-0.5 !py-2 !px-1 bg-sky-50 hover:bg-sky-100 text-sky-800 border border-sky-200 shadow-xs">' +
            '<span class="text-xs font-extrabold">⚡ Fácil</span>' +
            '<span class="text-[10px] font-semibold text-sky-600">' + previewNextInterval(current.id, 3) + '</span>' +
          '</button>' +
        '</div>' +

      '</div>';

      section.innerHTML = html;
    }

    function saveFCDraft(cardId, val) {
      fcDraftAnswers[cardId] = val;
    }

    function clearFCDraft(cardId) {
      delete fcDraftAnswers[cardId];
      var el = document.getElementById('fcScratchpad');
      if (el) {
        el.value = '';
        el.focus();
      }
    }

    function flipFlashcard() {
      isFlipped = !isFlipped;
      var inner = document.getElementById('flashcardInner');
      if (inner) {
        if (isFlipped) inner.classList.add('is-flipped');
        else inner.classList.remove('is-flipped');
      }
    }

    function nextFlashcard(total) {
      isFlipped = false;
      showHint = false;
      if (currentFlashcardIndex < total - 1) currentFlashcardIndex++;
      else currentFlashcardIndex = 0;
      renderFlashcards();
    }

    function prevFlashcard(total) {
      isFlipped = false;
      showHint = false;
      if (currentFlashcardIndex > 0) currentFlashcardIndex--;
      else currentFlashcardIndex = total - 1;
      renderFlashcards();
    }

    function rateCard(cardId, quality) {
      var s = Object.assign({}, getCardSRS(cardId));
      var wasNew = (s.state === 'new');
      var now = Date.now();
      s.lastReview = now;

      if (quality === 0) {
        s.lapses = (s.lapses || 0) + 1;
        s.reps = 0;
        s.interval = 0;
        s.ease = Math.max(1.3, (s.ease || 2.5) - 0.2);
        s.due = now + 5 * 60 * 1000; // Volta em 5 min na mesma sessão
        s.state = 'learning';
        flashcardScores.review++;
      } else if (quality === 1) {
        s.reps = Math.max(1, s.reps || 0);
        s.interval = computeNextIntervalDays(s, 1);
        s.ease = Math.max(1.3, (s.ease || 2.5) - 0.15);
        s.due = getStartOfDay(s.interval);
        s.state = 'learning';
        flashcardScores.review++;
      } else if (quality === 2) {
        s.interval = computeNextIntervalDays(s, 2);
        s.reps = (s.reps || 0) + 1;
        s.due = getStartOfDay(s.interval);
        s.state = (s.interval >= 6) ? 'mastered' : 'review';
        flashcardScores.correct++;
      } else if (quality === 3) {
        s.interval = computeNextIntervalDays(s, 3);
        s.reps = (s.reps || 0) + 2;
        s.ease = Math.min(3.0, (s.ease || 2.5) + 0.1);
        s.due = getStartOfDay(s.interval);
        s.state = (s.interval >= 6) ? 'mastered' : 'review';
        flashcardScores.correct++;
      }

      if (wasNew) srsStats.newToday = (srsStats.newToday || 0) + 1;
      srsData[cardId] = s;
      srsStats.reviewedToday = (srsStats.reviewedToday || 0) + 1;
      saveSRS();

      isFlipped = false;
      showHint = false;
      delete fcDraftAnswers[cardId];

      if (trailPinnedId === cardId) trailPinnedId = null;

      // Em todos os modos: se o card saiu da fila (agendado para outro dia), o próximo
      // ocupa a mesma posição; se continua (ex.: Errei -> 5 min), avança para o seguinte.
      var q = getStudyQueue();
      var pos = -1;
      for (var qi = 0; qi < q.length; qi++) { if (q[qi].id === cardId) { pos = qi; break; } }
      if (pos === -1) {
        if (currentFlashcardIndex >= q.length) currentFlashcardIndex = 0;
      } else if (q.length > 1) {
        currentFlashcardIndex = (pos + 1) % q.length;
      } else {
        currentFlashcardIndex = 0;
      }
      renderFlashcards();
    }

    function markCard(correct, total) {
      var filtered = getStudyQueue();
      var current = filtered[currentFlashcardIndex];
      if (current) rateCard(current.id, correct ? 2 : 0);
    }

    function openTrailModal() {
      var listEl = document.getElementById('trailModalList');
      if (!listEl) return;
      var base = getBaseFilteredFlashcards().slice().sort(function(a, b) { return a.id - b.id; });
      var endOfToday = getStartOfDay(1) - 1;
      var html = '';
      for (var i = 0; i < base.length; i++) {
        var c = base[i];
        var s = getCardSRS(c.id);
        var badge = '<span class="text-[10px] px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 font-bold">🆕 Novo</span>';
        if (s.state !== 'new') {
          if (s.due <= endOfToday) badge = '<span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 font-bold">🔥 Hoje</span>';
          else if (s.interval >= 7) badge = '<span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold">🏆 ' + s.interval + 'd</span>';
          else badge = '<span class="text-[10px] px-2 py-0.5 rounded-full bg-pink-50 text-rose-700 font-bold">🌱 ' + s.interval + 'd</span>';
        }
        html += '<button onclick="jumpToTrailCard(' + i + ')" class="w-full text-left p-2.5 rounded-xl bg-rose-50/40 hover:bg-pink-50 border border-rose-100 flex items-center justify-between gap-2 transition">' +
          '<div class="min-w-0">' +
            '<div class="text-[10px] font-bold text-rose-400">#' + c.id + ' • ' + getAreaLabel(c.area) + (c.cat ? ' • ' + getCatLabel(c.cat) : '') + '</div>' +
            '<div class="text-xs font-bold text-slate-800 truncate">' + escapeText(c.name || c.front) + '</div>' +
          '</div>' +
          badge +
        '</button>';
      }
      listEl.innerHTML = html || '<div class="text-center text-slate-400 py-4">Nenhum card neste filtro.</div>';
      openModal('trailModal');
    }

    function jumpToTrailCard(seqIndex) {
      var trailList = getBaseFilteredFlashcards().slice().sort(function(a, b) { return a.id - b.id; });
      var target = trailList[seqIndex];
      fcStudyMode = 'sequential';
      trailPinnedId = target ? target.id : null;
      var sq = getStudyQueue();
      currentFlashcardIndex = 0;
      for (var ti = 0; ti < sq.length; ti++) { if (target && sq[ti].id === target.id) { currentFlashcardIndex = ti; break; } }
      isFlipped = false;
      showHint = false;
      closeModal('trailModal');
      renderFlashcards();
    }

    function playCurrentFCAudio() {
      var filtered = getStudyQueue();
      var current = filtered[currentFlashcardIndex];
      if (current && current.audioText) {
        playItemAudio(current.name || 'Flashcard', current.audioText);
      }
    }

    // ==========================================
    // RENDER: JÁ CAIU NA MACKENZIE
    // ==========================================
    function renderGeral() {
      var container = document.getElementById('mackContainer');
      var countEl = document.getElementById('mackCount');
      if (!container) return;

      var filtered = appState.geral.filter(function(m) {
        return activeArea === 'todas' || m.area === activeArea;
      });

      if (countEl) countEl.innerText = filtered.length + " tópicos";

      if (filtered.length === 0) {
        container.innerHTML = '<div class="col-span-full glass-card p-6 text-center space-y-2 border border-pink-200">' +
          '<div class="text-2xl">🎯</div>' +
          '<h3 class="font-bold text-sm text-slate-800">Nenhum tópico nesta área</h3>' +
          '<p class="text-xs text-rose-500">Mude o filtro acima para ver todos os tópicos da banca.</p>' +
        '</div>';
        return;
      }

      var html = '';
      for (var i = 0; i < filtered.length; i++) {
        var item = filtered[i];
        html += '<div class="glass-card p-4 space-y-2 border border-pink-100">' +
          '<div class="flex items-center justify-between">' +
            '<span class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-pink-50 text-rose-700 border border-pink-200">' +
              getAreaLabel(item.area) +
            '</span>' +
            '<span class="text-[10px] font-mono font-bold text-rose-400">' + (item.year || 'Bancas') + '</span>' +
          '</div>' +
          '<h3 class="font-bold text-sm text-slate-800">' + escapeText(item.title) + '</h3>' +
          '<p class="text-xs text-slate-600 leading-relaxed bg-rose-50/50 p-2.5 rounded-xl border border-rose-100">' +
            '<strong class="text-rose-600 block mb-0.5">Pegadinha / Como a banca cobra:</strong>' +
            escapeText(item.tip) +
          '</p>' +
        '</div>';
      }
      container.innerHTML = html;
    }

    // ==========================================
    // MOTOR DE ÁUDIO 1.7X (COMPATIBILIDADE UNIVERSAL)
    // ==========================================
    function initSpeech() {
      if (!('speechSynthesis' in window)) return;
      function populate() {
        try {
          voicesList = window.speechSynthesis.getVoices() || [];
          var pt = voicesList.filter(function(v) { return v.lang && (v.lang.indexOf('pt') === 0 || v.lang.indexOf('BR') !== -1); });
          if (pt.length > 0) {
            selectedVoice = pt.find(function(v) {
              return v.name.indexOf('Francisca') !== -1 || v.name.indexOf('Google') !== -1 || v.name.indexOf('Daniel') !== -1 || v.name.indexOf('Natural') !== -1;
            }) || pt[0];
          }
        } catch(e) {}
      }
      populate();
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = populate;
      }
    }

    function splitSentences(text) {
      if (!text) return [];
      // Divisão segura de frases compatível com todos os navegadores sem lookbehind
      var cleaned = text.replace(/([.?!])\\s+/g, "$1|||");
      var parts = cleaned.split("|||");
      return parts.map(function(s) { return s.trim(); }).filter(function(s) { return s.length > 0; });
    }

    function playItemAudioByIndex(id, type) {
      var item = null;
      if (type === 'table') {
        item = appState.tables.find(function(t) { return t.id === id; });
      }
      if (item && item.audioText) {
        playItemAudio(item.name, item.audioText);
      }
    }

    function playItemAudio(title, fullText) {
      currentSpeechText = fullText;
      var titleEl = document.getElementById('audioPlayerTitle');
      if (titleEl) titleEl.innerText = title;

      speechChunks = splitSentences(fullText);
      if (speechChunks.length === 0) speechChunks = [fullText];
      currentChunkIndex = 0;

      showAudioPlayer();
      startAudioPlayback();
    }

    function showAudioPlayer() {
      var player = document.getElementById('bottomAudioPlayer');
      if (player) player.classList.remove('translate-y-full');
    }

    function closeAudioPlayer() {
      stopAudioPlayback();
      var player = document.getElementById('bottomAudioPlayer');
      if (player) player.classList.add('translate-y-full');
    }

    function toggleAudio() {
      if (isPlaying) pauseAudioPlayback();
      else startAudioPlayback();
    }

    function startAudioPlayback() {
      if (!('speechSynthesis' in window)) return;
      try {
        window.speechSynthesis.cancel();
        isPlaying = true;
        updateAudioUI(true);
        speakChunk(currentChunkIndex);
      } catch(e) {
        console.warn('Speech error:', e);
      }
    }

    function pauseAudioPlayback() {
      if (!('speechSynthesis' in window)) return;
      try {
        isPlaying = false;
        window.speechSynthesis.cancel();
        updateAudioUI(false);
      } catch(e) {}
    }

    function stopAudioPlayback() {
      if (!('speechSynthesis' in window)) return;
      try {
        isPlaying = false;
        currentChunkIndex = 0;
        window.speechSynthesis.cancel();
        updateAudioUI(false);
      } catch(e) {}
    }

    function speakChunk(idx) {
      if (!('speechSynthesis' in window)) return;
      if (idx >= speechChunks.length) {
        stopAudioPlayback();
        return;
      }
      currentChunkIndex = idx;
      updateScriptHighlight();

      var chunk = speechChunks[idx];
      try {
        speechUtterance = new SpeechSynthesisUtterance(chunk);
        speechUtterance.rate = currentSpeed;
        speechUtterance.lang = 'pt-BR';
        if (selectedVoice) speechUtterance.voice = selectedVoice;

        speechUtterance.onend = function() {
          if (isPlaying) {
            if (currentChunkIndex < speechChunks.length - 1) {
              currentChunkIndex++;
              speakChunk(currentChunkIndex);
            } else {
              stopAudioPlayback();
            }
          }
        };

        speechUtterance.onerror = function() {
          stopAudioPlayback();
        };

        window.speechSynthesis.speak(speechUtterance);
      } catch(e) {
        stopAudioPlayback();
      }
    }

    function audioSkip(dir) {
      if (dir > 0 && currentChunkIndex < speechChunks.length - 1) currentChunkIndex++;
      else if (dir < 0 && currentChunkIndex > 0) currentChunkIndex--;
      if (isPlaying) speakChunk(currentChunkIndex);
      else updateScriptHighlight();
    }

    function cycleSpeed() {
      var speeds = [1.0, 1.3, 1.5, 1.7, 2.0];
      var idx = speeds.indexOf(currentSpeed);
      idx = (idx + 1) % speeds.length;
      currentSpeed = speeds[idx];
      var badge = document.getElementById('speedBadge');
      if (badge) badge.innerText = currentSpeed + "x" + (currentSpeed === 1.7 ? " ⭐" : "");
      if (isPlaying) speakChunk(currentChunkIndex);
    }

    function updateAudioUI(playing) {
      var icon = document.getElementById('audioPlayIcon');
      var wave = document.getElementById('playerWave');
      var staticIcon = document.getElementById('playerStaticIcon');
      if (icon) icon.className = playing ? "fa-solid fa-pause" : "fa-solid fa-play";
      if (wave) {
        if (playing) wave.classList.remove('hidden');
        else wave.classList.add('hidden');
      }
      if (staticIcon) {
        if (playing) staticIcon.classList.add('hidden');
        else staticIcon.classList.remove('hidden');
      }
    }

    function openScriptModal() {
      var container = document.getElementById('scriptParagraphsContainer');
      if (!container) return;
      var html = '';
      for (var i = 0; i < speechChunks.length; i++) {
        var isCurrent = (i === currentChunkIndex);
        var cls = isCurrent ? 'bg-pink-100 text-rose-800 font-bold border-l-4 border-rose-500 pl-3' : 'bg-white text-slate-700 hover:bg-pink-50';
        html += '<div onclick="jumpToChunk(' + i + ')" class="p-2.5 rounded-xl border border-rose-100 cursor-pointer transition ' + cls + '">' +
          '<span class="font-mono text-rose-400 mr-1.5 text-[10px]">' + (i + 1) + '.</span>' +
          '<span>' + escapeText(speechChunks[i]) + '</span>' +
        '</div>';
      }
      container.innerHTML = html;
      openModal('scriptModal');
    }

    function jumpToChunk(idx) {
      currentChunkIndex = idx;
      startAudioPlayback();
      closeModal('scriptModal');
    }

    function updateScriptHighlight() {
      var cur = document.getElementById('audioCurrentTime');
      if (cur) cur.innerText = (currentChunkIndex + 1) + "/" + speechChunks.length + " (" + currentSpeed + "x)";
    }

    // ==========================================
    // MODAIS E INSERÇÃO
    // ==========================================
    function openModal(id) {
      var el = document.getElementById(id);
      if (el) {
        el.style.display = 'flex';
        el.classList.add('active');
        el.classList.remove('hidden');
      }
    }

    function closeModal(id) {
      var el = document.getElementById(id);
      if (el) {
        el.style.display = 'none';
        el.classList.remove('active');
        el.classList.add('hidden');
      }
    }

    function setAddType(type) {
      addModalType = type;
      var types = ['tabela', 'flashcard', 'geral', 'raw'];
      for (var i = 0; i < types.length; i++) {
        var t = types[i];
        var form = document.getElementById('form-' + t);
        var btn = document.getElementById('addType-' + t);
        if (form) {
          form.style.display = (t === type) ? 'block' : 'none';
          if (t === type) form.classList.remove('hidden');
          else form.classList.add('hidden');
        }
        if (btn) {
          if (t === type) btn.className = "py-1.5 px-3 border-b-2 border-rose-500 text-rose-600 font-bold";
          else btn.className = "py-1.5 px-3 text-slate-400 hover:text-slate-700";
        }
      }
      var areaCatRow = document.getElementById('field-area-cat');
      var catContainer = document.getElementById('field-cat-container');
      if (areaCatRow) {
        areaCatRow.style.display = (type === 'raw') ? 'none' : 'grid';
      }
      if (catContainer) {
        catContainer.style.display = (type === 'tabela') ? 'block' : 'none';
      }
    }

    function submitNewItem() {
      var area = document.getElementById('inputArea').value;
      var cat = document.getElementById('inputCat').value;

      if (addModalType === 'tabela') {
        var name = document.getElementById('tabName').value.trim();
        var col1 = document.getElementById('tabCol1').value.trim();
        var col2 = document.getElementById('tabCol2').value.trim();
        var audio = document.getElementById('tabAudio').value.trim();
        if (!name) return alert("Por favor, preencha o nome do item!");

        appState.tables.push({ id: Date.now(), area: area, cat: cat, name: name, col1: col1, col2: col2, audioText: audio });
        document.getElementById('tabName').value = '';
        document.getElementById('tabCol1').value = '';
        document.getElementById('tabCol2').value = '';
        document.getElementById('tabAudio').value = '';
      } else if (addModalType === 'flashcard') {
        var front = document.getElementById('fcFront').value.trim();
        var back = document.getElementById('fcBack').value.trim();
        var audioFc = document.getElementById('fcAudio').value.trim();
        if (!front || !back) return alert("Preencha a pergunta e a resposta do cartão!");

        appState.flashcards.push({ id: Date.now(), area: area, front: front, back: back, audioText: audioFc });
        document.getElementById('fcFront').value = '';
        document.getElementById('fcBack').value = '';
        document.getElementById('fcAudio').value = '';
      } else if (addModalType === 'geral') {
        var title = document.getElementById('mackTitle').value.trim();
        var tip = document.getElementById('mackTip').value.trim();
        var year = document.getElementById('mackYear').value.trim();
        if (!title || !tip) return alert("Preencha o tema e a pegadinha!");

        appState.geral.push({ id: Date.now(), area: area, title: title, tip: tip, year: year });
        document.getElementById('mackTitle').value = '';
        document.getElementById('mackTip').value = '';
        document.getElementById('mackYear').value = '';
      } else if (addModalType === 'raw') {
        var text = document.getElementById('rawText').value.trim();
        if (!text) return alert("Cole o texto!");
        appState.tables.push({
          id: Date.now(),
          area: 'clinica',
          cat: 'doencas',
          name: "Anotação da Ju (Texto Bruto)",
          col1: text,
          col2: "Salvo no aplicativo",
          audioText: text
        });
        document.getElementById('rawText').value = '';
      }

      saveState();
      closeModal('addModal');
      alert("Item adicionado com sucesso! ✨🌸");
    }

    // ==========================================
    // BACKUP E EXPORTAÇÃO
    // ==========================================
    function exportData() {
      var payload = Object.assign({}, appState, { srsData: srsData, srsStats: srsStats });
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(payload, null, 2));
      var a = document.createElement('a');
      a.setAttribute("href", dataStr);
      a.setAttribute("download", "MedFlashcards_Backup.json");
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    function importData(event) {
      var file = event.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function(e) {
        try {
          var imported = JSON.parse(e.target.result);
          if (imported.tables || imported.flashcards || imported.geral || imported.srsData) {
            if (imported.tables) appState.tables = imported.tables;
            if (imported.flashcards) appState.flashcards = imported.flashcards;
            if (imported.geral) appState.geral = imported.geral;
            if (imported.srsData) srsData = imported.srsData;
            if (imported.srsStats) {
              srsStats = imported.srsStats;
              if (srsStats.examDate) srsStats.examSetAt = Date.now(); // backup importado vale como a data mais recente
            }
            saveState();
            alert("Backup e cronograma SRS restaurados com sucesso! ✨");
            closeModal('exportModal');
          } else {
            alert("Arquivo JSON inválido.");
          }
        } catch(err) {
          alert("Erro ao ler arquivo.");
        }
      };
      reader.readAsText(file);
    }

    // ==========================================
    // UTILITÁRIOS
    // ==========================================
    function getAreaLabel(area) {
      var map = {
        'clinica': 'Clínica Médica',
        'cardiologia': '❤️ Cardiologia',
        'pneumologia': '🫁 Pneumologia',
        'gastroenterologia': '🩺 Gastroenterologia',
        'endocrinologia': '🦋 Endocrinologia',
        'reumatologia': '🦴 Reumatologia',
        'hematologia': '🩸 Hematologia',
        'cirurgia': 'Cirurgia Geral',
        'pediatria': 'Pediatria',
        'go': 'G.O.',
        'preventiva': 'Preventiva'
      };
      return map[area] || 'Geral';
    }

    function getCatLabel(cat) {
      var map = {
        'eponimos': 'Epônimo',
        'triades': 'Tríade / Pêntade',
        'doencas': 'Doença',
        'scas': 'SCAs / IAM',
        'aorta': 'Aorta',
        'ic': 'Insuf. Cardíaca',
        'valvopatias': 'Valvopatias',
        'arritmias': 'Arritmias',
        'pericardio': 'Pericárdio',
        'semiologia': 'Semiologia',
        'tep': 'TEP',
        'obstrutivas': 'Asma / DPOC',
        'pleura': 'Derrame Pleural',
        'infeccoes': 'TB / Infecções',
        'oncologia': 'CA Pulmão / Paraneo',
        'terapia_intensiva': 'UTI / SARA',
        'cirrose_ascite': 'Cirrose & Ascite',
        'pbe': 'PBE',
        'hda': 'HDA / Úlceras',
        'hepatites': 'Hepatites Virais',
        'pancreatite': 'Pancreatite',
        'dii': 'Crohn & RCU',
        'emergencias_dm': 'CAD & EHH',
        'tireoide': 'Tireoide',
        'adrenal': 'Adrenal',
        'metabolismo': 'Diabetes / Cálcio',
        'ar': 'Artrite Reumatoide',
        'les': 'Lúpus (LES)',
        'colagenoses': 'Esclerodermia / Mio / Sjögren',
        'espondilo': 'Espondiloartrites',
        'vasculites': 'Vasculites',
        'cristais': 'Gota & Pseudogota',
        'anemias': 'Anemias',
        'onco_hemato': 'Leucemias & Linfomas',
        'mieloma': 'Mieloma Múltiplo',
        'hemostasia': 'Plaquetas & Coagulação'
      };
      return map[cat] || cat || 'Geral';
    }

    function escapeText(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\\$\\ge\\$/g, '≥')
        .replace(/\\$\\le\\$/g, '≤')
        .replace(/\\$\\rightarrow\\$/g, '→')
        .replace(/\\$/g, '');
    }

    // GARANTE QUE AS FUNÇÕES ESTEJAM NO ESCOPO GLOBAL DO WINDOW
    window.switchTab = switchTab;
    window.setAreaFilter = setAreaFilter;
    window.setCategoryFilter = setCategoryFilter;
    window.setFCStudyMode = setFCStudyMode;
    window.setFCSpecialty = setFCSpecialty;
    window.setFCSubtopic = setFCSubtopic;
    window.toggleHint = toggleHint;
    window.saveFCDraft = saveFCDraft;
    window.clearFCDraft = clearFCDraft;
    window.rateCard = rateCard;
    window.openTrailModal = openTrailModal;
    window.jumpToTrailCard = jumpToTrailCard;
    window.adjustExamDays = adjustExamDays;
    window.reshuffleCards = reshuffleCards;
    window.flipFlashcard = flipFlashcard;
    window.nextFlashcard = nextFlashcard;
    window.prevFlashcard = prevFlashcard;
    window.markCard = markCard;
    window.playItemAudioByIndex = playItemAudioByIndex;
    window.playItemAudio = playItemAudio;
    window.playCurrentFCAudio = playCurrentFCAudio;
    window.toggleAudio = toggleAudio;
    window.audioSkip = audioSkip;
    window.cycleSpeed = cycleSpeed;
    window.closeAudioPlayer = closeAudioPlayer;
    window.openModal = openModal;
    window.closeModal = closeModal;
    window.setAddType = setAddType;
    window.submitNewItem = submitNewItem;
    window.openScriptModal = openScriptModal;
    window.jumpToChunk = jumpToChunk;
    window.exportData = exportData;
    window.importData = importData;
    window.cloudButtonClick = cloudButtonClick;
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html with {len(html_content)} characters!")
