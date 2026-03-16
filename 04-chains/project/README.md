# 04-Chains 项目实战 - 多步骤文档处理流水线

## 📋 项目概述

构建一个智能文档处理流水线，自动完成文档的摘要、翻译、格式化等多个处理步骤。

### 项目目标
- 掌握 LangChain 链式调用的实际应用
- 学会设计和实现多步骤处理流程
- 理解错误处理和容错机制

### 功能特性
- ✅ 文档摘要生成
- ✅ 多语言翻译
- ✅ 格式标准化
- ✅ 关键词提取
- ✅ 质量检查

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd 04-chains/project
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，配置 Ollama 或阿里云 API
# Ollama (本地):
OLLAMA_BASE_URL=http://localhost:11434

# 或阿里云:
# DASHSCOPE_API_KEY=your_key
```

### 3. 运行示例

```bash
# 基础示例
python examples/demo.py

# 使用 Ollama
python examples/demo.py --model ollama

# 使用阿里云
python examples/demo.py --model aliyun
```

---

## 📁 项目结构

```
project/
├── README.md              # 项目文档
├── requirements.txt       # 依赖列表
├── src/
│   ├── __init__.py
│   ├── pipeline.py        # 处理流水线核心
│   ├── chains.py          # 链定义
│   ├── utils.py           # 工具函数
│   └── config.py          # 配置管理
├── tests/
│   └── test_pipeline.py   # 测试代码
└── examples/
    └── demo.py            # 演示脚本
```

---

## 💡 核心代码示例

### 处理流水线

```python
from src.pipeline import DocumentPipeline

# 创建流水线
pipeline = DocumentPipeline(
    model="qwen3.5:9b",  # 或 "qwen-plus"
    enable_translation=True,
    enable_keyword_extraction=True
)

# 处理文档
result = pipeline.process("""
人工智能 (AI) 是计算机科学的一个分支，
致力于创建能够执行通常需要人类智能的任务的系统。
这些任务包括学习、推理、问题解决、感知和理解语言。
""")

print(f"摘要：{result.summary}")
print(f"关键词：{result.keywords}")
print(f"翻译：{result.translation}")
```

---

## 🔧 扩展建议

1. **添加更多处理步骤**
   - 情感分析
   - 实体识别
   - 文本分类

2. **支持更多模型**
   - OpenAI GPT
   - Anthropic Claude
   - 本地模型

3. **持久化存储**
   - 将处理结果保存到数据库
   - 实现结果缓存

4. **异步处理**
   - 使用 asyncio 提高并发性能
   - 支持批量文档处理

---

## 📝 学习要点

1. **链式设计模式**
   - 每个处理步骤独立可测试
   - 易于添加/移除步骤
   - 清晰的输入输出接口

2. **错误处理**
   - 单步骤失败不影响整体流程
   - 重试机制
   - 降级策略

3. **配置管理**
   - 环境变量配置
   - 运行时参数调整
   - 模型切换

---

## 🎯 练习任务

1. **基础**: 运行 demo.py，理解流水线工作原理
2. **进阶**: 添加一个新的处理步骤 (如情感分析)
3. **挑战**: 实现异步批量处理，支持并发处理多个文档

---

**祝你学习愉快！🎉**
