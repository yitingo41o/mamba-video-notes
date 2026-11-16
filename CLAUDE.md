# CLAUDE.md — Mamba × 影片動作辨識 論文筆記站

> 這份文件是給 AI（Claude、Codex、Cursor 等）與未來的我看的「專案說明書」。
> 任何新增、修改內容之前，請先完整讀完本文件，並嚴格遵守。
> `AGENTS.md` 只是指向本文件的捷徑，規則以本文件為準。

---

## 1. 專案目的

這是我（研究生）的**研究用論文筆記網站**，主題是：

- **State Space Model（SSM）/ Mamba 系列架構**
- 將 Mamba 應用到**影片理解，特別是動作辨識（action recognition）**
- 延伸方向：**雙人互動辨識（two-person interaction recognition）**

網站要做到三件事：

1. **每讀一篇論文就新增一頁筆記**，格式固定，方便日後比較、回顧與寫論文的 related work。
2. 首頁可以依**標籤、閱讀狀態、關鍵字**篩選所有論文，也列出「待讀清單」。
3. 有一個**名詞表（glossary）**，統一整理反覆出現的術語。

讀者：我自己、指導教授、實驗室同學。語氣是「清楚的讀書筆記」，不是宣傳文。

---

## 2. 技術規則（不可違反）

| 規則 | 說明 |
|---|---|
| 純靜態網站 | 只用 HTML + CSS + 原生 JavaScript。**不使用** React/Vue、npm、打包工具或任何 build 步驟。 |
| 部署 | GitHub Pages，`main` 分支根目錄直接發布。推上去就是上線版本。 |
| 外部資源 | 只允許 Google Fonts（已在頁面中引入）。不要新增其他 CDN。 |
| 資料驅動 | 首頁列表由 `papers.json` 產生，名詞表由 `glossary.json` 產生。**不要把論文卡片手寫在 `index.html` 裡。** |
| 樣式 | 只能使用 `assets/style.css` 中已定義的 class（見第 8 節）。需要新樣式時，先加到 `style.css` 並更新第 8 節，**不要寫 inline style**。 |
| 路徑 | 一律使用相對路徑（GitHub Pages 的網址有子路徑 `/<repo-name>/`，絕對路徑 `/assets/...` 會壞掉）。 |

本地預覽（`fetch` 在 `file://` 下無法讀 JSON，所以一定要開 server）：

```bash
python3 -m http.server 8000
# 打開 http://localhost:8000
```

---

## 3. 目錄結構

```
mamba-video-notes/
├── CLAUDE.md              ← 本文件：專案規則（最重要）
├── AGENTS.md              ← 指向 CLAUDE.md
├── README.md              ← 給 GitHub 訪客看的簡介
├── index.html             ← 首頁：論文列表 + 篩選 + 待讀清單
├── glossary.html          ← 名詞表頁
├── papers.json            ← 所有論文的索引資料（首頁從這裡讀）
├── glossary.json          ← 所有名詞的資料（名詞表從這裡讀）
├── assets/
│   ├── style.css          ← 全站唯一的樣式表
│   └── main.js            ← 首頁與名詞表的渲染、篩選邏輯
├── scripts/
│   └── check.py           ← 規則自動檢查（只在本地執行，不是網站的一部分）
└── papers/
    ├── _template.html     ← 新增筆記時「複製」這個檔案，不要直接改它
    ├── 2023-mamba.html
    ├── 2024-vision-mamba.html
    └── 2024-videomamba.html
```

**不要**新增其他頂層資料夾或頁面，除非我明確要求；若要求了，請一併更新本節。

---

## 4. 檔案命名規則

論文筆記檔：`papers/<年份>-<短名>.html`

- `<年份>`：**arXiv 第一版的提交年份**（不是會議年份）。例：VideoMamba 2024 年 3 月上 arXiv、ECCV 2024 發表 → `2024`。
- `<短名>`：論文模型名或常用簡稱，**全小寫英文、單字間用連字號 `-`**，不要空格、底線、中文。
  - ✅ `2024-videomamba.html`、`2024-vision-mamba.html`、`2024-mamba-2.html`
  - ❌ `VideoMamba.html`、`2024_video_mamba.html`、`影片mamba.html`
