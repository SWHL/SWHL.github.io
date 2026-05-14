from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any


def _clean_text(value: Any) -> str:
    text = "" if value is None else str(value)
    return re.sub(r"\s+", " ", text).strip()


def _strip_front_matter(content: str) -> str:
    if not content.startswith("---\n"):
        return content

    _, _, remainder = content.partition("---\n")
    _, separator, body = remainder.partition("\n---\n")
    if not separator:
        return content
    return body.lstrip()


def _summary_from_markdown(path: str | None, fallback: str) -> str:
    if not path:
        return fallback

    source_path = Path(path)
    if not source_path.exists():
        return fallback

    body = _strip_front_matter(source_path.read_text(encoding="utf-8"))
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(("#", "!", ">", "-", "*", "|", "<", "{%")):
            continue
        line = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", line)
        line = re.sub(r"`([^`]*)`", r"\1", line)
        summary = _clean_text(line)
        if summary:
            return summary[:180]

    return fallback


def _normalize_date(value: Any) -> str | None:
    if isinstance(value, dict):
        value = value.get("created") or value.get("updated")
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        text = re.sub(r"<[^>]+>", "", value)
        match = re.search(
            r"\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)?)?",
            text,
        )
        if match:
            return match.group(0).replace(" ", "T")
        return _clean_text(text) or None
    return None


def _metadata_list(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [_clean_text(value)]
    if isinstance(value, (list, tuple, set)):
        return [_clean_text(item) for item in value if _clean_text(item)]
    return [_clean_text(value)]


def _yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _markdown_path_from_page(page: Any) -> str:
    if getattr(page, "is_homepage", False):
        return "index.md"

    url = (getattr(page, "url", "") or "index.html").split("#", 1)[0].split("?", 1)[0]
    url = url.lstrip("/")
    if url.endswith("/"):
        url = url[:-1]
    if not url:
        return "index.md"
    if url.endswith(".html"):
        return f"{url[:-5]}.md"
    if url.endswith(".htm"):
        return f"{url[:-4]}.md"
    if url.endswith(".md"):
        return url
    return f"{url}.md"


def _markdown_url_from_page(page: Any) -> str:
    canonical_url = getattr(page, "canonical_url", "") or ""
    if getattr(page, "is_homepage", False):
        return f"{canonical_url.rstrip('/')}/index.md"
    if canonical_url.endswith("/"):
        return f"{canonical_url[:-1]}.md"
    if canonical_url.endswith(".html"):
        return f"{canonical_url[:-5]}.md"
    if canonical_url.endswith(".htm"):
        return f"{canonical_url[:-4]}.md"
    return f"{canonical_url}.md"


def _page_author(page: Any, config: Any) -> str:
    meta = getattr(page, "meta", {}) or {}
    authors = _metadata_list(meta.get("authors"))
    if authors:
        return authors[0]
    return _clean_text(meta.get("author") or config.site_author or config.site_name)


def _page_title(page: Any, config: Any) -> str:
    meta = getattr(page, "meta", {}) or {}
    if getattr(page, "is_homepage", False):
        return _clean_text(meta.get("title") or config.site_name)
    return _clean_text(meta.get("title") or getattr(page, "title", "") or config.site_name)


def _seo_image(config: Any, meta: dict[str, Any]) -> str | None:
    image = meta.get("image") or meta.get("cover") or meta.get("og_image")
    if image:
        return str(image)
    return ((config.extra or {}).get("seo") or {}).get("image")


def _schema_for_page(page: Any, config: Any, seo: dict[str, Any]) -> dict[str, Any]:
    meta = getattr(page, "meta", {}) or {}
    extra_seo = ((config.extra or {}).get("seo") or {})
    author_url = extra_seo.get("author_url") or config.site_url
    same_as = extra_seo.get("same_as") or []

    author = {
        "@type": "Person",
        "name": seo["author"],
        "url": author_url,
    }
    if same_as:
        author["sameAs"] = same_as

    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "BlogPosting" if seo["is_article"] else "WebPage",
        "headline": seo["title"],
        "name": seo["title"],
        "description": seo["description"],
        "url": seo["canonical_url"],
        "inLanguage": "zh-CN",
        "author": author,
        "publisher": {
            "@type": "Organization",
            "name": config.site_name,
            "url": config.site_url,
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": seo["canonical_url"],
        },
    }

    if seo.get("image"):
        schema["image"] = seo["image"]
    if seo.get("published_time"):
        schema["datePublished"] = seo["published_time"]
    if seo.get("modified_time"):
        schema["dateModified"] = seo["modified_time"]
    if seo.get("keywords"):
        schema["keywords"] = seo["keywords"]
    if meta.get("categories"):
        schema["articleSection"] = ", ".join(_metadata_list(meta.get("categories")))

    return schema


