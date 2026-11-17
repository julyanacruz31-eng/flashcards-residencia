# Plataforma de Estudos — Residência Médica (Flashcards & Resumos)

Aplicação web estática (`index.html`) com **189 flashcards** e **tabelas/resumos de alta incidência** para revisão ativa na reta final da Residência Médica.

## Principais Recursos

- **Repetição Espaçada (SRS) com Prazo de Prova**:
  - Cronograma automático ajustado para a contagem regressiva até a prova (padrão 37 dias, ajustável na interface).
  - 4 níveis de avaliação (`Errei 5 min`, `Difícil`, `Acertei`, `Fácil`) com avanço imediato para o próximo card e retorno programado.
  - Previsão de revisões para os próximos 7 dias.
- **Modos de Estudo**:
  - 📅 **Cronograma (Hoje)**: cards vencidos prontos primeiro → novos → erros recentes aguardando intervalo.
  - 🎲 **Misturado (Intercalado)**: alterna especialidades (`Cardio`, `Pneumo`, `Gastro`, `Endocrino`, `Reumato`, `Hemato`) para evitar fadiga de tema único.
  - 📖 **Sequencial (1→N)**: trilha completa em ordem numérica.
  - 🔥 **Pontos Fracos**: foco nos cards com erros/lapses.
- **✍️ Meu Rascunho (Active Recall)**:
  - Campo de texto livre abaixo do card para escrever a resposta e raciocinar antes de virar.
  - O texto permanece visível ao virar o card para conferência lado a lado e é limpo automaticamente ao avaliar o card.
- **Recursos Extras**:
  - 💡 Dica inteligente por card, 🗺️ Índice/Trilha completa, 🧠 Técnicas de Estudo e player de áudio integrado (`1.7x`).

---

## Arquivos Principais

| Arquivo | Função |
| :--- | :--- |
| `app_data_clean.json` | **Base de dados** com todas as tabelas e os 189 flashcards. |
| `build_perfect_app.py` | **Gerador** que lê `app_data_clean.json` e gera o `index.html` completo. |
| `index.html` | **Site final** (auto-contido, pronto para abrir localmente ou hospedar). |
| `deploy_ship.py` | Script auxiliar para publicar `index.html` no `ship.page`. |

---

## Como Editar e Atualizar (Importante para Múltiplos PCs/Agentes)

> ⚠️ **Regra de ouro:** **Não edite o `index.html` diretamente.** Ele é gerado automaticamente pelo `build_perfect_app.py`. Qualquer alteração manual no `index.html` será sobrescrita na próxima compilação.

1. **Puxe as alterações mais recentes** antes de começar:
   ```bash
   git pull origin main
   ```
2. **Edite a fonte**:
   - Para adicionar/corrigir cards ou tabelas: edite `app_data_clean.json`.
   - Para alterar interface, SRS ou funcionalidades: edite `build_perfect_app.py`.
3. **Regere o `index.html`**:
   ```bash
   python -W all build_perfect_app.py
   ```
   *(Verifique se não há `SyntaxWarning` — lembre que `build_perfect_app.py` usa string Python `"""..."""`, então regexes JS devem usar barra dupla como `\\s`, `\\r`, `\\n`.)*
4. **Publique / envie para o repositório**:
   ```bash
   git add app_data_clean.json build_perfect_app.py index.html README.md
   git commit -m "Descreva a alteração"
   git push origin main
   ```
   *(Ou rode `python deploy_ship.py` para gerar um link temporário no `ship.place`.)*