- 檔名去掉 `.html` 就是這篇論文的 **`id`**，必須和 `papers.json` 中的 `id` 完全一致。
- 若短名重複（同年兩篇同名），在後面加第一作者姓氏：`2024-videomamba-chen.html`。

---

## 5. `papers.json` 資料格式

`papers.json` 是一個陣列，每篇論文一個物件。**新增筆記頁時一定要同步新增這裡的資料**，否則首頁看不到。

```json
{
  "id": "2024-videomamba",
  "title": "VideoMamba: State Space Model for Efficient Video Understanding",
  "shortName": "VideoMamba",
  "authors": "Kunchang Li, Xinhao Li, Yi Wang, et al.",
  "year": 2024,
  "venue": "ECCV 2024",
  "arxiv": "2403.06977",
  "code": "https://github.com/OpenGVLab/VideoMamba",
  "tags": ["mamba", "video", "action-recognition", "self-distillation"],
  "status": "read",
  "readDate": "2026-11-16",
  "tldr": "一句話總結，50 字元以內。",
  "page": "papers/2024-videomamba.html"
}
```

| 欄位 | 必填 | 規則 |
|---|---|---|
| `id` | ✅ | 與檔名相同（去掉 `.html`）。待讀論文也要有 id，規則相同。 |
| `title` | ✅ | 論文完整英文標題，照原文大小寫。 |
| `shortName` | ✅ | 卡片上顯示的簡稱，例如 `Vim`、`VideoMamba`。 |
| `authors` | ✅ | 超過 3 位作者時寫前 3 位 + `et al.`。 |
| `year` | ✅ | 數字，arXiv 第一版年份。 |
| `venue` | ✅ | 例如 `ICML 2024`；只有 arXiv 時寫 `arXiv`。不確定就寫 `arXiv`，**不要猜會議**。 |
| `arxiv` | ⭕ | 只寫編號（`2403.06977`），不要整個網址。不確定就填 `""`。 |
| `code` | ⭕ | 官方程式碼網址；沒有就填 `""`。 |
| `tags` | ✅ | 只能從第 6 節的標籤清單中選，2～5 個。 |
| `status` | ✅ | 只能是 `"read"`（已讀）、`"reading"`（閱讀中）、`"to-read"`（待讀）。 |
| `readDate` | ⭕ | `YYYY-MM-DD`，`status` 為 `read` 時必填。 |
| `tldr` | ✅ | 繁體中文，50 字元以內（中英文、空白、標點都算 1 個字元）。待讀論文寫「為什麼想讀」。 |
| `page` | ✅ | 筆記頁的相對路徑；`to-read` 還沒寫筆記時填 `null`。 |

排序：陣列順序不重要，首頁會自動依 `year` 由新到舊排序。

---

## 6. 標籤（tags）詞彙表

標籤是**封閉清單**，只能用下面這些。要新增標籤時，先在這張表加一列並說明意思，再使用。

| 標籤 | 意思 |
|---|---|
| `ssm` | State Space Model 理論或通用 SSM 架構 |
| `mamba` | 以 Mamba / selective SSM 為核心 |
| `transformer` | 以 attention / Transformer 為核心或主要比較對象 |
| `vision-backbone` | 通用影像骨幹網路（分類、偵測、分割） |
| `video` | 影片理解（廣義） |
| `action-recognition` | 動作辨識 |
| `interaction` | 多人 / 雙人互動辨識 |
| `skeleton` | 以骨架（skeleton / pose）為輸入 |
| `long-video` | 長影片理解 |
| `efficiency` | 主要貢獻在速度、記憶體、複雜度 |
| `self-distillation` | 使用自蒸餾或知識蒸餾 |
| `pretraining` | 預訓練策略（masked modeling 等） |
| `language-model` | 語言建模 |

---

## 7. 筆記頁的固定格式

新增筆記時，**複製 `papers/_template.html`**，改名後填入內容。每一頁都必須有以下 9 個段落，**順序、`id`、標題文字都不能改**：