def on_page_context(context, page, config, nav):
    meta = getattr(page, "meta", {}) or {}
    fallback_description = _clean_text(config.site_description)
    title = _page_title(page, config)
    description = _clean_text(meta.get("description"))
    if not description:
        src_path = getattr(getattr(page, "file", None), "abs_src_path", None)
        description = _summary_from_markdown(src_path, fallback_description)

    keywords = []
    for key in ("tags", "categories", "keywords"):
        keywords.extend(_metadata_list(meta.get(key)))
    keywords = list(dict.fromkeys(keywords))

    date_meta = meta.get("date")
    published_time = _normalize_date(date_meta)
    modified_time = _normalize_date(meta.get("date_updated") or meta.get("updated"))
    if not modified_time:
        modified_time = _normalize_date(meta.get("git_revision_date_localized"))

    seo = {
        "title": title,
        "full_title": title if getattr(page, "is_homepage", False) else f"{title} - {config.site_name}",
        "description": description,
        "canonical_url": getattr(page, "canonical_url", "") or "",
        "markdown_url": _markdown_url_from_page(page),
        "author": _page_author(page, config),
        "image": _seo_image(config, meta),
        "keywords": ", ".join(keywords),
        "published_time": published_time,
        "modified_time": modified_time or published_time,
        "is_article": bool(published_time or "/posts/" in getattr(getattr(page, "file", None), "src_uri", "")),
        "twitter": ((config.extra or {}).get("seo") or {}).get("twitter"),
    }
    seo["schema_json"] = json.dumps(_schema_for_page(page, config, seo), ensure_ascii=False)

    context["seo"] = seo
    context["page_markdown_url"] = seo["markdown_url"]
    return context


def on_post_page(output_content, page, config, **kwargs):
    src_path = getattr(getattr(page, "file", None), "abs_src_path", None)
    if not src_path or not str(src_path).endswith(".md"):
        return output_content

    source_path = Path(src_path)
    if not source_path.exists():
        return output_content

    markdown_path = _markdown_path_from_page(page)
    destination = Path(config.site_dir) / markdown_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    meta = getattr(page, "meta", {}) or {}
    title = _page_title(page, config)
    description = _clean_text(meta.get("description")) or _summary_from_markdown(
        src_path,
        _clean_text(config.site_description),
    )
    body = _strip_front_matter(source_path.read_text(encoding="utf-8")).lstrip()
    first_line, separator, remainder = body.partition("\n")
    if first_line.strip() == f"# {title}":
        body = remainder.lstrip() if separator else ""

    markdown = "\n".join(
        [
            "---",
            f"title: {_yaml_scalar(title)}",
            f"canonical_url: {_yaml_scalar(getattr(page, 'canonical_url', ''))}",
            f"markdown_url: {_yaml_scalar(_markdown_url_from_page(page))}",
            f"description: {_yaml_scalar(description)}",
            "---",
            "",
            f"# {title}",
            "",
            f"> Canonical URL: {getattr(page, 'canonical_url', '')}",
            f"> Markdown URL: {_markdown_url_from_page(page)}",
            "",
            body,
            "",
        ]
    )
    destination.write_text(markdown, encoding="utf-8")
    return output_content
