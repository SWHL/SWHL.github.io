---
title: Codex（ChatGPT 桌面版）支持SSH连接远程服务器
date:
  created: 2026-08-03
authors:
  - SWHL
slug: TODO
categories:
  - 工具
tags:
  - ChatGPT
---

<!-- more -->

一直以来，我用 Codex 一般都只是服务器端用 Codex cli 版，mac 端用桌面版。这样有个问题：服务器端我要一直决定是否同意其某项改动，换句话说就是需要一直审批，一直按回车。效率完全卡在是否及时按回车同意了。

我也调研了好多命令，看看是否可以减少我的审批，变得更加自主一些。我查到可以用下面命令：

```bash linenums="1"
codex --sandbox workspace-write --ask-for-approval never
```

遗憾的是，这个命令在运行到容器中的服务器不管用。因为本身没有那么大的权限。

上周同事也遇到和我同样的困惑，他告诉了我一个好办法：用 **连接** 功能来远程连接服务文件，这样在桌面端这里就可以设置 **“替我审批”** 模式了。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-03_09-36-05-8991a13d.jpg)

