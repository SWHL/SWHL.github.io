---
title: 在 macOS 上使用 CoreML 加速 ONNX 模型推理：完全指南
hide:
  - toc
tags:
  - ONNXRuntime
  - CoreML
comments: true
---

## 前言

作为深度学习工程师，我们经常面临一个问题：如何在 Apple 设备上高效地部署已有的 ONNX 模型？本文将深入探讨两种主要方案，并通过实际测试给出详细的性能和精度对比。

## 目录

1. [背景：为什么要用 CoreML](#背景)
2. [方案对比：ONNX Runtime vs 原生 CoreML](#方案对比)
3. [性能测试：MobileNetV3 实战](#性能测试)
4. [ONNX 转 CoreML：可行性分析](#转换方案)
5. [最佳实践建议](#最佳实践)

---

## 背景：为什么要用 CoreML

CoreML 是 Apple 的机器学习框架，针对 Apple 芯片（特别是 Neural Engine）进行了深度优化。使用 CoreML 的主要优势：

- ⚡ **性能优化**：充分利用 Neural Engine 和 GPU
- 🔋 **能效比高**：更低的功耗，适合移动设备
- 📦 **集成简单**：原生支持 iOS/macOS 开发
- 🛡️ **隐私保护**：模型在本地运行，数据不上传

但问题来了：**如果我们已经有了 ONNX 模型，如何在 Apple 设备上使用 CoreML 加速？**

---

## 方案对比：ONNX Runtime vs 原生 CoreML

### 方案 1：ONNX Runtime + CoreML Provider

直接使用 ONNX Runtime 的 CoreML Execution Provider，无需手动转换。

```python linenums="1"
import onnxruntime as ort

session = ort.InferenceSession(
    'model.onnx',
    providers=['CoreMLExecutionProvider', 'CPUExecutionProvider']
)

# 推理
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
output = session.run(None, {'input': input_data})
```

**工作原理：**

- ONNX Runtime 在首次加载时会将 ONNX 模型即时转换为 CoreML
- 转换结果会缓存到 `~/Library/Caches/onnxruntime`
- 后续加载会直接使用缓存的 CoreML 模型

**优点：**

- ✅ 跨平台兼容（Windows/Linux/macOS）
- ✅ 一个 ONNX 文件，多平台通用
- ✅ 无需手动转换
- ✅ 自动回退机制（不支持的算子回退到 CPU）
- ✅ 开发体验好

**缺点：**

- ❌ 首次加载有转换开销（约 0.5 秒）
- ❌ 运行时性能不如原生 CoreML
- ❌ 可能不支持所有 ONNX 算子

---

### 方案 2：预转换为 CoreML 格式

将模型预先转换为 `.mlpackage` 或 `.mlmodel` 格式分发。

```python linenums="1"
import torch
import coremltools as ct

# 从 PyTorch 加载模型
model = torch.jit.load('model.pt')
model.eval()

# 转换为 CoreML
example_input = torch.rand(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)

mlmodel = ct.convert(
    traced_model,
    inputs=[ct.TensorType(name="input", shape=(1, 3, 224, 224))],
    convert_to='mlprogram',
    compute_units=ct.ComputeUnit.ALL,
)

mlmodel.save('model.mlpackage')
```

**使用：**

```python linenums="1"
import coremltools as ct

model = ct.models.MLModel('model.mlpackage')
output = model.predict({'input': input_data})
```

**优点：**

- ✅ 推理速度最快
- ✅ 加载后即可使用，无转换开销
- ✅ 模型文件更小
- ✅ 可在 Xcode 中预览和调试
- ✅ iOS/macOS 原生应用可直接使用

**缺点：**

- ❌ 仅支持 Apple 设备
- ❌ 需要维护多个格式（ONNX + CoreML）
- ❌ 转换过程可能失败
- ❌ 需要额外的转换和验证流程

---

## 性能测试：MobileNetV3 实战

### 测试环境

- **硬件**：MacBook（Apple Silicon）
- **系统**：macOS
- **模型**：MobileNetV3-Small (9.71 MB)
- **输入**：1×3×224×224 float32
- **框架版本**：
    - ONNX Runtime: 1.22.0
    - CoreMLTools: 8.3.0

### 测试代码

完整测试代码已开源（[Gist](https://gist.github.com/SWHL/fd48ffee4b39ece6f8c418031915872f)），包含以下功能：

1. CoreML Provider 可用性检测
2. 性能对比测试（100 次推理）
3. 精度验证（多样本对比）
4. Top-5 预测一致性检查

```bash
# 测试 ONNX Runtime + CoreML Provider
python test_coreml.py

# 对比两种方案
python compare_coreml_methods.py
```

---

### 测试结果 1：ONNX Runtime (CoreML vs CPU)

首先测试 ONNX Runtime 中 CoreML Provider 和 CPU Provider 的性能差异：

| 指标 | CoreML Provider | CPU Provider | 对比 |
|------|----------------|-------------|------|
| **平均推理时间** | 7.466 ms | 5.202 ms | CPU 快 30% |
| **标准差** | 0.562 ms | 3.593 ms | CoreML 更稳定 |
| **最小延迟** | 6.371 ms | 4.161 ms | - |
| **P95 延迟** | 8.676 ms | 6.938 ms | - |
| **P99 延迟** | 9.328 ms | 13.213 ms | CoreML 更好 |
| **吞吐量** | 133.94 FPS | 192.22 FPS | CPU 更高 |

**关键发现：**

- 🐌 在 ONNX Runtime 中，CoreML Provider 反而比 CPU 慢 30%
- ✅ 但 CoreML 的延迟更稳定（标准差小 6 倍）
- ⚠️ CPU 偶尔会出现极端延迟（最大 39.3ms）

**原因分析：**

- ONNX Runtime 的 CoreML Provider 有额外的转换和数据传输开销
- MobileNetV3 模型较小，转换开销占比大
- CPU Provider 使用了高度优化的 BLAS 库（可能是 Apple Accelerate）

---

### 测试结果 2：原生 CoreML vs ONNX Runtime

对比原生 CoreML 和 ONNX Runtime + CoreML Provider：

| 指标 | ONNX Runtime + CoreML | 原生 CoreML | 差异 |
|------|----------------------|------------|------|
| **加载时间** | 0.555 秒 | 0.974 秒 | ONNX 更快 |
| **首次推理** | 0.013 秒 | 0.023 秒 | ONNX 更快 |
| **平均推理时间** | **6.447 ms** | **0.313 ms** | 🚀 **原生快 20.6 倍** |
| **推理标准差** | 0.296 ms | 0.040 ms | 原生更稳定 |
| **模型大小** | 9.71 MB | 4.95 MB | 原生小 49% |

**性能可视化：**

```text
推理时间对比（越短越好）
┌────────────────────────────────────────────────────────────────────┐
│ ONNX Runtime + CoreML  ████████████████████ 6.447 ms              │
│ 原生 CoreML            █ 0.313 ms                                  │
└────────────────────────────────────────────────────────────────────┘
                         ↑ 20.6x 加速！
```

**关键发现：**

- 🚀 **原生 CoreML 推理速度快 20.6 倍**
- 📦 模型体积减少 49%（9.71 MB → 4.95 MB）
- ✅ 延迟更稳定（±0.040ms vs ±0.296ms）
- ⚠️ 但加载时间稍慢（多 0.4 秒）

**性能分布对比：**

```text
推理时间分布：
  ONNX Runtime:  min=6.371ms, p50=7.401ms, p95=8.676ms, p99=9.328ms
  原生 CoreML:   min=0.273ms, p50=0.303ms, p95=0.393ms, p99=0.433ms
```

---

### 精度对比

测试 10 个随机样本，对比输出差异：

**ONNX Runtime (CoreML vs CPU)：**

- 平均最大差异: 6.01e-02（约 6%）
- 平均平均差异: 1.30e-02（约 1.3%）
- Top-5 预测一致性: 2/3 样本完全相同
- **结论**: ⚠️ 存在轻微差异，但大部分预测一致

**原生 CoreML vs ONNX Runtime (CPU)：**

- 平均最大差异: 1.01
- 平均平均差异: 0.22
- Top-5 预测一致性: 2/3 样本完全相同
- **结论**: ⚠️ 差异较大，需要在实际应用中验证是否可接受

**精度差异原因：**

1. 浮点运算顺序不同
2. CoreML 可能使用低精度计算（FP16）
3. 算子实现差异
4. 优化和融合策略不同

---

## ONNX 转 CoreML：可行性分析

### 理想方案：直接转换

理论上，我们希望：

```bash
# 理想但不可行 ❌
onnx-model.onnx → CoreML 转换工具 → model.mlpackage
```

### 实际情况：转换工具现状

经过实测，目前的转换工具状态如下：

#### 1. onnx-coreml（已弃用）❌

```bash
pip install onnx-coreml
```

**状态：** 已停止维护，与新版 coremltools 不兼容

**错误信息：**

```text
ModuleNotFoundError: No module named 'coremltools.converters.nnssa'
```

**原因：** coremltools 7.0+ 重构了内部 API，移除了 `nnssa` 模块

**结论：** ❌ 不推荐使用

---

#### 2. coremltools 直接转换（已移除）❌

```python linenums="1"
import coremltools as ct

# 尝试直接转换 ONNX
mlmodel = ct.convert('model.onnx', source='onnx')
```

**错误信息：**

```text
ValueError: Unrecognized value of argument "source": onnx.
It must be one of ["auto", "tensorflow", "pytorch", "milinternal"].
```

**原因：** coremltools 8.x 已经移除了对 ONNX 的直接支持

**结论：** ❌ 不可行

---

#### 3. 通过原始框架转换（唯一可行）✅

```python linenums="1"
import torch
import coremltools as ct

# 1. 加载 PyTorch 模型
model = torch.jit.load('model.pt')
model.eval()

# 2. 追踪模型
example_input = torch.rand(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)

# 3. 转换为 CoreML
mlmodel = ct.convert(
    traced_model,
    inputs=[ct.TensorType(name="input", shape=(1, 3, 224, 224))],
    convert_to='mlprogram',
    compute_units=ct.ComputeUnit.ALL,
)

# 4. 保存
mlmodel.save('model.mlpackage')
```

**转换性能：**

- 转换时间: 3.3 秒
- 模型大小: 9.71 MB → 4.95 MB（减少 49%）

**结论：** ✅ **目前唯一可行的方案**

---

### 转换方案总结

| 方案 | 可行性 | 说明 |
|------|--------|------|
| **onnx-coreml** | ❌ 已弃用 | 与新版 coremltools 不兼容 |
| **coremltools 直接转 ONNX** | ❌ 已移除 | coremltools 8.x 不再支持 |
| **PyTorch → CoreML** | ✅ 推荐 | 需要原始 PyTorch 模型 |
| **TensorFlow → CoreML** | ✅ 可用 | 需要原始 TF 模型 |
| **ONNX Runtime + CoreML Provider** | ✅ 替代方案 | 运行时转换，无需手动转换 |

---

## 最佳实践建议

### 场景 1：只有 ONNX 模型，无原始代码

**推荐方案：** ONNX Runtime + CoreML Provider

```python linenums="1"
import onnxruntime as ort

# 创建 session，自动使用 CoreML
session = ort.InferenceSession(
    'model.onnx',
    providers=['CoreMLExecutionProvider', 'CPUExecutionProvider']
)

# 推理
output = session.run(None, {'input': input_data})
```

**适用场景：**

- ✅ 需要跨平台部署
- ✅ 模型频繁更新
- ✅ 追求开发效率
- ⚠️ 可以接受较慢的推理速度（比原生慢 20 倍）

---

### 场景 2：有原始 PyTorch/TensorFlow 模型

**推荐方案：** 直接转换为 CoreML

```python linenums="1"
# 转换脚本
import torch
import coremltools as ct

def convert_to_coreml(pytorch_model_path, output_path):
    # 加载模型
    model = torch.jit.load(pytorch_model_path)
    model.eval()

    # 追踪
    example_input = torch.rand(1, 3, 224, 224)
    traced_model = torch.jit.trace(model, example_input)

    # 转换
    mlmodel = ct.convert(
        traced_model,
        inputs=[ct.TensorType(name="input", shape=(1, 3, 224, 224))],
        convert_to='mlprogram',
        compute_units=ct.ComputeUnit.ALL,
    )

    # 保存
    mlmodel.save(output_path)
    print(f"✅ 已保存到: {output_path}")

# 使用
convert_to_coreml('model.pt', 'model.mlpackage')
```

**适用场景：**

- ✅ 仅支持 Apple 设备
- ✅ 追求极致性能（快 20 倍）
- ✅ 移动端应用（模型更小）
- ✅ 生产环境部署

---

### 场景 3：跨平台桌面应用

**推荐方案：** ONNX Runtime，根据平台选择 Provider

```python linenums="1"
import onnxruntime as ort
import platform

# 根据平台选择最佳 provider
def get_best_providers():
    system = platform.system()
    if system == 'Darwin':  # macOS
        return ['CoreMLExecutionProvider', 'CPUExecutionProvider']
    elif system == 'Windows':
        return ['DmlExecutionProvider', 'CPUExecutionProvider']
    else:  # Linux
        return ['CUDAExecutionProvider', 'CPUExecutionProvider']

session = ort.InferenceSession('model.onnx', providers=get_best_providers())
```

---

### 场景 4：iOS/macOS 原生应用

**推荐方案：** 使用 CoreML（Swift/Objective-C）

```swift
import CoreML

// 加载模型
guard let model = try? MobileNetV3() else {
    fatalError("Failed to load model")
}

// 准备输入
let input = MobileNetV3Input(input: inputImage)

// 推理
if let output = try? model.prediction(input: input) {
    print("Prediction: \\(output)")
}
```

---

### 场景 5：实时应用（AR/VR/直播）

**推荐方案：** 原生 CoreML

**原因：**

- 推理延迟 0.3 ms（vs ONNX Runtime 6.4 ms）
- 延迟稳定，P99 < 0.5 ms
- 更低的功耗

---

## 性能优化技巧

### 1. 固定输入形状

动态形状会降低性能，建议固定：

```python linenums="1"
import onnx
from onnx import shape_inference

# 加载模型
model = onnx.load('model.onnx')

# 推断形状
inferred_model = shape_inference.infer_shapes(model)

# 保存
onnx.save(inferred_model, 'model_fixed.onnx')
```

### 2. 使用 FP16 量化

减小模型大小，提升速度：

```python linenums="1"
import coremltools as ct

mlmodel = ct.models.MLModel('model.mlpackage')

# 量化为 FP16
mlmodel_fp16 = ct.models.neural_network.quantization_utils.quantize_weights(
    mlmodel, nbits=16
)

mlmodel_fp16.save('model_fp16.mlpackage')
```

### 3. 模型预热

首次推理较慢，建议预热：

```python linenums="1"
# 预热
for _ in range(10):
    session.run(None, {'input': dummy_input})

# 正式推理
output = session.run(None, {'input': real_input})
```

### 4. 批处理

如果场景允许，使用批处理提升吞吐：

```python linenums="1"
# 批量推理
batch_input = np.stack([img1, img2, img3, img4])  # (4, 3, 224, 224)
outputs = session.run(None, {'input': batch_input})
```

---

## 常见问题 FAQ

### Q1: 为什么 ONNX Runtime 的 CoreML Provider 这么慢？

**A:** 主要有三个原因：

1. **转换开销**：即使有缓存，仍有数据格式转换
2. **模型太小**：MobileNetV3 太小，转换开销占比大
3. **优化不足**：ONNX Runtime 的 CoreML Provider 还不够成熟

**建议**：对于大模型（如 ResNet50），CoreML Provider 的优势会更明显。

---

### Q2: 原生 CoreML 的精度为什么会有差异？

**A:** 主要原因：

1. CoreML 可能使用 FP16（半精度）计算
2. 算子融合和优化导致计算顺序不同
3. 某些算子的实现差异

**建议**：

- 在实际数据上验证精度
- 对比 Top-5/Top-10 预测的一致性
- 如果差异过大，可以关闭某些优化

---

### Q3: 如何选择 CoreML 的计算单元？

```python linenums="1"
import coremltools as ct

# 所有可用单元（推荐）
compute_units=ct.ComputeUnit.ALL

# 仅 CPU
compute_units=ct.ComputeUnit.CPU_ONLY

# CPU + GPU
compute_units=ct.ComputeUnit.CPU_AND_GPU

# CPU + Neural Engine
compute_units=ct.ComputeUnit.CPU_AND_NE
```

**建议**：

- 开发调试：使用 `CPU_ONLY`（结果确定）
- 生产部署：使用 `ALL`（最快）

---

### Q4: CoreML 模型可以在 Windows/Linux 上运行吗？

**A:** ❌ 不可以。CoreML 是 Apple 的专有框架，仅支持 macOS/iOS/iPadOS/tvOS/watchOS。

如果需要跨平台，使用 ONNX Runtime。

---

### Q5: 如何在 Python 中使用 .mlpackage 模型？

```python linenums="1"
import coremltools as ct
import numpy as np

# 加载模型
model = ct.models.MLModel('model.mlpackage')

# 查看输入输出
spec = model.get_spec()
print("输入:", spec.description.input[0].name)
print("输出:", spec.description.output[0].name)

# 推理
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
output = model.predict({'input': input_data})
print("结果:", output)
```

---

## 完整测试代码

所有测试代码已整理并添加详细注释：

### 1. [test_coreml.py](https://gist.github.com/SWHL/fd48ffee4b39ece6f8c418031915872f#file-test_coreml-py) - CoreML 可用性和性能测试

测试 ONNX Runtime 的 CoreML Provider 是否可用，并对比 CoreML 和 CPU 的性能。

```bash
python test_coreml.py
```

**功能：**

- ✅ 检测 CoreML Provider 可用性
- ✅ 创建测试 ONNX 模型
- ✅ 对比 CoreML 和 CPU 性能
- ✅ 验证输出精度

---

### 2. [compare_coreml_methods.py](https://gist.github.com/SWHL/fd48ffee4b39ece6f8c418031915872f#file-compare_coreml_methods-py) - 两种方案完整对比

对比 ONNX Runtime + CoreML Provider 和原生 CoreML 的性能和精度。

```bash
python compare_coreml_methods.py
```

**功能：**

- ✅ 从 PyTorch 导出/转换模型
- ✅ 对比加载时间
- ✅ 对比推理性能（平均/P50/P95/P99）
- ✅ 对比模型大小
- ✅ 精度验证（多样本）
- ✅ Top-5 预测一致性检查

---

### 3. [onnx_to_coreml_modern.py](https://gist.github.com/SWHL/fd48ffee4b39ece6f8c418031915872f#file-onnx_to_coreml_modern-py) - ONNX 转换工具

尝试将 ONNX 模型转换为 CoreML（会失败，用于演示当前限制）。

```bash
python onnx_to_coreml_modern.py model.onnx --info-only
```

**功能：**

- ✅ 显示 ONNX 模型详细信息
- ✅ 尝试转换（演示不可行）
- ✅ 精度验证
- ✅ 完整的错误处理和提示

---

## 结论

经过详细的测试和分析，我们得出以下结论：

### 性能对比总结

| 方案 | 推理速度 | 模型大小 | 跨平台 | 易用性 | 推荐度 |
|------|---------|---------|--------|--------|--------|
| **ONNX Runtime (CPU)** | 5.2 ms | 9.71 MB | ✅ | ⭐⭐⭐⭐⭐ | 开发首选 |
| **ONNX Runtime (CoreML)** | 6.4 ms | 9.71 MB | ✅ | ⭐⭐⭐⭐ | - |
| **原生 CoreML** | **0.3 ms** 🚀 | **4.95 MB** | ❌ | ⭐⭐⭐ | 生产首选 |

### 核心发现

1. **原生 CoreML 性能极佳**：比 ONNX Runtime 快 **20.6 倍**
2. **ONNX Runtime 的 CoreML Provider 不理想**：反而比 CPU 慢 30%
3. **直接转换 ONNX → CoreML 不可行**：必须通过原始框架
4. **精度有差异**：需要在实际应用中验证是否可接受

### 选择建议

```text
┌─────────────────────────────────────────────────────────┐
│  需要跨平台？                                              │
│    ├─ 是 → ONNX Runtime (CPU Provider)                  │
│    └─ 否 → 继续                                           │
│                                                          │
│  有原始 PyTorch/TF 模型？                                │
│    ├─ 是 → 原生 CoreML（快 20 倍）                      │
│    └─ 否 → ONNX Runtime + CoreML Provider              │
│                                                          │
│  追求极致性能？                                           │
│    ├─ 是 → 原生 CoreML                                  │
│    └─ 否 → ONNX Runtime                                 │
└─────────────────────────────────────────────────────────┘
```

### 未来展望

- **ONNX Runtime 的 CoreML Provider 还需优化**：期待未来版本性能提升
- **直接 ONNX → CoreML 转换**：希望 Apple 或社区提供更好的工具
- **量化和优化**：探索 FP16/INT8 量化对性能的影响

---

## 参考资源

- [ONNX Runtime 文档](https://onnxruntime.ai/)
- [CoreML Tools 文档](https://coremltools.readme.io/)
- [Apple CoreML 官方文档](https://developer.apple.com/documentation/coreml)
