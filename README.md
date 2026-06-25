# anan_everyday_news

安安每日信息流网页仓库。

核心规则：**仓库根目录只维护当前展示页 `index.html`，用于 GitHub Pages 直接展示今天的新闻；历史内容每天凌晨 1:00 归档到 `archive/YYYY/MM/YYYY-MM-DD.html`。**

## 当前页面

- [今日新闻页](index.html)

## 归档规则

- 当前正在更新的网页永远是：`index.html`
- 每天凌晨 1:00 归档上一天页面到：`archive/YYYY/MM/YYYY-MM-DD.html`
- 归档后重新生成当天新的 `index.html`
- 不再把每天的新闻文件全部堆在仓库根目录
- 不再使用 `daily/`、`afternoon/`、`weekly/`、`monthly/`、`raw/`

## 自动化任务分工

- 08:30：更新 `index.html` 的主简报内容
- 10:30：只提醒喝水，不写入新闻页
- 15:30：只更新 `index.html` 的下午增量内容
- 01:00：归档上一天 `index.html`，并重置当天 `index.html`

## 页面结构

`index.html` 使用固定区块 ID，便于自动化任务定位更新：

```html
<section id="update-log"></section>
<section id="overview"></section>
<section id="top-stories"></section>
<section id="ai-tech"></section>
<section id="freebies"></section>
<section id="games-community"></section>
<section id="devops"></section>
<section id="risk-policy"></section>
<section id="actions"></section>
<section id="afternoon-update"></section>
<section id="media-assets"></section>
```

## 图文并茂规则

- 重要条目优先使用来源链接、项目链接、官方截图、活动页图片或稳定公开图片。
- 本地图片放到 `assets/YYYY-MM-DD/`。
- 不为凑图插入无关图片。
- 每张图附近必须说明来源或用途。

## 去重规则

- 08:30 和 15:30 都必须先读取 `index.html`，再更新对应区块。
- 已经出现过且没有新进展的信息不要重复写。
- 同一事件有新进展时，在原条目里追加“后续更新”，不要另起重复条目。
- 15:30 只写增量，不重发上午内容。

## 目录结构

```text
anan_everyday_news/
├── index.html                     # 当前今日网页，GitHub Pages 首页
├── README.md
├── archive/
│   └── 2026/
│       └── 06/
│           └── 2026-06-25.html    # 每天凌晨 1:00 归档生成
├── assets/
│   └── 2026-06-25/
├── templates/
│   └── index.html                 # 今日网页模板
├── scripts/
│   ├── archive_today.py
│   ├── update_index.py
│   └── check_files.py
├── index/
└── topics/
```

## 索引区

- [2026 年索引](index/2026.md)
- [2026 年 6 月索引](index/2026-06.md)

## 主题索引

主题索引只做跳转，不放全文：

- [AI / Codex / Vibe](topics/ai.md)
- [开发 / 运维 / NAS / 网络](topics/devops.md)
- [游戏 / Steam / Epic / 小黑盒风格](topics/games.md)
- [免费资源 / 薅羊毛](topics/freebies.md)
- [副业 / 信息差](topics/side-hustle.md)
- [Linux.do / V2EX / 社区热议](topics/community.md)
- [国内外新闻 / 趣闻](topics/world-news.md)
