# Guia: como escrever flashcards que saem bonitos

Os cards ficam em `app_data_clean.json`, na lista `flashcards`. O app desenha o card sozinho a partir do texto, então o que importa é **como o texto é escrito**.

> Caminho mais fácil: cole a anotação, o resumo ou a questão no chat do agente (Claude, Gemini) e peça "transforma em flashcards seguindo o GUIA_FLASHCARDS.md".

---

## 1. Campos de cada card

```json
{
  "id": 191,
  "area": "cardiologia",
  "cat": "scas",
  "name": "IAM de VD - Pegadinhas de Conduta",
  "front": "Paciente com IAM inferior e supra em V4R, hipotenso com pulmões limpos. Quais medicações são PROIBIDAS e qual a conduta imediata?",
  "back": "🚫 PROIBIDOS no infarto de VD:\n• Nitratos, morfina, diuréticos e betabloqueadores.\n\n✅ CONDUTA IMEDIATA:\n• Expansão volêmica com SF 0,9% em bolus.\n\n💡 Por quê? O VD está 'mole': o volume enche o ventrículo e aumenta o débito por Frank-Starling.",
  "audioText": "No infarto de ventrículo direito são proibidos nitratos, morfina, diuréticos e betabloqueadores. A conduta é expansão volêmica com soro fisiológico."
}
```

| Campo | O que é | Dica |
| --- | --- | --- |
| `id` | Número único | Use o próximo número livre (veja o maior `id` atual) |
| `area` | Especialidade | Só os valores da seção 3 |
| `cat` | Tema dentro da especialidade | Só os valores da seção 3 |
| `name` | Título no verso e no Índice | Curto: 3 a 8 palavras |
| `front` | A pergunta | Uma pergunta só, de preferência em forma de caso clínico |
| `back` | A resposta | Uma ideia por linha (seção 2) |
| `audioText` | Texto lido em voz a 1.7x | Frases corridas, sem emojis, siglas por extenso quando possível |

---

## 2. Como o verso é desenhado

O app lê o `back` linha por linha (as linhas são separadas por `\n`):

| A linha começa com | Vira |
| --- | --- |
| `💡` ou `🔗` | Caixa de destaque com faixa terracota (bom para o "porquê") |
| `⚠️` | Caixa âmbar de alerta (pegadinha, contraindicação) |
| `•`, `-` ou `1.` | Item de lista, texto normal |
| qualquer outra coisa | Subtítulo em negrito (ex.: `✅ CONDUTA IMEDIATA:`) |

Para ficar bonito:

- **Uma ideia por linha.** Linha vazia (`\n\n`) entre blocos.
- **Um subtítulo e 2 a 4 itens por bloco.** Mais que isso vira parede de texto.
- **No máximo um `💡` e um `⚠️` por card.** Se tudo é destaque, nada é.
- **Verso curto:** até uns 80 a 120 palavras. Se passar disso, divida em dois cards.
- **Pegadinha de prova** vai no `⚠️`; **fisiopatologia** vai no `💡`.

Nas **tabelas** (lista `tables`, campos `col1` e `col2`), `• •` no começo de um item marca um subitem e aparece como `◦`.

---

## 3. Especialidades e temas aceitos

Use exatamente estes valores, senão o card não aparece nos filtros.

| `area` | `cat` possíveis |
| --- | --- |
| `cardiologia` | `scas`, `aorta`, `ic`, `valvopatias`, `arritmias`, `pericardio`, `semiologia` |
| `pneumologia` | `tep`, `obstrutivas`, `pleura`, `infeccoes`, `oncologia`, `terapia_intensiva` |
| `gastroenterologia` | `cirrose_ascite`, `pbe`, `hda`, `hepatites`, `pancreatite`, `dii` |
| `endocrinologia` | `emergencias_dm`, `tireoide`, `adrenal`, `metabolismo` |
| `reumatologia` | `ar`, `les`, `colagenoses`, `espondilo`, `vasculites`, `cristais` |
| `hematologia` | `anemias`, `onco_hemato`, `mieloma`, `hemostasia` |

### Especialidade ou tema novo

Dá para incluir (ex.: Nefrologia, Infectologia), mas é preciso cadastrar em `build_perfect_app.py`:

1. `getAreaLabel`: o nome que aparece na tela (ex.: `'nefrologia': 'Nefrologia'`).
2. `getCatLabel`: o nome de cada tema novo (ex.: `'glomerulopatias': 'Glomerulopatias'`).
3. A lista `specs` em `renderFCControls`: o botão do filtro (ex.: `{ id: 'nefrologia', label: 'Nefro' }`).
4. Se for de Clínica Médica, a lista de áreas de `activeArea === 'clinica'` em `getBaseFilteredFlashcards`.

---

## 4. Depois de editar

```bash
git pull origin main
python -W all build_perfect_app.py
git add app_data_clean.json build_perfect_app.py index.html
git commit -m "Adiciona cards de ..."
git push origin main
```

Confira que o build não mostrou nenhum `SyntaxWarning`. O site (GitHub Pages) atualiza sozinho em cerca de 1 minuto, e o progresso salvo na nuvem não é afetado.

**Não mude o `id` de um card que já existe:** o progresso de estudo é guardado pelo `id`. Para corrigir um card, edite o texto e mantenha o número.
