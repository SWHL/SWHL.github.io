---
title: "Code Fence Completer: markdown 代码块补全工具"
date:
  created: 2026-08-05
authors:
  - SWHL
slug: obsidian-code-fence-completer
categories:
  - 工具
tags:
 - Obsidian
---

<!-- more -->

## 引言

在使用 Obsidian 软件做日常笔记的时候，总是要写一些代码片段到笔记中。为了方便查看，代码块都是要用 **```** （反引号，键盘左上角数字 1 左边那个按键按 3 次） 来包裹起来的。

被包裹后的代码，在显示的时候，就会有语法高亮和行号了。这样就很方便看了。举个例子：

```python linenums="1"
def main():
  print('hello world')

main()
```

上面就是最简单的代码块。**```** 后面可以选择相应的编程语言，这样可以高亮不同编程语言的不同关键字。

## Code Fence Completer

Obsidian 本身对代码块围栏的自动补全支持不算理想，我之前使用的一款插件是：[obsidian-code-language-completer](https://github.com/stanley-910/obsidian-code-language-completer)，工作过程就像下图：

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-06_08-23-23-fb73ed22.gif)

但是我在使用过程中，发现选择语言后，按回车，时常不会自动补全尾部 ```，也不会将光标定位到下方新行。

在大约 2 年前，我通过修改这个插件的源码，勉强实现在插入 ``` 后，光标自动跳到新一行的功能，一直用到现在。

但是随着 Obsidian 软件的更新，我发现这个插件失灵的频率越来越高了，高到我难以忽视的地步。于是，我就想着用 GPT-5.6 Sol 来修复一下。

最终，就有了：[obsidian-code-fence-completer](https://github.com/SWHL/obsidian-code-fence-completer) 插件。为什么要新起一个名字呢？这是因为原有插件作者已经 2 年不维护了，我提交 PR，作者大概率不会很快审核。

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-06_09-33-02-371fa24e.gif)

## Code Fence Completer 插件相比于 Code Language Completer 有哪些异同呢？

| 维度 | Code Language Completer | Code Fence Completer |
|---|---|---|
| 来源关系 | 原项目 | 基于原项目继续开发，README 中明确致谢 |
| 基础功能 | 输入 ` ```py` 时补全语言 | 保留相同补全流程 |
| 默认语言 | 23 种 | 继承相同的 23 种 |
| 搜索方式 | 仅语言名前缀匹配 | 精确、前缀、子串、模糊匹配 |
| 别名 | 不支持 | 内置 `py`、`js`、`ts`、`sh` 等，也可自定义 |
| 最近使用 | 只优先一个最近语言 | 记录并排序最近 5 个语言 |
| 自定义语言 | 逗号分隔 | 支持逗号或换行，忽略大小写重复 |
| 标识符范围 | 正则只接受 `\w`，不能正常输入 `c++`、`c#`、`foo-bar` | 支持这些非单词字符标识符 |
| Fence 类型 | 仅精确的三个反引号 | 支持 3 个以上反引号或波浪号，如 `~~~~cpp` |
| Markdown 识别 | 只检查当前行结尾，可能把关闭 fence 当成打开 fence | 识别 fence 状态、缩进和关闭 fence，避免误触发 |
| 完成代码块 | 选择语言后只把光标移到下一行 | 检查并补上关闭 fence，复用已有 fence，避免重复 |
| 编辑已有代码块 | 不支持 | 可以修改或清除光标所在代码块的语言 |
| Info string | 没有专门处理 | 修改语言时保留 `title=demo` 等后续属性 |
| 插入命令 | 在光标处直接插入空代码块 | 可插入空块、处理非空行，也可把选区包进代码块 |
| 冲突处理 | 无 | 检测旧插件及 Codeblock Completer，并给出警告 |
| 移动端 | manifest 声明仅桌面端 | 桌面端和移动端均支持 |
| Obsidian 版本 | 最低 `0.15.0` | 最低 `1.13.0` |
| 测试与发布 | 没有自动化测试 | 有语言解析、fence 完成和版本同步测试及 CI |

几个实际体验上的差别最明显：

- 输入 ` ```jvs` 时，Code Fence Completer 可以模糊找到 `javascript`。
- 输入 ` ```py` 时，会显示别名匹配并插入规范名称 `python`。
- 输入 `~~~c++`、` ```c#` 或 ` ```foo-bar` 时，旧插件的 `\w*` 正则无法覆盖，新插件可以。
- 在已有的 ` ```python title=demo` 代码块里切换语言，新插件只替换 `python`，保留 `title=demo`。
- 手动输入打开 fence 后选择语言，新插件会确保代码块拥有匹配的关闭 fence，避免正文被意外吞进代码块。

选择上：

- **普通用户建议使用 Code Fence Completer**，功能和可靠性明显更完整。
- 只有仍在使用非常旧的 Obsidian，或者特别希望使用最简单实现时，Code Language Completer 才有兼容性优势。
- 两者不要同时启用，否则会出现两套补全菜单；Code Fence Completer 已内置冲突提示。

## 使用

点击 [Add to Obsidian](obsidian://show-plugin?id=code-fence-completer) 在 Obsidian 中打开。

或者

![](https://raw.githubusercontent.com/SWHL/SWHL.github.io-Assets/main/images/2026/2026-08-06_09-35-36-9c822e5a.jpg)

## 写在最后

这个小插件，也是源于我日常使用遇到的痛点，借助大模型完成开发。

我逐渐意识到，想要做好用的产品和工具，不妨从自身遇到的痛点出发。

我也发现大模型非常适合做这种小插件，因为小插件代码量少，功能容易验证。

欢迎大家使用。