| # | `<section id="...">` | 標題 | 要寫什麼 |
|---|---|---|---|
| 1 | `info` | 基本資訊 | 用 `info-table`：作者、發表、arXiv、程式碼、閱讀狀態、閱讀日期。 |
| 2 | `tldr` | 一句話總結 | 可比 `papers.json` 的 `tldr` 稍長（1～2 句），放在 `tldr` 框中。 |
| 3 | `problem` | 要解決的問題 | 前人方法的不足、這篇想解決什麼。2～4 點。 |
| 4 | `method` | 方法重點 | 核心設計，用編號列表，每點一個概念。可放 `figure-note` 描述架構圖。 |
| 5 | `results` | 實驗與結果 | 資料集、比較對象、主要結論。**數字必須來自論文並註明出處（Table / Fig. 編號）。** |
| 6 | `pros-cons` | 優點與限制 | 用 `two-col`：左邊優點、右邊限制。 |
| 7 | `relevance` | 與我研究的關聯 | 對「Mamba 做動作辨識 / 雙人互動」有什麼啟發或可借用的地方。 |
| 8 | `questions` | 待解問題與下一步 | 讀完還不懂的地方、想做的實驗、要追的引用論文。 |
| 9 | `related` | 相關筆記 | 連到站內其他筆記頁，以及 `glossary.html` 中的名詞。 |

頁首麵包屑、頁尾格式也要和模板一致。`<title>` 格式：`<shortName> — Mamba 影片理解筆記`。

---

## 8. 可用的 CSS class

只能使用以下 class（定義在 `assets/style.css`）：

| class | 用途 |
|---|---|
| `site-header`, `site-nav`, `site-footer` | 全站頁首、導覽列、頁尾 |
| `container` | 內容置中容器 |
| `breadcrumb` | 筆記頁頂端「首頁 / 論文名」 |
| `paper-header`, `paper-title`, `paper-subtitle` | 筆記頁標題區 |
| `info-table` | 基本資訊表格 |
| `tldr` | 一句話總結的強調框 |
| `note-section` | 每個段落 `<section>` 都要加 |
| `figure-note` | 用文字描述架構圖 / 流程（不放論文原圖） |
| `two-col`, `col-pros`, `col-cons` | 優點 / 限制兩欄 |
| `tag` | 標籤小膠囊，例如 `<span class="tag">mamba</span>` |
| `status`, `status-read`, `status-reading`, `status-to-read` | 閱讀狀態標示 |
| `todo` | **待確認**標記：`<span class="todo">待確認</span>` |
| `ai-draft` | 包住「AI 代寫、我還沒審過」的段落 |
| `src` | 數字出處標註，例如 `<span class="src">Table 2</span>` |
| `formula` | 單行公式 / 程式片段區塊 |
| `toc` | 筆記頁標題下方的段落目錄（模板已內建，照抄即可） |
| `card-tags` | 筆記頁標題區中放 `status` 與 `tag` 的容器 |
| `brand` | 頁首左上角站名連結 |

段落標題 `<h2 data-n="01">`：`data-n` 是段落編號 `01`～`09`，CSS 會自動顯示在標題前。

首頁與名詞表另有 `hero`, `eyebrow`, `stats`, `filters`, `chip`, `chip-row`, `section-label`, `paper-grid`, `paper-card`, `card-*`, `empty`, `glossary-list`, `term`, `zh`, `refs` 等 class，由 `index.html`、`glossary.html` 與 `main.js` 使用，**新增論文或名詞時不需要手動使用**。

---

## 9. 寫作規則（AI 必須遵守）

1. **語言**：繁體中文（台灣用語）。專有名詞第一次出現寫「中文（English）」，之後可只寫英文，例如「選擇性狀態空間模型（selective SSM）」。模型名、資料集名一律保留英文。
2. **不可捏造**：作者、會議、arXiv 編號、實驗數字，必須來自論文原文或我提供的資料。**找不到或不確定的，一律加 `<span class="todo">待確認</span>`**，不要猜。
3. **數字附出處**：寫到準確率、速度、記憶體等數字時，後面加 `<span class="src">Table X</span>` 或 `<span class="src">Fig. X</span>`。
4. **不貼大段原文**：用自己的話整理。引用原句最多一句、且要加引號。不要放論文的原始圖片（版權），用 `figure-note` 文字描述架構。
5. **標示 AI 草稿**：「與我研究的關聯」、「待解問題」這兩段是我的想法。AI 幫忙起草時，要用 `<div class="ai-draft">…</div>` 包起來，我審過之後才會拿掉。
6. **不要刪我的內容**：修改既有筆記時，不要刪除或改寫沒有 `ai-draft` 標記的「與我研究的關聯」「待解問題」段落；只能在後面補充。
7. **簡潔**：每篇筆記讀完約 5 分鐘。列點優先，每點 1～3 句。

