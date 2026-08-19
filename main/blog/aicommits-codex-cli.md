---
title: "aicommits 工具接入 Codex CLI 使用"
canonical_url: "https://swhl.github.io/main/blog/aicommits-codex-cli/"
markdown_url: "https://swhl.github.io/main/blog/aicommits-codex-cli.md"
description: "aicommits 是一款使用 AI 为你自动生成 git 提交信息的命令行工具。"
---

# aicommits 工具接入 Codex CLI 使用

> Canonical URL: https://swhl.github.io/main/blog/aicommits-codex-cli/
> Markdown URL: https://swhl.github.io/main/blog/aicommits-codex-cli.md

<!-- more -->

## 背景

aicommits 是一款使用 AI 为你自动生成 git 提交信息的命令行工具。

项目地址：https://github.com/Nutlope/aicommits

普通版 `aicommits v4.1.1` 通过 OpenAI-compatible HTTP API 调用模型，固定使用 `/chat/completions`。

Codex 专用代理可能只支持 Codex/Responses 协议，因此会出现：

```text
Invalid JSON response
```

这种情况无法仅靠设置 `OPENAI_BASE_URL` 解决，需要使用支持 `Codex CLI` provider 的分支：

```text
https://github.com/vwww-droid/aicommits/tree/feat/subscription-cli-providers
```

## 工作原理

该分支执行：

```bash
git diff --cached |
codex exec \
  --ephemeral \
  --sandbox read-only \
  --output-last-message <临时文件> \
  "<commit message prompt>"
```

特点：

- 只分析 Git staged changes
- 通过 `codex exec` 调用模型
- 自动读取 `~/.codex/config.toml`
- 复用 Codex 的模型、base URL 和认证
- 不要求接口兼容 `/chat/completions`
- `read-only` 模式不会修改代码
- `ephemeral` 模式不会保存 Codex 会话

如果当前用户是 `root`，配置路径是：

```text
/root/.codex/config.toml
```

## 安装支持 Codex CLI 的分支

```bash
BUILD_DIR="$(mktemp -d)"

git clone \
  --depth 1 \
  --branch feat/subscription-cli-providers \
  https://github.com/vwww-droid/aicommits.git \
  "$BUILD_DIR/aicommits"

cd "$BUILD_DIR/aicommits"

npm install
npm run build
npm install -g . --ignore-scripts
```

确认 Codex CLI 可用：

```bash
command -v codex
codex login status
codex exec --ephemeral --sandbox read-only "Output OK only"
```

## 配置 Codex Provider

推荐运行交互式配置：

```bash
aicommits setup
```

选择：

```text
Codex CLI (uses your Codex subscription)
```

也可以手动配置：

```bash
aicommits config set \
  OPENAI_BASE_URL="codex://cli" \
  OPENAI_MODEL="codex" \
  timeout=180000
```

清除之前遗留的 API Key：

```bash
aicommits config set OPENAI_API_KEY=
```

检查配置：

```bash
aicommits config
```

预期结果：

```text
Provider: codex
Base URL: codex://cli
Model: codex
```

这里的 `Model: codex` 只是 provider 标识。真正使用的模型来自 `~/.codex/config.toml`。

## 设置英文 Commit

```bash
aicommits config set locale=en
```

进一步强制使用英文：

```bash
aicommits config set \
  prompt="Write the commit message in English only. Use an imperative subject."
```

## 设置 Commit 格式

Conventional Commit，仅标题：

```bash
aicommits config set type=conventional
```

Conventional Commit，包含正文：

```bash
aicommits config set type=conventional+body
```

其他格式：

```bash
aicommits config set type=plain
aicommits config set type=subject+body
aicommits config set type=gitmoji
```

临时覆盖当前一次运行：

```bash
aicommits --type conventional
```

推荐完整配置：

```bash
aicommits config set \
  locale=en \
  type=conventional \
  generate=1 \
  timeout=180000 \
  prompt="Write the commit message in English only. Use an imperative subject."
```

生成效果：

```text
feat(scanner): track deleted objects during incremental scans
```

## `generate` 的含义

只生成一条候选消息：

```bash
aicommits config set generate=1
```

生成三条候选消息：

```bash
aicommits config set generate=3
```

临时生成三条：

```bash
aicommits --generate 3
```

Codex CLI provider 推荐使用 `generate=1`，因为速度更快，也不容易超时。

## 只生成消息，不自动提交

该分支没有正式的 `--dry-run` 参数，但 stdout 被管道或重定向时会进入 headless 模式，只输出消息，不执行 `git commit`：

```bash
set -o pipefail
aicommits | tee /tmp/commit-message.txt
```

检查或编辑消息：

```bash
${EDITOR:-vi} /tmp/commit-message.txt
```

手动提交：

```bash
git commit -F /tmp/commit-message.txt
```

只显示、不保存：

```bash
aicommits | cat
```

## Git Commit 10 秒超时

该工具最终的 `git commit` 超时时间硬编码为：

```ts
timeout: 10000
```

如果项目有耗时较长的 pre-commit hook，例如：

```text
ruff check
ruff format
```

可能出现：

```text
Commit timed out after 10 seconds
```

这表示 Codex 已经成功生成消息，超时的是后续 `git commit`。

当前执行 `aicommits` 后，会在选择 **Yes** 后，自动执行提交，如果仓库有 `pre-commit`，程序更容易超时，默认 10s，且不能更改。因此建议直接选择 **No**，退出 `aicommits` 后，手动提交。

## 推荐日常流程

```bash
git add <files>

aicommits

# 打印出commit mesage 后，选择 No

# 手动复制提交
git commit -m "复制粘贴
```

这样既能使用 Codex 自动生成英文 Conventional Commit，也不会受到 aicommits 内部 Git commit 超时的影响。

