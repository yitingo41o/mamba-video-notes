# AGENTS.md

本專案的完整規則寫在 **[CLAUDE.md](./CLAUDE.md)**。
不論你是 Claude、Codex、Cursor 或其他 coding agent，開始任何修改之前請先完整閱讀 `CLAUDE.md` 並遵守其中規則。

最重要的五條（細節見 CLAUDE.md）：

1. 純靜態網站：HTML + CSS + 原生 JS，不使用框架、npm 或 build 步驟。
2. 新增論文 = 複製 `papers/_template.html` → `papers/<年份>-<短名>.html`，並在 `papers.json` 新增一筆。
3. 每篇筆記固定 9 個段落（info / tldr / problem / method / results / pros-cons / relevance / questions / related）。
4. 標籤只能用 CLAUDE.md 第 6 節的清單。
5. 不可捏造數字或出處；不確定的加 `<span class="todo">待確認</span>`。
