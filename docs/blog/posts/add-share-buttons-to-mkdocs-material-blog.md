---
title: 如何给 MkDocs Material 博客文章添加分享按钮？
date:
  created: 2026-05-07
authors:
  - SWHL
slug: add-share-buttons-to-mkdocs-material-blog
categories:
  - 工具
tags:
  - mkdocs-material
hide:
  - toc
---

最近给博客文章页加了一组分享按钮，最终效果是放在文章元数据下方、评论区上方：

```text
分享： 微信 微博 X
```

这篇文章记录一下实现过程。核心思路是：覆盖 MkDocs Material 的博客文章模板，在合适的位置插入一个分享组件，再用少量 JavaScript 动态生成分享链接。

<!-- more -->

## 目标

我想要的效果比较简单：

- 分享按钮只出现在博客文章页和周刊文章页
- 位置放在文章正文元数据下方、评论区上方
- 图标风格和页脚社交图标保持一致
- 微信 / 公众号按钮点击后复制文章标题和链接
- 微博和 X 使用各自的网页分享链接

参考了 MkDocs Material 官方文档：[Share and like buttons](https://squidfunk.github.io/mkdocs-material/tutorials/blogs/engage/#share-and-like-buttons)。

## 为什么不能直接改 main.html？

一开始我以为覆盖 `overrides/main.html` 的 `content` block 就够了，但实际发现文章页没有生效。

原因是 MkDocs Material 的博客文章页使用的是 `blog-post.html` 模板。它会覆盖 `container` block，并在内部重新渲染文章内容：

```jinja linenums="1"
<article class="md-content__inner md-typeset">
  {% block content %}
    {% include "partials/content.html" %}
  {% endblock %}
</article>
```

所以如果要改博客文章页，应该覆盖 `overrides/blog-post.html`，而不是只改普通页面模板。

## 新增分享组件

新增文件：

```text linenums="1"
overrides/partials/share.html
```

内容如下：

```jinja linenums="1"
<aside class="post-share" aria-label="Share this post">
  <span class="post-share__title">分享：</span>
  <div class="post-share__actions">
    <button
      class="post-share__button share-wechat"
      type="button"
      data-share-wechat
      aria-label="Share this post via WeChat or WeChat Official Account"
    >
      <span class="post-share__icon md-icon" aria-hidden="true">
        {% include ".icons/fontawesome/brands/weixin.svg" %}
      </span>
      <span class="post-share__sr">Share this post via WeChat or WeChat Official Account</span>
    </button>
    <a
      class="post-share__button"
      href="#"
      data-share-weibo
      target="_blank"
      rel="noopener"
      aria-label="Share this post on Weibo"
    >
      <span class="post-share__icon md-icon" aria-hidden="true">
        {% include ".icons/fontawesome/brands/weibo.svg" %}
      </span>
      <span class="post-share__sr">Share this post on Weibo</span>
    </a>
    <a
      class="post-share__button"
      href="#"
      data-share-x
      target="_blank"
      rel="noopener"
      aria-label="分享到 X"
    >
      <span class="post-share__icon md-icon" aria-hidden="true">
        {% include ".icons/fontawesome/brands/x-twitter.svg" %}
      </span>
      <span class="post-share__sr">Share this post on X</span>
    </a>
  </div>
</aside>
```

这里直接复用了 MkDocs Material 内置的 FontAwesome 图标，不需要额外引入图标库。

## 插入到文章元数据下面

覆盖文件：

```text linenums="1"
overrides/blog-post.html
```

关键位置是文章内容区域。原本 `partials/content.html` 会依次渲染：

```jinja
{% include "partials/tags.html" %}
{% include "partials/actions.html" %}
{{ page.content }}
{% include "partials/source-file.html" %}
{% include "partials/feedback.html" %}
{% include "partials/comments.html" %}
```

为了把分享按钮放到元数据下方、评论区上方，可以把这段展开，并在 `source-file` 后插入 `share.html`：

```jinja
<article class="md-content__inner md-typeset">
  {% block content %}
    {% include "partials/tags.html" %}
    {% include "partials/actions.html" %}
    {% if "\u003ch1" not in page.content %}
      <h1>{{ page.title | d(config.site_name, true)}}</h1>
    {% endif %}
    {{ page.content }}
    {% include "partials/source-file.html" %}
    {% include "partials/share.html" %}
    {% include "partials/feedback.html" %}
    {% include "partials/comments.html" %}
  {% endblock %}
</article>
```

最终顺序就是：

```text linenums="1"
正文
文章源文件元数据
分享按钮
评论区
```

## 添加 JavaScript

在 `docs/javascripts/extra.js` 中添加分享逻辑：

```javascript linenums="1"
function getSharePayload() {
  return {
    title: document.querySelector("h1")?.textContent?.trim() || document.title,
    url: window.location.href.split("#")[0],
  };
}

async function copyShareText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const input = document.createElement("textarea");
  input.value = text;
  input.setAttribute("readonly", "");
  input.style.position = "fixed";
  input.style.opacity = "0";
  document.body.appendChild(input);
  input.select();
  document.execCommand("copy");
  input.remove();
}

function showShareToast(message) {
  document.querySelectorAll(".post-share-toast").forEach((toast) => toast.remove());

  const toast = document.createElement("div");
  toast.className = "post-share-toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add("post-share-toast--visible");
  });

  setTimeout(() => {
    toast.classList.remove("post-share-toast--visible");
    setTimeout(() => toast.remove(), 200);
  }, 3000);
}

function setupPostShare() {
  const container = document.querySelector(".post-share");
  if (!container) {
    return;
  }

  const payload = getSharePayload();
  const shareText = `${payload.title}\n${payload.url}`;
  const xLink = container.querySelector("[data-share-x]");

  if (xLink) {
    const params = new URLSearchParams({
      text: payload.title,
      url: payload.url,
    });
    xLink.href = `https://twitter.com/intent/tweet?${params.toString()}`;
  }

  const weiboLink = container.querySelector("[data-share-weibo]");
  if (weiboLink) {
    const params = new URLSearchParams({
      title: payload.title,
      url: payload.url,
    });
    weiboLink.href = `https://service.weibo.com/share/share.php?${params.toString()}`;
  }

  container.querySelectorAll("[data-share-wechat]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        await copyShareText(shareText);
        showShareToast("标题和链接已复制，请前往微信或公众号后台粘贴分享。");
      } catch (error) {
        showShareToast("复制失败，请手动复制地址栏链接。");
      }
    });
  });
}

