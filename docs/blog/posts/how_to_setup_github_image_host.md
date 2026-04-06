---
title: 如何使用Github作为博客图床？
date:
  created: 2026-04-05
authors:
  - SWHL
slug: how-to-setup-github-image-host
comments: true
hide:
  - toc
---

<!-- more -->

## 引言

近来，一直有写周报，遇到一个问题：想将相关资源附上对应的配图。因为有配图，文章更加生动一些。

可是图像存储空间一般是比较大的，如果放到当前仓库，该仓库在短时间内会迅速膨胀，难以维护。

## 最终方案

我有两个需求：博客需要满足国内和国外的需求。思来想去，确定了两条路线：

- 国内：通过公众号来分发，图像会自动托管到公众号服务上。
- 国外：直接建立转有 Github 仓库，来作为图床。

## Github 作为图床

Step 1: VSCode 安装 PicGo 插件

安装 PicGo 插件后，其他地方就不需要安装 PicGo 软件了。

![2026-04-05_21-41-13](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-04-05_21-41-13.jpg){.img1}

Step 2: 配置 PicGO

settings.json 中写法：

```json
"picgo.picBed.current": "github",
"picgo.picBed.github.branch": "main",
"picgo.picBed.github.repo": "SWHL/SWHL.github.io-Assets",
"picgo.picBed.github.token": "xxxxxxxxxxxxxxxxxxxxxxxx",
"picgo.picBed.github.path": "images/2026/",
```

这里需要配置一个 Token，来授予 PicGO 读写指定仓库的权限。

![2026-04-06_07-54-11](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-04-06_07-54-11.jpg){.img1}

只需要给选定的仓库读写权限即可，其余权限都不用给。

![2026-04-06_07-56-05](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-04-06_07-56-05.jpg){.img1}

Step 3：自动上传并返回对应图像 markdown url

我是使用 PixPin 工具截图并将图像复制到剪贴板，之后按快捷键：`Cmd + Alt + U`，就会自动上传图像到指定仓库，并返回对应的 markdown url。


