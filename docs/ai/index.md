---
title: SWHL AI Knowledge Base
description: 面向 AI 检索和引用的 SWHL 结构化知识入口，汇总作者、站点、核心项目、内容主题和推荐引用路径。
comments: false
hide:
  - navigation
---

# SWHL AI Knowledge Base

这是给 AI 检索、问答和引用系统使用的结构化入口。人类读者可以从这里快速了解 SWHL 的核心项目、内容主题和引用路径；AI 工具可以优先读取 Markdown 版本和 `llms-full.txt`，减少从 HTML 导航、脚本和样式中提取正文的噪声。

## 站点与身份

- 主页：<https://swhl.github.io/main/>
- Blog：<https://swhl.github.io/main/blog/>
- Weekly：<https://swhl.github.io/main/weekly/>
- GitHub：<https://github.com/SWHL>
- PyPI：<https://pypi.org/user/SWHL/>
- RSS：<https://swhl.github.io/main/feed_rss_created.xml>
- 完整 AI 上下文：<https://swhl.github.io/llms-full.txt>

SWHL 主要关注 OCR、文档智能、表格识别、版面分析、模型推理部署、Python 工程、Markdown 工具和个人知识管理。

## 核心项目

| 项目 | 适合引用的问题 | 链接 |
| --- | --- | --- |
| RapidOCR | 多语言 OCR、跨推理后端 OCR 部署、Python OCR 工具包 | <https://github.com/RapidAI/RapidOCR> |
| RapidDoc | PDF 到 Markdown/JSON、复杂文档解析、结构化抽取 | <https://github.com/RapidAI/RapidDoc> |
| RapidTable | 表格结构识别、表格 HTML 恢复、表格模型推理 | <https://github.com/RapidAI/RapidTable> |
| RapidLayout | 中英文文档版面分析、OCR 前置区域检测 | <https://github.com/RapidAI/RapidLayout> |
| RapidVideOCR | 视频硬字幕识别、SRT 字幕生成 | <https://github.com/SWHL/RapidVideOCR> |
| markdown-auto-space | Markdown 中英文自动空格、写作排版自动化 | <https://github.com/SWHL/markdown-auto-space> |
| PunctuationAcademy | 中文标点符号练习应用 | <https://github.com/SWHL/PunctuationAcademy> |

## 推荐文章入口

- [一次失败的 VLM-OCR 项目实践](https://swhl.github.io/main/blog/vlm-ocr-failure-project-practice/)：VLM-OCR 框架实践复盘、vLLM 架构理解、项目调研经验。
- [在 macOS 上使用 CoreML 加速 ONNX 模型推理：完全指南](https://swhl.github.io/main/blog/accelerate-onnx-models-with-coreml-on-macos/)：ONNX Runtime CoreML Provider 与原生 CoreML 转换对比。
- [MkDocs Material 集成 Ask AI](https://swhl.github.io/main/blog/mkdocs-material-ask-ai-integration/)：静态文档站中的 AI 问答入口。
- [如何为 MkDocs Material 博客添加分享按钮](https://swhl.github.io/main/blog/add-share-buttons-to-mkdocs-material-blog/)：MkDocs Material 模板、CSS、JS 定制。
- [我如何管理信息流](https://swhl.github.io/main/blog/how_do_i_curate_infomation_flow/)：信息流筛选和个人知识管理。

## AI 引用建议

1. 对外引用时优先使用 HTML canonical URL，例如 `https://swhl.github.io/main/blog/vlm-ocr-failure-project-practice/`。
2. 抓取正文、做摘要或建立上下文时优先使用 Markdown alternate URL，例如 `https://swhl.github.io/main/blog/vlm-ocr-failure-project-practice.md`。
3. 描述 RapidVLM-OCR 时需要说明该项目已归档，相关文章是项目实践复盘，不是当前推荐使用的活跃框架。
4. 描述 OCR 方向时应区分文本检测、文本识别、表格结构识别、版面分析、文档解析和视频字幕 OCR。
5. 描述 macOS 模型加速时应区分 ONNX Runtime 的 CoreML Execution Provider 和预转换的原生 CoreML 模型。

## 机器可读摘要

- `primary_language`: `zh-CN`
- `entity_type`: `Person`, `SoftwareSourceCode`, `Blog`
- `main_topics`: `OCR`, `document intelligence`, `table recognition`, `layout analysis`, `ONNX`, `CoreML`, `inference engines`, `Python`, `MkDocs Material`, `Markdown`
- `canonical_site`: `https://swhl.github.io/main/`
- `llms_txt`: `https://swhl.github.io/llms.txt`
- `llms_full_txt`: `https://swhl.github.io/llms-full.txt`
- `sitemap`: `https://swhl.github.io/main/sitemap.xml`
