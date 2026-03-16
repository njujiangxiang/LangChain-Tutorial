"""
示例：Ollama RAG 检索增强 - 中级

演示使用 Ollama 模型实现检索增强生成 (RAG)
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


def simple_rag_example():
    """简单 RAG 示例"""
    print("=" * 60)
    print("简单 RAG - 文档问答")
    print("=" * 60)
    
    # 示例文档
    documents = [
        Document(page_content="Python 是一种高级编程语言，由 Guido van Rossum 于 1989 年发明。", metadata={"source": "python_intro"}),
        Document(page_content="Python 广泛应用于 Web 开发、数据分析、人工智能、自动化等领域。", metadata={"source": "python_apps"}),
        Document(page_content="Python 的主要特点包括：语法简洁、易学易用、丰富的库、跨平台。", metadata={"source": "python_features"}),
        Document(page_content="学习 Python 建议从基础语法开始，然后选择感兴趣的方向深入。", metadata={"source": "python_learning"}),
    ]
    
    print(f"文档数量：{len(documents)}\n")
    
    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
    )
    splits = text_splitter.split_documents(documents)
    
    print(f"分块数量：{len(splits)}\n")
    
    # 创建向量存储 (使用 Ollama embedding)
    try:
        embeddings = OllamaEmbeddings(model="qwen3.5:9b")
        vectorstore = FAISS.from_documents(splits, embeddings)
        
        # 检索
        question = "Python 是什么？"
        print(f"问题：{question}\n")
        
        relevant_docs = vectorstore.similarity_search(question, k=2)
        
        print("检索到的相关文档:")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"{i}. {doc.page_content}")
        
        # 增强生成
        context = "\n\n".join([d.page_content for d in relevant_docs])
        
        llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
        
        prompt = ChatPromptTemplate.from_template("""
        根据以下上下文回答问题：
        
        上下文：
        {context}
        
        问题：{question}
        
        答案：""")
        
        chain = prompt | llm | StrOutputParser()
        
        result = chain.invoke({"context": context, "question": question})
        
        print(f"\n生成的答案:\n{result}")
        
    except Exception as e:
        print(f"⚠️  向量检索需要 Ollama embedding 模型")
        print(f"错误：{e}")
        print("\n演示代码结构:")
        print("""
        # RAG 流程:
        1. 文档加载
        2. 文本分块
        3. 生成 embedding
        4. 向量检索
        5. 增强生成
        """)


def multi_hop_retrieval():
    """多跳检索示例"""
    print("\n" + "=" * 60)
    print("多跳检索 (Multi-hop Retrieval)")
    print("=" * 60)
    
    # 多跳检索需要多次检索来获取完整信息
    documents = [
        Document(page_content="马云是阿里巴巴集团的创始人。", metadata={"source": "ma_yun"}),
        Document(page_content="阿里巴巴集团成立于 1999 年，总部位于杭州。", metadata={"source": "alibaba"}),
        Document(page_content="马云于 2019 年退休，张勇接任 CEO。", metadata={"source": "succession"}),
    ]
    
    print("文档库:")
    for doc in documents:
        print(f"  - {doc.page_content}")
    
    # 多跳问题
    question = "阿里巴巴创始人是谁？他在哪一年退休？"
    print(f"\n多跳问题：{question}")
    print("需要检索：1) 创始人信息 2) 退休时间")
    
    # 简化演示
    print("\n多跳检索流程:")
    print("  第 1 跳：检索'阿里巴巴创始人' -> 马云")
    print("  第 2 跳：检索'马云 退休' -> 2019 年")
    print("  合并答案：马云是阿里巴巴创始人，于 2019 年退休。")


def hybrid_search_example():
    """混合检索示例"""
    print("\n" + "=" * 60)
    print("混合检索 (关键词 + 向量)")
    print("=" * 60)
    
    print("""
    混合检索结合两种方法:
    
    1. 关键词检索 (BM25)
       - 优点：精确匹配术语
       - 缺点：语义理解弱
    
    2. 向量检索 (Embedding)
       - 优点：语义相似性
       - 缺点：可能漏掉精确匹配
    
    3. 混合策略
       - 分别检索
       - 结果合并
       - 重新排序
       - 取 top-k
    """)
    
    # 演示代码结构
    print("\n代码结构:")
    print("""
    # 关键词检索
    keyword_results = bm25_retriever.search(query, k=10)
    
    # 向量检索
    vector_results = vectorstore.similarity_search(query, k=10)
    
    # 合并和重排序
    combined = merge_results(keyword_results, vector_results)
    reranked = cross_encoder.rerank(query, combined)
    
    # 取 top-5
    final = reranked[:5]
    """)


def rag_with_sources():
    """带来源的 RAG"""
    print("\n" + "=" * 60)
    print("带来源引用的 RAG")
    print("=" * 60)
    
    documents = [
        Document(page_content="Python 由 Guido van Rossum 发明。", metadata={"source": "wiki", "page": "1"}),
        Document(page_content="Python 1.0 发布于 1994 年。", metadata={"source": "history", "page": "5"}),
        Document(page_content="Python 3.0 发布于 2008 年。", metadata={"source": "history", "page": "12"}),
    ]
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 要求 LLM 标注来源
    prompt = ChatPromptTemplate.from_template("""
    根据上下文回答问题，并标注信息来源。
    
    上下文：
    {context}
    
    问题：{question}
    
    答案格式：
    [答案内容]
    来源：[来源信息]
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    context = "\n".join([
        f"[{d.metadata['source']}:{d.metadata['page']}] {d.page_content}"
        for d in documents
    ])
    
    question = "Python 是什么时候发布的？"
    
    print(f"问题：{question}\n")
    
    # 演示输出格式
    print("期望输出:")
    print("""
    Python 1.0 于 1994 年发布，Python 3.0 于 2008 年发布。
    来源：[history:5], [history:12]
    """)


def rag_evaluation():
    """RAG 评估指标"""
    print("\n" + "=" * 60)
    print("RAG 系统评估")
    print("=" * 60)
    
    print("""
    评估 RAG 系统的关键指标:
    
    1. 检索质量
       - Recall@K: 相关文档是否被检索到
       - MRR: 第一个相关结果的排名
       - NDCG: 排序质量
    
    2. 生成质量
       - 答案准确性
       - 答案相关性
       - 事实一致性
    
    3. 端到端评估
       - 用户满意度
       - 任务完成率
       - 响应时间
    
    4. 常见问题检测
       - 检索为空
       - 上下文不相关
       - 答案幻觉
    """)


if __name__ == "__main__":
    print("\n🦙 Ollama RAG 检索增强 - 中级示例\n")
    
    simple_rag_example()
    multi_hop_retrieval()
    hybrid_search_example()
    rag_with_sources()
    rag_evaluation()
    
    print("\n✅ Ollama RAG 示例完成！")
