# 臨床毒物學精要

急診臨床毒物學快速參考。作者：潘麒亘 醫師（中國醫藥大學附設醫院 急診部｜毒物及急診專科醫師）。

網站：https://ck5227.github.io/toxicology/

## 檔案結構

```
.
├── index.html      主頁（唯一已上線的內容頁）
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
