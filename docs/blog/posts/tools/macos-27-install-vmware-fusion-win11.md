---
title: macOS 27 安装 VMware Fusion 和 Win11
date:
  created: 2026-09-19
authors:
  - SWHL
slug: macos-27-install-vmware-fusion-win11
categories:
  - 工具
tags:
  - macOS
---

<!-- more -->

### 引言

9 月 15 号，苹果发布了 macOS 27 系统。我在自己本上升级到这个版本。当使用 Parallel Desktop 时，发现打不开了。查阅资料才发现，Parallel Desktop 27 版本才能在 macOS 27 上运行。

无奈，暂时先放弃这个 Paralle Desktop 软件，即使体验很好。

很久之前，我就知道了 VMware Fusion。在 2023 年博通收购 VMware 之后，在 2024 年 5 月宣布 Workstation Pro, Fusion Pro 个人使用免费。同年 11 月 Workstation Pro, Fusion Pro 全部免费，个人 / 教育 / 商用都可以免费用，不再售卖付费许可证。

现在，可以重新来考虑这个软件了。经过两天的折腾，VMware + Win11 总算都跑通了。下面是我的一些经验，希望可以帮助到大家。

### 在哪里下载安装包？

下载地址：[link](https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Fusion&displayGroup=VMware+Fusion+26H1&freeDownloads=true&tab=Products)

注意：需要注册博通账号。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-09-19_20-14-59-896f8b8e.jpg)

### Win11 镜像在哪里下载？

官网下载地址：https://www.microsoft.com/zh-cn/software-download/windows11

⚠️注意：我的电脑是 Apple M1 Pro，因此下载的是 Arm64 的。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-09-19_20-17-22-9c51651c.jpg)

### 安装 Win11

现在，VMware Fusion 已经安装好，Win11 ISO 已经下载好，ISO 大概 7～8 GB，注意根据官网给出的 SHA256 校验是否下载的完整。

在新建并选择 iso 镜像后，一直进不去系统安装程序，这时需要选择一下从 CD/DVD 启动，就可以了。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-09-19_20-24-48-f39e9ca2.jpg)

### 如何让系统自动适配屏幕？

需要安装 VMware Tools 来实现。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-09-19_20-25-55-3da26d83.jpg)

安装步骤：

1. 看 Mac 顶部菜单栏，找到 **虚拟机 (Virtual Machine)** → 点 **安装 VMware Tools**
2. Windows 里面会弹出一个 DVD 盘符（VMware Tools 光盘），打开，运行 `setup.exe`
3. 一路【下一步】，选择 **典型安装**，等待安装完成，**重启 Windows 虚拟机**。

### 日常使用建议

- 用完之后，先正常关闭 Win11 系统，再关闭 VMware Fusion 软件。一般不选挂起，因为 Win11 系统挂起，再启动也不会快多少。
- 虚拟机内存选 6 GB，基本够用。默认是 4 GB。我的电脑是 16 GB。
- 清理 Win11 中不用的软件，关闭不用的更新，具体可以问问大模型。只安装自己必须的有限软件。毕竟虚拟机就是一个临时使用的场景。
