---
title: "关于 Raycast for Mac v2 的使用体验"
canonical_url: "https://swhl.github.io/main/blog/raycast-for-mac-v2-usage-experience/"
markdown_url: "https://swhl.github.io/main/blog/raycast-for-mac-v2-usage-experience.md"
description: "最近发现了 Raycast 在 Mac 平台上出了 v2 beta 版本。相关更新链接：What's New in Raycast for Mac v2"
---

# 关于 Raycast for Mac v2 的使用体验

> Canonical URL: https://swhl.github.io/main/blog/raycast-for-mac-v2-usage-experience/
> Markdown URL: https://swhl.github.io/main/blog/raycast-for-mac-v2-usage-experience.md

<!-- more -->

最近发现了 Raycast 在 Mac 平台上出了 v2 beta 版本。相关更新链接：[What's New in Raycast for Mac v2](https://manual.raycast.com/new-in-v2)

作为 Raycast 的新进用户，我使用其功能相对克制，主要是下面几点：

- Applications: 快速打开指定 App
- Calculator: 计算器
- File Search: 搜索本地文件
- Quicklinks: 快速打开指定关键词的谷歌搜索 / 百度搜索界面
- Snippets: 快捷短语。这个是我使用 Raycast 的主要原因
- Window Management: 窗口分屏
- Browser Bookmarks: 快速搜索浏览器书签并打开

Raycast 的 AI 功能、云同步、剪贴板、转录等功能都不在我核心诉求上。因为这些功能有些是有其他小软件替代，有些是我用不到。

还有一点是：用不用注册 Raycast 账号。经过我的调研，发现没有必要。注册免费账号会有一些自动同步的功能，最大卖点是不同设备自动同步设置。这一点我是通过手动导出配置文件到坚果云同步目录下来做到不同设备之间的同步的。因此，我觉得就没必要了。

这篇文章，我想探讨的是：升级 v2 的必要性。从其官方博客：[A Technical Deep Dive Into the New Raycast](https://www.raycast.com/blog/a-technical-deep-dive-into-the-new-raycast) 中总结来说：

v2 是 Raycast for Mac 有史以来最大重构：保留 Swift 原生外壳，把 UI 换成 Web、核心性能逻辑用 Rust 重写；界面适配 Tahoe 玻璃态，文件搜索彻底摆脱 Spotlight、主搜索直接混排文件；AI 全面升级；代价是内存更高、目前只支持 Tahoe。

从更新情况来说，我更倾向于认为：这次更新为 Raycast 长远发展铺平了道路，算是一个里程碑了。我个人比较在意的是 Snippets 的功能。因为其他功能都还好，个人不是十分倚重。

v1 版的 Snippets，在有触发符号时，存在不能触发情况。例如：`//rq`，`rq` 前面有两个 `//` 时，v1 大概率不能正确解析为：`/20260611`。但是 v2 却可以。

从 v2 的更新日志中，我找到了 Snippets 部分更新说明：（[Snippets](https://manual.raycast.com/snippets)）

- 增加了 Tag 功能。可以为每一条 snippets 指定标签，方便管理。
- 增加了一个新的 `{calculator}` 动态占位符。

从 v2 的每个版本的更新日志中，我发现更多的是：优化了 Snippets 匹配的准确性。这一点是我最看重的。从我这几天体验下来，的确会更好一些。

除上面之外，还有一点：不同设备导入和导出配置没有了失效或丢失的问题了。这一点让我感觉也更好了。

UI 的适配感觉也挺好的。毕竟这是一个每天用的频率挺高的软件。

如果你也和我有一样的类似诉求，可以考虑升级到 v2 版，注意 v2 版对 macOS 系统有要求，必须是 macOS Tahoe 版本。

