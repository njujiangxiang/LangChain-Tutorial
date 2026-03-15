# 01-Core Concepts - 核心概念

> 理解 LangChain 的核心概念是掌握这个框架的基础

---

## 🎯 学习目标

- ✅ 理解 LLM 的工作原理
- ✅ 掌握 Token 的概念
- ✅ 了解 LangChain 的架构设计
- ✅ 熟悉基本组件：Models、Prompts、Chains、Agents

---

## 📚 理论部分

### 1. LLM 基础

**什么是 LLM？**
- Large Language Model (大型语言模型)
- 基于 Transformer 架构
- 通过海量文本训练
- 能够理解和生成人类语言

**LLM 能做什么？**
- 文本生成
- 问答
- 翻译
- 摘要
- 代码生成
- 推理

### 2. Token 理解

**什么是 Token？**
- LLM 处理文本的基本单位
- 可以是单词、子词或字符
- 英文：1 Token ≈ 4 个字符 ≈ 0.75 个单词
- 中文：1 个汉字 ≈ 1-2 个 Token

**Token 计算示例：**
```
"Hello, world!" → 3 Tokens
"你好，世界！" → 4-6 Tokens
```

**为什么重要？**
- 影响 API 调用成本
- 限制上下文长度
- 影响响应速度

### 3. LangChain 架构

```
┌─────────────────────────────────────────────────────────┐
│                    LangChain 应用                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Models  │  │ Prompts │  │ Chains  │  │ Agents  │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
│       ↓            ↓            ↓            ↓         │
│  ┌─────────────────────────────────────────────────┐   │
│  │            LangChain Core                       │   │
│  └─────────────────────────────────────────────────┘   │
│       ↓            ↓            ↓            ↓         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Memory  │  │Retrieval│  │ Parsers │  │ Tools   │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 4. 基本组件

#### Models (模型)
- **LLM**: 基础语言模型
- **ChatModel**: 聊天模型
- **Embeddings**: 嵌入模型

#### Prompts (提示)
- **PromptTemplate**: 提示模板
- **FewShotPrompt**: 少样本提示
- **SystemMessage**: 系统消息

#### Chains (链)
- **LLMChain**: 基础链
- **SequentialChain**: 顺序链
- **TransformChain**: 转换链

#### Agents (智能体)
- **ReAct Agent**: 推理 + 行动
- **Tool Use**: 工具使用
- **Memory**: 记忆

---

## 💻 实践代码

### 示例 1: 基础 LLM 调用

```python
# examples/basic/llm_call.py
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 使用 Anthropic Claude
llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
response = llm.invoke("你好，请介绍一下自己")
print(response.content)
```

### 示例 2: Token 计数

```python
# examples/basic/token_count.py
def count_tokens(text: str) -> int:
    """估算文本的 Token 数量"""
    # 简单估算：英文 4 字符≈1 Token，中文 1 字≈1.5 Token
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - chinese_chars
    return chinese_chars * 1.5 + other_chars // 4

text = "Hello, 你好！LangChain is awesome."
print(f"文本：{text}")
print(f"估算 Token 数：{count_tokens(text)}")
```

### 示例 3: 提示模板

```python
# examples/basic/prompt_template.py
from langchain_core.prompts import ChatPromptTemplate

# 创建提示模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，擅长{skill}"),
    ("human", "{question}")
])

# 格式化提示
messages = template.format_messages(
    role="AI 助手",
    skill="解释复杂概念",
    question="什么是机器学习？"
)

print(messages)
```

---

## 📝 练习

### 练习 1: 环境验证
运行 `../../00-setup/examples/verify_install.py` 确保环境配置正确

### 练习 2: 第一个 LLM 调用
创建一个 Python 脚本，调用 LLM 并让它回答一个问题

### 练习 3: Token 计算
编写一个函数，计算给定文本的 Token 数量

---

## 🔗 相关资源

- [LangChain 官方文档 - Core Concepts](https://python.langchain.com/docs/concepts/)
- [Understanding Tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
- [Transformer 架构详解](https://jalammar.github.io/illustrated-transformer/)

---

## 📋 检查清单

- [ ] 理解 LLM 的基本原理
- [ ] 知道 Token 是什么
- [ ] 了解 LangChain 的架构
- [ ] 能够调用基础 LLM
- [ ] 能够创建提示模板

---

**完成学习后，继续下一章：[02-Models](../02-models/README.md)** 🚀
