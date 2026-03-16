# 07-Retrieval 项目实战 - 文档问答系统 (RAG)

> 基于检索增强生成 (RAG) 的智能文档问答系统

---

## 🎯 项目目标

构建一个能够理解文档内容并回答相关问题的智能问答系统。

**核心功能**:
- ✅ 文档加载和解析
- ✅ 文本分块和向量化
- ✅ 相似度检索
- ✅ 上下文增强生成
- ✅ 支持多种文档格式

---

## 📁 项目结构

```
project/
├── README.md              # 本文件
├── requirements.txt       # 项目依赖
├── src/
│   ├── __init__.py
│   ├── document_loader.py # 文档加载
│   ├── text_splitter.py   # 文本分块
│   ├── vector_store.py    # 向量存储
│   ├── retriever.py       # 检索器
│   └── qa_system.py       # 问答系统
├── tests/
│   └── test_qa.py         # 测试文件
└── examples/
    └── demo.py            # 演示脚本
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd project
pip install -r requirements.txt
```

### 2. 准备文档

将 PDF/TXT/MD 文档放入 `documents/` 目录

### 3. 运行演示

```bash
python examples/demo.py
```

---

## 💻 核心代码

### 文档加载器 (src/document_loader.py)

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)

def load_document(filepath: str):
    """加载文档"""
    if filepath.endswith('.pdf'):
        loader = PyPDFLoader(filepath)
    elif filepath.endswith('.txt'):
        loader = TextLoader(filepath)
    elif filepath.endswith('.md'):
        loader = UnstructuredMarkdownLoader(filepath)
    else:
        raise ValueError("不支持的文件格式")
    
    return loader.load()
```

### 文本分块 (src/text_splitter.py)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(documents, chunk_size=500, chunk_overlap=50):
    """文本分块"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_documents(documents)
```

### 向量存储 (src/vector_store.py)

```python
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

def create_vectorstore(documents):
    """创建向量存储"""
    embeddings = OllamaEmbeddings(model="qwen3.5:9b")
    return FAISS.from_documents(documents, embeddings)
```

### 问答系统 (src/qa_system.py)

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class QASystem:
    def __init__(self, vectorstore):
        self.llm = ChatOllama(model="qwen3.5:9b")
        self.retriever = vectorstore.as_retriever()
        
        prompt = ChatPromptTemplate.from_template("""
        根据以下上下文回答问题：
        
        上下文：{context}
        
        问题：{question}
        
        答案：""")
        
        self.chain = prompt | self.llm | StrOutputParser()
    
    def ask(self, question: str) -> str:
        """回答问题"""
        docs = self.retriever.invoke(question)
        context = "\n\n".join([d.page_content for d in docs])
        return self.chain.invoke({"context": context, "question": question})
```

---

## 📝 使用示例

```python
from src.document_loader import load_document
from src.text_splitter import split_text
from src.vector_store import create_vectorstore
from src.qa_system import QASystem

# 1. 加载文档
docs = load_document("documents/manual.pdf")

# 2. 分块
chunks = split_text(docs)

# 3. 创建向量存储
vectorstore = create_vectorstore(chunks)

# 4. 创建问答系统
qa = QASystem(vectorstore)

# 5. 提问
answer = qa.ask("如何安装软件？")
print(f"答案：{answer}")
```

---

## 🧪 测试

```bash
# 运行测试
pytest tests/test_qa.py -v

# 测试用例
- 测试文档加载
- 测试文本分块
- 测试向量检索
- 测试问答准确性
```

---

## 🔧 配置选项

### 文本分块配置
```python
chunk_size = 500      # 块大小
chunk_overlap = 50    # 重叠大小
```

### 检索配置
```python
top_k = 3            # 返回文档数量
score_threshold = 0.7 # 相似度阈值
```

### 模型配置
```python
model = "qwen3.5:9b"  # Ollama 模型
temperature = 0.5     # 温度参数
```

---

## 📊 性能优化

1. **缓存机制**: 缓存常见问题答案
2. **批量处理**: 批量加载和向量化文档
3. **索引优化**: 使用 HNSW 等高效索引
4. **并行处理**: 多线程加载文档

---

## 🛡️ 注意事项

1. **文档质量**: 确保文档清晰、结构化
2. **隐私保护**: 不上传敏感文档到云端
3. **答案验证**: 重要信息需人工核实
4. **版权合规**: 遵守文档版权规定

---

## 📚 扩展方向

1. **多文档支持**: 同时检索多个文档
2. **混合检索**: 关键词 + 向量检索
3. **多轮对话**: 支持上下文对话
4. **答案溯源**: 标注答案来源
5. **Web 界面**: 使用 Streamlit 构建 UI

---

## 🎓 学习目标

完成本项目后，你将掌握:
- ✅ RAG 基本原理
- ✅ 文档加载和分块
- ✅ 向量检索技术
- ✅ 上下文增强生成
- ✅ 完整系统构建

---

**祝你学习愉快！🚀**