---

## 10. 新增一篇論文筆記的流程（Checklist）

當我說「**新增一篇筆記：<論文名 / arXiv 連結 / PDF>**」時，請依序：

1. 確認論文資訊（標題、作者、年份、會議、arXiv 編號、程式碼）。
2. 依第 4 節決定檔名與 `id`。
3. 複製 `papers/_template.html` → `papers/<id>.html`。
4. 依第 7 節填完 9 個段落，遵守第 9 節寫作規則。
5. 在 `papers.json` 新增一筆（或把原本 `to-read` 那筆改成 `read`，並把 `page` 從 `null` 改成路徑）。
6. 若筆記中出現名詞表還沒有的重要術語，依第 11 節加到 `glossary.json`。
7. 在相關舊筆記的「相關筆記」段落加上指向新筆記的連結（雙向連結）。
8. 執行第 12 節的檢查。
9. 回報：新增了哪些檔案、哪些地方標了「待確認」。

當我說「**加到待讀清單：<論文名>**」時：只在 `papers.json` 新增 `status: "to-read"`、`page: null` 的資料，不建立筆記頁。

---

## 11. 名詞表 `glossary.json` 格式

```json
{
  "term": "Selective SSM (S6)",
  "zh": "選擇性狀態空間模型",
  "definition": "繁中說明，1～3 句。",
  "papers": ["2023-mamba"]
}
```

- `term`：英文名稱（可含常用縮寫）。
- `zh`：中文譯名。
- `definition`：用自己的話解釋，1～3 句，不要複製論文原文。
- `papers`：相關論文 `id` 陣列，必須是 `papers.json` 中存在的 id。
- 名詞表頁會依 `term` 字母排序，陣列順序不重要。
- **錨點連結規則**：每個名詞在 `glossary.html` 的錨點是 `term` 轉小寫、非英數字元換成 `-`、去掉頭尾 `-`。
  例：`Selective SSM (S6)` → `glossary.html#selective-ssm-s6`；`State Space Model (SSM)` → `#state-space-model-ssm`。
  筆記頁「相關筆記」段落連到名詞時用這個規則（從 `papers/` 內要寫 `../glossary.html#...`）。

---

## 12. 完成前檢查

每次修改後**先執行自動檢查腳本**，必須顯示 `全部通過` 才算完成：

```bash
python3 scripts/check.py
```

腳本會自動檢查下列前 5 項；最後一項需要開瀏覽器人工確認：

- [ ] `papers.json`、`glossary.json` 是合法 JSON，且必填欄位齊全、`status` 值合法。
- [ ] `papers.json` 每筆 `page` 指向的檔案都存在；每個 `papers/*.html`（除了 `_template.html`）都在 `papers.json` 裡。
- [ ] 所有 `tags` 都在第 6 節清單中；`glossary.json` 的 `papers` 都是存在的 id。
- [ ] 新筆記頁有完整 9 個段落，`id` 與順序正確。
- [ ] 沒有 inline style、沒有絕對路徑、沒有新增 CDN。
- [ ] 用 `python3 -m http.server` 開首頁，確認新卡片出現、篩選正常、點進去頁面正常。

---

## 13. 常用指令範例（給我自己複製用）

- 「讀完這篇 PDF，照 CLAUDE.md 新增一篇筆記。」
- 「把 Mamba-2 加到待讀清單。」
- 「幫 2024-videomamba 的實驗段落補上 Kinetics-400 的數字，記得附 Table 編號。」
- 「掃過所有筆記，列出所有『待確認』的地方。」
- 「新增一個標籤 `temporal-modeling`，並幫相關論文加上。」

---

## 14. 不要做的事

- ❌ 改動 `_template.html` 的段落結構（除非我要求，且要同步改第 7 節）。
- ❌ 把論文資料寫死在 `index.html`。
- ❌ 使用清單以外的標籤或 `status` 值。
- ❌ 引入框架、npm 套件或 build 步驟。
- ❌ 為了「看起來完整」而編造數字或會議名稱。
