---
title: "mkdocs-material-format-convert:用于把 Material for MkDocs 扩展 Markdown 语法降级为更通用的 Markdown的小工具"
canonical_url: "https://swhl.github.io/main/blog/mkdocs-material-format-convert/"
markdown_url: "https://swhl.github.io/main/blog/mkdocs-material-format-convert.md"
description: "我经手的所有开源项目的文档站点基本都使用了 mkdocs-material 文档主题搭建，包括 RapidOCR, PaddleOCR, LabelConvert 和当前的博客站点等等。"
---

# mkdocs-material-format-convert:用于把 Material for MkDocs 扩展 Markdown 语法降级为更通用的 Markdown的小工具

> Canonical URL: https://swhl.github.io/main/blog/mkdocs-material-format-convert/
> Markdown URL: https://swhl.github.io/main/blog/mkdocs-material-format-convert.md

<!-- more -->

## 缘起

我经手的所有开源项目的文档站点基本都使用了 [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) 文档主题搭建，包括 RapidOCR, PaddleOCR, LabelConvert 和当前的博客站点等等。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-15_21-36-22.jpg)

选择这个文档主题经历了很多波折。之前我一直在寻觅各种文档主题，包括 Hugo, Hexo 和 Jekyll 框架。最后才发现了 mkdocs-material 这个主题。前面这 3 个框架下都有丰富的主题模板，最终效果看起来都很惊艳。

但是从可扩展性、易维护性来看，没有一个可以和 mkdocs-material 能比的。个人观点，不喜勿喷。

虽然 mkdocs-material 作者在面临诸多难点难以解决时，新起了 [Zensical](https://zensical.org/) 项目。这个项目与 mkdocs-material 可以无缝迁移。但是考虑到新的项目插件支持并不完善，需要假以时日了。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-15_21-43-38.jpg)

言归正传，我很多博客都是在 mkdocs-materail 主题框架写的，有很多这个框架特有的写法。这些写法并不是通用的 markdown 语法，但是我想将博客同步到其他平台上，例如 CSDN、知乎和公众号上，这些特殊写法就有些不兼容了。

于是就有了今天的这个工具：mkdocs-material-format-convert。

## mkdocs-material-format-convert

简介：用于把 Material for MkDocs 扩展 Markdown 语法降级为更通用的 Markdown。

项目地址：https://github.com/SWHL/mkdocs-material-format-convert

在线地址：https://swhl.github.io/mkdocs-material-format-convert/

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-15_21-46-34.jpg)

整个项目借助 Codex，仅使用 JavaScript + CSS + HTML 搭建而成。之所以选择这 3 个实现，是因为：

- 功能本身并不复杂，最简单的实现最容易维护
- 想要部署到 Github Pages 上，Github Pages 上仅支持静态页面

目前可以手动将写好的 mkdocs-material 格式的文档源码粘贴到输入框中，右侧就是格式化后的通用 markdown 源码。这样就可以快速分发了。

欢迎大家使用。

