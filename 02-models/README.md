# 02-Models - 模型集成

> LangChain 支持多种 LLM 提供商，学会灵活切换和使用不同模型

---

## 🎯 学习目标

- ✅ 掌握 OpenAI 模型的使用
- ✅ 掌握 Anthropic Claude 模型的使用
- ✅ 了解本地模型部署
- ✅ 学会模型切换和比较

---

## 📚 支持的模型提供商

### 云模型
| 提供商 | 模型 | LangChain 类 |
|--------|------|-------------|
| OpenAI | GPT-3.5/4 | `ChatOpenAI` |
| Anthropic | Claude 2/3 | `ChatAnthropic` |
| Google | Gemini | `ChatGoogleGenerativeAI` |
| Azure | Azure OpenAI | `AzureChatOpenAI` |

### 本地模型
| 框架 | 模型 | LangChain 类 |
|------|------|-------------|
| Ollama | Llama/Mistral | `ChatOllama` |
| LM Studio | 各种模型 | `ChatOpenAI`(兼容) |

---

## 💻 示例代码

### 示例 1: OpenAI GPT

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.7,
    max_tokens=1024
)

response = llm.invoke("你好")
print(response.content)
```

### 示例 2: Anthropic Claude

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-opus-20240229",
    temperature=0.7,
    max_tokens=1024
)

response = llm.invoke("你好")
print(response.content)
```

---

## 📝 练习

1. 尝试不同的模型
2. 调整 temperature 参数观察输出变化
3. 比较不同模型的响应质量

---

**继续学习：[03-Prompts](../03-prompts/README.md)** 🚀
