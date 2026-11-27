import json

with open("app_data_clean.json", "r", encoding="utf-8") as f:
    app_data = json.load(f)

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="description" content="Flashcards com repetição espaçada, tabelas de revisão e pegadinhas de banca para a prova de residência médica.">
  <title>MedFlashcards · Residência médica</title>

  <!-- Fonte: Figtree (interface e texto) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <!-- Firebase (login Google + Firestore para salvar o progresso na nuvem) -->
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore-compat.js"></script>

  <!-- FontAwesome (ícones) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Tailwind CDN: só utilitários de layout; todas as cores e fontes saem dos tokens em :root -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    if (typeof tailwind !== 'undefined') {
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              paper: 'var(--color-paper)',
              paper2: 'var(--color-paper-2)',
              paper3: 'var(--color-paper-3)',
              ink: 'var(--color-ink)',
              ink2: 'var(--color-ink-2)',
              muted: 'var(--color-muted)',
              rule: 'var(--color-rule)',
              inkrule: 'var(--color-ink-rule)',
              accent: 'var(--color-accent)',
              accentink: 'var(--color-accent-ink)',
              amber: 'var(--color-accent-2)'
            },
            fontFamily: {
              display: 'var(--font-display)',
              sans: 'var(--font-body)'
            },
            boxShadow: {
              card: 'var(--shadow-card)'
            }
          }
        }
      }
    }
  </script>

  <script>document.documentElement.classList.add('js');</script>
  <style>
/* Hallmark · shape: app screen · genre: modern-minimal · theme: custom, warm paper (from Wayfind, by request) · redesign: full
 * nav: kept (three tabs) · signature: the study card with its four-way grade row · states: empty queue, all scheduled, offline, signed out
 * axes: light/sans/warm · posture: quiet · contrast: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H4 E4 S4 R4 V3 · weakest: V, the user found Wayfind cold and the mono harsh; warm paper, one humanist sans and fewer controls on screen answer it */
    :root {
      color-scheme: light;
      --space-3xs: 2px; --space-2xs: 4px; --space-xs: 8px; --space-sm: 12px; --space-md: 16px; --space-lg: 24px; --space-xl: 40px;
      --text-xs: 0.8125rem; --text-sm: 0.875rem; --text-md: 1rem; --text-lg: 1.2rem; --text-xl: 1.44rem;
      --dur-micro: 120ms; --dur-short: 220ms; --dur-long: 420ms;
      --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
      --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* movimento na tela (virar o card, indicador das abas) */
      --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* folha que sobe, curva do iOS */
      /* Papel creme, tinta marrom-escura, terracota para a ação principal, mel para os números */
      --color-paper: oklch(96.6% 0.012 82); --color-paper-2: oklch(93% 0.017 80); --color-paper-3: oklch(99.2% 0.006 85);
      --color-ink: oklch(25% 0.02 55); --color-ink-2: oklch(36% 0.02 55); --color-muted: oklch(49% 0.022 62);
      --color-rule: oklch(86% 0.02 78); --color-ink-rule: oklch(40% 0.02 55);
      --color-accent: oklch(52% 0.14 42); --color-accent-2: oklch(82% 0.13 78); --color-accent-ink: oklch(99% 0.006 85); --color-focus: oklch(52% 0.14 42);
      --color-accent-soft: oklch(93.5% 0.035 55);
      --color-dog: oklch(56% 0.115 52); --color-dog-dark: oklch(40% 0.09 45); --color-dog-belly: oklch(66% 0.1 60);
      --color-sock: oklch(97% 0.012 85); --color-sock-stripe: oklch(52% 0.14 42);
      --color-scrim: oklch(25% 0.02 55 / 0.45);
      --font-display: "Figtree", system-ui, sans-serif;
      --font-body: "Figtree", system-ui, sans-serif;
      --radius-card: 14px; --radius-control: 10px; --radius-pill: 999px; --rule-hair: 1px; --rule-bar: 1px;
      --shadow-tab: 0 1px 2px oklch(25% 0.02 55 / 0.12);
      --shadow-card: 0 1px 2px oklch(25% 0.02 55 / 0.06), 0 8px 24px -12px oklch(25% 0.02 55 / 0.18);
      --tracking-display: -0.015em;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    html, body { overflow-x: clip; }
    html { scrollbar-color: var(--color-rule) var(--color-paper); scroll-padding-top: 120px; }
    body {
      font-family: var(--font-body);
      background: var(--color-paper);
      color: var(--color-ink);
      min-height: 100dvh;
      line-height: 1.55;
      padding-bottom: var(--space-xl);
      touch-action: manipulation;
      -webkit-font-smoothing: antialiased;
      font-variant-numeric: tabular-nums;
      caret-color: var(--color-accent);
    }
    body.player-open { padding-bottom: 96px; }
    ::selection { background: var(--color-accent-2); color: var(--color-ink); }
    :focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
    button, input, select, textarea { font: inherit; color: inherit; touch-action: manipulation; }
    button:disabled, [aria-disabled="true"] { opacity: 0.55; cursor: not-allowed; }
    h1, h2, h3 { font-family: var(--font-display); font-weight: 700; letter-spacing: var(--tracking-display); line-height: 1.2; overflow-wrap: break-word; min-width: 0; text-wrap: balance; }
    .text-xs { font-size: var(--text-xs) !important; line-height: 1.4; }
    .visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }

    .hidden, [hidden] { display: none !important; }

    /* Cantos suaves e bordas finas em tudo que o Tailwind marca com borda */
    .border, .border-2 { border-width: var(--rule-hair) !important; }
    .border-ink { border-color: var(--color-rule) !important; }
    button.border, button.border-2, label.border, textarea, input, select { border-radius: var(--radius-control); }

    /* Modais */
    .modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: var(--color-scrim);
      align-items: center;
      justify-content: center;
      padding: var(--space-md);
    }
    .modal-overlay.active { display: flex !important; }
    .modal-overlay > div { border: var(--rule-hair) solid var(--color-rule) !important; border-radius: var(--radius-card); box-shadow: var(--shadow-card); }

    /* Superfícies */
    .glass-card {
      background: var(--color-paper-3);
      border: var(--rule-hair) solid var(--color-rule);
      border-radius: var(--radius-card);
      overflow: hidden;
    }
    .glass-header {
      background: var(--color-paper);
      border-bottom: var(--rule-hair) solid var(--color-rule);
    }

    /* Abas principais: trilho creme, a escolhida em papel claro */
    .tab-track { background: var(--color-paper-2); border-radius: 12px; padding: var(--space-2xs); display: flex; gap: var(--space-2xs); }
    .main-tab-btn {
      flex: 1;
      min-height: 40px;
      padding: var(--space-xs) var(--space-sm);
      font-size: var(--text-sm);
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-xs);
      cursor: pointer;
      border-radius: 9px;
      white-space: nowrap;
      user-select: none;
      -webkit-user-select: none;
      transition: background-color var(--dur-micro) ease, color var(--dur-micro) ease;
    }
    .main-tab-btn.active { background: var(--color-paper-3); color: var(--color-ink); box-shadow: var(--shadow-tab); }
    .main-tab-btn.active span[id^="badgeCount"] { background: var(--color-accent-soft) !important; color: var(--color-accent) !important; }
    .main-tab-btn.inactive { color: var(--color-muted); }
    .main-tab-btn.inactive:hover { color: var(--color-ink); }
    .main-tab-btn span[id^="badgeCount"] { border-radius: var(--radius-pill); font-weight: 600; }

    /* Filtros: pílulas; a escolhida é tinta cheia */
    .filter-pill {
      min-height: 34px;
      padding: var(--space-2xs) var(--space-sm);
      font-size: var(--text-sm);
      font-weight: 500;
      white-space: nowrap;
      cursor: pointer;
      flex-shrink: 0;
      border-radius: var(--radius-pill);
      border: var(--rule-hair) solid var(--color-rule);
      user-select: none;
      -webkit-user-select: none;
      transition: background-color var(--dur-micro) ease, color var(--dur-micro) ease, border-color var(--dur-micro) ease;
    }
    .filter-pill.active { background: var(--color-ink); border-color: var(--color-ink); color: var(--color-paper-3); }
    .filter-pill.inactive { background: var(--color-paper-3); color: var(--color-ink-2); }
    .filter-pill.inactive:hover { border-color: var(--color-muted); color: var(--color-ink); }
    .seg { gap: var(--space-xs); }

    /* Flashcard */
    .flashcard-wrapper {
      perspective: 1400px;
      -webkit-perspective: 1400px;
      width: 100%;
      /* sobra da tela tirando o cabeçalho fixo, as setas e as notas (cerca de 290px) */
      height: clamp(260px, calc(100vh - 290px), 460px);
      height: clamp(260px, calc(100svh - 290px), 460px);
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      position: relative;
    }
    .flashcard-inner {
      position: relative;
      width: 100%;
      height: 100%;
      transition: transform 300ms var(--ease-in-out);
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
    }
    .flashcard-inner.is-flipped { transform: rotateY(180deg); -webkit-transform: rotateY(180deg); }
    .card-face {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      padding: var(--space-lg);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      background: var(--color-paper-3);
      border: var(--rule-hair) solid var(--color-rule);
      border-radius: var(--radius-card);
      box-shadow: var(--shadow-card);
      overflow-y: auto;
    }
    .card-front { z-index: 2; transform: rotateY(0deg); -webkit-transform: rotateY(0deg); }
    .card-back { transform: rotateY(180deg); -webkit-transform: rotateY(180deg); border-top: 4px solid var(--color-accent); }
    .flashcard-inner.is-flipped .card-front { pointer-events: none; }
    .flashcard-inner:not(.is-flipped) .card-back button, .flashcard-inner.is-flipped .card-front button { visibility: hidden; }

    .fc-action-btn {
      min-height: 44px;
      padding: var(--space-xs) var(--space-md);
      font-size: var(--text-sm);
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-xs);
      cursor: pointer;
      border-radius: var(--radius-control);
      transition: background-color var(--dur-micro) ease, color var(--dur-micro) ease;
    }

    /* Avaliação: quatro botões lado a lado */
    .grade-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-xs); }
    .grade-btn {
      min-height: 58px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: var(--space-3xs);
      border: var(--rule-hair) solid var(--color-rule);
      border-radius: var(--radius-control);
      background: var(--color-paper-3);
      color: var(--color-ink);
      cursor: pointer;
      transition: background-color var(--dur-micro) ease, color var(--dur-micro) ease, border-color var(--dur-micro) ease;
    }
    .grade-btn .grade-name { font-size: var(--text-md); font-weight: 600; }
    .grade-btn .grade-when { font-size: var(--text-xs); color: var(--color-muted); }
    .grade-btn:hover { background: var(--color-ink); border-color: var(--color-ink); color: var(--color-paper-3); }
    .grade-btn:hover .grade-when { color: var(--color-accent-2); }
    .grade-btn:active { background: var(--color-ink-2); color: var(--color-paper-3); }

    /* Resumo do dia e números */
    .summary { background: var(--color-paper-3); border: var(--rule-hair) solid var(--color-rule); border-radius: var(--radius-card); }
    .figure { font-weight: 700; color: var(--color-ink); }
    .figure--accent { color: var(--color-accent); }
    .stat-grid { display: grid; gap: var(--space-xs); }
    .stat-cell { background: var(--color-paper-3); border: var(--rule-hair) solid var(--color-rule); border-radius: var(--radius-control); }
    .forecast-cell { border-radius: 8px; background: var(--color-paper-3); border: var(--rule-hair) solid var(--color-rule); }
    .forecast-cell.is-today { background: var(--color-ink); border-color: var(--color-ink); color: var(--color-paper-3); }

    /* Selo de estado do card */
    .tag { display: inline-flex; align-items: center; font-size: var(--text-xs); font-weight: 600; padding: var(--space-3xs) var(--space-sm); border-radius: var(--radius-pill); background: var(--color-paper-2); color: var(--color-ink-2); white-space: nowrap; }
    .tag--new { background: var(--color-accent-soft); color: var(--color-accent); }
    .tag--due { background: var(--color-accent-2); color: var(--color-ink); }
    .tag--done { background: var(--color-ink); color: var(--color-paper-3); }

    /* Link discreto em forma de texto */
    .text-btn { font-size: var(--text-sm); font-weight: 600; color: var(--color-ink); text-decoration: underline; text-underline-offset: 0.2em; text-decoration-color: var(--color-rule); min-height: 32px; padding: var(--space-2xs) var(--space-3xs); }
    .text-btn:hover { text-decoration-color: var(--color-ink); }

    .custom-scroll::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scroll::-webkit-scrollbar-thumb { background: var(--color-rule); border-radius: 999px; }
    .no-scrollbar { scrollbar-width: none; }
    .no-scrollbar::-webkit-scrollbar { display: none; }

    @keyframes pulse-wave { 0%, 100% { transform: scaleY(0.35); } 50% { transform: scaleY(1); } }
    .wave-bar { height: 16px; transform-origin: bottom; animation: pulse-wave 1s ease-in-out infinite; background: var(--color-accent-2); border-radius: 2px; }



    /* ===== Movimento (receitas de Emil Kowalski): só transform e opacity, curto, com propósito ===== */

    /* Indicador das abas: um fundo que desliza até a aba escolhida */
    .tab-track { position: relative; }
    .tab-indicator {
      position: absolute;
      top: var(--space-2xs);
      bottom: var(--space-2xs);
      left: 0;
      width: 0;
      border-radius: 9px;
      background: var(--color-paper-3);
      box-shadow: var(--shadow-tab);
      pointer-events: none;
    }
    .tab-indicator.is-ready { transition: transform 250ms var(--ease-in-out); }
    .tab-track.has-indicator .main-tab-btn.active { background: transparent; box-shadow: none; }
    .main-tab-btn { position: relative; z-index: 1; }

    /* Toque: o botão afunda um pouco */
    .grade-btn, .filter-pill, .main-tab-btn { transition-property: background-color, color, border-color, transform; transition-duration: var(--dur-micro), var(--dur-micro), var(--dur-micro), 160ms; transition-timing-function: ease, ease, ease, var(--ease-out); }
    .grade-btn:active, .filter-pill:active, .main-tab-btn:active { transform: scale(0.97); }

    /* Troca de card: o avaliado sai pela esquerda, o próximo entra pela direita */
    .flashcard-wrapper.card-leave { animation: card-leave 150ms var(--ease-out) forwards; pointer-events: none; }
    .flashcard-wrapper.card-enter-next { animation: card-enter-next 220ms var(--ease-out); }
    .flashcard-wrapper.card-enter-prev { animation: card-enter-prev 220ms var(--ease-out); }
    @keyframes card-leave { to { opacity: 0; transform: translateX(-24px); } }
    @keyframes card-enter-next { from { opacity: 0; transform: translateX(24px); } }
    @keyframes card-enter-prev { from { opacity: 0; transform: translateX(-24px); } }

    /* Painel de progresso: abre com um esmaecer curto */
    .reveal { animation: reveal 200ms var(--ease-out); }
    @keyframes reveal { from { opacity: 0; transform: translateY(-4px); } }

    /* Modais: tela escurece junto; painel cresce de 96% no computador e sobe como folha no celular */
    .modal-overlay { opacity: 0; transition: opacity 250ms var(--ease-out); }
    .modal-overlay.is-open { opacity: 1; }
    .modal-overlay > div { transform: scale(0.96); transition: transform 250ms var(--ease-out); }
    .modal-overlay.is-open > div { transform: none; }
    @media (max-width: 40rem) {
      .modal-overlay { align-items: flex-end; padding: 0; }
      .modal-overlay > div { width: 100%; max-width: none !important; border-radius: var(--radius-card) var(--radius-card) 0 0 !important; transform: translateY(100%); transition: transform 450ms var(--ease-drawer); }
      .modal-overlay.is-open > div { transform: none; }
    }

    /* Hover só onde existe mouse (no toque o hover "gruda" depois do toque) */
    @media (hover: none) {
      .grade-btn:hover { background: var(--color-paper-3); border-color: var(--color-rule); color: var(--color-ink); }
      .grade-btn:hover .grade-when { color: var(--color-muted); }
      .filter-pill.inactive:hover { border-color: var(--color-rule); color: var(--color-ink-2); }
    }

    /* Tela de abertura: só aparece com JavaScript ligado (sem JS o conteúdo fica visível).
       O salsicha corre por baixo da palavra; as letras aparecem atrás dele. */
    .splash { display: none; }
    html.js .splash {
      position: fixed;
      inset: 0;
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--color-paper);
      transition: opacity var(--dur-long) var(--ease-out);
      cursor: pointer;
      overflow: hidden;
    }
    .splash--out { opacity: 0; pointer-events: none; }
    .splash__stage { position: relative; padding-bottom: clamp(84px, 16vw, 124px); }
    .splash__word {
      font-size: clamp(2.5rem, 9vw, 4.5rem);
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1;
      color: var(--color-ink);
      clip-path: inset(0 100% 0 0);
      animation: splash-reveal 1200ms linear 400ms forwards;
    }
    .splash__word span { color: var(--color-accent); }
    @keyframes splash-reveal { to { clip-path: inset(0 0 0 0); } }

    /* O corredor tem a largura da palavra: ir de -100% a 0 leva o focinho do começo ao fim dela */
    .splash__runner {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: clamp(84px, 16vw, 124px);
      transform: translateX(calc(-100% - 160px));
      animation: splash-run 1600ms linear forwards;
    }
    @keyframes splash-run {
      25% { transform: translateX(-100%); }
      100% { transform: translateX(0); }
    }
    .splash__dog {
      position: absolute;
      right: calc(clamp(150px, 30vw, 230px) * -0.1);
      bottom: 0;
      width: clamp(150px, 30vw, 230px);
      height: auto;
      overflow: visible;
      animation: splash-exit 600ms linear 1600ms forwards;
    }
    @keyframes splash-exit { to { transform: translateX(70vw); opacity: 0; } }

    /* Corrida: o corpo quica, as patas vão e voltam em pares, a orelha balança, o rabo abana */
    .dog-body { animation: dog-bob 260ms ease-in-out infinite alternate; }
    @keyframes dog-bob { to { transform: translateY(-2.5px); } }
    .dog-leg { transform-box: fill-box; transform-origin: 50% 0; animation: dog-leg 260ms ease-in-out infinite alternate; }
    .dog-leg--b { animation-delay: -260ms; }
    @keyframes dog-leg { from { transform: rotate(32deg); } to { transform: rotate(-32deg); } }
    .dog-ear { transform-box: fill-box; transform-origin: 50% 10%; animation: dog-ear 260ms ease-in-out infinite alternate; }
    @keyframes dog-ear { from { transform: rotate(-14deg); } to { transform: rotate(10deg); } }
    .dog-tail { transform-box: fill-box; transform-origin: 100% 100%; animation: dog-tail 180ms ease-in-out infinite alternate; }
    @keyframes dog-tail { from { transform: rotate(-12deg); } to { transform: rotate(14deg); } }
    .dog-sock { transform-box: fill-box; transform-origin: 30% 0; animation: dog-sock 260ms ease-in-out infinite alternate; }
    @keyframes dog-sock { from { transform: rotate(-8deg); } to { transform: rotate(12deg); } }
    .dog-shadow { animation: dog-shadow 260ms ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }
    @keyframes dog-shadow { to { transform: scaleX(0.9); opacity: 0.6; } }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation-iteration-count: 1 !important; scroll-behavior: auto !important; }
      .flashcard-inner, .tab-indicator.is-ready { transition: none; }
      .flashcard-wrapper.card-leave { animation: fade-out 120ms ease forwards; }
      .flashcard-wrapper.card-enter-next, .flashcard-wrapper.card-enter-prev, .reveal { animation: fade-in 160ms ease; }
      .modal-overlay > div, .modal-overlay.is-open > div { transform: none !important; transition: none; }
      .grade-btn:active, .filter-pill:active, .main-tab-btn:active { transform: none; }
      .splash__word { clip-path: none; animation: fade-in 200ms ease forwards; }
      .splash__runner { transform: none; animation: none; }
      .splash__dog, .dog-body, .dog-leg, .dog-ear, .dog-tail, .dog-sock, .dog-shadow { animation: none; }
      .wave-bar { animation: none; transform: scaleY(0.7); }
    }
    @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fade-out { to { opacity: 0; } }
  </style>
