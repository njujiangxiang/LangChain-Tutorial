# 07-Retrieval - 检索增强 (RAG)

> 让 LLM 能够访问外部知识，回答私有数据相关问题

---

## 🎯 学习目标

- ✅ 理解 RAG 的工作原理
- ✅ 掌握 Document 加载
- ✅ 学会 Text 分割
- ✅ 了解检索策略

---

## 📚 RAG 架构

```
┌─────────────────────────────────────────────────────┐
│                    RAG Pipeline                      │
├─────────────────────────────────────────────────────┤
│  文档 → 分割 → 嵌入 → 向量库 → 检索 → 增强提示 → LLM │
└─────────────────────────────────────────────────────┘
```

### 核心步骤

1. **加载**: 读取文档 (PDF、Word、网页等)
2. **分割**: 将长文本分成小块
3. **嵌入**: 转换为向量
4. **存储**: 存入向量数据库
5. **检索**: 查询相关片段
6. **增强**: 将检索结果加入提示
7. **生成**: LLM 生成答案

---

## 💻 示例代码

### 示例 1: 文档加载

```python
from langchain_community.document_loaders import PyPDFLoader

# 加载 PDF
loader = PyPDFLoader("document.pdf")
docs = loader.load()

print(f"加载了 {len(docs)} 页")
print(f"第一页内容：{docs[0].page_content[:200]}")
```

### 示例 2: 文本分割

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)

chunks = splitter.split_documents(docs)
print(f"分割成 {len(chunks)} 个片段")
```

### 示例 3: 检索问答

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# 创建向量库
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 检索器
retriever = vectorstore.as_retriever()

# 提示
prompt = ChatPromptTemplate.from_messages([
    ("system", "根据以下上下文回答：{context}"),
    ("human", "{question}")
])

# 问答链
question = "文档的主要内容是什么？"
results = retriever.invoke(question)
```

---

## 📝 练习

1. 加载一个 PDF 文档
2. 分割并创建向量索引
3. 实现问答功能

---

**继续学习：[08-Vector-Stores](../08-vector-stores/README.md)** 🚀
