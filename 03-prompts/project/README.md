# 03-Prompts 项目：提示词模板管理器

> 一个用于创建、管理和优化 LangChain 提示词模板的工具

## 📋 项目简介

本项目是一个提示词模板管理工具，帮助用户：
- 创建和管理可复用的提示词模板
- 支持多种模型后端 (OpenAI、Anthropic、Ollama、阿里云)
- 提供模板版本控制
- 支持模板测试和评估

## 🎯 功能特性

- ✅ 模板创建和存储
- ✅ 变量替换和格式化
- ✅ 多模型支持
- ✅ 模板版本管理
- ✅ 批量测试工具
- ✅ 性能评估

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# .env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DASHSCOPE_API_KEY=your_key_here  # 阿里云
```

### 3. 运行示例

```bash
# 运行主程序
python src/main.py

# 运行测试
python -m pytest tests/

# 运行示例
python examples/basic_usage.py
```

## 📁 项目结构

```
project/
├── README.md           # 项目文档
├── requirements.txt    # 依赖列表
├── src/               # 源代码
│   ├── __init__.py
│   ├── main.py        # 主程序
│   ├── template_manager.py  # 模板管理器
│   └── models.py      # 模型配置
├── tests/             # 测试代码
│   ├── __init__.py
│   └── test_templates.py
└── examples/          # 使用示例
    └── basic_usage.py
```

## 💡 使用示例

### 创建模板

```python
from src.template_manager import TemplateManager

manager = TemplateManager()

# 创建模板
manager.create_template(
    name="qa_template",
    template="请回答以下问题：{question}",
    description="基础问答模板"
)
```

### 使用模板

```python
# 加载模板
template = manager.load_template("qa_template")

# 格式化并调用模型
result = template.format(question="什么是 AI？")
response = llm.invoke(result)
```

## 📊 支持的模型

| 模型提供商 | 模型名称 | 配置方式 |
|-----------|---------|---------|
| Anthropic | Claude 3 | ANTHROPIC_API_KEY |
| OpenAI | GPT-4/3.5 | OPENAI_API_KEY |
| 阿里云 | Qwen-Max/Plus | DASHSCOPE_API_KEY |
| Ollama | qwen3.5:9b | 本地运行 |

## 🔧 高级功能

### 模板版本控制

```python
# 创建新版本
manager.create_version("qa_template", "v2.0", new_template)

# 查看历史
versions = manager.get_versions("qa_template")
```

### 批量测试

```python
# 批量测试模板
test_cases = [
    {"question": "问题 1"},
    {"question": "问题 2"},
]

results = manager.batch_test("qa_template", test_cases)
```

## 📝 最佳实践

1. **模板命名**: 使用清晰的命名，如 `qa_basic`, `summarize_long`
2. **变量命名**: 使用描述性变量名，如 `{question}` 而非 `{q}`
3. **版本管理**: 重要更改时创建新版本
4. **文档化**: 为每个模板添加描述和使用示例

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
