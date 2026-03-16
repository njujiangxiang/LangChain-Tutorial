"""
示例：ChromaDB 高级使用

演示 ChromaDB 向量数据库的高级功能
"""

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()


def chroma_persistent_storage():
    """ChromaDB 持久化存储"""
    print("=" * 60)
    print("ChromaDB 持久化存储")
    print("=" * 60)
    
    # 示例文档
    documents = [
        Document(page_content="Python 是一种高级编程语言", metadata={"category": "language", "level": "basic"}),
        Document(page_content="机器学习是 AI 的重要分支", metadata={"category": "ai", "level": "intermediate"}),
        Document(page_content="深度学习使用神经网络", metadata={"category": "ai", "level": "advanced"}),
        Document(page_content="Django 是 Python Web 框架", metadata={"category": "web", "level": "intermediate"}),
    ]
    
    print(f"文档数量：{len(documents)}\n")
    
    try:
        # 创建 embeddings
        embeddings = OllamaEmbeddings(model="qwen3.5:9b")
        
        # 创建持久化向量存储
        persist_directory = "./chroma_db"
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        
        print(f"✅ 向量存储已保存到：{persist_directory}")
        
        # 相似度搜索
        query = "Python 编程"
        results = vectorstore.similarity_search(query, k=2)
        
        print(f"\n查询：{query}\n")
        print("检索结果:")
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc.page_content} [{doc.metadata.get('category')}]")
        
        # 重新加载
        print("\n重新加载持久化的向量存储...")
        loaded_vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        
        print(f"✅ 已加载 {len(loaded_vectorstore.get()['ids'])} 个文档")
        
    except Exception as e:
        print(f"⚠️  演示模式：{e}")
        print("\n代码示例:")
        print("""
        from langchain_community.vectorstores import Chroma
        from langchain_ollama import OllamaEmbeddings
        
        embeddings = OllamaEmbeddings(model="qwen3.5:9b")
        
        # 持久化存储
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        # 加载已有存储
        loaded = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        """)


def chroma_metadata_filtering():
    """元数据过滤检索"""
    print("\n" + "=" * 60)
    print("ChromaDB 元数据过滤")
    print("=" * 60)
    
    documents = [
        Document(page_content="Python 基础语法", metadata={"category": "language", "level": "basic", "year": 2023}),
        Document(page_content="Python 进阶技巧", metadata={"category": "language", "level": "advanced", "year": 2024}),
        Document(page_content"机器学习入门", metadata={"category": "ai", "level": "basic", "year": 2023}),
        Document(page_content="深度学习实战", metadata={"category": "ai", "level": "advanced", "year": 2024}),
    ]
    
    print("文档库:")
    for doc in documents:
        print(f"  [{doc.metadata['category']}] [{doc.metadata['level']}] {doc.page_content}")
    
    print("\n元数据过滤示例:")
    print("""
    # 只检索 AI 类别
    filter1 = {"category": "ai"}
    
    # 只检索 advanced 级别
    filter2 = {"level": "advanced"}
    
    # 组合过滤
    filter3 = {"category": "ai", "level": "advanced"}
    
    # 使用操作符
    filter4 = {"year": {"$gte": 2024}}
    """)


def chroma_collection_management():
    """集合管理"""
    print("\n" + "=" * 60)
    print("ChromaDB 集合管理")
    print("=" * 60)
    
    print("""
    ChromaDB 支持多集合管理:
    
    1. 创建集合
       chroma.create_collection("python_docs")
       chroma.create_collection("ai_docs")
    
    2. 添加到集合
       collection.add(documents=docs, ids=ids)
    
    3. 查询集合
       results = collection.query(query_texts=[query])
    
    4. 删除集合
       chroma.delete_collection("python_docs")
    
    5. 列出集合
       collections = chroma.list_collections()
    
    适用场景:
    - 多租户系统
    - 多知识库管理
    - 数据隔离
    """)


def chroma_batch_operations():
    """批量操作"""
    print("\n" + "=" * 60)
    print("ChromaDB 批量操作")
    print("=" * 60)
    
    print("""
    批量操作优化性能:
    
    1. 批量添加
       vectorstore.add_documents(
           documents=large_doc_list,
           batch_size=100
       )
    
    2. 批量删除
       vectorstore.delete(ids=id_list)
    
    3. 批量更新
       vectorstore.update_document(id, new_doc)
    
    4. 分页查询
       results = vectorstore.similarity_search(
           query,
           k=10,
           offset=0
       )
    
    性能建议:
    - 批量大小：100-500
    - 避免单次过多数据
    - 定期清理无用数据
    """)


if __name__ == "__main__":
    print("\n📚 ChromaDB 高级使用示例\n")
    
    chroma_persistent_storage()
    chroma_metadata_filtering()
    chroma_collection_management()
    chroma_batch_operations()
    
    print("\n✅ ChromaDB 高级示例完成！")
