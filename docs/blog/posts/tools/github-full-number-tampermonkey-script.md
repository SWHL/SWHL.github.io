---
title: 让Github  Star、Fork 和 Watching 显示完整数字的油猴脚本
date:
  created: 2026-08-04
authors:
  - SWHL
slug: github-full-number-tampermonkey-script
categories:
  - 工具
tags:
  - Github
---

<!-- more -->

## 引言

自己有个小习惯，早起会看一下开源项目的 Star 是否有变化。这就像发了条朋友圈，总是去看有没有人点赞一样。

写到这里，我感觉这不是一个好习惯，因为会被这些数据裹挟，容易丢了初心。切记!

我发现自己使用的一个油猴脚本（[Github 显示具体 Star 数字](https://greasyfork.org/zh-CN/scripts/391285-github%E6%98%BE%E7%A4%BA%E5%85%B7%E4%BD%93star%E6%95%B0%E5%AD%97)）失灵了。每次我随意打开一个 [RapidOCR](https://github.com/RapidAI/RapidOCR) 仓库，右上角 Star 仍然显示 `7.4k`，正常应该是具体的 `7368`

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-04_09-46-20-df5c46e3.jpg)

期望的是：

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-04_09-47-14-66613eda.jpg)

## 修复

油猴脚本就是一段 javascript 代码，当我们打开网页时，这段代码会事先执行，获取网页源码，然后先执行这段油猴脚本对网页内容做定制化，最后渲染出来，就是我们看到的定制化的网页。

上述失灵问题，我直接将源码扔给 GPT-5.6 Sol，直接接给出了原因和修复后的方案。写这种工具性代码，用大模型来写最合适了，我们很容易验证是否正确。

GPT 给出的失灵原因是：Github 改版，页面结构和计数数据来源改变导致。

旧脚本依赖两个假设：

```js linenums="1"
headerNode.querySelectorAll('.Counter')
node.getAttribute('title')
```

以前 Star/Fork 数字使用 `.Counter` 元素，缩写显示为 `31.3k`，同时 `title` 属性中保存着精确数字，例如 `31,290`。

现在 GitHub：

- 不再使用 `.Counter`，改成了 React 组件生成的 `[data-component="CounterLabel"]`
- 不再把精确数字放在 `title` 属性中
- 可见 DOM 里通常只有 `31.3k`
- 精确数字被放到了页面内嵌的结构化 JSON 中，例如：

```json linenums="1"
{
  "stargazerCount": 31290,
  "forksCount": 5091,
  "watcherCount": 399
}
```

因此旧脚本找不到 `.Counter`；即使找到类似节点，下面这行也可能因为 `title` 为 `null` 而报错：

```js
node.getAttribute("title").replace(/,/g, '')
```

此外，原来的监听器只观察 `main` 的直接子节点：

```js
observer.observe(main, {
    childList: true
})
```

GitHub 现在大量使用 React 和 Turbo 局部更新，计数可能在更深层节点更新，甚至整个 `main` 被替换，所以旧监听器也捕获不到。新版脚本同时修复了选择器、精确数字来源和无刷新导航监听。

## 最终源码

我已经将源码放到了 [Greasy Fork](https://greasyfork.org/zh-CN/scripts/589799-github-%E6%98%BE%E7%A4%BA%E5%AE%8C%E6%95%B4-star-%E6%95%B0%E5%AD%97) 上，有需要的小伙伴，可以安装使用。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-04_09-58-15-66977baf.jpg)
