"""
示例：FAISS 向量存储 - 中级

演示 FAISS 向量数据库的使用
"""

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()


def faiss_basic():
    """FAISS 基础使用"""
    print("=" * 60)
    print("FAISS 基础使用")
    print("=" * 60)
    
    # 示例文档
    documents = [
        Document(page_content="Python 是一种高级编程语言", metadata={"source": "intro"}),
        Document(page_content="机器学习是 AI 的分支", metadata={"source": "ml"}),
        Document(page_content="深度学习使用神经网络", metadata={"source": "dl"}),
    ]
    
    print(f"文档数量：{len(documents)}\n")
    
    try:
        # 创建 embeddings
        embeddings = OllamaEmbeddings(model="qwen3.5:9b")
        
        # 创建向量存储
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # 相似度搜索
        query = "什么是 Python？"
        results = vectorstore.similarity_search(query, k=2)
        
        print(f"查询：{query}\n")
        print("检索结果:")
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc.page_content} (source: {doc.metadata.get('source', 'unknown')})")
        
        # 保存到本地
        vectorstore.save_local("./faiss_index")
        print("\n✅ 向量索引已保存到 ./faiss_index")
        
    except Exception as e:
        print(f"⚠️  需要 Ollama embeddings 模型")
        print(f"错误：{e}")
        print("\n演示代码:")
        print("""
        from langchain_ollama import OllamaEmbeddings
        from langchain_community.vectorstores import FAISS
        
        embeddings = OllamaEmbeddings(model="qwen3.5:9b")
        vectorstore = FAISS.from_documents(documents, embeddings)
        results = vectorstore.similarity_search(query, k=2)
        """)


def faiss_with_metadata():
    """带过滤的检索"""
    print("\n" + "=" * 60)
    print("FAISS 带元数据过滤")
    print("=" * 60)
    
    documents = [
        Document(page_content="Python 基础教程", metadata={"level": "beginner", "category": "language"}),
        Document(page_content"Django Web 开发", metadata={"level": "intermediate", "category": "web"}),
        Document(page_content"机器学习实战", metadata={"level": "advanced", "category": "ai"}),
        Document(page_content="Python 数据分析", metadata={"level": "intermediate", "category": "data"}),
    ]
    
    print("文档库:")
    for doc in documents:
        print(f"  [{doc.metadata['level']}] [{doc.metadata['category']}] {doc.page_content}")
    
    print("\n元数据过滤检索:")
    print("  - 只检索 beginner 级别")
    print("  - 只检索 ai 类别")
    print("  - 组合过滤条件")


if __name__ == "__main__":
    print("\n📚 FAISS 向量存储示例\n")
    
    faiss_basic()
    faiss_with_metadata()
    
    print("\n✅ FAISS 示例完成！")
