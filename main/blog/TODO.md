---
title: "VSCode Remote SSH插件不要安装v0.126.0"
canonical_url: "https://swhl.github.io/main/blog/TODO/"
markdown_url: "https://swhl.github.io/main/blog/TODO.md"
description: "VSCode 的远程连接插件 Remote-SSH 在升级到 v0.126.0 时，会遇到以下不能连接问题："
---

# VSCode Remote SSH插件不要安装v0.126.0

> Canonical URL: https://swhl.github.io/main/blog/TODO/
> Markdown URL: https://swhl.github.io/main/blog/TODO.md

<!-- more -->

VSCode 的远程连接插件 Remote-SSH 在升级到 v0.126.0 时，会遇到以下不能连接问题：

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-26_10-26-11-012a2ffd.png)

我在 Remote-SSH 仓库 issue 中也看到已经有小伙伴遇到了同样的问题：[#11810](https://github.com/Microsoft/vscode-remote-release/issues/11810)

目前解决方案是降到版本到 v0.124.0。安装指定版本方法如下：

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-26_10-28-32-832e570c.jpg)

选择 v0.124.0 即可。

