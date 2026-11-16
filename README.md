# Mamba × 影片理解論文筆記

State Space Model（SSM）/ Mamba 系列架構，以及它們在**影片動作辨識**與**雙人互動辨識**上的應用——我的研究論文筆記網站。

🔗 網站：https://yitingo41o.github.io/mamba-video-notes/

## 特色

- 每篇論文一頁，固定 9 段格式（基本資訊、一句話總結、問題、方法、結果、優缺點、與我研究的關聯、待解問題、相關筆記）
- 首頁可依標籤、閱讀狀態、關鍵字篩選，並列出待讀清單
- 名詞表統一整理反覆出現的術語，並與筆記雙向連結
- 純靜態網站（HTML + CSS + 原生 JS），資料由 `papers.json`、`glossary.json` 驅動

## 給 AI 的規則

專案規則寫在 **[CLAUDE.md](./CLAUDE.md)**（`AGENTS.md` 指向它）。AI 讀完後就能照同一套格式新增筆記，例如：

> 「讀完這篇 PDF，照 CLAUDE.md 新增一篇筆記。」

修改後執行 `python3 scripts/check.py` 自動檢查是否符合規則。

## 本地預覽

```bash
python3 -m http.server 8000
# 打開 http://localhost:8000
```
