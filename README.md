# 臨床毒物學精要

急診臨床毒物學快速參考。作者：潘麒亘 醫師（中國醫藥大學附設醫院 急診部｜毒物及急診專科醫師）。

網站：https://ck5227.github.io/toxicology/

## 檔案結構

```
.
├── index.html      主頁
├── toxidrome/
│   └── index.html  Toxidrome 互動式鑑別與教學工具（純前端，無外部呼叫）
├── antidote/
│   └── index.html  全國解毒劑儲備 ＆ 罕見中毒決策副駕（衛福部儲備網、Micromedex、EXTRIP）
├── resus/
│   └── index.html  2025 ACLS ＆ E-CPR 急救復甦副駕（5H5T、VA-ECMO 適應症門檻、HIS 醫藥囑套裝）
├── template.html   Phase 2 子頁模板，複製後填入內容
├── 404.html        找不到頁面
├── robots.txt
├── sitemap.xml     每上線一個子頁就取消對應區塊的註解
└── .nojekyll       關閉 GitHub Pages 的 Jekyll 處理（勿刪）
```

## 重要快捷鍵（急救室全流程）

- `Alt + O`：一鍵產生標準化 HIS SOP 醫藥囑套裝（含 E-CPR / 2025 AHA ACLS / Post-ROSC）
- `Alt + S`：一鍵產出心臟外科／加護病房交班 SBAR 結構化病歷與通報摘要
- `Alt + E`：急診重症床邊 EBM 臨床實證精粹（BICAR-ICU、高血鉀穩定膜電位、毒物休克）
- `Alt + T`：啟動 / 暫停高精度 CPR 節拍器（110 bpm，對標 AHA 指引）

## 系統設計原則與資安規範

- **零網路呼叫（Zero-data-egress）**：100% 於瀏覽器記憶體端完成，無任何後端上傳，合規於 HIPAA 與醫療個資法。
- **結構化與確定性**：拒絕黑盒子幻覺，數值運算、5H5T 病因排查與適應症檢核均為嚴謹醫學邏輯。
- **劑量與治療內容只能來自國際權威指引與衛福部官方公佈規格**（AHA 2025 ACLS、ELSO、EXTRIP、Micromedex、衛福部解毒劑儲備網）。

## 更新樣式

新增或變更 Tailwind class 後，請在專案根目錄執行，並提交產生的 CSS：

```sh
npx --yes tailwindcss@3.4.17 -i ./assets/input.css -o ./assets/style.css --content "./*.html,./toxidrome/*.html,./antidote/*.html,./resus/*.html" --minify
```
