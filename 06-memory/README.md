# 06-Memory - 记忆系统

> 让 LLM 记住对话历史，实现连贯的多轮对话

---

## 🎯 学习目标

- ✅ 理解 Memory 的作用
- ✅ 掌握 ConversationBufferMemory
- ✅ 学会 ConversationSummaryMemory
- ✅ 能够自定义 Memory

---

## 📚 核心概念

### 为什么需要 Memory？

LLM 本身是无状态的，每次调用都是独立的。Memory 让 LLM"记住"之前的对话。

### Memory 类型

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| Buffer | 保存所有历史 | 短对话 |
| Summary | 总结历史 | 长对话 |
| Vector | 向量检索 | 大量历史 |
| Entity | 实体记忆 | 知识图谱 |

---

## 💻 示例代码

### 示例 1: ConversationBufferMemory

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 带记忆的提示
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 链
chain = prompt | ChatAnthropic(model="claude-3-sonnet-20240229")

# 对话
memory.save_context({"input": "你好"}, {"output": "你好！有什么可以帮助你的？"})
history = memory.load_memory_variables({})
```

### 示例 2: ConversationSummaryMemory

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(
    llm=ChatAnthropic(model="claude-3-sonnet-20240229"),
    memory_key="summary"
)

# 自动总结长对话
```

---

## 📝 练习

1. 创建一个多轮对话机器人
2. 实现对话总结功能
3. 比较不同 Memory 的效果

---

**继续学习：[07-Retrieval](../07-retrieval/README.md)** 🚀
