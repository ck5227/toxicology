# -*- coding: utf-8 -*-
# 產生 teach/index.html：常見急性中毒一分鐘翻轉教學檢核卡（12 套）
# 每張卡的臨床內容「原樣取自」本站既有頁面（子頁的重點摘要，或首頁卡片），此腳本不改寫任何臨床文字。
# 日後專頁內容更新時，重新執行本腳本即可同步。
import io, re

ROOT = r"C:\Users\pan\toxicology"
read = lambda p: io.open(ROOT + "\\" + p, encoding="utf-8").read()
MAIN = read("index.html")

# (id, 卡片標題, 分類, 來源型態, 來源鍵, 專頁連結)
TOPICS = [
    ("organophosphate", "有機磷／氨基甲酸鹽", "農藥",   "sub",  "organophosphate", "../organophosphate/"),
    ("paraquat",        "巴拉刈",             "農藥",   "main", "巴拉刈 (Paraquat)</h3>", "../#pesticide-poisoning"),
    ("glufosinate",     "固殺草",             "農藥",   "main", "固殺草 (Glufosinate)</h3>", "../#pesticide-poisoning"),
    ("sedatives",       "鎮靜安眠藥",         "藥物",   "main", "鎮靜安眠藥 (Sedative-hypnotics)</h3>", "../#pharmaceutical-poisoning"),
    ("acetaminophen",   "乙醯胺酚",           "藥物",   "sub",  "acetaminophen", "../acetaminophen/"),
    ("salicylates",     "水楊酸",             "藥物",   "sub",  "salicylates", "../salicylates/"),
    ("tca",             "三環抗鬱劑",         "藥物",   "sub",  "tca", "../tca/"),
    ("ccb-betablocker", "鈣離子阻斷劑／β 阻斷劑", "心血管", "sub", "ccb-betablocker", "../ccb-betablocker/"),
    ("digoxin",         "毛地黃",             "心血管", "sub",  "digoxin", "../digoxin/"),
    ("methanol",        "甲醇",               "化學氣體", "sub", "methanol", "../methanol/"),
    ("co",              "一氧化碳",           "化學氣體", "main", "一氧化碳 (CO)</h3>", "../#chemical-gas-poisoning"),
    ("cyanide",         "氰化物",             "化學氣體", "sub", "cyanide", "../cyanide/"),
]

def sub_summary(slug):
    t = read(slug + r"\index.html")
    m = re.search(r'<h2[^>]*>\s*重點摘要\s*</h2>\s*(<ul[\s\S]*?</ul>)', t)
    assert m, slug
    return m.group(1).strip()

