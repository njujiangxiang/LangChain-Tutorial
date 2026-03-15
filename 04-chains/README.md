# 04-Chains - 链式调用

> 将多个操作串联起来，构建复杂的 LLM 应用

---

## 🎯 学习目标

- ✅ 理解 Chain 的概念
- ✅ 掌握 LLMChain 的使用
- ✅ 学会创建 SequentialChain
- ✅ 能够自定义 Chain

---

## 📚 核心概念

### 什么是 Chain？

Chain 是将多个组件（模型、提示、解析器等）组合在一起的方式。

```
输入 → Prompt → LLM → Output Parser → 输出
      ↓
   Chain
```

### 常见 Chain 类型

| Chain | 用途 |
|-------|------|
| LLMChain | 基础链 |
| SequentialChain | 顺序执行多个链 |
| TransformChain | 转换输入/输出 |
| RouterChain | 根据输入路由到不同链 |

---

## 💻 示例代码

### 示例 1: 基础 LLMChain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

# 组件
prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
parser = StrOutputParser()

# 组合成链
chain = prompt | llm | parser

# 执行
result = chain.invoke({"topic": "程序员"})
print(result)
```

### 示例 2: SequentialChain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

# 链 1: 生成主题
prompt1 = ChatPromptTemplate.from_template("列出 3 个{domain}领域的热门话题")
chain1 = prompt1 | ChatAnthropic(model="claude-3-sonnet-20240229")

# 链 2: 详细解释
prompt2 = ChatPromptTemplate.from_template("详细解释这个话题：{topic}")
chain2 = prompt2 | ChatAnthropic(model="claude-3-sonnet-20240229")

# 顺序执行
topics = chain1.invoke({"domain": "人工智能"})
explanation = chain2.invoke({"topic": topics.content})
print(explanation.content)
```

---

## 📝 练习

1. 创建一个简单的问答链
2. 设计一个多步骤的内容生成链
3. 实现一个自定义 Chain

---

**继续学习：[05-Agents](../05-agents/README.md)** 🚀
