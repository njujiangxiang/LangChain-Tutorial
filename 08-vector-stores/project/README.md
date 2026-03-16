# 08-Vector-Stores 项目实战 - 知识库检索系统

> 基于向量数据库的企业级知识库检索系统

---

## 🎯 项目目标

构建一个支持多源文档、高效检索的企业知识库系统。

**核心功能**:
- ✅ 多格式文档支持
- ✅ 向量数据库 (FAISS/Chroma)
- ✅ 元数据过滤
- ✅ 批量文档管理
- ✅ 权限控制基础

---

## 📁 项目结构

```
project/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── vector_db.py        # 向量数据库管理
│   ├── document_manager.py # 文档管理
│   ├── search_engine.py    # 搜索引擎
│   └── api.py              # API 接口
├── tests/
│   └── test_search.py
└── examples/
    └── demo.py
```

---

## 🚀 快速开始

```bash
cd project
pip install -r requirements.txt
python examples/demo.py
```

---

## 💻 核心功能

### 1. 向量数据库管理

```python
from langchain_community.vectorstores import FAISS, Chroma
from langchain_ollama import OllamaEmbeddings

class VectorDB:
    def __init__(self, db_type="faiss"):
        self.embeddings = OllamaEmbeddings(model="qwen3.5:9b")
        self.db_type = db_type
        self.collections = {}
    
    def create_collection(self, name: str):
        """创建集合"""
        if self.db_type == "faiss":
            self.collections[name] = {"type": "faiss", "data": None}
        elif self.db_type == "chroma":
            self.collections[name] = Chroma(
                collection_name=name,
                embedding_function=self.embeddings,
                persist_directory=f"./chroma_db/{name}"
            )
    
    def add_documents(self, collection: str, documents):
        """添加文档"""
        if self.db_type == "faiss":
            if not self.collections[collection]["data"]:
                self.collections[collection]["data"] = FAISS.from_documents(
                    documents, self.embeddings
                )
            else:
                self.collections[collection]["data"].add_documents(documents)
```

### 2. 搜索引擎

```python
class SearchEngine:
    def __init__(self, vector_db):
        self.db = vector_db
    
    def search(self, query: str, collection: str, top_k: int = 5):
        """搜索"""
        if self.db.db_type == "faiss":
            store = self.db.collections[collection]["data"]
            return store.similarity_search(query, k=top_k)
        elif self.db.db_type == "chroma":
            store = self.db.collections[collection]
            return store.similarity_search(query, k=top_k)
    
    def search_with_filter(self, query: str, collection: str, filter_dict: dict):
        """带过滤的搜索"""
        # ChromaDB 支持元数据过滤
        if self.db.db_type == "chroma":
            store = self.db.collections[collection]
            return store.similarity_search(
                query,
                k=5,
                filter=filter_dict
            )
```

---

## 📝 使用示例

```python
from src.vector_db import VectorDB
from src.search_engine import SearchEngine

# 1. 创建数据库
db = VectorDB(db_type="chroma")
db.create_collection("company_wiki")

# 2. 添加文档
docs = load_documents("documents/")
db.add_documents("company_wiki", docs)

# 3. 搜索
engine = SearchEngine(db)
results = engine.search("报销流程", "company_wiki")

for doc in results:
    print(f"- {doc.page_content}")
```

---

## 🎓 学习目标

- ✅ 向量数据库原理
- ✅ FAISS vs ChromaDB
- ✅ 元数据过滤
- ✅ 批量文档管理
- ✅ 知识库系统设计

---

**祝你学习愉快！🚀**