def main_card(h3_end):
    pos = MAIN.index(h3_end)
    starts = [m.start() for m in re.finditer(r'<div class="[^"]*content-card[^"]*"', MAIN) if m.start() < pos]
    s = starts[-1]
    # 以 div 深度找出卡片結尾
    depth, i = 0, s
    for m in re.finditer(r'<div\b|</div>', MAIN[s:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            i = s + m.end(); break
    card = MAIN[s:i]
    inner = card[card.index('>') + 1: card.rindex('</div>')]
    inner = re.sub(r'<h3[\s\S]*?</h3>', '', inner, count=1)             # 標題由卡片自己顯示
    inner = re.sub(r'<button[\s\S]*?</button>', '', inner)             # 首頁專用的彈出視窗按鈕
    inner = re.sub(r'href="(?!https?:|\.\./|#|mailto:)([^"]+)"', r'href="../\1"', inner)   # 相對連結改由 teach/ 出發
    inner = re.sub(r'href="#', 'href="../#', inner)
    return inner.strip()

CHECK = [
    ("S", "一句話說出病人與<b>最危急的問題</b>"),
    ("B", "暴露時間、途徑、攝入量（mg/kg）、外院處置"),
    ("A", "符合哪個中毒症候群、關鍵檢驗、嚴重度"),
    ("R①", "腸胃道除污：有無適應症與禁忌"),
    ("R②", "解毒劑：種類、初始劑量、滴定終點"),
    ("R③", "體外移除：是否需要透析或灌流"),
    ("R④", "未來 6 小時的監測排程與動向"),
]
check_html = "\n".join(
    '                <label><input type="checkbox"><span><b class="k">%s</b>%s</span></label>' % c for c in CHECK)

cards, chips, tags = [], [], []
for cid, title, tag, kind, key, link in TOPICS:
    body = sub_summary(key) if kind == "sub" else main_card(key)
    src = "專頁重點摘要" if kind == "sub" else "總覽卡片"
    more = "完整處置專頁 →" if kind == "sub" else "回總覽看這一類 →"
    if tag not in tags: tags.append(tag)
    cards.append('''        <details class="tc-card" id="c-%s">
            <summary>
                <span class="tc-tag">%s</span>
                <h2>%s</h2>
                <span class="tc-count" aria-live="polite"></span>
            </summary>
            <div class="tc-body">
                <div class="tc-check">
%s
                </div>
                <div>
                    <details class="tc-ans">
                        <summary>翻開核對：本站%s</summary>
                        <div class="tc-sum">
%s
                        </div>
                    </details>
                    <p class="tc-links"><a href="%s">%s</a></p>
                </div>
            </div>
        </details>''' % (cid, tag, title, check_html, src, body, link, more))

PAGE = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>常見急性中毒一分鐘翻轉教學檢核卡（12 套） | 臨床毒物學精要 ToxWeb</title>
<meta name="description" content="常見急性中毒一分鐘翻轉教學檢核卡 12 套：有機磷、巴拉刈、固殺草、鎮靜安眠藥、乙醯胺酚、水楊酸、三環抗鬱劑、鈣離子阻斷劑與 β 阻斷劑、毛地黃、甲醇、一氧化碳、氰化物。學員先以 SBAR 提出處置方案四要素，主治醫師逐項檢核、提問修正，再翻開重點核對。">
<meta name="author" content="潘麒亘 醫師">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ck5227.github.io/toxicology/teach/">

<meta property="og:type" content="article">
<meta property="og:site_name" content="臨床毒物學精要 ToxWeb">
<meta property="og:title" content="常見急性中毒一分鐘翻轉教學檢核卡（12 套）">
<meta property="og:description" content="學員先提案、主治醫師逐項檢核與提問、再翻開重點核對 —— 急性中毒的床邊一分鐘翻轉教學。">
<meta property="og:url" content="https://ck5227.github.io/toxicology/teach/">
<meta property="og:locale" content="zh_TW">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "name": "常見急性中毒一分鐘翻轉教學檢核卡（12 套）",
  "url": "https://ck5227.github.io/toxicology/teach/",
  "inLanguage": "zh-Hant",
  "description": "急性中毒床邊翻轉教學檢核卡 12 套：學員 SBAR 提案四要素檢核、主治醫師提問、重點核對。",
  "dateModified": "2026-11-24",
  "isPartOf": { "@type": "WebSite", "name": "臨床毒物學精要", "alternateName": "ToxWeb", "url": "https://ck5227.github.io/toxicology/" },
  "author": {
    "@type": "Person", "name": "潘麒亘", "jobTitle": "毒物及急診專科醫師",
    "affiliation": { "@type": "MedicalOrganization", "name": "中國醫藥大學附設醫院 急診部" }
  },
  "audience": { "@type": "MedicalAudience", "audienceType": "Clinician" }
}
</script>

<link rel="stylesheet" href="../assets/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">

<style>
    .hidden { display: none !important; }
    body { font-family: 'Noto Sans TC', sans-serif; background-color: #f3f6f8; color: #1f2937; }

    .tc-intro { max-width: 46rem; margin: 0 auto 2rem; text-align: center; }
    .tc-steps { display: flex; flex-wrap: wrap; justify-content: center; gap: .4rem .5rem; font-size: .95rem; color: #334155; }
    .tc-steps span { white-space: nowrap; }
    .tc-steps span + span::before { content: "→"; color: #94a3b8; margin-right: .5rem; }
    .tc-steps b { color: #264653; }
    .tc-q { margin-top: .9rem; font-size: .9rem; }
    .tc-q > summary { cursor: pointer; color: #0f766e; list-style: none; display: inline-block; }
    .tc-q > summary::-webkit-details-marker { display: none; }
    .tc-q > summary::after { content: " ＋"; }
    .tc-q[open] > summary::after { content: " －"; }
    .tc-q ul { list-style: none; margin-top: .6rem; color: #475569; font-style: italic; line-height: 1.9; }
    .tc-intro a { color: #0f766e; text-decoration: underline; text-underline-offset: 2px; }

    .tc-grid { display: grid; gap: .8rem; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); align-items: start; }
    .tc-card {
        background: #fff; border: 1px solid #e2e8ec; border-radius: 14px;
        transition: border-color .15s, box-shadow .2s; scroll-margin-top: 1rem;
    }
    .tc-card:hover { border-color: #2a9d8f; }
    .tc-card[open] { grid-column: 1 / -1; border-color: #264653; box-shadow: 0 10px 30px -14px rgba(16, 42, 52, .25); }
    .tc-card > summary {
        list-style: none; cursor: pointer; padding: 1rem 1.15rem;
        display: flex; align-items: baseline; gap: .6rem;
    }
    .tc-card > summary::-webkit-details-marker { display: none; }
    .tc-card h2 { font-size: 1.08rem; font-weight: 700; color: #264653; line-height: 1.35; flex: 1; }
    .tc-tag { flex: none; font-size: .72rem; color: #94a3b8; letter-spacing: .06em; }
    .tc-count { flex: none; font-size: .8rem; font-weight: 700; color: #94a3b8; }
    .tc-count.done { color: #0f766e; }

    .tc-body { padding: 0 1.15rem 1.1rem; display: grid; gap: 1rem; }
    @media (min-width: 860px) { .tc-body { grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr); gap: 1.75rem; } }
    .tc-check label {
        display: flex; gap: .6rem; align-items: flex-start; padding: .4rem .35rem; border-radius: 8px; cursor: pointer;
        font-size: .94rem; line-height: 1.5; transition: background-color .12s;
    }
    .tc-check label:hover { background: #f4f8f8; }
    .tc-check input { flex: none; width: 1.1rem; height: 1.1rem; margin-top: .18rem; accent-color: #2a9d8f; cursor: pointer; }
    .tc-check .k { display: inline-block; min-width: 2rem; color: #264653; }
    .tc-check input:checked + span { color: #94a3b8; }

    .tc-ans { border: 1px solid #e2e8ec; border-radius: 10px; overflow: hidden; }
    .tc-ans > summary {
        cursor: pointer; padding: .6rem .85rem; font-weight: 700; font-size: .92rem; color: #264653; background: #f8fafc;
        list-style: none; display: flex; justify-content: space-between; align-items: center;
    }
    .tc-ans > summary::-webkit-details-marker { display: none; }
    .tc-ans > summary::after { content: "＋"; color: #2a9d8f; font-weight: 700; }
    .tc-ans[open] > summary::after { content: "－"; }
    .tc-sum { padding: .85rem .9rem .5rem; font-size: .93rem; }
    .tc-sum ul { margin-bottom: .6rem; }
    .tc-sum li { line-height: 1.65; margin-bottom: .35rem; }
    .tc-sum h4 { font-size: 1rem !important; }
    .tc-sum a { color: #0f766e; text-decoration: underline; text-underline-offset: 2px; }
    .tc-links { margin-top: .7rem; font-size: .9rem; text-align: right; }
    .tc-links a { color: #0f766e; font-weight: 700; }
    .tc-links a:hover { text-decoration: underline; }
    .tc-foot { display: flex; justify-content: center; margin-top: 1.5rem; }
    .tc-act { font-size: .85rem; color: #64748b; text-decoration: underline; text-underline-offset: 2px; }

    /* 取自首頁卡片內容所需之樣式（與首頁一致） */
    .list-item-label { font-weight: 600; color: #4a5568; margin-right: .5rem; }
    .disposition-box { margin-top: .75rem; padding: .7rem; background-color: #ebf8ff; border-left: 4px solid #4299e1; color: #2c5282; border-radius: 0 10px 10px 0; }
    .pitfall-box { margin-top: .5rem; padding: .7rem; background-color: #fffbeb; border-left: 4px solid #f59e0b; color: #78350f; border-radius: 0 10px 10px 0; }
    .corrosive-note { margin-top: .5rem; padding: .7rem; background-color: #fee2e2; border-left: 4px solid #ef4444; color: #991b1b; border-radius: 0 10px 10px 0; }
    .kpi-card { background-color: #264653; color: #fff; border-radius: .75rem; padding: 1rem; text-align: center; }
    .kpi-number { font-size: 2rem; font-weight: 700; color: #e9c46a; line-height: 1.2; }
    .kpi-label { font-size: .9rem; margin-top: .3rem; color: #f0f4f8; }

    @media print {
        header a, footer, .tc-foot, .tc-q { display: none !important; }
        body { background: #fff; }
        .tc-grid { display: block; }
        .tc-card { break-inside: avoid; margin-bottom: 1rem; box-shadow: none !important; }
    }
</style>
</head>
<body>

<header class="bg-[#264653] text-white p-6 shadow-lg">
    <div class="container mx-auto max-w-6xl">
        <a href="../" class="text-sm text-gray-300 hover:text-[#e9c46a]">← 回臨床毒物學精要 ToxWeb 總覽</a>
        <h1 class="text-2xl md:text-3xl font-bold text-[#e9c46a] mt-2">常見急性中毒一分鐘翻轉教學檢核卡</h1>
        <p class="mt-2 text-gray-300">12 套 —— <b class="text-[#e9c46a]">學員先提案，主治醫師逐項檢核與提問，再翻開重點核對</b></p>
    </div>
</header>

<main class="container mx-auto max-w-6xl p-4 md:p-8">

    <section class="tc-intro">
        <p class="tc-steps">
            <span><b>學員先提案</b></span>
            <span><b>主治醫師逐項勾選</b>、提問</span>
            <span><b>翻開核對</b></span>
            <span>細節進專頁</span>
        </p>
        <details class="tc-q">
            <summary>主治醫師可以這樣問</summary>
            <ul>
                <li>「你選這個解毒劑的理由是什麼？監測終點是什麼？」</li>
                <li>「如果這個處置無效，你的下一步是什麼？」</li>
                <li>「這個病人有沒有不能給這個藥的理由？」</li>
                <li>「什麼情況下你會啟動透析或灌流？」</li>
            </ul>
            <p style="margin-top:.5rem">完整流程見 <a href="../sop/">三階協同翻轉學習標準作業指引</a></p>
        </details>
    </section>

    <div class="tc-grid" id="tcGrid">
__CARDS__
    </div>

    <div class="tc-foot"><button type="button" class="tc-act" id="tcReset">清除所有勾選</button></div>

    <p class="text-sm mt-6 text-center" style="color:#94a3b8;line-height:1.7;max-width:46rem;margin-left:auto;margin-right:auto">「翻開核對」的內容原樣取自本站對應專頁之重點摘要或總覽卡片，供教學討論使用。劑量與處置細節請以專頁內容、最新文獻、院內規範及毒物諮詢中心建議為準。勾選狀態只留在這個畫面，不會儲存或傳送。</p>

</main>

<footer class="bg-[#264653] text-white mt-12 py-10 px-6">
    <div class="container mx-auto max-w-3xl">
        <div class="bg-[#1d3a47] rounded-lg p-5 mb-6">
            <p class="font-bold text-[#e9c46a] mb-2">作者</p>
            <p class="text-lg">潘麒亘 醫師</p>
            <p class="text-sm text-gray-300 mt-1">中國醫藥大學附設醫院 急診部｜毒物及急診專科醫師</p>
            <p class="text-sm text-gray-400 mt-3">最後更新：2026 年 11 月 24 日</p>
        </div>
        <div class="text-center text-sm">
            <p>本頁僅供醫療專業人員學術教育參考，不得取代專業臨床判斷。所有臨床決策應基於最新文獻與治療指引。</p>
        </div>
    </div>
</footer>

<script>
(function () {
    var cards = Array.prototype.slice.call(document.querySelectorAll('.tc-card'));
    var printing = false;

    function count(card) {
        var total = card.querySelectorAll('.tc-check input').length;
        var n = card.querySelectorAll('.tc-check input:checked').length;
        var el = card.querySelector('.tc-count');
        el.textContent = n ? n + '／' + total : '';
        el.classList.toggle('done', n === total);
    }
    cards.forEach(function (card) {
        card.addEventListener('change', function () { count(card); });
        // 一次只展開一張，畫面保持乾淨
        card.addEventListener('toggle', function () {
            if (card.open && !printing) cards.forEach(function (c) { if (c !== card) c.open = false; });
        });
    });

    document.getElementById('tcReset').addEventListener('click', function () {
        Array.prototype.forEach.call(document.querySelectorAll('.tc-check input'), function (i) { i.checked = false; });
        cards.forEach(count);
    });

    // 由其他頁面以 #c-xxx 連進來時，直接展開那張卡
    function openHash() {
        if (!location.hash) return;
        var t = document.getElementById(location.hash.slice(1));
        if (t && t.classList.contains('tc-card')) { t.open = true; t.scrollIntoView(); }
    }
    openHash();
    window.addEventListener('hashchange', openHash);

    // 列印時全部展開，可直接當講義
    window.addEventListener('afterprint', function () { printing = false; });
    window.addEventListener('beforeprint', function () {
        printing = true;
        Array.prototype.forEach.call(document.querySelectorAll('details'), function (d) { d.open = true; });
    });
})();
</script>

</body>
</html>
'''
out = PAGE.replace("__CARDS__", "\n\n".join(cards))
import os
os.makedirs(ROOT + r"\teach", exist_ok=True)
io.open(ROOT + r"\teach\index.html", "w", encoding="utf-8", newline="").write(out)
print("cards=%d" % len(cards))