</head>
<body class="custom-scroll">

  <!-- TELA DE ABERTURA -->
  <div id="splash" class="splash" aria-hidden="true" onclick="hideSplash()">
    <div class="splash__stage">
      <div class="splash__word">Flashcards<span>.</span></div>
      <div class="splash__runner">
        <svg class="splash__dog" viewBox="0 0 190 78" xmlns="http://www.w3.org/2000/svg">
          <ellipse class="dog-shadow" cx="86" cy="71" rx="62" ry="3" fill="var(--color-dog-dark)" opacity="0.18"/>
          <g class="dog-legs-back">
            <rect class="dog-leg dog-leg--b" x="34" y="44" width="8" height="22" rx="4" fill="var(--color-dog-dark)"/>
            <rect class="dog-leg dog-leg--b" x="104" y="44" width="8" height="22" rx="4" fill="var(--color-dog-dark)"/>
          </g>
          <g class="dog-body">
            <path class="dog-tail" d="M24 34 C14 30 8 22 6 14 C10 20 16 25 26 28 Z" fill="var(--color-dog)"/>
            <rect x="18" y="24" width="104" height="28" rx="14" fill="var(--color-dog)"/>
            <rect x="30" y="42" width="82" height="10" rx="5" fill="var(--color-dog-belly)"/>
            <path d="M108 30 C112 18 122 12 132 14 L136 30 C128 36 116 38 108 30 Z" fill="var(--color-dog)"/>
            <ellipse cx="136" cy="22" rx="17" ry="13" fill="var(--color-dog)"/>
            <ellipse cx="154" cy="27" rx="12" ry="7.5" fill="var(--color-dog)"/>
            <circle cx="165" cy="24.5" r="3" fill="var(--color-ink)"/>
            <circle cx="142" cy="18" r="2" fill="var(--color-ink)"/>
            <ellipse class="dog-ear" cx="129" cy="24" rx="6.5" ry="12" fill="var(--color-dog-dark)"/>
            <g class="dog-sock">
              <path d="M152 28 L163 28 L163 52 C163 58 168 61 176 61 C182 61 186 64 186 68 C186 72 182 74 176 74 L160 74 C153 74 150 69 150 62 Z" fill="var(--color-sock)" stroke="var(--color-dog-dark)" stroke-width="1.2"/>
              <rect x="151" y="28" width="13" height="5" rx="1.5" fill="var(--color-sock-stripe)"/>
              <rect x="151" y="37" width="12" height="3.5" fill="var(--color-sock-stripe)"/>
              <rect x="151" y="44" width="12" height="3.5" fill="var(--color-sock-stripe)"/>
              <path d="M178 61 C183 61 186 64 186 68 C186 72 183 74 178 74 Z" fill="var(--color-sock-stripe)"/>
              <path d="M150 64 C150 70 153 74 159 74 L161 74 C157 71 156 67 157 63 Z" fill="var(--color-sock-stripe)"/>
            </g>
          </g>
          <g class="dog-legs-front">
            <rect class="dog-leg" x="42" y="44" width="8" height="22" rx="4" fill="var(--color-dog)"/>
            <rect class="dog-leg" x="112" y="44" width="8" height="22" rx="4" fill="var(--color-dog)"/>
          </g>
        </svg>
      </div>
    </div>
  </div>

  <!-- ==========================================
       HEADER FIXO E COMPACTO (Foco Mobile/Tablet)
       ========================================== -->
  <header class="glass-header sticky top-0 z-40">
    <h1 class="visually-hidden">MedFlashcards</h1>
    <div class="max-w-4xl mx-auto px-4 py-3 flex flex-wrap items-center gap-3">
      <!-- ABAS PRINCIPAIS -->
      <nav class="tab-track flex-1 min-w-[260px]" id="tabTrack" aria-label="Seções">
        <span class="tab-indicator" id="tabIndicator" aria-hidden="true"></span>
        <button type="button" onclick="switchTab('tabelas')" id="tabBtn-tabelas" class="main-tab-btn active">
          <span>Tabelas</span> <span class="text-xs bg-paper2 text-muted px-2" id="badgeCount-tabelas">169</span>
        </button>
        <button type="button" onclick="switchTab('flashcards')" id="tabBtn-flashcards" class="main-tab-btn inactive">
          <span>Cards</span> <span class="text-xs bg-paper2 text-muted px-2" id="badgeCount-flashcards">204</span>
        </button>
        <button type="button" onclick="switchTab('geral')" id="tabBtn-geral" class="main-tab-btn inactive">
          <span>Já caiu</span> <span class="text-xs bg-paper2 text-muted px-2" id="badgeCount-geral">8</span>
        </button>
        <button type="button" onclick="switchTab('fgv')" id="tabBtn-fgv" class="main-tab-btn inactive">
          <span>FGV</span> <span class="text-xs bg-paper2 text-muted px-2" id="badgeCount-fgv">0</span>
        </button>
      </nav>

      <!-- Ações -->
      <div class="flex items-center gap-2 ml-auto">
        <button type="button" id="cloudBtn" onclick="cloudButtonClick()" class="hidden h-10 px-3 bg-paper3 text-ink border border-rule flex items-center gap-2 text-sm font-semibold hover:border-muted transition-colors" title="Salvar progresso na nuvem">
          <i id="cloudIcon" class="fa-brands fa-google text-xs" aria-hidden="true"></i>
          <span id="cloudLabel">Entrar</span>
        </button>
        <button type="button" onclick="openModal('exportModal')" class="h-10 px-3 bg-paper3 text-ink border border-rule text-sm font-semibold hover:border-muted transition-colors" title="Backup do progresso">Backup</button>
        <button type="button" onclick="openModal('addModal')" class="h-10 px-4 bg-accent text-accentink border border-accent text-sm font-semibold hover:bg-ink hover:border-ink transition-colors">Adicionar</button>
      </div>
    </div>
  </header>

  <!-- ==========================================
       CONTEÚDO PRINCIPAL
       ========================================== -->
  <main class="max-w-4xl mx-auto px-4 py-4 w-full">

    <!-- FILTRO DE GRANDES ÁREAS (Comum a todas as abas) -->
    <div class="mb-4">
      <div class="seg flex items-center overflow-x-auto no-scrollbar">
        <button onclick="setAreaFilter('todas')" class="filter-pill active" data-area="todas">Todas</button>
        <button onclick="setAreaFilter('clinica')" class="filter-pill inactive" data-area="clinica">Clínica</button>
        <button onclick="setAreaFilter('cirurgia')" class="filter-pill inactive" data-area="cirurgia">Cirurgia</button>
        <button onclick="setAreaFilter('pediatria')" class="filter-pill inactive" data-area="pediatria">Pediatria</button>
        <button onclick="setAreaFilter('go')" class="filter-pill inactive" data-area="go">GO</button>
        <button onclick="setAreaFilter('preventiva')" class="filter-pill inactive" data-area="preventiva">Preventiva</button>
      </div>
    </div>

    <!-- ==========================================
         ABA 1: TABELAS DE REVISÃO
         ========================================== -->
    <section id="view-tabelas" class="tab-view block space-y-4">
      <!-- Subfiltro por tipo de tabela -->
      <div class="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-rule">
        <div class="seg flex items-center overflow-x-auto no-scrollbar">
          <button onclick="setCategoryFilter('todas')" class="filter-pill active" data-cat="todas">Todas</button>
          <button onclick="setCategoryFilter('eponimos')" class="filter-pill inactive" data-cat="eponimos">Epônimos</button>
          <button onclick="setCategoryFilter('triades')" class="filter-pill inactive" data-cat="triades">Tríades e pêntades</button>
          <button onclick="setCategoryFilter('doencas')" class="filter-pill inactive" data-cat="doencas">Doenças</button>
        </div>
        <div class="text-xs font-bold text-muted shrink-0" id="tableItemCount">169 itens</div>
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
      <div class="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-rule">
        <h2 class="text-lg text-ink">Revisão espaçada</h2>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs font-display font-medium text-ink" id="flashcardCounter">Card 1 de 133</div>
            <div class="text-xs font-display text-muted" id="flashcardScore">0 revisados hoje</div>
          </div>
          <div class="flex gap-2">
            <button type="button" onclick="openTrailModal()" class="h-10 px-3 bg-paper3 hover:bg-paper2 text-ink border-2 border-ink text-xs font-medium flex items-center gap-2 transition-colors">
              <span>Índice</span>
            </button>
            <button type="button" onclick="openModal('tipsModal')" class="h-10 px-3 bg-paper3 hover:bg-paper2 text-ink border-2 border-ink text-xs font-medium flex items-center gap-2 transition-colors">
              <span>Técnicas</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Painel de Cronograma SRS e Previsão 7 Dias -->
      <div id="srsDashboard" class="space-y-3">
        <!-- Renderizado dinamicamente via JS -->
      </div>

      <!-- Modos de Estudo e Trilhas por Especialidade -->
      <div id="fcControls" class="space-y-2">
        <!-- Renderizado dinamicamente via JS -->
      </div>

      <!-- Card Interativo e Controles -->
      <div id="flashcardSection" class="w-full max-w-2xl mx-auto pt-2">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>

    <!-- ==========================================
         ABA 3: JÁ CAIU NA MACKENZIE (Bancas)
         ========================================== -->
    <section id="view-geral" class="tab-view hidden space-y-4">
      <div class="flex items-center justify-between pb-2 border-b border-rule">
        <div>
          <h2 class="text-lg text-ink">Pegadinhas de banca</h2>
          <p class="text-sm text-muted">O que a banca repete e o detalhe que decide a questão.</p>
        </div>
        <div class="font-display text-xs text-muted shrink-0" id="mackCount">8 tópicos</div>
      </div>

      <div id="mackContainer" class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>

    <!-- ==========================================
         ABA 4: BANCA FGV (FLASHCARDS & TABELAS)
         ========================================== -->
    <section id="view-fgv" class="tab-view hidden space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-rule">
        <div>
          <h2 class="text-lg text-ink">Banca FGV</h2>
          <p class="text-sm text-muted">Flashcards e tabelas baseados em questões prévias da FGV.</p>
        </div>
        <div class="flex items-center gap-1.5" id="fgvSubTabs">
          <button type="button" onclick="setFGVSubTab('cards')" id="fgvSubBtn-cards" class="filter-pill active">Cards FGV (0)</button>
          <button type="button" onclick="setFGVSubTab('tables')" id="fgvSubBtn-tables" class="filter-pill inactive">Tabelas FGV (0)</button>
        </div>
      </div>

      <div id="fgvContent" class="space-y-4">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>

  </main>

  <!-- ==========================================
       BOTTOM MINI AUDIO PLAYER (Fixo no Rodapé)
       ========================================== -->
  <div id="bottomAudioPlayer" class="fixed bottom-0 left-0 right-0 z-50 bg-ink text-paper border-t-2 border-ink px-4 py-3 transition-transform duration-300 translate-y-full">
    <div class="max-w-4xl mx-auto flex items-center justify-between gap-3">

      <!-- Info do Áudio -->
      <div class="flex items-center gap-3 min-w-0 flex-1">
        <div class="w-10 h-10 text-amber flex items-center justify-center shrink-0 border-2 border-inkrule">
          <div id="playerWave" class="hidden flex items-end gap-0.5 h-4">
            <span class="w-1 wave-bar" style="animation-delay: 0.1s"></span>
            <span class="w-1 wave-bar" style="animation-delay: 0.3s"></span>
            <span class="w-1 wave-bar" style="animation-delay: 0.2s"></span>
          </div>
          <i id="playerStaticIcon" class="fa-solid fa-headphones text-xs" aria-hidden="true"></i>
        </div>
        <div class="min-w-0">
          <p id="audioPlayerTitle" class="font-display text-sm font-medium text-paper truncate">Macete em áudio</p>
          <div class="flex items-center gap-3 text-xs">
            <span id="audioCurrentTime" class="font-display text-amber">1.7x</span>
            <button type="button" onclick="openScriptModal()" class="text-paper underline min-h-6 py-1">Ver texto e pular</button>
          </div>
        </div>
      </div>

      <!-- Controles de Áudio -->
      <div class="flex items-center gap-1">
        <button type="button" onclick="audioSkip(-1)" class="w-10 h-10 border-2 border-inkrule text-paper hover:bg-ink2 flex items-center justify-center text-xs transition-colors" title="Frase anterior" aria-label="Frase anterior">
          <i class="fa-solid fa-backward-step" aria-hidden="true"></i>
        </button>
        <button type="button" id="audioPlayBtn" onclick="toggleAudio()" class="w-10 h-10 bg-accent border-2 border-accent text-accentink flex items-center justify-center text-sm transition-colors" aria-label="Tocar ou pausar">
          <i id="audioPlayIcon" class="fa-solid fa-play" aria-hidden="true"></i>
        </button>
        <button type="button" onclick="audioSkip(1)" class="w-10 h-10 border-2 border-inkrule text-paper hover:bg-ink2 flex items-center justify-center text-xs transition-colors" title="Próxima frase" aria-label="Próxima frase">
          <i class="fa-solid fa-forward-step" aria-hidden="true"></i>
        </button>
        <button type="button" onclick="cycleSpeed()" id="speedBadge" class="h-10 px-2 border-2 border-inkrule text-amber font-display font-extrabold text-xs hover:bg-ink2 transition-colors" aria-label="Mudar velocidade">
          1.7x
        </button>
        <button type="button" onclick="closeAudioPlayer()" class="w-10 h-10 ml-1 text-paper hover:text-amber flex items-center justify-center text-sm transition-colors" aria-label="Fechar player">
          <i class="fa-solid fa-xmark" aria-hidden="true"></i>
        </button>
      </div>

    </div>
  </div>

  <!-- ==========================================
       MODAL: VER TEXTO DO ÁUDIO
       ========================================== -->
  <div id="scriptModal" class="modal-overlay" style="display: none;">
    <div class="bg-paper3 border border-rule w-full max-w-lg max-h-[85vh] flex flex-col shadow-card overflow-hidden">
      <div class="p-4 border-b border-rule flex items-center justify-between bg-paper2">
        <div class="flex items-center gap-2">
          <h3 class="text-sm text-ink">Roteiro do áudio</h3>
        </div>
        <button type="button" onclick="closeModal('scriptModal')" class="text-muted hover:text-ink2 w-10 h-10 flex items-center justify-center -mr-2" aria-label="Fechar">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div id="scriptParagraphsContainer" class="p-4 overflow-y-auto space-y-2 text-xs leading-relaxed custom-scroll flex-1">
        <!-- Preenchido via JS -->
      </div>
      <div class="p-3 border-t border-rule bg-paper2 text-xs text-ink2 text-center font-medium">
        Toque numa frase para o áudio começar dali.
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: ADICIONAR NOVO ITEM
       ========================================== -->
  <div id="addModal" class="modal-overlay" style="display: none;">
    <div class="bg-paper3 border border-rule w-full max-w-lg max-h-[90vh] flex flex-col shadow-card overflow-hidden">
      <div class="p-4 border-b border-rule flex items-center justify-between bg-paper2">
        <div class="flex items-center gap-2">
          <h3 class="text-sm text-ink">Adicionar ao MedFlashcards</h3>
        </div>
        <button type="button" onclick="closeModal('addModal')" class="text-muted hover:text-ink2 w-10 h-10 flex items-center justify-center -mr-2" aria-label="Fechar">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Abas de Tipo de Inserção -->
      <div class="flex border-b border-rule px-4 pt-2 gap-2 text-xs font-bold overflow-x-auto no-scrollbar">
        <button onclick="setAddType('tabela')" id="addType-tabela" class="py-1.5 px-3 border-b-2 border-ink text-ink2">Tabela</button>
        <button onclick="setAddType('flashcard')" id="addType-flashcard" class="py-1.5 px-3 text-muted hover:text-ink">Flashcard</button>
        <button onclick="setAddType('geral')" id="addType-geral" class="py-1.5 px-3 text-muted hover:text-ink">Já caiu</button>
        <button onclick="setAddType('raw')" id="addType-raw" class="py-1.5 px-3 text-muted hover:text-ink">Texto solto</button>
      </div>

      <!-- Form Body -->
      <div class="p-4 overflow-y-auto space-y-3 text-xs flex-1 custom-scroll">
        <div class="grid grid-cols-2 gap-2.5" id="field-area-cat">
          <div>
            <label class="block font-bold text-ink mb-1">Grande Área</label>
            <select id="inputArea" class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
              <option value="clinica">Clínica Médica / Cardio</option>
              <option value="cirurgia">Cirurgia Geral</option>
              <option value="pediatria">Pediatria</option>
              <option value="go">Ginecologia & Obstetrícia</option>
              <option value="preventiva">Medicina Preventiva</option>
            </select>
          </div>
          <div id="field-cat-container">
            <label class="block font-bold text-ink mb-1">Tipo de Tabela</label>
            <select id="inputCat" class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
              <option value="eponimos">Epônimo</option>
              <option value="triades">Tríade / Pêntade</option>
              <option value="doencas">Doença (Epidemio + Tto)</option>
            </select>
          </div>
        </div>

        <!-- Form Tabela -->
        <div id="form-tabela" class="space-y-2.5">
          <div>
            <label class="block font-bold text-ink mb-1">Nome do Epônimo / Doença / Tríade</label>
            <input type="text" id="tabName" placeholder="Ex: Tríade de Beck ou Técnica de Lichtenstein..." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Definição / Achados / Epidemiologia</label>
            <textarea id="tabCol1" rows="2" placeholder="Ex: Hipotensão + Bulhas hipofonéticas + Turgência jugular..." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Diagnóstico & Conduta Terapêutica</label>
            <textarea id="tabCol2" rows="2" placeholder="Ex: Pericardiocentese de alívio imediata..." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Macete em Áudio (Lido a 1.7x)</label>
            <textarea id="tabAudio" rows="2" placeholder="Texto explicativo para ser lido em áudio..." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
        </div>

        <!-- Form Flashcard -->
        <div id="form-flashcard" class="space-y-2.5 hidden">
          <div>
            <label class="block font-bold text-ink mb-1">Frente do Cartão (Pergunta)</label>
            <textarea id="fcFront" rows="2" placeholder="Ex: Qual o antibiótico de escolha para celulite estreptocócica?" class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Verso do Cartão (Resposta Direta)</label>
            <textarea id="fcBack" rows="2" placeholder="Ex: Cefazolina ou Oxacilina IV; Cefalexina VO." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Macete Falado em Áudio</label>
            <textarea id="fcAudio" rows="2" placeholder="Explicação falada para fixação rápida..." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
        </div>

        <!-- Form Já Caiu Geral -->
        <div id="form-geral" class="space-y-2.5 hidden">
          <div>
            <label class="block font-bold text-ink mb-1">Tema / Assunto Cobrado</label>
            <input type="text" id="mackTitle" placeholder="Ex: SHU pós-STEC" class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Pegadinha / Como a banca cobra</label>
            <textarea id="mackTip" rows="3" placeholder="Ex: Antibiótico é contraindicado por risco de liberação maciça de toxina Shiga..." class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent"></textarea>
          </div>
          <div>
            <label class="block font-bold text-ink mb-1">Ano / Prova (Ex: Geral 2024, ENARE 2025)</label>
            <input type="text" id="mackYear" placeholder="Ex: Geral 2024 / Bancas" class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
          </div>
        </div>

        <!-- Form Colar Texto Solto -->
        <div id="form-raw" class="space-y-2.5 hidden">
          <div>
            <label class="block font-bold text-ink mb-1">Cole aqui notas, tabelas ou resumos soltos</label>
            <textarea id="rawText" rows="6" placeholder="Pode colar qualquer anotação bruta. O app salva e eu posso estruturar tudo para você aqui no chat!" class="w-full bg-paper2 border border-rule p-2 text-ink focus:outline-none focus:ring-2 focus:ring-accent custom-scroll"></textarea>
          </div>
        </div>
      </div>

      <!-- Form Footer -->
      <div class="p-3 border-t border-rule flex items-center justify-end gap-2 bg-paper3">
        <button onclick="closeModal('addModal')" class="px-3.5 py-2 text-muted hover:text-ink2 text-xs font-bold">Cancelar</button>
        <button onclick="submitNewItem()" class="px-5 py-2 bg-accent text-accentink font-bold text-xs flex items-center gap-1.5 transition-colors">
          <i class="fa-solid fa-check" aria-hidden="true"></i> Salvar
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: BACKUP E SINCRONIZAÇÃO
       ========================================== -->
  <div id="exportModal" class="modal-overlay" style="display: none;">
    <div class="bg-paper3 border border-rule w-full max-w-sm flex flex-col shadow-card overflow-hidden">
      <div class="p-4 border-b border-rule flex items-center justify-between bg-paper2">
        <div class="flex items-center gap-2">
          <h3 class="text-sm text-ink">Backup</h3>
        </div>
        <button type="button" onclick="closeModal('exportModal')" class="text-muted hover:text-ink2 w-10 h-10 flex items-center justify-center -mr-2" aria-label="Fechar">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="p-4 space-y-3 text-xs">
        <p class="text-ink2 leading-relaxed">
          Leve o progresso de um aparelho para outro sem login:
        </p>

        <div class="space-y-2">
          <button onclick="exportData()" class="w-full py-2.5 px-4 bg-paper2 text-ink2 font-bold hover:bg-paper2 transition-colors flex items-center justify-center gap-2">
            <i class="fa-solid fa-download" aria-hidden="true"></i> Baixar arquivo de backup
          </button>
          
          <label class="w-full py-2.5 px-4 border border-dashed border-rule text-ink2 font-bold hover:bg-paper2 transition-colors flex items-center justify-center gap-2 cursor-pointer">
            <i class="fa-solid fa-upload" aria-hidden="true"></i> Restaurar de um arquivo
            <input type="file" id="importFileInput" onchange="importData(event)" class="hidden" accept=".json">
          </label>
        </div>

        <p class="text-xs text-muted text-center pt-1">
          Com login pelo Google o progresso já fica salvo na nuvem. O arquivo serve de cópia extra.
        </p>
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: ÍNDICE SEQUENCIAL DA TRILHA
       ========================================== -->
  <div id="trailModal" class="modal-overlay" style="display: none;">
    <div class="bg-paper3 border border-rule w-full max-w-lg max-h-[85vh] flex flex-col shadow-card overflow-hidden">
      <div class="p-4 border-b border-rule flex items-center justify-between bg-paper2">
        <div class="flex items-center gap-2">
          <div>
            <h3 class="text-sm text-ink">Índice da trilha</h3>
            <p class="text-xs text-muted">Toque num card para ir direto a ele.</p>
          </div>
        </div>
        <button type="button" onclick="closeModal('trailModal')" class="text-muted hover:text-ink2 w-10 h-10 flex items-center justify-center -mr-2" aria-label="Fechar">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div id="trailModalList" class="px-3 pb-3 overflow-y-auto custom-scroll text-xs">
        <!-- Renderizado via JS -->
      </div>
    </div>
  </div>

  <!-- ==========================================
       MODAL: TÉCNICAS DE MEMORIZAÇÃO ATIVA
       ========================================== -->
  <div id="tipsModal" class="modal-overlay" style="display: none;">
    <div class="bg-paper3 border border-rule w-full max-w-md max-h-[85vh] flex flex-col shadow-card overflow-hidden">
      <div class="p-4 border-b border-rule flex items-center justify-between bg-paper2">
        <div class="flex items-center gap-2">
          <h3 class="text-sm text-ink">Como fixar mais rápido</h3>
        </div>
        <button type="button" onclick="closeModal('tipsModal')" class="text-muted hover:text-ink2 w-10 h-10 flex items-center justify-center -mr-2" aria-label="Fechar">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div class="p-4 overflow-y-auto custom-scroll space-y-3 text-xs text-ink leading-relaxed">
        <div class="bg-paper2 p-3 border border-rule">
          <div class="font-bold text-ink mb-1">1. Repetição espaçada</div>
          <p>Não revise tudo todo dia! Se acertou fácil, o card volta em <b>3 dias</b>, depois em <b>7</b>, e o intervalo continua crescendo até a véspera da prova. Se errou, ele volta em <b>5 minutos</b> na mesma sessão e reaparece amanhã.</p>
        </div>
        <div class="bg-paper2 p-3 border border-rule">
          <div class="font-bold text-ink mb-1">2. Pista antes de virar</div>
          <p>Travou na pergunta? Não vire direto! Clique em <b>“Quero uma dica”</b> na frente do card. Forçar o cérebro a lembrar com uma pista cria sinapses muito mais fortes do que apenas ler a resposta.</p>
        </div>
        <div class="bg-paper2 p-3 border border-rule">
          <div class="font-bold text-ink mb-1">3. Ancore no porquê</div>
          <p>Sempre leia o bloco <b>Por que? / Fisiopatologia</b> no verso. Quando você entende a lógica física (ex: a albumina é grande e fica presa na peneira), você deduz o número na prova mesmo se der branco.</p>
        </div>
        <div class="bg-paper2 p-3 border border-rule">
          <div class="font-bold text-ink mb-1">4. Quinze segundos e áudio a 1.7x</div>
          <p>Responda <b>em voz alta</b> em até 15s antes de virar. Se errar, clique em <b>“Ouvir 1.7x”</b> no verso para fixar pela via auditiva também.</p>
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
    // Os dados guardam as pegadinhas em "mackenzie"; a aba Já caiu lê "geral"
    if (!appState.geral) appState.geral = appState.mackenzie || [];
    if (!appState.fgv_flashcards) appState.fgv_flashcards = [];
    if (!appState.fgv_tables) appState.fgv_tables = [];

    var activeTab = 'tabelas';
    var activeArea = 'todas';
    var activeCategory = 'todas';
    var fgvSubTab = 'cards';
    var fgvCardIndex = 0;
    var fgvFlipped = false;
    var fgvShowHint = false;
    var currentFlashcardIndex = 0;
    var isFlipped = false;
    var showHint = false;
    var fcDraftAnswers = {};
    var clozeMode = false;
    var fcStudyMode = 'schedule'; // 'schedule' | 'mixed' | 'sequential' | 'hard'
    var fcQueueFilter = 'today'; // 'today' | 'due' | 'new'
    var fgvQueueFilter = 'today'; // 'today' | 'due' | 'new'
    var shuffleSeed = Date.now();
    var trailPinnedId = null; // card aberto pela Trilha, exibido mesmo se agendado para depois
    var fgvPinnedId = null;   // card FGV aberto pela Agenda, exibido mesmo se agendado para depois
    var lastRatingNotice = '';
    var trailModalSource = 'fc';
    var fcSpecialty = 'todas';
    var fcSubtopic = 'todos';
    var showProgress = false; // números e previsão de 7 dias recolhidos
    var showFilters = false;  // especialidade e tema recolhidos
    var cardEnterDir = '';    // 'next' | 'prev': de que lado o próximo card entra
    var cardLeaving = false;  // trava enquanto o card avaliado sai
    var progressJustOpened = false;
    var srsData = {};
    var srsStats = { reviewedToday: 0, newToday: 0, lastReviewDate: '', examDate: 0 };
    var addModalType = 'tabela';
    var flashcardScores = { correct: 0, review: 0 };
    var lastRatedSnapshot = null;
    var pendingCloudDeletes = {};

    // Player de Áudio
    var currentSpeed = 1.7;
    var isPlaying = false;
    var currentSpeechText = "";
    var speechUtterance = null;
    var speechChunks = [];
    var currentChunkIndex = 0;
    var speechToken = 0;
    var selectedVoice = null;
    var voicesList = [];

    // INICIALIZAÇÃO SEGURA
    window.addEventListener('DOMContentLoaded', function() {
      try { loadState(); } catch(e) { console.warn('loadState err', e); }
      try { initCloud(); } catch(e) { console.warn('initCloud err', e); }
      try { initSpeech(); } catch(e) { console.warn('initSpeech err', e); }
      try { updateBadges(); } catch(e) {}
      try { renderCurrentTab(); } catch(e) { console.error('render err', e); }
      var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      setTimeout(hideSplash, reduceMotion ? 1200 : 2500);
      moveTabIndicator();
      window.addEventListener('resize', moveTabIndicator);
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(moveTabIndicator);
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
          if (parsed.geral && parsed.geral.length > 0) {
            var existingGIds = {};
            for (var gi = 0; gi < appState.geral.length; gi++) existingGIds[appState.geral[gi].id] = true;
            for (var gj = 0; gj < parsed.geral.length; gj++) {
              if (!existingGIds[parsed.geral[gj].id]) appState.geral.push(parsed.geral[gj]);
            }
          }
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
        if (!srsStats.examDate || (!srsStats.examSetAt && srsStats.examDate < getStartOfDay(14))) {
          srsStats.examDate = getStartOfDay(60);
          saveSRS();
        }
      } catch (e) {
        console.warn('Storage read restricted:', e);
      }
    }

    // Some com a tela de abertura (também ao tocar nela)
    function hideSplash() {
      var el = document.getElementById('splash');
      if (!el || el.classList.contains('splash--out')) return;
      el.classList.add('splash--out');
      setTimeout(function() { if (el.parentNode) el.parentNode.removeChild(el); }, 450);
    }

    function ensureTodayStats() {
      var today = getTodayStr();
      if (srsStats.lastReviewDate && srsStats.lastReviewDate !== today) {
        srsStats.reviewedToday = 0;
        srsStats.newToday = 0;
      }
      srsStats.lastReviewDate = today;
    }

    function writeLocalSRS() {
      try {
        ensureTodayStats();
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
    var cloud = { auth: null, db: null, user: null, unsub: null, pushTimer: null, status: 'off', hydrated: false };

    function initCloud() {
      if (typeof firebase === 'undefined') { setCloudStatus('unavailable'); return; }
      try {
        if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
        cloud.auth = firebase.auth();
        cloud.db = firebase.firestore();
        setCloudStatus('off');
        cloud.auth.onAuthStateChanged(function(user) {
          cloud.user = user;
          cloud.hydrated = false;
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
        cloud.hydrated = true;
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
      if (cloud.pushTimer && cloud.hydrated) pushCloudNow();
    }

    function pushCloudNow() {
      if (cloud.pushTimer) { clearTimeout(cloud.pushTimer); cloud.pushTimer = null; }
      if (!cloud.user || !cloud.db) return;
      if (!cloud.hydrated) return;
      var payloadSrsData = Object.assign({}, srsData);
      var deletedIds = Object.keys(pendingCloudDeletes);
      for (var di = 0; di < deletedIds.length; di++) {
        var delId = deletedIds[di];
        if (!payloadSrsData.hasOwnProperty(delId)) {
          payloadSrsData[delId] = firebase.firestore.FieldValue.delete();
        }
      }
      cloudDocRef().set({
        srsData: payloadSrsData,
        srsStats: srsStats,
        updatedAt: firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: true }).then(function() {
        for (var dj = 0; dj < deletedIds.length; dj++) delete pendingCloudDeletes[deletedIds[dj]];
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
        icon.className = 'fa-brands fa-google text-xs';
        label.innerText = 'Entrar';
        btn.title = 'Entrar com Google para salvar o progresso na nuvem';
      } else if (status === 'syncing') {
        icon.className = 'fa-solid fa-rotate fa-spin text-xs text-muted';
        label.innerText = first || 'Salvando';
        btn.title = 'Sincronizando com a nuvem...';
      } else if (status === 'ok') {
        icon.className = 'fa-solid fa-cloud text-xs text-accent';
        label.innerText = first || 'Na nuvem';
        btn.title = 'Progresso salvo na nuvem' + (cloud.user && cloud.user.email ? ' (' + cloud.user.email + ')' : '');
      } else {
        icon.className = 'fa-solid fa-triangle-exclamation text-xs text-ink';
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
      var bFgv = document.getElementById('badgeCount-fgv');
      if (bTab) bTab.innerText = appState.tables ? appState.tables.length : 0;
      if (bFc) bFc.innerText = appState.flashcards ? appState.flashcards.length : 0;
      if (bMack) bMack.innerText = appState.geral ? appState.geral.length : 0;
      if (bFgv) bFgv.innerText = (appState.fgv_flashcards ? appState.fgv_flashcards.length : 0) + (appState.fgv_tables ? appState.fgv_tables.length : 0);
    }

    // ==========================================
    // NAVEGAÇÃO DE ABAS (100% GARANTIDA POR STYLE.DISPLAY)
    // ==========================================
    function moveTabIndicator() {
      var track = document.getElementById('tabTrack');
      var ind = document.getElementById('tabIndicator');
      var active = track ? track.querySelector('.main-tab-btn.active') : null;
      if (!track || !ind || !active) return;
      ind.style.width = active.offsetWidth + 'px';
      ind.style.transform = 'translateX(' + active.offsetLeft + 'px)';
      if (!track.classList.contains('has-indicator')) {
        track.classList.add('has-indicator');
        requestAnimationFrame(function() { ind.classList.add('is-ready'); });
      }
    }

    function switchTab(tabId) {
      activeTab = tabId;
      lastRatedSnapshot = null;

      // Esconde todas as abas
      var tabs = ['tabelas', 'flashcards', 'geral', 'fgv'];
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

      moveTabIndicator();
      renderCurrentTab();
      try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch(e) {}
    }

    function setAreaFilter(area) {
      activeArea = area;
      lastRatedSnapshot = null;
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
      else if (activeTab === 'fgv') renderFGV();
    }

    // ==========================================
    // RENDER: TABELAS
    // ==========================================
    // "• •" nos dados marca um subitem: mostra como "◦"
    function tidyBullets(text) {
      return String(text || '-').replace(/•\\s*•/g, '◦');
    }

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
        container.innerHTML = '<div class="glass-card p-6 space-y-2">' +
          '<h3 class="text-base text-ink">Nada nesta área</h3>' +
          '<p class="text-sm text-muted">Troque o filtro acima ou adicione um item pelo botão Adicionar.</p>' +
        '</div>';
        return;
      }

      var html = '';
      for (var i = 0; i < filtered.length; i++) {
        var item = filtered[i];
        var audioBtn = '';
        if (item.audioText) {
          audioBtn = '<button type="button" onclick="playItemAudioByIndex(' + item.id + ', \\'table\\')" class="h-9 px-3 border-2 border-ink bg-paper3 text-ink hover:bg-ink hover:text-paper text-xs font-medium flex items-center gap-2 transition-colors shrink-0">' +
                        '<span>Ouvir 1.7x</span>' +
          '</button>';
        }

        html += '<article class="glass-card">' +
          '<div class="flex items-start justify-between gap-3 p-4 border-b-2 border-ink">' +
            '<div class="min-w-0 space-y-1">' +
              '<div class="flex items-center gap-2 flex-wrap">' +
                '<span class="tag">' + getAreaLabel(item.area) + '</span>' +
                '<span class="font-display text-xs text-muted">' + getCatLabel(item.cat) + '</span>' +
              '</div>' +
              '<h3 class="text-base text-ink leading-snug">' + escapeText(item.name) + '</h3>' +
            '</div>' +
            audioBtn +
          '</div>' +
          '<div class="grid grid-cols-1 md:grid-cols-2 text-sm">' +
            '<div class="p-4 md:border-r border-rule">' +
              '<div class="font-display text-xs text-muted mb-2">Definição e achados</div>' +
              '<p class="text-ink leading-relaxed whitespace-pre-line">' + escapeText(tidyBullets(item.col1)) + '</p>' +
            '</div>' +
            '<div class="p-4 border-t md:border-t-0 border-rule">' +
              '<div class="font-display text-xs text-muted mb-2">Diagnóstico e conduta</div>' +
              '<p class="text-ink leading-relaxed whitespace-pre-line">' + escapeText(tidyBullets(item.col2)) + '</p>' +
            '</div>' +
          '</div>' +
        '</article>';
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
      if (!srsStats.examSetAt) return days;
      var rem = getDaysRemaining();
      if (rem <= 3) return 1;
      var maxAllowed = Math.max(1, rem - 2);
      return Math.min(days, maxAllowed);
    }

    function isClinicalSpecialty(area) {
      return area === 'clinica' || area === 'cardiologia' || area === 'pneumologia' ||
        area === 'gastroenterologia' || area === 'endocrinologia' || area === 'reumatologia' ||
        area === 'hematologia' || area === 'nefrologia' || area === 'neurologia' ||
        area === 'infectologia' || area === 'psiquiatria';
    }

    function isCardNew(s) {
      return !s || s.state === 'new' || !s.lastReview;
    }

    function getCardBucket(s, now, endOfToday) {
      if (isCardNew(s)) return 'new';
      if (s.due <= now) return 'due';
      if (s.due <= endOfToday) return 'relearn';
      return 'scheduled';
    }

    function formatShortDate(ts) {
      if (!ts) return '';
      var d = new Date(ts);
      return String(d.getDate()).padStart(2, '0') + '/' + String(d.getMonth() + 1).padStart(2, '0');
    }

    function getDaysUntilDue(s) {
      if (!s || !s.due) return 0;
      var todayStart = getStartOfDay(0);
      var dueStart = new Date(s.due);
      dueStart.setHours(0, 0, 0, 0);
      return Math.max(0, Math.round((dueStart.getTime() - todayStart) / (24 * 60 * 60 * 1000)));
    }

    function formatScheduleNotice(cardId, quality, s) {
      if (quality === 0) {
        return 'Card #' + cardId + ' marcado como Errei — volta em 5 min (e reaparece amanhã).';
      }
      var days = Math.max(1, s.interval || getDaysUntilDue(s));
      var dateStr = formatShortDate(s.due);
      return 'Card #' + cardId + ' agendado para daqui a ' + days + (days === 1 ? ' dia' : ' dias') + (dateStr ? ' (' + dateStr + ')' : '') + ' — não aparece antes disso.';
    }

    function getSRSCounts(cards) {
      var now = Date.now();
      var endOfToday = getStartOfDay(1) - 1;
      var counts = { due: 0, relearn: 0, newCount: 0, scheduled: 0, hard: 0, learning: 0, mastered: 0, total: cards.length };
      for (var i = 0; i < cards.length; i++) {
        var s = getCardSRS(cards[i].id);
        if (s.lapses > 0) counts.hard++;
        var b = getCardBucket(s, now, endOfToday);
        if (b === 'new') counts.newCount++;
        else if (b === 'due') counts.due++;
        else if (b === 'relearn') counts.relearn++;
        else counts.scheduled++;
        if (b !== 'new') {
          if (s.interval >= 7) counts.mastered++;
          else counts.learning++;
        }
      }
      return counts;
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
            matchTop = isClinicalSpecialty(fc.area);
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

      // Card já avaliado e agendado para um dia futuro (due > endOfToday) NUNCA aparece
      // em nenhum modo até a data dele. Exceção: o card aberto manualmente pela Agenda/Índice (trailPinnedId).
      var base = allBase.filter(function(fc) {
        if (fc.id === trailPinnedId) return true;
        var s = getCardSRS(fc.id);
        var b = getCardBucket(s, now, endOfToday);
        if (b === 'scheduled') return false;
        if (fcQueueFilter === 'due') return b === 'due' || b === 'relearn';
        if (fcQueueFilter === 'new') return b === 'new';
        return true;
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
      // 1) Revisões vencidas prontas AGORA (due <= now) -> 2) Novos -> 3) Erros recentes aguardando 5 min
      var readyDueList = [];
      var waitingRelearnList = [];
      var newList = [];
      var pinnedScheduledList = [];
      for (var i = 0; i < base.length; i++) {
        var fc = base[i];
        var s = getCardSRS(fc.id);
        var b = getCardBucket(s, now, endOfToday);
        if (fc.id === trailPinnedId && b === 'scheduled') {
          pinnedScheduledList.push(fc);
        } else if (b === 'new') {
          newList.push(fc);
        } else if (b === 'due') {
          readyDueList.push(fc);
        } else if (b === 'relearn') {
          waitingRelearnList.push(fc);
        }
      }
      readyDueList.sort(function(a, b) {
        return getCardSRS(a.id).due - getCardSRS(b.id).due;
      });
      waitingRelearnList.sort(function(a, b) {
        return getCardSRS(a.id).due - getCardSRS(b.id).due;
      });
      return pinnedScheduledList
        .concat(interleaveBySpecialty(readyDueList))
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

      var dayLabels = ['Hoje', '+1 d', '+2 d', '+3 d', '+4 d', '+5 d', '+6 d'];
      var forecastHtml = '';
      for (var f = 0; f < 7; f++) {
        var isToday = (f === 0);
        forecastHtml += '<div class="forecast-cell text-center py-2 px-1' + (isToday ? ' is-today' : '') + '">' +
          '<div class="font-display text-xs ' + (isToday ? '' : 'text-muted') + '">' + dayLabels[f] + '</div>' +
          '<div class="font-display text-base font-extrabold ' + (isToday ? 'text-amber' : (forecast[f] > 0 ? 'text-ink' : 'text-muted')) + '">' + forecast[f] + '</div>' +
        '</div>';
      }

      var daysLeft = getDaysRemaining();
      var studyDaysLeft = Math.max(1, daysLeft - 4);
      var dailyNewGoal = newCount > 0 ? Math.min(newCount, Math.max(5, Math.ceil(newCount / studyDaysLeft))) : 0;

      function stat(label, value) {
        return '<div class="stat-cell px-3 py-2">' +
          '<div class="text-xs text-muted">' + label + '</div>' +
          '<div class="figure text-xl leading-tight">' + value + '</div>' +
        '</div>';
      }

      var progressHtml = showProgress
        ? '<div class="px-4 pb-4 space-y-3 border-t border-rule pt-4' + (progressJustOpened ? ' reveal' : '') + '">' +
            '<div class="stat-grid grid-cols-2 sm:grid-cols-4">' +
              stat('Para hoje', dueToday + newCount) +
              stat('Difíceis', hardCount) +
              stat('Fixando', learningCount) +
              stat('Dominados', masteredCount) +
            '</div>' +
            '<div>' +
              '<div class="flex items-center justify-between text-xs text-muted mb-2">' +
                '<span>Revisões nos próximos 7 dias</span>' +
                '<span>' + srsStats.reviewedToday + ' revisados hoje</span>' +
              '</div>' +
              '<div class="grid grid-cols-7 gap-1">' + forecastHtml + '</div>' +
            '</div>' +
          '</div>'
        : '';

      var counts = getSRSCounts(baseCards);
      var dueToday = counts.due + counts.relearn;
      var newCount = counts.newCount;
      var scheduledCount = counts.scheduled;

      function qPill(filterId, label, num) {
        var isAct = (fcQueueFilter === filterId);
        return '<button type="button" onclick="setFCQueueFilter(\\'' + filterId + '\\')" class="filter-pill ' + (isAct ? 'active' : 'inactive') + '">' + label + ' (' + num + ')</button>';
      }

      dash.innerHTML =
        '<div class="summary">' +
          '<div class="flex flex-wrap items-center justify-between gap-x-6 gap-y-2 px-4 py-3">' +
            '<div class="flex items-baseline gap-2">' +
              '<span class="figure figure--accent text-3xl leading-none">' + daysLeft + '</span>' +
              '<span class="text-sm text-ink2">' + (daysLeft === 1 ? 'dia até a prova' : 'dias até a prova') + '</span>' +
            '</div>' +
            '<div class="text-sm text-ink2 flex-1 min-w-[200px]">' +
              'Para revisar hoje: <b class="text-ink">' + dueToday + '</b> · Novos: <b class="text-ink">' + newCount + '</b> · Em dia: <b class="text-ink">' + scheduledCount + '</b>' +
            '</div>' +
            '<div class="flex items-center gap-3">' +
              '<button type="button" onclick="toggleProgress()" class="text-btn" aria-expanded="' + (showProgress ? 'true' : 'false') + '">' + (showProgress ? 'Esconder progresso' : 'Ver progresso') + '</button>' +
              '<button type="button" onclick="adjustExamDays()" class="text-btn">Mudar data</button>' +
            '</div>' +
          '</div>' +
          '<div class="px-4 pb-3 flex flex-wrap items-center gap-2 border-t border-rule pt-2.5">' +
            '<span class="font-display text-xs text-muted mr-1">Mostrar agora:</span>' +
            qPill('today', 'Hoje (Revisões + Novos)', dueToday + newCount) +
            qPill('due', 'Só Revisões do Dia', dueToday) +
            qPill('new', 'Só Novos', newCount) +
          '</div>' +
          progressHtml +
        '</div>';
    }

    function toggleProgress() {
      showProgress = !showProgress;
      progressJustOpened = showProgress;
      renderFlashcards();
      progressJustOpened = false;
    }

    function renderFCControls() {
      var ctrl = document.getElementById('fcControls');
      if (!ctrl) return;

      var modes = [
        { id: 'schedule', label: 'Cronograma de hoje' },
        { id: 'mixed', label: 'Misturado' },
        { id: 'sequential', label: 'Sequencial' },
        { id: 'hard', label: 'Pontos fracos' }
      ];
      var modeHtml = '';
      for (var m = 0; m < modes.length; m++) {
        var active = (fcStudyMode === modes[m].id);
        modeHtml += '<button onclick="setFCStudyMode(\\'' + modes[m].id + '\\')" class="filter-pill ' + (active ? 'active' : 'inactive') + '">' + modes[m].label + '</button>';
      }
      if (fcStudyMode === 'mixed' || fcStudyMode === 'schedule') {
        modeHtml += '<button type="button" onclick="reshuffleCards()" class="filter-pill inactive" title="Gerar nova mistura de especialidades">Embaralhar</button>';
      }

      var specs = [
        { id: 'todas', label: 'Todas' },
        { id: 'cardiologia', label: 'Cardio' },
        { id: 'pneumologia', label: 'Pneumo' },
        { id: 'gastroenterologia', label: 'Gastro' },
        { id: 'endocrinologia', label: 'Endócrino' },
        { id: 'reumatologia', label: 'Reumato' },
        { id: 'hematologia', label: 'Hemato' }
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
        subHtml += '<button onclick="setFCSubtopic(\\'todos\\')" class="filter-pill ' + (fcSubtopic === 'todos' ? 'active' : 'inactive') + '">Todos</button>';
        for (var k = 0; k < subs.length; k++) {
          var subId = subs[k];
          subHtml += '<button onclick="setFCSubtopic(\\'' + subId + '\\')" class="filter-pill ' + (fcSubtopic === subId ? 'active' : 'inactive') + '">' + getCatLabel(subId) + '</button>';
        }
      }

      var filterCount = (fcSpecialty !== 'todas' ? 1 : 0) + (fcSubtopic !== 'todos' ? 1 : 0);
      var filtersOpen = showFilters || filterCount > 0;
      ctrl.innerHTML =
        '<div class="flex items-center gap-2">' +
          '<div class="seg flex overflow-x-auto no-scrollbar min-w-0">' + modeHtml + '</div>' +
          '<button type="button" onclick="toggleFilters()" class="filter-pill ' + (filtersOpen ? 'active' : 'inactive') + ' shrink-0 ml-auto" aria-expanded="' + (filtersOpen ? 'true' : 'false') + '">Filtros' + (filterCount ? ' (' + filterCount + ')' : '') + '</button>' +
        '</div>' +
        (filtersOpen
          ? '<div class="seg flex overflow-x-auto no-scrollbar">' + specHtml + '</div>' +
            (subHtml ? '<div class="seg flex overflow-x-auto no-scrollbar">' + subHtml + '</div>' : '')
          : '');
    }

    function toggleFilters() {
      // Fechar com um filtro ativo limpa o filtro, para nada ficar escondido sem aviso
      var active = fcSpecialty !== 'todas' || fcSubtopic !== 'todos';
      if (showFilters || active) {
        showFilters = false;
        if (active) { fcSpecialty = 'todas'; fcSubtopic = 'todos'; currentFlashcardIndex = 0; }
      } else {
        showFilters = true;
      }
      renderFlashcards();
    }

    function setFCStudyMode(mode) {
      fcStudyMode = mode;
      lastRatedSnapshot = null;
      trailPinnedId = null;
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function setFCQueueFilter(filter) {
      fcQueueFilter = filter;
      lastRatedSnapshot = null;
      trailPinnedId = null;
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function setFGVQueueFilter(filter) {
      fgvQueueFilter = filter;
      fgvPinnedId = null;
      fgvCardIndex = 0;
      fgvFlipped = false;
      fgvShowHint = false;
      renderFGV();
    }

    function setFCSpecialty(spec) {
      fcSpecialty = spec;
      fcSubtopic = 'todos';
      lastRatedSnapshot = null;
      currentFlashcardIndex = 0;
      isFlipped = false;
      showHint = false;
      renderFlashcards();
    }

    function setFCSubtopic(sub) {
      fcSubtopic = sub;
      lastRatedSnapshot = null;
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
          out += '<div class="border-l-4 border-accent bg-paper2 px-3 py-2 text-sm text-ink leading-relaxed rounded-r-lg">' + escaped + '</div>';
        } else if (line.indexOf('⚠️') === 0) {
          out += '<div class="bg-amber px-3 py-2 text-sm text-ink font-medium leading-relaxed rounded-lg">' + escaped + '</div>';
        } else if (line.indexOf('•') === 0 || line.indexOf('-') === 0 || /^\\d+\\./.test(line)) {
          out += '<div class="text-sm text-ink leading-relaxed pl-1">' + escaped + '</div>';
        } else {
          out += '<div class="text-base font-semibold text-ink leading-snug">' + escaped + '</div>';
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

      ensureTodayStats();
      var baseCards = getBaseFilteredFlashcards();
      renderSRSDashboard(baseCards);
      renderFCControls();

      var filtered = getStudyQueue();

      if (scoreEl) {
        scoreEl.innerText = srsStats.reviewedToday + " revisados hoje";
      }

      if (filtered.length === 0) {
        if (counter) counter.innerText = "0 de 0";
        var emptyTitle = (fcStudyMode === 'schedule') ? 'Meta de hoje cumprida' : (fcStudyMode === 'hard' ? 'Nenhum ponto fraco pendente' : 'Nenhum card neste filtro');
        var allScheduled = baseCards.length > 0;
        if (fcStudyMode !== 'schedule' && fcStudyMode !== 'hard' && allScheduled) emptyTitle = 'Tudo em dia neste filtro';
        var emptyDesc = (fcStudyMode === 'schedule' && allScheduled)
          ? 'Todas as revisões de hoje deste filtro estão feitas. As próximas aparecem no dia certo.'
          : (allScheduled
            ? 'Todos os cards deste filtro já estão agendados para os próximos dias. Eles voltam sozinhos na data certa; o Índice mostra quando.'
            : 'Os flashcards atuais são de Clínica Médica. Limpe os filtros para estudar todas as áreas.');
        var emptyAction = allScheduled
          ? '<button type="button" onclick="openTrailModal()" class="h-11 px-4 bg-accent text-accentink border-2 border-accent font-display text-sm font-extrabold hover:bg-ink hover:border-ink transition-colors">Ver índice da trilha</button>'
          : '<button type="button" onclick="resetFlashcardArea()" class="h-11 px-4 bg-accent text-accentink border-2 border-accent font-display text-sm font-extrabold hover:bg-ink hover:border-ink transition-colors">Ver todas as áreas</button>';
        var undoBanner = lastRatedSnapshot
          ? '<div class="pt-1"><button type="button" onclick="undoLastRating()" class="text-btn">Desfazer última avaliação</button></div>'
          : '';
        section.innerHTML = (lastRatingNotice ? '<div class="mb-3 bg-paper2 border border-rule px-3 py-2 text-xs text-ink flex items-center justify-between gap-2"><span>' + escapeText(lastRatingNotice) + '</span><button type="button" onclick="lastRatingNotice=\\'\\'; renderCurrentTab();" class="text-muted hover:text-ink px-1" aria-label="Fechar aviso">✕</button></div>' : '') +
          '<div class="glass-card p-6 space-y-4">' +
          '<h3 class="text-lg text-ink">' + emptyTitle + '</h3>' +
          '<p class="text-sm text-ink2">' + emptyDesc + '</p>' +
          '<div class="flex flex-wrap items-center gap-3">' + emptyAction + undoBanner + '</div>' +
        '</div>';
        return;
      }

      if (currentFlashcardIndex >= filtered.length) currentFlashcardIndex = 0;
      var current = filtered[currentFlashcardIndex];
      var srs = getCardSRS(current.id);
      if (counter) counter.innerText = "Card " + (currentFlashcardIndex + 1) + " de " + filtered.length + " (#" + current.id + ")";

      var now = Date.now();
      var endOfToday = getStartOfDay(1) - 1;
      var bucket = getCardBucket(srs, now, endOfToday);
      var statusBadge = '';
      if (bucket === 'new') {
        statusBadge = '<span class="tag tag--new">Novo</span>';
      } else if (bucket === 'scheduled') {
        var daysWait = Math.max(1, getDaysUntilDue(srs));
        statusBadge = '<span class="tag tag--done">Agendado · volta em ' + daysWait + (daysWait === 1 ? ' dia' : ' dias') + ' (' + formatShortDate(srs.due) + ')</span>';
      } else {
        var revExtra = (srs.lapses > 0 && srs.interval <= 1) ? (' · ' + srs.lapses + (srs.lapses === 1 ? ' erro' : ' erros')) : (' · último: ' + srs.interval + (srs.interval === 1 ? ' dia' : ' dias'));
        statusBadge = '<span class="tag tag--due">Revisão de hoje' + revExtra + '</span>';
      }

      var noticeBanner = lastRatingNotice
        ? '<div class="bg-paper2 border border-rule px-3 py-2 text-xs text-ink flex items-center justify-between gap-2">' +
            '<span>' + escapeText(lastRatingNotice) + '</span>' +
            '<button type="button" onclick="lastRatingNotice=\\'\\'; renderCurrentTab();" class="text-muted hover:text-ink px-1" aria-label="Fechar aviso">✕</button>' +
          '</div>'
        : '';

      var hintData = buildSmartHint(current);
      var hintBox = showHint
        ? '<div onclick="event.stopPropagation()" class="mt-4 border-l-4 border-accent bg-paper2 px-3 py-2 text-left space-y-1 rounded-r-lg">' +
            '<div class="font-display text-xs text-muted">' + escapeText(hintData.topic) + '</div>' +
            '<div class="text-sm text-ink">Pista: ' + escapeText(hintData.clue) + '</div>' +
          '</div>'
        : '';

      var flippedClass = isFlipped ? " is-flipped" : "";

      var html = '<div class="space-y-3">' +
        noticeBanner +
        '<!-- Cartão 3D Interativo -->' +
        '<div class="flashcard-wrapper' + (cardEnterDir ? ' card-enter-' + cardEnterDir : '') + '" onclick="flipFlashcard()">' +
          '<div id="flashcardInner" class="flashcard-inner' + flippedClass + '">' +

            '<!-- FRENTE -->' +
            '<div class="card-face card-front">' +
              '<div class="flex items-center justify-between gap-2 flex-wrap">' +
                '<div class="flex items-center gap-2">' +
                  '<span class="font-display text-xs text-muted">' + getAreaLabel(current.area) + '</span>' +
                  statusBadge +
                '</div>' +
                '<button type="button" onclick="toggleHint(event)" class="h-9 px-3 border-2 border-ink bg-paper3 text-ink hover:bg-paper2 font-display text-xs font-medium transition-colors">' +
                  (showHint ? 'Esconder dica' : 'Quero uma dica') +
                '</button>' +
              '</div>' +
              '<div class="my-auto py-4">' +
                '<p class="text-lg sm:text-xl font-medium text-ink leading-snug">' + escapeText(current.front) + '</p>' +
                hintBox +
              '</div>' +
              '<div class="font-display text-xs text-muted">Toque no card para ver a resposta e o porquê.</div>' +
            '</div>' +

            '<!-- VERSO -->' +
            '<div class="card-face card-back">' +
              '<div class="flex items-center justify-between gap-2 pb-2 border-b border-rule">' +
                '<span class="font-display text-sm font-extrabold text-ink">' + escapeText(current.name || 'Resposta') + '</span>' +
                (current.audioText ?
                  '<button type="button" onclick="event.stopPropagation(); playCurrentFCAudio()" class="h-9 px-3 border-2 border-ink bg-paper3 text-ink hover:bg-ink hover:text-paper font-display text-xs font-medium flex items-center gap-2 transition-colors shrink-0">' +
                    'Ouvir 1.7x' +
                  '</button>' : '') +
              '</div>' +
              '<div class="my-auto py-3 space-y-2">' +
                formatCardBack(current.back) +
                (current.audioText ? '<p class="text-sm text-ink2 italic border-l-4 border-rule pl-3 leading-relaxed">“' + escapeText(current.audioText) + '”</p>' : '') +
              '</div>' +
              '<div class="font-display text-xs text-muted pt-2">Avalie abaixo para marcar a próxima revisão.</div>' +
            '</div>' +

          '</div>' +
        '</div>' +

        '<!-- Virar e navegar -->' +
        '<div class="flex items-stretch gap-2">' +
          '<button type="button" onclick="prevFlashcard(' + filtered.length + ')" class="w-12 h-11 bg-paper3 hover:bg-paper2 text-ink border-2 border-ink transition-colors" aria-label="Card anterior"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i></button>' +
          '<button type="button" onclick="flipFlashcard()" class="flex-1 h-11 bg-paper3 hover:bg-paper2 text-ink font-display text-sm font-medium border-2 border-ink transition-colors flex items-center justify-center gap-2">' +
                        '<span id="flipLabel">' + (isFlipped ? 'Voltar à pergunta' : 'Mostrar resposta') + '</span>' +
          '</button>' +
          '<button type="button" onclick="nextFlashcard(' + filtered.length + ')" class="w-12 h-11 bg-paper3 hover:bg-paper2 text-ink border-2 border-ink transition-colors" aria-label="Próximo card"><i class="fa-solid fa-arrow-right" aria-hidden="true"></i></button>' +
        '</div>' +

        '<!-- Avaliação: quatro células coladas, como um quadro de horários -->' +
        '<div class="grade-row" role="group" aria-label="Como foi">' +
          '<button type="button" onclick="rateCard(' + current.id + ', 0)" class="grade-btn"><span class="grade-name">Errei</span><span class="grade-when">' + previewNextInterval(current.id, 0) + '</span></button>' +
          '<button type="button" onclick="rateCard(' + current.id + ', 1)" class="grade-btn"><span class="grade-name">Difícil</span><span class="grade-when">' + previewNextInterval(current.id, 1) + '</span></button>' +
          '<button type="button" onclick="rateCard(' + current.id + ', 2)" class="grade-btn"><span class="grade-name">Acertei</span><span class="grade-when">' + previewNextInterval(current.id, 2) + '</span></button>' +
          '<button type="button" onclick="rateCard(' + current.id + ', 3)" class="grade-btn"><span class="grade-name">Fácil</span><span class="grade-when">' + previewNextInterval(current.id, 3) + '</span></button>' +
        '</div>' +
        (lastRatedSnapshot ? '<div class="flex justify-end"><button type="button" onclick="undoLastRating()" class="text-btn">Desfazer última avaliação</button></div>' : '') +

        '<!-- Rascunho (recordação ativa) -->' +
        '<div class="space-y-2 pt-3">' +
          '<div class="flex items-center justify-between">' +
            '<label for="fcScratchpad" class="font-display text-xs text-muted">Rascunho: escreva o que lembra antes de virar</label>' +
            '<button type="button" onclick="clearFCDraft(' + current.id + ')" class="font-display text-xs text-ink underline hover:text-accent px-1 py-1">Limpar</button>' +
          '</div>' +
          '<textarea id="fcScratchpad" rows="3" oninput="saveFCDraft(' + current.id + ', this.value)" placeholder="O que você lembra?" class="w-full border-2 border-ink bg-paper3 px-3 py-2 text-base text-ink placeholder:text-muted resize-y leading-relaxed">' + escapeText(fcDraftAnswers[current.id] || '') + '</textarea>' +
        '</div>' +

      '</div>';

      section.innerHTML = html;
      cardEnterDir = '';
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
      var flipLabel = document.getElementById('flipLabel');
      if (flipLabel) flipLabel.innerText = isFlipped ? 'Voltar à pergunta' : 'Mostrar resposta';
      if (isFlipped) revealGradeRow();
    }

    // Deixa os botões de nota visíveis sem a pessoa precisar rolar
    function revealGradeRow() {
      var row = document.querySelector('#flashcardSection .grade-row');
      if (!row) return;
      var player = document.getElementById('bottomAudioPlayer');
      var playerH = (document.body.classList.contains('player-open') && player) ? player.offsetHeight : 0;
      var gap = 12 + playerH;
      var over = row.getBoundingClientRect().bottom + gap - window.innerHeight;
      if (over <= 0) return;
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      try { window.scrollBy({ top: over, behavior: reduce ? 'auto' : 'smooth' }); } catch (e) { window.scrollBy(0, over); }
    }

    function nextFlashcard(total) {
      cardEnterDir = 'next';
      isFlipped = false;
      showHint = false;
      if (currentFlashcardIndex < total - 1) currentFlashcardIndex++;
      else currentFlashcardIndex = 0;
      renderFlashcards();
    }

    function prevFlashcard(total) {
      cardEnterDir = 'prev';
      isFlipped = false;
      showHint = false;
      if (currentFlashcardIndex > 0) currentFlashcardIndex--;
      else currentFlashcardIndex = total - 1;
      renderFlashcards();
    }

    function rateCard(cardId, quality) {
      if (cardLeaving) return;
      ensureTodayStats();
      lastRatedSnapshot = {
        cardId: cardId,
        prevCardSRS: srsData.hasOwnProperty(cardId) ? Object.assign({}, srsData[cardId]) : null,
        prevStats: Object.assign({}, srsStats),
        prevScores: Object.assign({}, flashcardScores),
        prevIndex: currentFlashcardIndex,
        prevPinnedId: trailPinnedId
      };
      delete pendingCloudDeletes[cardId];
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
      lastRatingNotice = formatScheduleNotice(cardId, quality, s);
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
      var wrapper = document.querySelector('#flashcardSection .flashcard-wrapper');
      if (wrapper) {
        cardLeaving = true;
        wrapper.classList.add('card-leave');
        setTimeout(function() {
          cardLeaving = false;
          cardEnterDir = 'next';
          renderFlashcards();
        }, 150);
      } else {
        renderFlashcards();
      }
    }

    function undoLastRating() {
      if (!lastRatedSnapshot || cardLeaving) return;
      var snap = lastRatedSnapshot;
      lastRatedSnapshot = null;
      if (snap.prevCardSRS) {
        snap.prevCardSRS.lastReview = Date.now();
        srsData[snap.cardId] = snap.prevCardSRS;
        delete pendingCloudDeletes[snap.cardId];
      } else {
        delete srsData[snap.cardId];
        pendingCloudDeletes[snap.cardId] = true;
      }
      srsStats = snap.prevStats;
      flashcardScores = snap.prevScores;
      trailPinnedId = snap.prevPinnedId || null;
      isFlipped = false;
      showHint = false;
      saveSRS();
      var q = getStudyQueue();
      currentFlashcardIndex = snap.prevIndex || 0;
      for (var i = 0; i < q.length; i++) {
        if (q[i].id === snap.cardId) { currentFlashcardIndex = i; break; }
      }
      renderFlashcards();
    }

    function resetFlashcardArea() {
      fcSpecialty = 'todas';
      fcSubtopic = 'todos';
      setAreaFilter('todas');
    }

    function markCard(correct, total) {
      var filtered = getStudyQueue();
      var current = filtered[currentFlashcardIndex];
      if (current) rateCard(current.id, correct ? 2 : 0);
    }

    function openTrailModal(source) {
      trailModalSource = (source === 'fgv') ? 'fgv' : 'fc';
      var listEl = document.getElementById('trailModalList');
      if (!listEl) return;
      var base = (trailModalSource === 'fgv' ? getBaseFGVCards() : getBaseFilteredFlashcards()).slice().sort(function(a, b) { return a.id - b.id; });
      var now = Date.now();
      var endOfToday = getStartOfDay(1) - 1;
      var html = '';
      for (var i = 0; i < base.length; i++) {
        var c = base[i];
        var s = getCardSRS(c.id);
        var b = getCardBucket(s, now, endOfToday);
        var badge = '<span class="tag tag--new">Novo</span>';
        if (b === 'due' || b === 'relearn') {
          badge = '<span class="tag tag--due">Revisar hoje</span>';
        } else if (b === 'scheduled') {
          var daysWait = Math.max(1, getDaysUntilDue(s));
          badge = '<span class="tag tag--done">Volta em ' + daysWait + (daysWait === 1 ? 'd' : 'd') + ' (' + formatShortDate(s.due) + ')</span>';
        }
        html += '<button type="button" onclick="jumpToTrailCard(' + i + ')" class="w-full text-left px-2 py-3 hover:bg-paper2 border-b border-rule flex items-center justify-between gap-3 transition-colors">' +
          '<span class="font-display text-xs text-muted w-10 shrink-0">' + c.id + '</span>' +
          '<span class="min-w-0 flex-1">' +
            '<span class="block text-sm font-medium text-ink truncate">' + escapeText(c.name || c.front) + '</span>' +
            '<span class="block font-display text-xs text-muted truncate">' + getAreaLabel(c.area) + (c.cat ? ', ' + getCatLabel(c.cat) : '') + '</span>' +
          '</span>' +
          badge +
        '</button>';
      }
      listEl.innerHTML = html || '<div class="text-center text-muted py-4">Nenhum card neste filtro.</div>';
      openModal('trailModal');
    }

    function jumpToTrailCard(seqIndex) {
      if (trailModalSource === 'fgv') {
        var fgvBase = getBaseFGVCards().slice().sort(function(a, b) { return a.id - b.id; });
        var fgvTarget = fgvBase[seqIndex];
        fgvPinnedId = fgvTarget ? fgvTarget.id : null;
        fgvQueueFilter = 'today';
        var fq = getFGVQueue();
        fgvCardIndex = 0;
        for (var fi = 0; fi < fq.length; fi++) { if (fgvTarget && fq[fi].id === fgvTarget.id) { fgvCardIndex = fi; break; } }
        fgvFlipped = false;
        fgvShowHint = false;
        closeModal('trailModal');
        renderFGV();
        return;
      }
      var trailList = getBaseFilteredFlashcards().slice().sort(function(a, b) { return a.id - b.id; });
      var target = trailList[seqIndex];
      fcStudyMode = 'sequential';
      fcQueueFilter = 'today';
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
        container.innerHTML = '<div class="col-span-full glass-card p-6 space-y-2">' +
          '<h3 class="text-base text-ink">Nenhum tópico nesta área</h3>' +
          '<p class="text-sm text-muted">Troque o filtro acima para ver os tópicos de todas as áreas.</p>' +
        '</div>';
        return;
      }

      var html = '';
      for (var i = 0; i < filtered.length; i++) {
        var item = filtered[i];
        html += '<article class="glass-card">' +
          '<div class="flex items-center justify-between gap-2 px-4 py-2 border-b-2 border-ink">' +
            '<span class="tag">' + getAreaLabel(item.area) + '</span>' +
            '<span class="font-display text-xs text-muted text-right">' + escapeText(item.year || 'Bancas') + '</span>' +
          '</div>' +
          '<div class="p-4 space-y-2">' +
            '<h3 class="text-base text-ink leading-snug">' + escapeText(item.title) + '</h3>' +
            '<div class="font-display text-xs text-muted">Como a banca cobra</div>' +
            '<p class="text-sm text-ink leading-relaxed">' + escapeText(item.tip) + '</p>' +
          '</div>' +
        '</article>';
      }
      container.innerHTML = html;
    }

    // ==========================================
    // RENDER: BANCA FGV (CARDS + TABELAS)
    // ==========================================
    function setFGVSubTab(sub) {
      fgvSubTab = sub;
      fgvFlipped = false;
      fgvShowHint = false;
      renderFGV();
    }

    function getBaseFGVCards() {
      return (appState.fgv_flashcards || []).filter(function(fc) {
        if (activeArea === 'todas') return true;
        if (activeArea === 'clinica') return isClinicalSpecialty(fc.area);
        return fc.area === activeArea;
      });
    }

    function getFGVQueue() {
      var all = getBaseFGVCards();
      var now = Date.now();
      var endOfToday = getStartOfDay(1) - 1;
      var pinnedScheduled = [], readyDue = [], newCards = [], waitingRelearn = [];
      for (var i = 0; i < all.length; i++) {
        var fc = all[i];
        var s = getCardSRS(fc.id);
        var b = getCardBucket(s, now, endOfToday);
        if (fc.id === fgvPinnedId && b === 'scheduled') {
          pinnedScheduled.push(fc);
          continue;
        }
        if (b === 'scheduled') continue;
        if (fgvQueueFilter === 'due' && b === 'new') continue;
        if (fgvQueueFilter === 'new' && b !== 'new') continue;
        if (b === 'new') newCards.push(fc);
        else if (b === 'due') readyDue.push(fc);
        else if (b === 'relearn') waitingRelearn.push(fc);
      }
      readyDue.sort(function(a, b) { return getCardSRS(a.id).due - getCardSRS(b.id).due; });
      waitingRelearn.sort(function(a, b) { return getCardSRS(a.id).due - getCardSRS(b.id).due; });
      return pinnedScheduled.concat(readyDue).concat(newCards).concat(waitingRelearn);
    }

    function flipFGVCard() {
      fgvFlipped = !fgvFlipped;
      var inner = document.getElementById('fgvFlashcardInner');
      if (inner) {
        if (fgvFlipped) inner.classList.add('is-flipped');
        else inner.classList.remove('is-flipped');
      }
      var lbl = document.getElementById('fgvFlipLabel');
      if (lbl) lbl.innerText = fgvFlipped ? 'Voltar à pergunta' : 'Mostrar resposta';
    }

    function toggleFGVHint(e) {
      if (e) e.stopPropagation();
      fgvShowHint = !fgvShowHint;
      renderFGV();
    }

    function nextFGVCard(total) {
      fgvFlipped = false;
      fgvShowHint = false;
      if (total > 0) fgvCardIndex = (fgvCardIndex + 1) % total;
      renderFGV();
    }

    function prevFGVCard(total) {
      fgvFlipped = false;
      fgvShowHint = false;
      if (total > 0) fgvCardIndex = (fgvCardIndex - 1 + total) % total;
      renderFGV();
    }

    function rateFGVCard(cardId, quality) {
      var s = Object.assign({}, getCardSRS(cardId));
      var wasNew = (s.state === 'new');
      var now = Date.now();
      s.lastReview = now;
      if (quality === 0) {
        s.lapses = (s.lapses || 0) + 1;
        s.reps = 0;
        s.interval = 0;
        s.ease = Math.max(1.3, (s.ease || 2.5) - 0.2);
        s.due = now + 5 * 60 * 1000;
        s.state = 'learning';
      } else if (quality === 1) {
        s.reps = Math.max(1, s.reps || 0);
        s.interval = computeNextIntervalDays(s, 1);
        s.ease = Math.max(1.3, (s.ease || 2.5) - 0.15);
        s.due = getStartOfDay(s.interval);
        s.state = 'learning';
      } else if (quality === 2) {
        s.interval = computeNextIntervalDays(s, 2);
        s.reps = (s.reps || 0) + 1;
        s.due = getStartOfDay(s.interval);
        s.state = (s.interval >= 6) ? 'mastered' : 'review';
      } else if (quality === 3) {
        s.interval = computeNextIntervalDays(s, 3);
        s.reps = (s.reps || 0) + 2;
        s.ease = Math.min(3.0, (s.ease || 2.5) + 0.1);
        s.due = getStartOfDay(s.interval);
        s.state = (s.interval >= 6) ? 'mastered' : 'review';
      }
      if (wasNew) srsStats.newToday = (srsStats.newToday || 0) + 1;
      srsData[cardId] = s;
      srsStats.reviewedToday = (srsStats.reviewedToday || 0) + 1;
      lastRatingNotice = formatScheduleNotice(cardId, quality, s);
      saveSRS();
      fgvFlipped = false;
      fgvShowHint = false;
      if (fgvPinnedId === cardId) fgvPinnedId = null;
      delete fcDraftAnswers[cardId];
      var q = getFGVQueue();
      if (fgvCardIndex >= q.length) fgvCardIndex = 0;
      if (q.length > 1 && q[fgvCardIndex] && q[fgvCardIndex].id === cardId) {
        fgvCardIndex = (fgvCardIndex + 1) % q.length;
      }
      renderFGV();
    }

    function playFGVCardAudio() {
      var q = getFGVQueue();
      if (fgvCardIndex >= q.length) return;
      var cur = q[fgvCardIndex];
      if (cur && cur.audioText) playItemAudio(cur.name || 'Card FGV', cur.audioText);
    }

    function playFGVTableAudio(id) {
      var list = appState.fgv_tables || [];
      var item = list.find(function(t) { return t.id === id; });
      if (item && item.audioText) playItemAudio(item.name || 'Tabela FGV', item.audioText);
    }

    function renderFGV() {
      var container = document.getElementById('fgvContent');
      var btnCards = document.getElementById('fgvSubBtn-cards');
      var btnTables = document.getElementById('fgvSubBtn-tables');
      if (!container) return;

      var allCards = appState.fgv_flashcards || [];
      var allTables = appState.fgv_tables || [];
      if (btnCards) {
        btnCards.innerText = 'Cards FGV (' + allCards.length + ')';
        btnCards.className = 'filter-pill ' + (fgvSubTab === 'cards' ? 'active' : 'inactive');
      }
      if (btnTables) {
        btnTables.innerText = 'Tabelas FGV (' + allTables.length + ')';
        btnTables.className = 'filter-pill ' + (fgvSubTab === 'tables' ? 'active' : 'inactive');
      }

      if (fgvSubTab === 'tables') {
        var filteredTables = allTables.filter(function(item) {
          return activeArea === 'todas' || item.area === activeArea;
        });
        if (filteredTables.length === 0) {
          container.innerHTML = '<div class="glass-card p-6 space-y-2">' +
            '<h3 class="text-base text-ink">Nenhuma tabela da FGV ainda</h3>' +
            '<p class="text-sm text-muted">Envie as questões prévias da FGV no chat para preencher esta seção com tabelas e fluxogramas da banca.</p>' +
          '</div>';
          return;
        }
        var tHtml = '';
        for (var i = 0; i < filteredTables.length; i++) {
          var item = filteredTables[i];
          var audioBtn = item.audioText
            ? '<button type="button" onclick="playFGVTableAudio(' + item.id + ')" class="h-9 px-3 border-2 border-ink bg-paper3 text-ink hover:bg-ink hover:text-paper text-xs font-medium flex items-center gap-2 transition-colors shrink-0"><span>Ouvir 1.7x</span></button>'
            : '';
          tHtml += '<article class="glass-card">' +
            '<div class="flex items-start justify-between gap-3 p-4 border-b-2 border-ink">' +
              '<div class="min-w-0 space-y-1">' +
                '<div class="flex items-center gap-2 flex-wrap">' +
                  '<span class="tag">' + getAreaLabel(item.area) + '</span>' +
                  (item.cat ? '<span class="font-display text-xs text-muted">' + getCatLabel(item.cat) + '</span>' : '') +
                  (item.year ? '<span class="tag tag--new">' + escapeText(item.year) + '</span>' : '') +
                '</div>' +
                '<h3 class="text-base text-ink leading-snug">' + escapeText(item.name) + '</h3>' +
              '</div>' +
              audioBtn +
            '</div>' +
            '<div class="grid grid-cols-1 md:grid-cols-2 text-sm">' +
              '<div class="p-4 md:border-r border-rule">' +
                '<div class="font-display text-xs text-muted mb-2">' + escapeText(item.col1Title || 'Como a FGV cobra') + '</div>' +
                '<p class="text-ink leading-relaxed whitespace-pre-line">' + tidyBullets(item.col1) + '</p>' +
              '</div>' +
              '<div class="p-4 border-t md:border-t-0 border-rule">' +
                '<div class="font-display text-xs text-muted mb-2">' + escapeText(item.col2Title || 'Diagnóstico e conduta') + '</div>' +
                '<p class="text-ink leading-relaxed whitespace-pre-line">' + tidyBullets(item.col2) + '</p>' +
              '</div>' +
            '</div>' +
          '</article>';
        }
        container.innerHTML = tHtml;
        return;
      }

      // Sub-aba: Cards FGV
      var baseFgv = getBaseFGVCards();
      var fgvCounts = getSRSCounts(baseFgv);
      var fgvDue = fgvCounts.due + fgvCounts.relearn;
      var fgvNew = fgvCounts.newCount;
      var fgvSched = fgvCounts.scheduled;
      function fgvPill(filterId, label, num) {
        var isAct = (fgvQueueFilter === filterId);
        return '<button type="button" onclick="setFGVQueueFilter(\\'' + filterId + '\\')" class="filter-pill ' + (isAct ? 'active' : 'inactive') + '">' + label + ' (' + num + ')</button>';
      }
      var fgvSummaryHtml =
        '<div class="summary">' +
          '<div class="flex flex-wrap items-center justify-between gap-3 px-4 py-3">' +
            '<div class="text-sm text-ink2">' +
              'Para revisar hoje: <b class="text-ink">' + fgvDue + '</b> · Novos: <b class="text-ink">' + fgvNew + '</b> · Em dia: <b class="text-ink">' + fgvSched + '</b>' +
            '</div>' +
            '<button type="button" onclick="openTrailModal(\\'fgv\\')" class="text-btn">Ver agenda (' + baseFgv.length + ')</button>' +
          '</div>' +
          '<div class="px-4 pb-3 flex flex-wrap items-center gap-2 border-t border-rule pt-2.5">' +
            '<span class="font-display text-xs text-muted mr-1">Mostrar agora:</span>' +
            fgvPill('today', 'Hoje (Revisões + Novos)', fgvDue + fgvNew) +
            fgvPill('due', 'Só Revisões do Dia', fgvDue) +
            fgvPill('new', 'Só Novos', fgvNew) +
          '</div>' +
        '</div>';

      var q = getFGVQueue();
      if (allCards.length === 0) {
        container.innerHTML = '<div class="glass-card p-6 space-y-2">' +
          '<h3 class="text-base text-ink">Nenhum flashcard da FGV ainda</h3>' +
          '<p class="text-sm text-muted">Envie as questões de provas anteriores da FGV no chat para montar seu baralho direcionado aqui.</p>' +
        '</div>';
        return;
      }
      if (q.length === 0) {
        container.innerHTML = fgvSummaryHtml +
          (lastRatingNotice ? '<div class="bg-paper2 border border-rule px-3 py-2 text-xs text-ink flex items-center justify-between gap-2"><span>' + escapeText(lastRatingNotice) + '</span><button type="button" onclick="lastRatingNotice=\\'\\'; renderCurrentTab();" class="text-muted hover:text-ink px-1" aria-label="Fechar aviso">✕</button></div>' : '') +
          '<div class="glass-card p-6 space-y-3">' +
          '<h3 class="text-base text-ink">' + (fgvQueueFilter === 'due' ? 'Nenhuma revisão pendente hoje na FGV' : (fgvQueueFilter === 'new' ? 'Nenhum card novo pendente na FGV' : 'Tudo em dia na FGV')) + '</h3>' +
          '<p class="text-sm text-ink2">Os cards já avaliados deste filtro estão agendados para os próximos dias e não reaparecem antes da data certa. Você pode conferir quando cada um volta na agenda.</p>' +
          '<button type="button" onclick="openTrailModal(\\'fgv\\')" class="h-10 px-4 bg-accent text-accentink border-2 border-accent font-display text-xs font-extrabold hover:bg-ink hover:border-ink transition-colors">Ver agenda da FGV</button>' +
        '</div>';
        return;
      }

      if (fgvCardIndex >= q.length) fgvCardIndex = 0;
      var current = q[fgvCardIndex];
      var srs = getCardSRS(current.id);
      var now = Date.now();
      var endOfToday = getStartOfDay(1) - 1;
      var bucket = getCardBucket(srs, now, endOfToday);
      var statusBadge = '';
      if (bucket === 'new') {
        statusBadge = '<span class="tag tag--new">Novo</span>';
      } else if (bucket === 'scheduled') {
        var daysWait = Math.max(1, getDaysUntilDue(srs));
        statusBadge = '<span class="tag tag--done">Agendado · volta em ' + daysWait + (daysWait === 1 ? ' dia' : ' dias') + ' (' + formatShortDate(srs.due) + ')</span>';
      } else {
        var revExtra = (srs.lapses > 0 && srs.interval <= 1) ? (' · ' + srs.lapses + (srs.lapses === 1 ? ' erro' : ' erros')) : (' · último: ' + srs.interval + (srs.interval === 1 ? ' dia' : ' dias'));
        statusBadge = '<span class="tag tag--due">Revisão de hoje' + revExtra + '</span>';
      }

      var noticeBanner = lastRatingNotice
        ? '<div class="bg-paper2 border border-rule px-3 py-2 text-xs text-ink flex items-center justify-between gap-2">' +
            '<span>' + escapeText(lastRatingNotice) + '</span>' +
            '<button type="button" onclick="lastRatingNotice=\\'\\'; renderCurrentTab();" class="text-muted hover:text-ink px-1" aria-label="Fechar aviso">✕</button>' +
          '</div>'
        : '';

      var hintData = buildSmartHint(current);
      var hintBox = fgvShowHint
        ? '<div onclick="event.stopPropagation()" class="mt-4 border-l-4 border-accent bg-paper2 px-3 py-2 text-left space-y-1 rounded-r-lg">' +
            '<div class="font-display text-xs text-muted">' + escapeText(hintData.topic) + '</div>' +
            '<div class="text-sm text-ink">Pista: ' + escapeText(hintData.clue) + '</div>' +
          '</div>'
        : '';

      var html = fgvSummaryHtml + '<div class="space-y-3">' +
        noticeBanner +
        '<div class="flex items-center justify-between text-xs font-display text-muted">' +
          '<span>Card ' + (fgvCardIndex + 1) + ' de ' + q.length + ' (#' + current.id + ')</span>' +
          (current.year ? '<span class="tag">' + escapeText(current.year) + '</span>' : '') +
        '</div>' +
        '<div class="flashcard-wrapper" onclick="flipFGVCard()">' +
          '<div id="fgvFlashcardInner" class="flashcard-inner' + (fgvFlipped ? ' is-flipped' : '') + '">' +
            '<div class="card-face card-front">' +
              '<div class="flex items-center justify-between gap-2 flex-wrap">' +
                '<div class="flex items-center gap-2">' +
                  '<span class="font-display text-xs text-muted">' + getAreaLabel(current.area) + '</span>' +
                  statusBadge +
                '</div>' +
                '<button type="button" onclick="toggleFGVHint(event)" class="h-9 px-3 border-2 border-ink bg-paper3 text-ink hover:bg-paper2 font-display text-xs font-medium transition-colors">' +
                  (fgvShowHint ? 'Esconder dica' : 'Quero uma dica') +
                '</button>' +
              '</div>' +
              '<div class="my-auto py-4">' +
                '<p class="text-lg sm:text-xl font-medium text-ink leading-snug">' + escapeText(current.front) + '</p>' +
                hintBox +
              '</div>' +
              '<div class="font-display text-xs text-muted">Toque no card para ver a resposta e o porquê.</div>' +
            '</div>' +
            '<div class="card-face card-back">' +
              '<div class="flex items-center justify-between gap-2 pb-2 border-b border-rule">' +
                '<span class="font-display text-sm font-extrabold text-ink">' + escapeText(current.name || 'Resposta') + '</span>' +
                (current.audioText ? '<button type="button" onclick="event.stopPropagation(); playFGVCardAudio()" class="h-9 px-3 border-2 border-ink bg-paper3 text-ink hover:bg-ink hover:text-paper font-display text-xs font-medium flex items-center gap-2 transition-colors shrink-0">Ouvir 1.7x</button>' : '') +
              '</div>' +
              '<div class="my-auto py-3 space-y-2">' +
                formatCardBack(current.back) +
                (current.audioText ? '<p class="text-sm text-ink2 italic border-l-4 border-rule pl-3 leading-relaxed">“' + escapeText(current.audioText) + '”</p>' : '') +
              '</div>' +
              '<div class="font-display text-xs text-muted pt-2">Avalie abaixo para marcar a próxima revisão.</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="glass-card p-3 space-y-1.5">' +
          '<div class="flex items-center justify-between">' +
            '<label for="fcScratchpad" class="font-display text-xs font-bold text-ink">Meu Rascunho <span class="font-normal text-muted">(para raciocinar e conferir depois)</span></label>' +
            '<button type="button" onclick="clearFCDraft(' + current.id + ')" class="font-display text-xs text-muted hover:text-ink px-2 py-0.5">Limpar</button>' +
          '</div>' +
          '<textarea id="fcScratchpad" rows="2" oninput="saveFCDraft(' + current.id + ', this.value)" placeholder="Escreva aqui o que você lembra antes de virar o card..." class="w-full rounded-lg border border-rule bg-paper2 px-3 py-2 text-sm text-ink placeholder:text-muted focus:outline-none focus:border-ink focus:bg-paper3 resize-y leading-relaxed">' + escapeText(fcDraftAnswers[current.id] || '') + '</textarea>' +
        '</div>' +
        '<div class="flex items-stretch gap-2">' +
          '<button type="button" onclick="prevFGVCard(' + q.length + ')" class="w-12 h-11 bg-paper3 hover:bg-paper2 text-ink border-2 border-ink transition-colors" aria-label="Card anterior"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i></button>' +
          '<button type="button" onclick="flipFGVCard()" class="flex-1 h-11 bg-paper3 hover:bg-paper2 text-ink font-display text-sm font-medium border-2 border-ink transition-colors flex items-center justify-center gap-2">' +
            '<span id="fgvFlipLabel">' + (fgvFlipped ? 'Voltar à pergunta' : 'Mostrar resposta') + '</span>' +
          '</button>' +
          '<button type="button" onclick="nextFGVCard(' + q.length + ')" class="w-12 h-11 bg-paper3 hover:bg-paper2 text-ink border-2 border-ink transition-colors" aria-label="Próximo card"><i class="fa-solid fa-arrow-right" aria-hidden="true"></i></button>' +
        '</div>' +
        '<div class="grade-row" role="group" aria-label="Como foi">' +
          '<button type="button" onclick="rateFGVCard(' + current.id + ', 0)" class="grade-btn"><span class="grade-name">Errei</span><span class="grade-when">' + previewNextInterval(current.id, 0) + '</span></button>' +
          '<button type="button" onclick="rateFGVCard(' + current.id + ', 1)" class="grade-btn"><span class="grade-name">Difícil</span><span class="grade-when">' + previewNextInterval(current.id, 1) + '</span></button>' +
          '<button type="button" onclick="rateFGVCard(' + current.id + ', 2)" class="grade-btn"><span class="grade-name">Acertei</span><span class="grade-when">' + previewNextInterval(current.id, 2) + '</span></button>' +
          '<button type="button" onclick="rateFGVCard(' + current.id + ', 3)" class="grade-btn"><span class="grade-name">Fácil</span><span class="grade-when">' + previewNextInterval(current.id, 3) + '</span></button>' +
        '</div>' +
      '</div>';
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
      document.body.classList.add('player-open');
    }

    function closeAudioPlayer() {
      stopAudioPlayback();
      var player = document.getElementById('bottomAudioPlayer');
      if (player) player.classList.add('translate-y-full');
      document.body.classList.remove('player-open');
    }

    function toggleAudio() {
      if (isPlaying) pauseAudioPlayback();
      else startAudioPlayback();
    }

    function startAudioPlayback() {
      if (!('speechSynthesis' in window)) return;
      try {
        speechToken++;
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
        speechToken++;
        isPlaying = false;
        window.speechSynthesis.cancel();
        updateAudioUI(false);
      } catch(e) {}
    }

    function stopAudioPlayback() {
      if (!('speechSynthesis' in window)) return;
      try {
        speechToken++;
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
      var myToken = speechToken;
      try {
        speechUtterance = new SpeechSynthesisUtterance(chunk);
        speechUtterance.rate = currentSpeed;
        speechUtterance.lang = 'pt-BR';
        if (selectedVoice) speechUtterance.voice = selectedVoice;

        speechUtterance.onend = function() {
          if (myToken !== speechToken || !isPlaying) return;
          if (currentChunkIndex < speechChunks.length - 1) {
            currentChunkIndex++;
            speakChunk(currentChunkIndex);
          } else {
            stopAudioPlayback();
          }
        };

        speechUtterance.onerror = function(ev) {
          if (myToken !== speechToken) return;
          if (ev && (ev.error === 'canceled' || ev.error === 'interrupted')) return;
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
      if (isPlaying) {
        speechToken++;
        try { window.speechSynthesis.cancel(); } catch(e) {}
        speakChunk(currentChunkIndex);
      } else {
        updateScriptHighlight();
      }
    }

    function cycleSpeed() {
      var speeds = [1.0, 1.3, 1.5, 1.7, 2.0];
      var idx = speeds.indexOf(currentSpeed);
      idx = (idx + 1) % speeds.length;
      currentSpeed = speeds[idx];
      var badge = document.getElementById('speedBadge');
      if (badge) badge.innerText = currentSpeed + "x";
      if (isPlaying) {
        speechToken++;
        try { window.speechSynthesis.cancel(); } catch(e) {}
        speakChunk(currentChunkIndex);
      } else {
        updateScriptHighlight();
      }
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
        var cls = isCurrent ? 'bg-paper2 text-ink font-bold border-l-4 border-ink pl-3' : 'bg-paper3 text-ink hover:bg-paper2';
        html += '<div onclick="jumpToChunk(' + i + ')" class="p-2.5 border border-rule cursor-pointer transition-colors ' + cls + '">' +
          '<span class="font-display text-muted mr-1.5 text-xs">' + (i + 1) + '.</span>' +
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
        clearTimeout(el._closeTimer);
        el.style.display = 'flex';
        el.classList.add('active');
        el.classList.remove('hidden');
        el.offsetWidth; // aplica o estado inicial antes de animar
        el.classList.add('is-open');
      }
    }

    function closeModal(id) {
      var el = document.getElementById(id);
      if (el) {
        el.classList.remove('is-open');
        clearTimeout(el._closeTimer);
        el._closeTimer = setTimeout(function() {
          el.style.display = 'none';
          el.classList.remove('active');
          el.classList.add('hidden');
        }, 260);
      }
    }

    document.addEventListener('click', function(ev) {
      if (ev.target && ev.target.classList && ev.target.classList.contains('modal-overlay') && ev.target.id) {
        closeModal(ev.target.id);
      }
    });
    document.addEventListener('keydown', function(ev) {
      if (ev.key === 'Escape') {
        var openModals = document.querySelectorAll('.modal-overlay.active');
        for (var i = 0; i < openModals.length; i++) {
          if (openModals[i].id) closeModal(openModals[i].id);
        }
      }
    });

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
          if (t === type) btn.className = "py-1.5 px-3 border-b-2 border-ink text-ink2 font-bold";
          else btn.className = "py-1.5 px-3 text-muted hover:text-ink";
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
      alert("Item adicionado.");
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
            alert("Backup e cronograma SRS restaurados com sucesso!");
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
        'cardiologia': 'Cardiologia',
        'pneumologia': 'Pneumologia',
        'gastroenterologia': 'Gastroenterologia',
        'endocrinologia': 'Endocrinologia',
        'reumatologia': 'Reumatologia',
        'hematologia': 'Hematologia',
        'nefrologia': 'Nefrologia',
        'neurologia': 'Neurologia',
        'psiquiatria': 'Psiquiatria',
        'infectologia': 'Infectologia',
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
        'diarreia': 'Diarreia Aguda',
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
        'hemostasia': 'Plaquetas & Coagulação',
        'nefrolitiase': 'Nefrolitíase',
        'ira_dialise': 'IRA & Diálise',
        'wernicke': 'Wernicke & Carências',
        'cefaleias': 'Cefaleias',
        'demencias': 'Demências & HPN',
        'shu': 'SHU & Diarreia',
        'anafilaxia': 'Anafilaxia & Alergia',
        'intussuscepcao': 'Intussuscepção',
        'diverticulite': 'Diverticulite',
        'apendicite': 'Apendicite',
        'dheg': 'Pré-eclâmpsia & DHEG',
        'trauma': 'Trauma / ATLS',
        'suicidio': 'Risco de Suicídio',
        'ists': 'ISTs & Uretrites',
        'meningite': 'Meningite',
        'sepse': 'Sepse & UTI',
        'vacinas': 'Vacinas & Preventiva',
        'itu': 'ITU & Pielonefrite'
      };
      return map[cat] || cat || 'Geral';
    }

    function escapeText(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\\$/g, '');
    }

    // GARANTE QUE AS FUNÇÕES ESTEJAM NO ESCOPO GLOBAL DO WINDOW
    window.switchTab = switchTab;
    window.setFGVSubTab = setFGVSubTab;
    window.flipFGVCard = flipFGVCard;
    window.toggleFGVHint = toggleFGVHint;
    window.nextFGVCard = nextFGVCard;
    window.prevFGVCard = prevFGVCard;
    window.rateFGVCard = rateFGVCard;
    window.playFGVCardAudio = playFGVCardAudio;
    window.playFGVTableAudio = playFGVTableAudio;
    window.setAreaFilter = setAreaFilter;
    window.setCategoryFilter = setCategoryFilter;
    window.setFCStudyMode = setFCStudyMode;
    window.setFCQueueFilter = setFCQueueFilter;
    window.setFGVQueueFilter = setFGVQueueFilter;
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
    window.toggleProgress = toggleProgress;
    window.toggleFilters = toggleFilters;
    window.hideSplash = hideSplash;
    window.undoLastRating = undoLastRating;
    window.resetFlashcardArea = resetFlashcardArea;
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html with {len(html_content)} characters!")
