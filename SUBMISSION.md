# 作業繳交內容（複製貼上用，交完可刪除本檔）

## 1. 專案簡介

「Mamba × 影片理解論文筆記」是我的研究用論文筆記網站。我的研究方向是把 State Space Model / Mamba 架構應用到影片動作辨識，未來可能延伸到雙人互動辨識，所以需要持續閱讀並整理大量相關論文。

網站中每篇論文一頁，用固定的 9 段格式整理（基本資訊、一句話總結、要解決的問題、方法重點、實驗與結果、優點與限制、與我研究的關聯、待解問題、相關筆記）。首頁可以依標籤、閱讀狀態和關鍵字篩選，也列出待讀清單；另外有一個名詞表統一解釋 SSM、Selective SSM、Bidirectional scan 等術語。目前已完成 Mamba、Vision Mamba、VideoMamba 三篇筆記，另有 3 篇論文在待讀清單中。

網站是純靜態網站（HTML + CSS + 原生 JavaScript），內容由 `papers.json` 與 `glossary.json` 驅動，並以 GitHub Pages 發布。

## 2. GitHub Repository 連結

https://github.com/yitingo41o/mamba-video-notes

## 3. 網頁連結

https://yitingo41o.github.io/mamba-video-notes/

## 4. CLAUDE.md

https://github.com/yitingo41o/mamba-video-notes/blob/main/CLAUDE.md
（`AGENTS.md` 也放在 repo 中，內容指向 `CLAUDE.md`，讓不同的 AI 工具都能讀到同一套規則。）

## 5. 新增頁面時，這套規則如何幫助 AI 繼續完成？

我設計 `CLAUDE.md` 時，目標是讓 AI 只要收到一句「讀完這篇 PDF，照 CLAUDE.md 新增一篇筆記」，就能做出和現有頁面格式一致、可以直接上線的新頁面。主要靠以下幾點：

1. **明確的新增流程**：第 10 節列出 9 個步驟。AI 會依序確認論文資訊、照規則命名檔案（`papers/<年份>-<短名>.html`）、複製模板、填完 9 個固定段落、在 `papers.json` 登記、補名詞表，並在舊筆記加上雙向連結，不需要自己猜要改哪些檔案。
2. **模板與資料格式固定**：`_template.html` 規定了段落的 id、順序和標題；`papers.json` 每個欄位都有格式和允許值的說明；標籤是封閉清單。因此新頁面在外觀和結構上都會和舊頁面一致，首頁篩選也能自動運作。
3. **寫作與誠信規則**：規定 AI 不可捏造作者、會議或實驗數字，數字要附 Table / Fig. 出處，不確定的地方要標「待確認」；AI 代寫的「研究關聯」段落要用紫色框標示，等我審閱。這讓 AI 產生的筆記可以放心累積在研究資料中。
4. **可自動驗證**：`scripts/check.py` 直接讀取 `CLAUDE.md` 的標籤清單，檢查 JSON 格式、檔名與 id 是否一致、段落是否完整、連結和名詞錨點是否存在、有沒有 inline style 或絕對路徑。AI 改完後執行檢查，看到「全部通過」才算完成，不必靠人工逐項核對。

這套結構也可以延伸使用：把標籤清單和第 1 節的研究主題換掉，就能變成其他領域的論文筆記站；若想新增其他內容類型（例如實驗紀錄），也可以照「JSON 資料 + 模板 + 規則章節 + 檢查腳本」的方式擴充。
