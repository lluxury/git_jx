---
marp: true
html: true
theme: am_blue
paginate: true
size: 16:9
header: ''
footer: '<em>XJTU</em> <em>Master of Science in Entrepreneurship and Innovation</em> <em>2026年6月1日（v1.3）</em>'
headingDivider: false
style: |
  @import 'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css';
  @import url(https://fonts.bunny.net/css?family=charm:700);

  :root {
    --color-code-bg: #e8f4f6; --color-coverbg: #2c9cb1; --color-few: #91a814;
    --color-footer: #8c8c8c; --color-main: #041d22; --color-much: #1482a8;
    --color-navbar-bg: #d0e9ee; --color-navbar-font: rgb(108, 95, 91);
    --color-quote: rgba(254, 176, 98, 0.1); --color-title: #ffffff; --color-trans: #72bdcb;
    --font-family-main: 'Latin Modern Math','Adobe Garamond','方正宋刻本秀楷简体','Calibri','楷体','华文中宋','霞鹜文楷 屏幕阅读版';
    --font-family-title: 'Optima LT Medium','Arial','方正苏新诗柳楷简体','黑体';
    --font-family-footer: 'Charm','Calibri','叶根友毛笔行书修正版','方正苏新诗柳楷简体','楷体';
    --font-family-code: 'Fira Code','HYMingChanKeBen W','Consolas','霞鹜文楷等宽','华文中宋','宋体';
    --font-size-1: 55px; --foot-size-subtitle: 42px;
    --font-size-2-3: 38px; --font-size-4-5: 30px;
    --font-size-main: 25px; --font-size-footer: 22px;
    --font-size-page: 12px;
  }

  section { font-family: var(--font-family-main); font-size: var(--font-size-main);
    color: var(--color-main); background: #fff; text-align: justify; }
  section h1 { font-family: var(--font-family-title); font-size: var(--font-size-1); color: var(--color-title); }
  section h2, section h3 { font-family: var(--font-family-title); font-size: var(--font-size-2-3);
    color: var(--color-much); border-bottom: none; }
  section h4, section h5 { font-family: var(--font-family-title); font-size: var(--font-size-4-5); color: var(--color-much); }
  section strong { color: var(--color-much); font-size: 1.03em; }
  section blockquote { border-left: 8px solid var(--color-much); padding: 10px 25px;
    border-radius: 8px; background: var(--color-quote); }
  section blockquote > p::before { content: "\f10d"; color: var(--color-much);
    padding-right: 2%; font-family: "FontAwesome"; }
  section a { color: var(--color-main); text-decoration: none; }
  section a::after { content: "\f148"; font-size: .6em; padding-left: .5%;
    color: var(--color-much); font-family: "FontAwesome"; }
  section code { background: var(--color-code-bg); font-family: var(--font-family-code);
    border-radius: 4px; padding: 2px 5px; font-size: .8em; }
  section table { border-collapse: collapse; text-align: center; font-size: .8em; margin: 0 auto; }
  section th, section thead { height: 40px; border-top: 3px solid var(--color-main);
    border-bottom: 3px solid var(--color-main); padding: 6px; }
  section tbody:last-child { border-bottom: 3px solid var(--color-main); }
  section table tr:nth-child(2n) { background: #fff; }

  section::after { font-family: "FontAwesome"; font-size: var(--font-size-page);
    margin-right: -10px; margin-bottom: -14px;
    content: attr(data-marpit-pagination) " \f101 " attr(data-marpit-pagination-total);
    letter-spacing: 3px; padding: 4px 10px; border-radius: 5px;
    border: 1px solid var(--color-footer); color: var(--color-footer); }
  section footer { color: var(--color-footer); bottom: 1%; left: 2%;
    width: 100%; height: 4%; display: flex; justify-content: space-between; }
  section footer > em { font-family: var(--font-family-footer);
    font-size: var(--font-size-footer); letter-spacing: 1px; font-style: normal; }

  .cols-2  { display: grid; gap: 1rem; grid-template-columns: 50% 50%;
    grid-template-rows: 10% 90%; grid-template-areas: "hd hd" "left right"; }
  .cols-3  { display: grid; gap: 1rem; grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 10% 90%; grid-template-areas: "hd hd hd" "left mid right"; }
  .cols-2-73 { display: grid; gap: 1rem; grid-template-columns: 70% 30%;
    grid-template-rows: 10% 90%; grid-template-areas: "hd hd" "left right"; }
  .pin-3 { display: grid; gap: 1rem; grid-template-columns: 50% 50%;
    grid-template-rows: 7% 42% 48%; grid-template-areas: "hd hd" "top top" "left right"; }
  .cols-2 > h2, .cols-3 > h2, .cols-2-73 > h2, .pin-3 > h2 { grid-area: hd; }
  .cols-2 .ldiv, .cols-2 .limg { grid-area: left;  margin-top: -2%; }
  .cols-2 .rdiv, .cols-2 .rimg { grid-area: right; margin-top: -2%; }
  .cols-3 .ldiv, .cols-3 .limg { grid-area: left; }
  .cols-3 .mdiv, .cols-3 .mimg { grid-area: mid; }
  .cols-3 .rdiv, .cols-3 .rimg { grid-area: right; }
  .cols-2-73 .ldiv, .cols-2-73 .limg { grid-area: left; }
  .cols-2-73 .rdiv, .cols-2-73 .rimg { grid-area: right; }
  .pin-3 .tdiv, .pin-3 .timg { grid-area: top; }
  .pin-3 .ldiv, .pin-3 .limg { grid-area: left; }
  .pin-3 .rdiv, .pin-3 .rimg { grid-area: right; }
  .limg, .rimg, .mimg, .timg { display: flex; align-items: center; justify-content: center; }

  section.fglass ul { padding: 20px 20px 20px 60px; margin-left: -25px;
    border-radius: 0 0 20px 20px; border-top: 8px solid var(--color-navbar-bg);
    background: #fff; box-shadow: 1px 1px 12px rgb(215,224,235); }

  section.col1_ol_sq > ul { list-style: none; display: table; line-height: 180%; }
  section.col1_ol_sq ul li { counter-increment: ol_sq; }
  section.col1_ol_sq ul li::before { content: counter(ol_sq);
    margin: 0 20px 0 0; width: 27px; height: 27px;
    display: inline-flex; align-items: center; justify-content: center;
    background: var(--color-much); color: #fff; font-family: var(--font-family-title); }

  section.col1_ol_ci > ol { list-style: none; display: table; line-height: 180%; }
  section.col1_ol_ci ol li { counter-increment: ol_ci; position: relative;
    padding-left: 2.6em; margin-bottom: 1em; }
  section.col1_ol_ci ol li::before { content: counter(ol_ci);
    position: absolute; left: 0; top: 0;
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--color-much); color: #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-family: var(--font-family-title); }

  section.cols2_ul_ci ul { display: grid; grid-template-columns: 1fr 1fr;
    gap: .7em 3em; list-style: none; width: 98%; }
  section.cols2_ul_ci ul li { counter-increment: ci; display: block;
    position: relative; padding-left: 2em; margin-bottom: 1.2em; }
  section.cols2_ul_ci ul li::before { content: counter(ci);
    position: absolute; left: 0; top: 0; width: 26px; height: 26px;
    border-radius: 50%; background: var(--color-much); color: #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-family: var(--font-family-title); font-size: .8em; }

  section.smalltext > p, section.smalltext > ul, section.smalltext > ol,
  section.smalltext > table, section.smalltext > blockquote { font-size: 90%; }
  section.tinytext  > p, section.tinytext  > ul, section.tinytext  > ol,
  section.tinytext  > table, section.tinytext  > blockquote { font-size: 80%; }
  section.caption .caption { padding-top: 20px; text-align: center;
    font-size: smaller; color: var(--color-footer); }

  section.trans { background: var(--color-trans); }
  section.trans h2 { color: var(--color-title); text-align: center; font-size: 2em; }

  section.cover_c { background: linear-gradient(to bottom, #fff 20%, var(--color-coverbg) 20% 88%, #fff 88%);
    text-align: left; }
  section.cover_c h1 { width: 95%; padding-top: 8%; color: #000; }
  section.cover_c h6 { font-family: var(--font-family-title);
    font-size: var(--foot-size-subtitle); color: #000; margin-top: 0; width: 95%; }
  section.cover_c p  { margin-top: 5%; color: #000; }
  section.cover_c strong, section.cover_c a { color: #000; }
  section.cover_c header img { filter: none !important; background: transparent !important; }
  section.cover_c footer { left: auto !important; right: 5% !important;
    width: auto !important; text-align: right !important;
    bottom: 20px !important; font-size: .9em; }

  section.cover_e { background: linear-gradient(108deg, #fff 70%, var(--color-coverbg) 30%); text-align: left; }
  section.cover_e h1 { top: 28%; width: 70%; position: absolute; color: var(--color-much); }
  section.cover_e h6 { font-family: var(--font-family-title); font-size: var(--foot-size-subtitle);
    color: var(--color-much); top: 38%; width: 68%; position: absolute; }
  section.cover_e p  { bottom: 15%; transform: translateX(5%); position: absolute; }
  section.cover_e header { background: var(--color-coverbg); height: 100px; width: 100px;
    top: 0; left: 80px; text-align: center; }
  section.cover_e header > img { transform: scale(.88); filter: brightness(3000%) grayscale(100%); }
  section.cover_e footer { height: 128px; width: 26%; left: 72%; bottom: 0; }
  section.cover_e footer > img { transform: scale(1.2); filter: brightness(2000%) grayscale(60%); }

  section.toc_b { background: linear-gradient(to right, #fff 6%, var(--color-coverbg) 6% 30%, #fff 30%);
    display: flex; flex-direction: column; justify-content: center; padding: 0 4%; }
  section.toc_b > ol { position: static !important; width: 55% !important;
    margin-left: 35% !important; line-height: 1.5 !important; font-size: .9em !important;
    list-style: none !important; counter-reset: toc; }
  section.toc_b ol li { counter-increment: toc; margin: .3em 0;
    position: relative; padding-left: 2.2em; }
  section.toc_b ol li::before { content: counter(toc);
    position: absolute; left: 0; top: 0; width: 28px; height: 28px;
    background: var(--color-much); border-radius: 50%; color: #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-family: var(--font-family-title); transition: transform .3s ease; }
  section.toc_b ol li:hover::before { transform: rotate(360deg); }
  section.toc_b header { text-align: center; width: 20%; left: 8%; top: 25%;
    font-size: var(--font-size-2-3); color: var(--color-title);
    font-weight: bolder; line-height: 200%; letter-spacing: 3px; }
  section.toc_b header img { width: 70%; filter: brightness(1000%) grayscale(100%); padding-top: 30px; }

  .var-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; }
  .var-grid .right-col { background: rgba(255,255,255,.1); border-radius: 12px;
    padding: 1rem; text-align: center; }
  .var-grid .right-col h4 { margin: 0 0 .5rem 0; color: var(--color-much); font-size: 1.2em; }
  .var-grid .arrow { font-size: 1.1em; margin: .4rem 0; }
  .var-grid .model-badge { display: inline-block; background: var(--color-much);
    color: #fff; border-radius: 20px; padding: .3rem .8rem; margin: .2rem; font-size: .9em; }

  section.lastpage { background: linear-gradient(to bottom, #fff 20%, var(--color-coverbg) 20% 60%, #fff 55%);
    padding: 0; display: grid; grid-template-rows: 80% 20%; grid-template-areas: "heading" "icons"; }
  section.lastpage h6 { grid-area: heading; height: 100%; width: 100%;
    align-content: center; justify-content: center; text-align: center;
    font-family: var(--font-family-title); font-size: var(--font-size-1);
    color: #fff; display: grid; padding: 0; margin: 0; }
  section.lastpage .icons { grid-area: icons; }
  section.lastpage div > ul { font-family: var(--font-family-main);
    width: 100%; display: grid; grid-template-columns: 1.8fr 1fr 1fr;
    gap: 5em; align-content: center; list-style: none; }
  section.lastpage ul > li > ul > li { margin-left: -120px; list-style: none; }
  section .fa-envelope, section .fa-weixin, section .fa-house,
  section .fa-phone-volume {
    border: 2px solid; padding: 10px; border-radius: 50%; font-size: 1.2em; }
---

<!-- ════════════════════════════════════════════════ -->
<!-- 前 10 页：正常流程完整演示（1 → 17）              -->
<!-- ════════════════════════════════════════════════ -->

<!-- p1 · cover_c · 主封面 -->
<!-- _class: cover_c -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Research on the Impact of Founding Team
## Occupational Background Diversity
### on Early-Stage Financing Performance

**Master of Science**  
Presented by: **xx**  
Supervisor: **Prof. x CAI**  
May 30, 2026

---
<!-- p2 · toc_b · 目录 -->
<!-- _class: toc_b -->
<!-- _paginate: false -->
<!-- _footer: '' -->

1. [Research Background & Significance](#research-background--significance)
2. [Research Methods](#research-design)
3. [Results & Analysis](#results--analysis)
4. [Conclusion & Future Work](#conclusion--future-work)
5. [Acknowledgements](#acknowledgements)

---
<!-- p3 · trans · 章节过渡 -->
<!-- _class: trans -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Research Background & Significance
## 研究背景与意义

---
<!-- p4 · cols-2-73 · 章节大纲 -->
<!-- _class: cols-2-73 -->

## Outline: Research Background

<div class="limg">
  ![w:420](https://mytuchuang-1303248785.cos.ap-beijing.myqcloud.com/picgo/202309221010523.png)
</div>

<div class="rdiv">

- 1.1 Research Background
- 1.2 Literature Review
- 1.3 Research Gaps
- 1.4 Hypothesis Development
- 1.5 Research Contributions

</div>

---
<!-- p5 · cover_e · 封面变体 -->
<!-- _class: cover_e -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Many startups fail due to a lack of early funding
### *The difference between success and failure can be very narrow*

- Early-stage investing: **betting on the team, not just the idea**
- Information asymmetry → hard for VCs to assess true potential
- **Occupational background diversity** = observable proxy signal
- This signal mitigates information asymmetry and conveys quality
- Yet diversity also brings **coordination costs** — a trade-off

---
<!-- p6 · pin-3 · 三区布局（上图 + 下文） -->
<!-- _class: pin-3 -->

## Research Significance

<div class="tdiv">

> **Theoretical**  
> · Extends team diversity research from established firms to entrepreneurial ventures  
> · Advances Signaling Theory from single-signal to composite-signal mechanisms  
>
> **Practical**  
> · For entrepreneurs: team composition + stage-specific strategies  
> · For investors: diversity as an evaluation indicator across stages  
> · For policymakers: foster diverse ecosystems

</div>

<div class="limg">![h:240](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/9258/images/15b5c81-fbb-f61d-ff8e-8386f035a4b_4fa90c08-8a35-4505-afb6-380a9ca098b3.jpg)</div>
<div class="rimg">![h:240](https://ts3.tc.mm.bing.net/th/id/OIP-C.1qIoPMZ3LkGBM1AR21n09AHaEJ)</div>

---
<!-- p7 · cols-3 · 三栏并列 -->
<!-- _class: cols-3 -->

## Literature Review

<div class="ldiv">

#### Signaling Theory
*Spence (1973)*

Education / Experience  
↓  
Quality signal  
↓  
Mitigates information asymmetry

</div>
<div class="mdiv">

#### Upper Echelons Theory
*Hambrick & Mason (1984)*

TMT characteristics  
↓  
Cognitive foundations  
↓  
Strategic choices / Performance  
↓  
Heterogeneity enhances decision quality

</div>
<div class="rdiv">

#### Human Capital Theory
*Becker (1964)*

Education / Experience / Skills  
↓  
Knowledge stock  
↓  
Diversity → Competitive advantage

</div>

---
<!-- p8 · col1_ol_sq fglass · 方块编号列表 -->
<!-- _class: fglass col1_ol_sq -->

## Research Gaps

- Prior studies focus on **single diversity dimensions** (e.g., education only), lacking a multi-dimensional framework.
- **Limited evidence** on how diversity affects **different funding stages** (Angel vs. Series A).
- Financing performance research largely emphasizes **funding amount**, while **funding speed and success rate** receive insufficient attention.
- Most signaling studies examine **individual-level single signals**, with little testing of **team-level composite signals**.

---
<!-- p9 · cols2_ul_ci fglass · 双栏圆编号（1/2） -->
<!-- _class: cols2_ul_ci smalltext fglass -->

## Hypotheses Development (1/2)

<div class="ldiv">

- **H1a:** Professional background diversity positively influences angel-round funding amount.
- **H2a:** Professional background diversity negatively influences angel-round funding speed.

</div>
<div class="rdiv">

- **H1b:** Professional background diversity positively influences Series A funding amount.
- **H2b:** Professional background diversity negatively influences Series A funding speed.

</div>

---
<!-- p10 · cols2_ul_ci fglass · 双栏圆编号（2/2） -->
<!-- _class: cols2_ul_ci smalltext fglass -->

## Hypotheses Development (2/2)

<div class="ldiv">

- **H3:** A core entrepreneurial hub positively moderates the diversity → angel funding amount relationship.
- **H4:** Angel-round financing experience positively moderates the diversity → angel funding amount relationship.

</div>
<div class="rdiv">

- **H5:** Professional background diversity positively influences the probability of Series A success.
- **H6:** High-tech industry negatively moderates the diversity → Series A success relationship.

</div>

<!-- ════════════════════════════════════════════════ -->
<!-- 后 7 页：每种布局 1 个示例                        -->
<!-- ════════════════════════════════════════════════ -->

---
<!-- p11 · col1_ol_ci fglass · 大圆编号列表（新布局） -->
<!-- _class: fglass col1_ol_ci -->

## Research Contributions

1. **Extension of context and signal dimensions**  
   Extends team diversity research from established firms to early-stage financing; advances signaling theory from single signals to composite signals.

2. **Multi-dimensional financing performance & contextual mechanisms**  
   Examines diversity effects on funding amount, speed, and success rate; introduces three moderators and reveals their stage-specific patterns.

---
<!-- p12 · cols-2 · 两栏并列（新布局） -->
<!-- _class: cols-2 -->

## Outline: Research Methods

<div class="limg">![w:420](https://mytuchuang-1303248785.cos.ap-beijing.myqcloud.com/picgo/202309201154535.png)</div>

<div class="rdiv">

- 2.1 Data Source & Sample Selection
- 2.2 Variable Measurement
- 2.3 Model Specification
- 2.4 Implementation & Toolchain

</div>

---
<!-- p13 · 默认（无 class）· 标题 + 正文 + 大图（新布局） -->
<!-- _paginate: true -->

## Data Processing Flow

下图展示从原始数据到分析样本的关键步骤，包括缺失值填补、多样性计算、调节变量构建，以及三个融资结果的分支模型。

![w:900](https://mermaid.ink/img/pako:eNqFkFFvmzAUhf-K5adOIxnGBAKaKpHQSpMSbUr2NOiDCzdgCWxkm7VZlP8-QxaVtA_zk4_93XvPPSdcyBJwjA-NfClqpgza7HKB7NH9c6VYV6MNHAzK1rJtpUA_lCxAay6qpws2nJIrKAy33z9Xb69JtmMvKGWGPaHZ7B6tskfeGFDoM_rWdr2BSYfVSKyzlP8Gpbk5WmhrnSlmpNITcD2CaXaXiAoatJO9KL8-qy_3gRMR-mlCpiP5kN3tQXHQKBkx4nhRdMVAlLl4t-2OV7VddxjeoESw5qi5_u-uW5J93-zHCY_WkY0HJa31ZiaVW8-G-HrD7DuAcorQbCMrrg0vRu5qHe37Yoj9o-_Llltyo7wbRS_q4Yb8pzzs4ErxEsdG9eDgFlTLBolPA5djU0MLOY7ttYQD6xuT41ycbVnHxC8p22ulkn1V4_jAGm1V35XMQMqZDfUNsb5BrYdYcOyFYwscn_ArjmdLOie-RxZuEPn-InLwEcdkQeeu60dhsHR94ocRPTv4zziTzBdLjwbUDd0gjIjv0vNff77PRA?type=png)

---
<!-- p14 · var-grid · 变量/概念对比卡（新布局） -->
<!-- _paginate: true -->

## Variable Measurement (Part 1)

<div class="var-grid">
<div class="left-col">

**Dependent Variables**
- Angel-round funding amount
- Funding speed
- Series A success rate

**Independent Variables**
- Diversity (Z-score composite: functional + industry Blau indices)

**Moderating Variables**
- Core entrepreneurial hubs
- Team angel experience
- High-tech industry

</div>
<div class="right-col">

#### 📐 Conceptual Framework

<div class="arrow">IV (Diversity) → DV (Funding)</div>
<div class="arrow">⤷ Moderators: Hub / Experience / High-tech</div>

---

Signaling theory + Upper echelons + Human capital

</div>
</div>

---
<!-- p15 · smalltext caption · 表格 + 注释（新布局） -->
<!-- _class: smalltext caption -->

## Descriptive Statistics by Funding Round

| Variable | Angel Mean | Angel SD | Series A Mean | Series A SD |
|---|---:|---:|---:|---:|
| log_amount | 12.00 | 1.42 | 14.69 | 1.31 |
| Diversity (Z) | 0.00 | 0.87 | –0.03 | 0.88 |
| is_core_hub | 0.50 | 0.50 | 0.66 | 0.47 |
| angel_experience | 0.34 | 0.47 | 0.58 | 0.49 |
| is_high_tech | 0.52 | 0.50 | 0.54 | 0.50 |
| Company Age | 2.31 | 2.15 | 3.89 | 2.47 |
| Crisis (2008≤) | 0.23 | 0.42 | 0.22 | 0.41 |

<div class="caption">Diversity = Z-score composite (functional + industry + degree Blau indices).</div>

---
<!-- p16 · smalltext · 纯文本小号（参考文献，新布局） -->
<!-- _class: smalltext -->

## References

- Becker, G. S. (1964). *Human capital*. University of Chicago Press.
- Beckman, C. M. (2006). The influence of founding team company affiliations on firm behavior. *AMJ*, 49(4), 741–758.
- Blau, P. M. (1977). *Inequality and heterogeneity*. Free Press.
- Hambrick, D. C., & Mason, P. A. (1984). Upper echelons. *AMR*, 9(2), 193–206.
- McCarthy, P. X., et al. (2023). The impact of founder personalities on startup success. *Scientific Reports*, 13(1), 17200.
- Spence, M. (1973). Job market signaling. *QJE*, 87(3), 355–374.
- van Knippenberg, D., et al. (2004). Work group diversity and group performance. *JAP*, 89(6), 1008–1022.

---
<!-- p17 · lastpage · 结束页（新布局） -->
<!-- _class: lastpage -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Q&A

<div class="icons">
<ul>
<li><i class="fa-solid fa-envelope"></i>
  <ul><li><a href="mailto:xx@foxmail.com">xx@foxmail.com</a></li></ul>
</li>
<li><i class="fa-brands fa-weixin"></i>
  <ul><li>xx_2023</li></ul>
</li>
<li><i class="fa-solid fa-house"></i>
  <ul><li><a href="https://github.com/">github.com/xx</a></li></ul>
</li>
</ul>
</div>
