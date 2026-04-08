---
title: 如何在 mkdocs-material 中设置图像圆角显示？
date:
  created: 2026-04-08
authors:
  - SWHL
slug: mkdocs-material-image-rounded-corners
categories:
  - mkdocs-material
hide:
  - toc
---

<!-- more -->

## 引言

之前参考：[网页圆角化设计](https://wcowin.work/Mkdocs-Wcowin/blog/websitebeauty/yuanjiaohua/) 教程来设置的网站图像圆角化显示。

上述整体实现容易，效果还不错。但是当我构建自己的图床后，我发现上述实现不方便的地方在于：每次插入图像后，都要在 markdown url 后添加 `{.img1}` 来让圆角生效。

```markdown linenums="1" title="原方案示例写法"
![image.png](https://s2.loli.net/2024/04/26/Czi9uAQhmbBlkfG.png){.img1}
```

这样在其他平台上渲染同样的 markdown 时，`{.img1}` 类就会失效。此时需要手动去掉这个。这就有些麻烦了。

我设想的是：是否可以设置为默认圆角，个别图像不需要圆角时，可以单独设置？

## 实现方法

在 **docs** 目录下新建目录 **stylesheets**，在下面新建 **extra.css** 文件

```bash linenums="1"
docs
└─ stylesheets
    └─ extra.css
```

**extra.css** 中内容：

```css linenums="1"
.md-typeset img {
  /* 圆角设置：使用 rem 单位以适配不同屏幕 */
  border-radius: 1rem;

  /* 关键：防止图片内容溢出圆角区域（特别是 GIF 或带透明底的图） */
  overflow: hidden;

  /* 质感提升：轻微阴影，让图片看起来像浮在纸上 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  /* 交互体验：平滑过渡，鼠标悬停时更自然 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* 鼠标悬停效果：图片微微放大 */
.md-typeset img:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

/*
   当你给图片加上 {.no-radius} 时，应用此样式
   !important 用于强制覆盖上面的全局圆角和阴影
*/
.md-typeset img.no-radius {
  border-radius: 0 !important;
  box-shadow: none !important;
  overflow: visible !important;
}

/* 悬停时也取消放大效果 */
.md-typeset img.no-radius:hover {
  transform: none !important;
}
```

在 `mkdocs.yml` 中添加以下内容：

```yaml
extra_css:
  - stylesheets/extra.css
```

最终使用：

```markdown linenums="1"
# 默认圆角
![image.png](https://s2.loli.net/2024/04/26/Czi9uAQhmbBlkfG.png)

# 不使用圆角
![image.png](https://s2.loli.net/2024/04/26/Czi9uAQhmbBlkfG.png){.no-radius}

# HTML 写法
<img src="https://github.com/RapidAI/RapidOCRWeb/releases/download/v1.0.0/rapidocr_web_logo_v2_white.png" class="no-radius">
```
