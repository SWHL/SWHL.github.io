---
title: 使用 Raycast Snippets 指南
date:
  created: 2026-04-14
authors:
  - SWHL
comments: true
slug: guide-to-using-raycast-snippets
categories:
  - 工具
tags:
  - Raycast
hide:
  - toc
---

<!-- more -->

## 引言

最近从 Alfred 5 换到了 Raycast，本着只用自己必须功能的想法，我就自动忽略了 Raycast 内置的一些功能，有点舍近求远了。我发现其 Snippets 功能正是我需要的。

一直以来，我在使用搜狗输入法，最大的原因是它的自定义短语功能。我自定义大量的常用短语，像不同格式的当前日期、常用的符号等等。

## Snippets 是做什么的？

Snippet 单词意思为：代码片段，就是咱们日常常用的一些文本。

例如，我们如果在批注学生作业，需要一直要写一样的评语：“今天你的表现不错，继续加油呀！”全班有 50 个学生，我们就要打 50 遍，当然，可以复制粘贴。但是下一次呢？

这时，我们就可以将这句话保存为 snippet，直接快速输入相关缩写，就可以快速输入。

进一步，我们可以设置带有动态变量的 snippet。例如，我们可以设置“获得指定格式当前日期”的 snippet。平时用到的日期可能有很多格式：

```text linenums="1"
20260415
2026-04-15
04-15-2022 13:44
```

我们可以设置 `/rq`（日期拼音两个首字母）来快速输入当前日期。

## 怎么设置和同步？

视频主要讲解怎么添加、查找和使用 Snippets，以及怎么导入导出 Snippets 到其他设备。

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
  <iframe
    src="https://player.bilibili.com/player.html?isOutside=true&aid=116415038364950&bvid=BV1BLdaBZEB6&cid=37561109520&p=1"
    scrolling="no"
    frameborder="0"
    allowfullscreen="true"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
  </iframe>
</div>

## 常用动态输入变量

官网文档：https://manual.raycast.com/dynamic-placeholders

`{cursor}`: 光标位置。可以通过这个变量来决定插入后，将光标放在哪里。后续 Raycast 应该会支持 Tab 键，类似 VSCode 中，通过 Tab 键，光标跳到指定的位置，那样会更加灵活。

`{date format="yyyy-MM-dd" offset="-5d"}`: 日期格式与偏移混合使用。当前日期往前移 5 天。
