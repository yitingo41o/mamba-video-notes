// ==========================================================
// 首頁（論文列表）與名詞表的渲染邏輯
// 資料來源：papers.json、glossary.json —— 新增內容請改 JSON，不要改這支程式
// ==========================================================

const STATUS_LABEL = { read: "已讀", reading: "閱讀中", "to-read": "待讀" };

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v);
  }
  for (const c of [].concat(children)) if (c) node.append(c);
  return node;
}

async function loadJSON(path) {
  const res = await fetch(path, { cache: "no-cache" });
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.json();
}

function showLoadError(target, err) {
  target.replaceChildren(
    el("p", { class: "empty", text: `資料載入失敗（${err.message}）。如果是直接用瀏覽器打開檔案，請改用：python3 -m http.server 8000` })
  );
}

// ---------------- 首頁 ----------------
function paperCard(p) {
  const hasPage = Boolean(p.page);
  const card = el(hasPage ? "a" : "div", {
    class: "paper-card" + (hasPage ? "" : " no-page"),
    ...(hasPage ? { href: p.page } : {}),
  });
  card.append(
    el("div", { class: "card-top" }, [
      el("span", { class: `status status-${p.status}`, text: STATUS_LABEL[p.status] || p.status }),
      el("span", { text: `${p.year} · ${p.venue}` }),
    ]),
    el("div", { class: "card-name", text: p.shortName }),
    el("p", { class: "card-title", text: p.title }),
    el("p", { class: "card-tldr", text: p.tldr }),
    el("div", { class: "card-tags" }, p.tags.map((t) => el("span", { class: "tag", text: t })))
  );
  return card;
}

async function renderHome() {
  const listRead = document.getElementById("list-notes");
  const listTodo = document.getElementById("list-todo");
  let papers;
  try {
    papers = await loadJSON("papers.json");
  } catch (err) {
    showLoadError(listRead, err);
    return;
  }
  papers.sort((a, b) => b.year - a.year || a.shortName.localeCompare(b.shortName));

  // stats
  const count = (s) => papers.filter((p) => p.status === s).length;
  document.getElementById("stat-read").textContent = count("read");
  document.getElementById("stat-reading").textContent = count("reading");
  document.getElementById("stat-todo").textContent = count("to-read");

  // tag chips
  const allTags = [...new Set(papers.flatMap((p) => p.tags))].sort();
  const activeTags = new Set();
  const chipRow = document.getElementById("tag-chips");
  for (const t of allTags) {
    const chip = el("button", { class: "chip", type: "button", text: t });
    chip.addEventListener("click", () => {
      activeTags.has(t) ? activeTags.delete(t) : activeTags.add(t);
      chip.classList.toggle("on");
      update();
    });
    chipRow.append(chip);
  }

  const search = document.getElementById("search");
  const statusSel = document.getElementById("status-filter");

  function matches(p) {
    const q = search.value.trim().toLowerCase();
    const text = `${p.title} ${p.shortName} ${p.authors} ${p.tldr} ${p.tags.join(" ")}`.toLowerCase();
    if (q && !text.includes(q)) return false;
    if (statusSel.value !== "all" && p.status !== statusSel.value) return false;
    for (const t of activeTags) if (!p.tags.includes(t)) return false;
    return true;
  }

  function fill(target, items, emptyText) {
    target.replaceChildren(...(items.length ? items.map(paperCard) : [el("p", { class: "empty", text: emptyText })]));
  }

  function update() {
    const shown = papers.filter(matches);
    fill(listRead, shown.filter((p) => p.page), "沒有符合條件的筆記。");
    fill(listTodo, shown.filter((p) => !p.page), "沒有符合條件的待讀論文。");
  }

  search.addEventListener("input", update);
  statusSel.addEventListener("change", update);
  update();
}

// ---------------- 名詞表 ----------------
async function renderGlossary() {
  const list = document.getElementById("glossary");
  let terms, papers;
  try {
    [terms, papers] = await Promise.all([loadJSON("glossary.json"), loadJSON("papers.json")]);
  } catch (err) {
    showLoadError(list, err);
    return;
  }
  const byId = Object.fromEntries(papers.map((p) => [p.id, p]));
  terms.sort((a, b) => a.term.localeCompare(b.term));

  const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

  list.replaceChildren(
    ...terms.map((t) => {
      const refs = t.papers
        .map((id) => byId[id])
        .filter(Boolean)
        .flatMap((p, i) => {
          const node = p.page ? el("a", { href: p.page, text: p.shortName }) : el("span", { text: p.shortName });
          return i ? [", ", node] : [node];
        });
      return el("article", { class: "term", id: slug(t.term) }, [
        el("h3", {}, [t.term, el("span", { class: "zh", text: t.zh })]),
        el("p", { text: t.definition }),
        refs.length ? el("div", { class: "refs" }, ["相關論文：", ...refs]) : null,
      ]);
    })
  );

  if (location.hash) document.querySelector(location.hash)?.scrollIntoView();
}

const page = document.body.dataset.page;
if (page === "home") renderHome();
if (page === "glossary") renderGlossary();