document$.subscribe(function() {
  setupPostShare();
});
```

这里用了 `document$.subscribe`，是为了兼容 MkDocs Material 的即时导航。页面无刷新切换时，也能重新绑定分享按钮。

## 加载自定义 JS

在 `mkdocs.yml` 中添加：

```yaml linenums="1"
extra_javascript:
  - javascripts/extra.js
```

如果项目里已经配置了 `extra_javascript`，把这一项追加进去即可。

## 添加样式

在 `docs/stylesheets/extra.css` 中添加：

```css linenums="1"
.post-share {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 2.5rem;
  color: var(--md-footer-fg-color--lighter);
}

.post-share__title {
  display: inline-flex;
  align-items: center;
  margin: 0;
  font-size: 0.9rem;
  font-style: italic;
  font-weight: 600;
  line-height: 1.55rem;
}

.post-share__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  align-items: center;
}

.post-share__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.55rem;
  height: 1.55rem;
  padding: 0;
  border: 0;
  border-radius: 0.25rem;
  background: transparent;
  color: currentColor;
  font: inherit;
  cursor: pointer;
  transition: color 125ms, transform 125ms;
}

.md-typeset .post-share__button {
  color: var(--md-footer-fg-color--lighter);
}

.md-typeset .post-share__button:is(:hover, :focus-visible) {
  color: var(--md-footer-fg-color--light);
  transform: rotate(6deg);
}

.post-share__icon {
  width: 1.25rem;
  height: 1.25rem;
  flex: 0 0 auto;
}

.post-share__sr {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.post-share-toast {
  position: fixed;
  top: 2.5rem;
  left: 50%;
  z-index: 80;
  padding: 0.55rem 0.85rem;
  border-radius: 0.35rem;
  background: var(--md-accent-fg-color);
  color: var(--md-accent-bg-color);
  font-size: 0.7rem;
  box-shadow: 0 0.35rem 1.2rem rgba(0, 0, 0, 0.16);
  transform: translate(-50%, -0.8rem);
  opacity: 0;
  transition: opacity 180ms, transform 180ms;
}

.post-share-toast--visible {
  transform: translate(-50%, 0);
  opacity: 1;
}
```

这里有一个细节：文章正文里的链接通常会使用主题色，如果不额外覆盖，分享图标可能会变成正文链接的蓝色。因此需要：

```css linenums="1"
.md-typeset .post-share__button {
  color: var(--md-footer-fg-color--lighter);
}
```

这样分享图标就能和页脚社交图标保持一致。

## 本地预览

运行：

```bash linenums="1"
python -m mkdocs serve --dev-addr 127.0.0.1:8000
```

打开任意文章页，例如：

```text
http://127.0.0.1:8000/blog/vlm-ocr-failure-project-practice/
```

如果修改了 `overrides/partials/*.html` 这类模板文件，`mkdocs serve` 有时不会自动热重载。遇到页面没有变化时，直接重启服务即可。

## 小结

这次改造里最容易踩坑的点有两个：

- 博客文章页要覆盖 `blog-post.html`，不要只改 `main.html`
- 分享按钮放在 `source-file` 后面，才能位于文章元数据下方、评论区上方

整体实现不复杂，但最好顺着 MkDocs Material 的模板结构来改。这样后续维护起来会更清晰。
