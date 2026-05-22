---
title: MkDocs Material 集成 Ask AI 教程
date:
  created: 2026-04-10
authors:
  - SWHL
slug: mkdocs-material-ask-ai-integration
comments: true
categories:
  - 工具
tags:
  - mkdocs-material
hide:
  - toc
---

<!-- more -->

## 调研工具

### Kapa.ai

官网：https://www.kapa.ai/

![2026-04-10_20-58-03](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-04-10_20-58-03.jpg)

尝试注册账号无响应。看了一下，对开源项目有专门计划（https://docs.kapa.ai/kapa-for-open-source）支持，需要填写申请表。

![2026-04-11_16-22-23](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-04-11_16-22-23.jpg)

### Biel.ai

官网：https://biel.ai/

![2026-04-10_20-59-03](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-04-10_20-59-03.jpg)

14 天免费试用，到期必须付费才可用。

### mkdocs-gemini-chatbot

官网：https://github.com/vimmoos/mkdocs-gemini-chatbot

集成 Google Gemini API Key，可以提供自己的 Key。我尝试部署了一下，发现送到接口中的内容很容易超出上下文长度限制，尤其是站点内容较多时。

这个插件基本功能都有了，就是需要进一步打磨才可用。

## 集成示例

我以 Biel.ai 来讲如何集成。下面视频讲解了如何注册 Biel.ai 账号，并创建项目。

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
  <iframe
    src="https://player.bilibili.com/player.html?bvid=BV1Y4DyBgERW&page=1&danmaku=0"
    scrolling="no"
    frameborder="0"
    allowfullscreen
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
  </iframe>
</div>

之后在 `overrides/main.html` 中添加上面复制到的 HTML Code 即可。

```html
{% block extrahead %}
<!-- Load the widget -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/biel-search/dist/biel-search/biel-search.css">
<script type="module" src="https://cdn.jsdelivr.net/npm/biel-search/dist/biel-search/biel-search.esm.js"></script>

<!-- Add the widget -->
<biel-button project="g6gmcrnpnb" header-title="Biel.ai Chatbot" button-position="bottom-right"
    modal-position="sidebar-right" button-style="dark">
    Ask AI
</biel-button>

{% endblock %}
```
