---
title: 使用 Raycast 快速在 Obsidian 笔记中搜索笔记
date:
  created: 2026-03-17
  updated: 2026-08-31
authors:
  - SWHL
slug: raycast-with-obsidian
categories:
  - 工具
tags:
  - Raycast
  - Obsidian
links:
  - 从 Alfred 转到 Raycast: blog/posts/alfred_to_raycast.md
---

记录如何配置 Raycast 来快速其窗口中搜索 Obsidian 中的笔记。

<!-- more -->

<figure markdown="span">
  ![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-30_14-53-36-0541bca4.png)
  <figcaption> 配图来自 Google Gemini</figcaption>
</figure>

自己从 Alfred 转到 Raycast，很大一部分原因在于 Raycast 中支持 Obsidian 笔记的快速搜索。

经过一系列实践，先说结论：**部分功能支持，尚不完善，值得期待**。

2026-08-31 update: 我已经提了 [[Obsidian] Add Exact Content Match Navigation](https://github.com/raycast/extensions/pull/30150)，在 Raycast > 2.1.2.0 版本应该集中了。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-31_09-28-20-69f7c2b1.gif)

## 配置和使用

Step 1：Raycast 安装 Obsidian 插件：[Obsidian](https://www.raycast.com/marcjulian/obsidian)。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-30_14-54-29-f10d6beb.png)

Step 2: 按照下图来配置 Obsidian 插件。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-30_14-54-46-43235e7f.png)

Step 3: 开始使用。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-30_14-55-01-1880a0a4.png)

## 不足之处

在开启了 **Search content** 后，Raycast 会自动定位到关键词所在 md 文件，并打开。但是不会自动跳转到关键词所在位置。

我搜索了全网，发现在 [obsidian-raycast](https://github.com/marcjulianschwarz/obsidian-raycast) 上有关于这个的讨论 （issue [#83](https://github.com/marcjulianschwarz/obsidian-raycast/issues/83)），但是已经好久不更新了。因此，我提了新的 issue：[#26396](https://github.com/raycast/extensions/issues/26396)。

敬请期待。
