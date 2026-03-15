# 09-Output-Parsers - 输出解析

> 将 LLM 的输出转换为结构化数据

---

## 🎯 学习目标

- ✅ 理解 Output Parser 的作用
- ✅ 掌握 Pydantic 解析
- ✅ 学会 JSON 解析
- ✅ 能够处理解析错误

---

## 📚 核心概念

### 为什么需要 Output Parser？

LLM 输出是文本，但我们需要结构化数据：
- JSON
- Python 对象
- 特定格式

### 常见 Parser 类型

| Parser | 用途 |
|--------|------|
| StrOutputParser | 字符串 |
| PydanticOutputParser | Pydantic 模型 |
| JSONOutputParser | JSON |
| EnumOutputParser | 枚举 |

---

## 💻 示例代码

### 示例 1: Pydantic 解析

```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_anthropic import ChatAnthropic

# 定义输出结构
class Person(BaseModel):
    name: str = Field(description="人名")
    age: int = Field(description="年龄")
    occupation: str = Field(description="职业")

# 创建解析器
parser = PydanticOutputParser(pydantic_object=Person)

# 提示
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "提取信息：{format_instructions}"),
    ("human", "{text}")
]).partial(format_instructions=parser.get_format_instructions())

# 执行
chain = prompt | ChatAnthropic(model="claude-3-sonnet-20240229") | parser
result = chain.invoke({"text": "张三，35 岁，是一名工程师"})
print(result)  # Person(name='张三', age=35, occupation='工程师')
```

### 示例 2: JSON 解析

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
prompt = ChatPromptTemplate.from_template(
    "提取信息为 JSON: {format_instructions}\n{text}"
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | ChatAnthropic(model="claude-3-sonnet-20240229") | parser
result = chain.invoke({"text": "..."})
```

---

## 📝 练习

1. 创建一个联系人提取器
2. 实现 JSON 格式输出
3. 处理解析错误

---

**继续学习：[10-Real-World](../10-real-world/README.md)** 🚀
