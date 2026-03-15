# 08-Vector-Stores - 向量数据库

> 高效存储和检索语义向量

---

## 🎯 学习目标

- ✅ 理解向量数据库的作用
- ✅ 掌握 FAISS 的使用
- ✅ 学会 ChromaDB
- ✅ 了解向量优化技巧

---

## 📚 核心概念

### 什么是向量数据库？

存储向量嵌入，支持语义搜索：
- 不是关键词匹配
- 而是语义相似度
- "苹果" 可以搜到 "水果"

### 常见向量数据库

| 数据库 | 类型 | 特点 |
|--------|------|------|
| FAISS | 内存 | 快速、简单 |
| ChromaDB | 本地/服务器 | 持久化、易用 |
| Pinecone | 云服务 | 大规模、托管 |
| Weaviate | 本地/云 | 图数据库 |

---

## 💻 示例代码

### 示例 1: FAISS

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 创建嵌入
embeddings = OpenAIEmbeddings()

# 创建向量库
texts = ["苹果", "香蕉", "橙子"]
vectorstore = FAISS.from_texts(texts, embeddings)

# 检索
results = vectorstore.similarity_search("水果")
print(results)
```

### 示例 2: ChromaDB

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 持久化存储
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings()
)

# 添加文档
vectorstore.add_texts(["文档 1", "文档 2"])

# 检索
results = vectorstore.similarity_search("查询")
```

---

## 📝 练习

1. 创建 FAISS 向量库
2. 实现持久化存储
3. 比较不同数据库的性能

---

**继续学习：[09-Output-Parsers](../09-output-parsers/README.md)** 🚀
