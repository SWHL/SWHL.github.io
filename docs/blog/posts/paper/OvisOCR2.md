---
title: 论文速读：OvisOCR2
date:
  created: 2026-07-28
authors:
  - SWHL
slug: ovisocr2
categories:
  - 论文阅读
---

<!-- more -->

> 系列说明：本文为快速阅览笔记，侧重梳理方案骨架与技术演进关系，不深入实现细节；后续若开展相关方向研究，再补充精读分析。

论文地址：https://arxiv.org/abs/2607.13639v1

模型地址：https://huggingface.co/ATH-MaaS/OvisOCR2

在线 demo: https://huggingface.co/spaces/ATH-MaaS/OvisOCR2

## 现存痛点

流水线方案准但是部署复杂，且有级联误差，端到端方案优雅但是精度有限，部署要求高。

## 核心思路

模型结构没有改动，采用的是 Qwen3.5-0.8B。

数据构建：真实数据 + 合成数据

![2026-07-28_19-01-00-095d499d](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-28_19-01-00-095d499d.jpg)

值得一提的是合成数据中采用一套 HTML 源码，采用 Playwright 渲染为图像，同时生成 markdown 格式标注。这样规避了很多噪声。同时合成数据也不是随机合成，而是先找到真实数据中失败的数据，合成的时候针对性合成。

训练方法：SFT + RL + OPD + Model Fusion

![2026-07-28_19-13-43-ab945a10](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-07-28_19-13-43-ab945a10.jpg)

SFT：构建初始的端到端文档解析策略

RL: 通过文本、公式和表格奖励进一步优化困难页面的策略

OPD: 将 Qwen3.5-4B 教室模型的 reward-aligned 行为到 0.8B 的学生模型

Model Fusion: 融合多个不同数据配比和训练配置的模型

## 整体架构

全文没有给出模型结构，主要因为没有改动。

## 简要评价

这个挖掘难样本的策略让我想到 PaddleOCR-VL，它也是这么做的。

优势：整体指标表现强势，部署容易，目前 SOTA。如果手头有正在用端到端的模型的，可以切换为 OvisOCR2 试试。

局限：这个工作更像一系列工程组合得到的结果，并无太大创新点，但是仍然具有借鉴意义。
