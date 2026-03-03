---
title: pathlib库中那些容易被忽略的好用方法
hide:
  - toc
tags:
  - python
comments: true
---

### `read_text`和`write_text`读写文件

这两个方法在Python 3.5+中支持。官方文档：[link](https://docs.python.org/3/library/pathlib.html#reading-and-writing-files)

```python linenums="1"
>> p = Path('my_text_file')
>> p.write_text('Text file contents')
18
>> p.read_text()
'Text file contents'
```

### `symlink_to`

生成指定文件的软连接

```python linenums="1"
# 生成tmp/1.txt的软连接 tmp/4
>>> a = Path('tmp/4')
>>> a.symlink_to('tmp/1.txt')
>>> a
PosixPath('tmp/4')
```

### 获得指定文件的绝对路径

```python linenums="1"
>> Path('1.txt').resolve()
/xxxx/xxxx/xxxx/1.txt
```

### 删除具体文件

python 3.8+：添加了`missing_ok`参数

```python linenums="1"
>> path_txt = Path('1.txt')
>> path_txt.unlink(missing_ok=True)
```
