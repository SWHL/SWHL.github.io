---
title: Github Star History 趋势图工具推荐
date:
  created: 2026-08-04
authors:
  - SWHL
slug: github-star-history-tools-recommendation
categories:
  - 工具
tags:
  - Github
---

<!-- more -->

## 引言

一直以来，在 RapidOCR 仓库中，用来显示 Github Star History 的都是 [star-history](https://www.star-history.com/) 网站提供的趋势图。

但是前些时间，发现仓库 README 中 Star History 不显示了。自己追查了一下原因，看到 Star History 网站的公告：[GitHub Has Restricted Access to Star Data](https://www.star-history.com/blog/github-stargazer-api-restriction)

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-04_09-20-55-de7d7e35.jpg)

Star History 网站给出了解决方案：提供一个令牌给它们，它们进行加密，等获取 Star 数据时，先读取令牌，再获取 Star 数据。具体文档可以参见：[How to embed the chart in your README](https://www.star-history.com/blog/how-to-use-github-star-history#how-to-embed-the-chart-in-your-readme)

## github-star-tracker

我之前并未看到这个通告，于是就去问了一下豆包，发现一个基于 Github Action 的项目也是做仓库 Star 趋势显示的：[github-star-tracker](https://github.com/fbuireu/github-star-tracker)
。

它是一个 GitHub Action，可定期跟踪你所有仓库的星标数量，生成包含图表和徽章的可视化报告，并在检测到更改时发送通知的项目。

使用这个项目产生的 Star History 趋势图：

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-04_09-27-30-3e2e3fd2.jpg)

这个工具会生成一个名为 [**star-tracker-data**](https://github.com/RapidAI/RapidOCR/tree/star-tracker-data) 的分支，用于详细记录 Star 的变化，整体使用起来还是比较友好的。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-04_09-29-06-3f80ca1f.jpg)

我用的 `star-tracker.yml` 如下：

```yml linenums="1"
name: Track Stars

on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight
  workflow_dispatch:

permissions:
  contents: write

jobs:
  track:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
      - uses: fbuireu/github-star-tracker@v1
        with:
          github-token: ${{ secrets.STAR_TRACKER_TOKEN }}
          visibility: 'public' # public | private | all | owned
          only-repos: 'RapidOCR'
```

## 写在最后

从原理上来看，和 Star History 网站说的一样，也是生成了一个令牌，这样才能正常获取到 Star 数。但是这个工具有着更为详细的记录和统计信息。这使得我们可以更加全面窥见仓库 Star 变化趋势。

有着同样困扰的小伙伴，推荐使用这个项目来生成 Star 趋势图，再也不用担心哪天这个图不显示了。
