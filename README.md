# 臨床毒物學精要

急診臨床毒物學快速參考。作者：潘麒亘 醫師（中國醫藥大學附設醫院 急診部｜毒物及急診專科醫師）。

網站：https://ck5227.github.io/toxicology/

## 檔案結構

```
.
├── index.html      主頁
├── toxidrome/
│   └── index.html  Toxidrome 互動式鑑別與教學工具（純前端，無外部呼叫）
├── template.html   Phase 2 子頁模板，複製後填入內容
├── 404.html        找不到頁面
├── robots.txt
├── sitemap.xml     每上線一個子頁就取消對應區塊的註解
└── .nojekyll       關閉 GitHub Pages 的 Jekyll 處理（勿刪）
```

## 新增一個子頁（Phase 2）

1. 建立資料夾，例如 `organophosphate/`
2. 複製 `template.html` 成 `organophosphate/index.html`
3. 取代所有 `【】` 標記的欄位（標題、description、canonical、內文）
4. `sitemap.xml` 取消對應區塊註解
5. `index.html` 裡該毒物卡片的連結，從
   `https://sites.google.com/view/xxx/` 改成 `organophosphate/`，
   並移除 `target="_blank" rel="noopener"`

## 重要慣例

- **一律使用相對路徑**（`../`、`organophosphate/`），不要用 `/` 開頭的絕對路徑。
  站台目前位於 `/toxicology/` 子目錄，未來接上自訂網域會移到根目錄，
  絕對路徑會在其中一種情況下失效。
- 檔名大小寫敏感，一律小寫。
- 每頁只能有一個 `<h1>`，且必須包含主要關鍵字。
- 每頁都要有獨立的 `<title>`、`<meta name="description">` 與 `<link rel="canonical">`。

## 已知待辦

- [ ] 把 26 個仍指向 Google Sites 的外連逐步改成站內頁面
- [ ] Tailwind 目前使用 Play CDN，內容穩定後改為預先編譯的 `assets/style.css`
- [ ] Google Search Console 驗證並提交 sitemap

## Toxidrome 工具的設計約束（修改前務必閱讀）

- **不得加入任何對外的網路呼叫。** 全部判讀與計算都在瀏覽器內完成，這是它不涉及個資
  與法規問題的根本原因。一旦送資料出去，性質就完全改變了。
- **輸入一律為結構化欄位**，不接受自由文字病歷貼上 —— 避免使用者輸入可識別資訊。
- **劑量與治療內容只能來自本站既有內容**，不可由外部生成。
- 比對引擎的兩道安全限制不可移除：
  1. `veto` —— 出現決定性反證（權重 3 的 negative）時強制降至 35% 以下。
  2. `hallmarks === 0` —— 一項決定性特徵都沒對上就封頂 40%。
     少了這道限制，生命徵象全正常的病人會被誤判成鎮靜安眠中毒，
     那正是乙醯胺酚被漏掉的方式。
