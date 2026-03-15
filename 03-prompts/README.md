# 03-Prompts - 提示工程

> 好的提示 = 好的输出。掌握提示工程是发挥 LLM 能力的关键

---

## 🎯 学习目标

- ✅ 理解提示模板的作用
- ✅ 掌握 Few-Shot 提示技巧
- ✅ 学会设计系统提示
- ✅ 了解提示优化方法

---

## 📚 核心概念

### 1. Prompt Template

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("human", "{input}")
])

prompt = template.format(role="翻译助手", input="Hello, world!")
```

### 2. Few-Shot Learning

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "你好", "output": "Hello"},
    {"input": "谢谢", "output": "Thank you"},
]

few_shot = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}")
    ])
)
```

### 3. System Prompt 设计

**好的 System Prompt:**
- 明确角色定位
- 设定行为准则
- 提供上下文
- 限制输出格式

---

## 💻 示例代码

### 示例 1: 基础提示模板

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

# 创建模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{profession}，擅长{skill}"),
    ("human", "请解释：{topic}")
])

# 格式化
prompt = template.format_messages(
    profession="数据科学家",
    skill="机器学习",
    topic="什么是神经网络？"
)

# 调用模型
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
response = llm.invoke(prompt)
print(response.content)
```

---

## 📝 练习

1. 创建一个翻译助手的提示模板
2. 设计一个 Few-Shot 示例
3. 优化系统提示以获得更好的输出

---

**继续学习：[04-Chains](../04-chains/README.md)** 🚀
