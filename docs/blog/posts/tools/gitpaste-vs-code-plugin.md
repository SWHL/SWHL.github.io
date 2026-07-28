---
title: GitPaste——vs-picgo的轻量平替
date: 2026-03-03
authors:
  - SWHL
slug: gitpaste-light-alternative-to-vs-picgo
categories:
  - 工具
tags:
  - VS Code
---

<!-- more -->

## 缘起

自己一直在使用 [vs-picgo](https://github.com/PicGo/vs-picgo) vscode 插件用于插入日常写文章所用的一些图。这个插件在本地上运行没啥问题。

但是有时我需要在网页端直接插入图像，不想通过本地。这种情况下，vs-picgo 就不行了，其依赖 PicGo，不满足在 web vs-code 中运行的条件。

我想了一下 vs-picgo 做的事情并不复杂，我这里可以直接用 GPT-5.6 来实现一波，着重支持 web vs-code。

于是就有了：GitPaste。

## GitPaste

项目地址：https://github.com/SWHL/GitPaste

![2026-07-28_16-48-40-e7ecba49](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-28_16-48-40-e7ecba49.jpg)

### 安装方法

VSCode 插件市场中搜索：GitPaste，点击安装即可。

marketplace: https://marketplace.visualstudio.com/items?itemName=SWHL.gitpaste

### 使用方法

1. 在命令面板运行 **GitPaste: Configure GitHub Repository**。
2. 按 `owner/repository` 格式填写仓库，然后填写分支和图片目录。
3. 使用 VS Code 内置 GitHub 登录，或者提供具有仓库 **Contents: Read and write** 权限的细粒度 PAT。
4. 复制图片并打开 Markdown 或 MDX 文档。Web 版使用 `Ctrl+V` 或 `Cmd+V`；桌面版使用 `Ctrl+Alt+U` 或 `Cmd+Alt+U`。

PAT 会保存在 VS Code `SecretStorage` 中，不会以明文配置写入 `settings.json`。
细粒度 PAT 的 **Resource owner** 必须是目标仓库所有者，**Repository access** 必须包含目标仓库。组织仓库还可能要求管理员批准令牌或完成 SSO 授权。
选择 PAT 后，GitPaste 不会在令牌暂时不可用时静默切换到 VS Code GitHub 登录；它会要求重新输入 PAT。

### 快捷键

| 功能 | Windows/Linux | macOS |
| --- | --- | --- |
| 从剪贴板上传（桌面版） | `Ctrl+Alt+U` | `Cmd+Alt+U` |
| 粘贴并上传图片（Web 版） | `Ctrl+V` | `Cmd+V` |
| 选择图片上传 | `Ctrl+Alt+E` | `Cmd+Alt+E` |
| 从路径或 URL 上传 | `Ctrl+Alt+O` | `Cmd+Alt+O` |

需要复制图片本身，而不是图片地址。Web 版中，`Ctrl/Cmd+V` 遇到图片时会上传，遇到文字或其他内容时仍执行普通粘贴。由于浏览器只会通过真实粘贴事件提供图片二进制数据，GitPaste 的专用剪贴板快捷键仅用于桌面版。

上传完成后默认插入 GitHub 返回的 `https://raw.githubusercontent.com/...` 原始链接，不经过第三方 CDN。仅在明确配置 `gitpaste.github.publicUrl` 时才使用自定义 URL 模板。

任意 HTTP 图片 URL 的下载会受到来源网站 CORS 策略限制；工作区文件和直接粘贴的图片不受此限制。

### 与 PicGo, vs-picgo 的关系与区别

GitPaste 是基于 MIT 许可证项目
[`PicGo/vs-picgo`](https://github.com/PicGo/vs-picgo) 重写的浏览器兼容扩展。
项目按照 MIT 许可证保留了原作者版权声明，但 GitPaste 是独立项目，并非 PicGo
或 vs-picgo 的官方版本。

| 项目 | 主要定位 | 运行环境 | 存储支持 |
| --- | --- | --- | --- |
| [PicGo](https://github.com/Molunerfinn/PicGo) | 桌面图床上传应用与插件生态 | 桌面应用 | 通过内置上传器和插件支持多种图床 |
| [vs-picgo](https://github.com/PicGo/vs-picgo) | 基于 PicGo 的 VS Code 集成 | 桌面 VS Code 与 PicGo/Node.js 组件 | 使用 PicGo 上传器和配置 |
| GitPaste | 面向编辑器图片粘贴的 VS Code Web Extension | 同一浏览器兼容包运行于 Web 和桌面 VS Code | 当前版本直接使用 GitHub Contents API |

GitPaste 不加载 PicGo 插件，也不读取 PicGo 或 vs-picgo 配置。它使用
`gitpaste.*` 设置，将凭据保存在 VS Code `SecretStorage` 中，并直接调用 GitHub
API 上传。已有的 PicGo 或 vs-picgo 设置需要在 GitPaste 中重新配置。

凭据处理方式是两者一个重要且有意为之的区别。vs-picgo 的 GitHub 上传器要求
在配置文件中填写 token，因此 token 会成为明文配置；GitPaste 则始终将 token
排除在 `gitpaste.*` 设置之外。使用内置 GitHub 登录时，认证由 VS Code 管理；
使用 PAT 时，密钥保存在 `SecretStorage` 中，`settings.json` 只记录所选择的认证方式。

## 写在最后

这个小工具只是从我解决我的小痛点出发而来，因此可能带有一定的个人色彩，但是我会保证这个东西的专业性，即使是 vibe coding 而来的，我这里会逐渐完善它的，毕竟自己每天都要用的。
