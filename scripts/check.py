#!/usr/bin/env python3
"""依 CLAUDE.md 的規則自動檢查專案。用法：python3 scripts/check.py

標籤清單直接從 CLAUDE.md 第 6 節的表格讀取，所以 CLAUDE.md 是唯一的規則來源。
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ["info", "tldr", "problem", "method", "results", "pros-cons", "relevance", "questions", "related"]
STATUSES = {"read", "reading", "to-read"}
REQUIRED = ["id", "title", "shortName", "authors", "year", "venue", "tags", "status", "tldr", "page"]
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def slug(term: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", term.lower()))


def allowed_tags() -> set[str]:
    text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    part = text.split("## 6.", 1)[1].split("\n## ", 1)[0]
    return set(re.findall(r"^\| `([a-z0-9-]+)` \|", part, flags=re.M))


def load(name: str):
    try:
        return json.loads((ROOT / name).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err(f"{name} 不是合法 JSON：{e}")
        return []


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections, self.links, self.inline_styles = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "style" in a:
            self.inline_styles += 1
        if tag == "section" and "note-section" in (a.get("class") or ""):
            self.sections.append(a.get("id"))
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def main() -> int:
    tags_ok = allowed_tags()
    papers = load("papers.json")
    glossary = load("glossary.json")
    ids = set()
    term_slugs = {slug(t.get("term", "")) for t in glossary}

    # ---- papers.json ----
    for p in papers:
        pid = p.get("id", "<缺 id>")
        for f in REQUIRED:
            if f not in p:
                err(f"papers.json [{pid}] 缺少欄位 {f}")
        if pid in ids:
            err(f"papers.json id 重複：{pid}")
        ids.add(pid)
        if not re.fullmatch(r"\d{4}-[a-z0-9]+(-[a-z0-9]+)*", pid):
            err(f"[{pid}] id 不符合 <年份>-<短名> 規則")
        elif str(p.get("year")) != pid[:4]:
            err(f"[{pid}] id 年份與 year={p.get('year')} 不一致")
        if p.get("status") not in STATUSES:
            err(f"[{pid}] status 不合法：{p.get('status')}")
        if p.get("status") == "read" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.get("readDate") or ""):
            err(f"[{pid}] status 為 read 但 readDate 不是 YYYY-MM-DD")
        tags = p.get("tags", [])
        if not 2 <= len(tags) <= 5:
            err(f"[{pid}] 標籤數量應為 2～5 個，目前 {len(tags)} 個")
        for t in tags:
            if t not in tags_ok:
                err(f"[{pid}] 標籤 `{t}` 不在 CLAUDE.md 第 6 節清單中")
        if len(p.get("tldr", "")) > 50:
            err(f"[{pid}] tldr 超過 50 字元（{len(p['tldr'])} 字）")
        page = p.get("page")
        if page is not None:
            if page != f"papers/{pid}.html":
                err(f"[{pid}] page 應為 papers/{pid}.html，目前是 {page}")
            elif not (ROOT / page).exists():
                err(f"[{pid}] page 檔案不存在：{page}")

    # ---- 每個筆記頁都要在 papers.json ----
    listed = {p.get("page") for p in papers}
    for f in sorted((ROOT / "papers").glob("*.html")):
        if f.name == "_template.html":
            continue
        rel = f"papers/{f.name}"
        if rel not in listed:
            err(f"{rel} 沒有登記在 papers.json")
            continue
        html = f.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(html)
        if parser.sections != SECTIONS:
            err(f"{rel} 段落 id/順序不符：{parser.sections}")
        if parser.inline_styles:
            err(f"{rel} 有 {parser.inline_styles} 處 inline style")
        if "{{" in html:
            err(f"{rel} 還有未替換的 {{{{...}}}} 佔位符")
        for link in parser.links:
            if link.startswith("/"):
                err(f"{rel} 使用了絕對路徑：{link}")
            elif not link.startswith(("http", "#", "mailto:")):
                target, _, anchor = link.partition("#")
                if target and not (f.parent / target).resolve().exists():
                    err(f"{rel} 連結到不存在的檔案：{link}")
                if target.endswith("glossary.html") and anchor and anchor not in term_slugs:
                    err(f"{rel} 名詞錨點不存在：#{anchor}")

    # ---- glossary.json ----
    for t in glossary:
        for f in ("term", "zh", "definition", "papers"):
            if f not in t:
                err(f"glossary.json [{t.get('term')}] 缺少欄位 {f}")
        for pid in t.get("papers", []):
            if pid not in ids:
                err(f"glossary.json [{t.get('term')}] 參照不存在的論文 id：{pid}")

    if errors:
        print(f"發現 {len(errors)} 個問題：")
        for e in errors:
            print("  ✗", e)
        return 1
    n_pages = sum(1 for p in papers if p.get("page"))
    print(f"全部通過 ✓  論文 {len(papers)} 篇（筆記 {n_pages} 篇）、名詞 {len(glossary)} 個、標籤清單 {len(tags_ok)} 個")
    return 0


if __name__ == "__main__":
    sys.exit(main())
