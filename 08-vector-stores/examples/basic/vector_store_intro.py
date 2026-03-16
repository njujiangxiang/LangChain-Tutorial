"""
示例：向量数据库基础

演示向量数据库的基本用法
"""

from dotenv import load_dotenv
import os

load_dotenv()


def test_faiss():
    """测试 FAISS 向量存储"""
    print("=" * 60)
    print("FAISS 向量存储")
    print("=" * 60)
    
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import FakeEmbeddings
    from langchain_core.documents import Document
    
    # 使用模拟 embedding (实际使用需要真实模型)
    embeddings = FakeEmbeddings(size=10)
    
    # 创建文档
    documents = [
        Document(page_content="机器学习是人工智能的分支", metadata={"source": "doc1"}),
        Document(page_content="深度学习使用神经网络", metadata={"source": "doc2"}),
        Document(page_content="Python 是流行的编程语言", metadata={"source": "doc3"}),
    ]
    
    # 创建向量存储
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    print(f"文档数量：{len(vectorstore.index_to_docstore_id)}")
    
    # 相似性搜索
    query = "什么是机器学习？"
    results = vectorstore.similarity_search(query, k=2)
    
    print(f"\n查询：{query}")
    print(f"最相关的 {len(results)} 个结果:")
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.page_content} (来源：{doc.metadata['source']})")


def test_chroma():
    """测试 ChromaDB 向量存储"""
    print("\n" + "=" * 60)
    print("ChromaDB 向量存储")
    print("=" * 60)
    
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import FakeEmbeddings
        from langchain_core.documents import Document
        
        embeddings = FakeEmbeddings(size=10)
        
        documents = [
            Document(page_content="北京是中国的首都", metadata={"city": "北京"}),
            Document(page_content="上海是经济中心", metadata={"city": "上海"}),
            Document(page_content="广州是南方大城市", metadata={"city": "广州"}),
        ]
        
        # 创建向量存储
        vectorstore = Chroma.from_documents(documents, embeddings)
        
        print(f"文档数量：{len(vectorstore._collection.get()['ids'])}")
        
        # 搜索
        query = "哪个城市是首都？"
        results = vectorstore.similarity_search(query, k=1)
        
        print(f"\n查询：{query}")
        print(f"结果：{results[0].page_content}")
        
    except Exception as e:
        print(f"需要安装：pip install chromadb")
        print(f"错误：{e}")


def test_in_memory_vectorstore():
    """测试内存向量存储"""
    print("\n" + "=" * 60)
    print("内存向量存储")
    print("=" * 60)
    
    from langchain_community.vectorstores import InMemoryVectorStore
    from langchain_community.embeddings import FakeEmbeddings
    from langchain_core.documents import Document
    
    embeddings = FakeEmbeddings(size=10)
    
    documents = [
        Document(page_content="苹果是一种水果", metadata={"type": "水果"}),
        Document(page_content="香蕉富含钾元素", metadata={"type": "水果"}),
        Document(page_content="Python 可以数据分析", metadata={"type": "编程"}),
    ]
    
    vectorstore = InMemoryVectorStore.from_documents(documents, embeddings)
    
    print(f"存储文档数：{len(vectorstore._vectorstore)}")
    
    # 搜索
    query = "有什么水果？"
    results = vectorstore.similarity_search(query, k=2)
    
    print(f"\n查询：{query}")
    for doc in results:
        print(f"  - {doc.page_content}")


def test_vectorstore_with_retriever():
    """测试向量存储 + 检索器"""
    print("\n" + "=" * 60)
    print("向量存储 + 检索器")
    print("=" * 60)
    
    from langchain_community.vectorstores import InMemoryVectorStore
    from langchain_community.embeddings import FakeEmbeddings
    from langchain_core.documents import Document
    
    embeddings = FakeEmbeddings(size=10)
    
    documents = [
        Document(page_content="LangChain 是 LLM 应用开发框架"),
        Document(page_content="向量数据库用于存储 embeddings"),
        Document(page_content="RAG 结合检索和生成"),
    ]
    
    vectorstore = InMemoryVectorStore.from_documents(documents, embeddings)
    
    # 创建检索器
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )
    
    # 使用检索器
    query = "什么是 LangChain？"
    results = retriever.invoke(query)
    
    print(f"查询：{query}")
    print(f"检索到 {len(results)} 个相关文档:")
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.page_content}")


def vectorstore_comparison():
    """向量存储对比"""
    print("\n" + "=" * 60)
    print("向量存储对比")
    print("=" * 60)
    
    print("""
    | 向量存储      | 特点                      | 适用场景          |
    |--------------|--------------------------|------------------|
    | FAISS        | Facebook 开源，快速高效    | 本地部署，中小规模 |
    | ChromaDB     | 轻量级，易用              | 开发测试，小规模  |
    | Pinecone     | 云服务，自动扩展          | 生产环境，大规模  |
    | Weaviate     | 开源 + 云，支持混合搜索    | 复杂查询场景      |
    | Milvus       | 高性能，分布式            | 大规模生产环境    |
    | Qdrant       | Rust 编写，高性能          | 需要高性能场景    |
    
    💡 选择建议:
    - 开发测试：ChromaDB 或 InMemoryVectorStore
    - 本地部署：FAISS
    - 生产环境：Pinecone、Weaviate、Milvus
    - 大规模：Milvus、Qdrant
    """)


if __name__ == "__main__":
    print("\n🗄️ 向量数据库基础示例\n")
    
    test_faiss()
    test_chroma()
    test_in_memory_vectorstore()
    test_vectorstore_with_retriever()
    vectorstore_comparison()
    
    print("\n✅ 所有测试完成！")
