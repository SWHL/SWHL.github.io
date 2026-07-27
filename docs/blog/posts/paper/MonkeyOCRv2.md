---
title: 论文速读：MonkeyOCRv2
date:
  created: 2026-07-27
authors:
  - SWHL
slug: monkeyocrv2
categories:
  - 论文阅读
tags:
  - 论文速读
---

<!-- more -->

> 系列说明：本文为快速阅览笔记，侧重梳理方案骨架与技术演进关系，不深入实现细节；后续若开展相关方向研究，再补充精读分析。

论文地址：https://arxiv.org/abs/2607.11562

源码：https://github.com/Yuliang-Liu/MonkeyOCRv2

## 现存痛点

当前视觉 encoder 预训练都是在较为通用的自然图像上训练得来的。这些对于文档类图像适配较差，尤其是密集文本和一些需要精细字符笔画来确定内容的场景。

## 核心思路

1. 提出了 MonkeyDocv2——1.13 亿，涵盖 17 种语言的文档类图像预训练集。
2. 提出新的训练思路联合训练 image-to-text 生成和 pixel-level 重建。前者用于对齐语义信息，后者用于保持字符笔画和版面细节。

## 整体架构

这篇工作核心构建了一个文档类的数据集，并在此基础上训练了一个适配文档类图像的 encoder，并为此证明了这个 encoder 的通用性。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-27_11-49-39.jpg)

## 简要评价

优势：弥补了文档类 pretrain 数据集的缺陷，encoder 具有一定的通用性，促使模型关注整体和局部。工作值得推荐。

局限：不同任务需要做一定的 fine-tuned。
