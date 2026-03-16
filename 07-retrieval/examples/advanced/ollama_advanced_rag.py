"""
示例：Ollama 高级 RAG

演示高级检索增强生成技术
"""

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()


def advanced_chunking():
    """高级文本分块策略"""
    print("=" * 60)
    print("高级文本分块")
    print("=" * 60)
    
    # 示例长文本
    long_text = """
    人工智能 (AI) 是计算机科学的一个分支，致力于创建能够执行需要人类智能的任务的系统。
    机器学习 (ML) 是 AI 的一个子集，使用算法从数据中学习模式。
    深度学习 (DL) 是 ML 的一个子集，使用神经网络处理复杂模式。
    
    大语言模型 (LLM) 是基于深度学习的大型模型，能够理解和生成自然语言。
    代表性的 LLM 包括 GPT 系列、Claude、通义千问等。
    
    LangChain 是一个用于开发 LLM 应用的框架，提供以下核心功能:
    1. 模型集成 - 支持多种 LLM 提供商
    2. 链式调用 - 组合多个操作
    3. Agent 系统 - 自主执行任务
    4. 记忆管理 - 维护对话历史
    5. RAG - 检索增强生成
    """
    
    print(f"原始文本长度：{len(long_text)} 字符\n")
    
    # 不同分块策略
    strategies = [
        {"chunk_size": 100, "chunk_overlap": 20},
        {"chunk_size": 200, "chunk_overlap": 40},
        {"chunk_size": 300, "chunk_overlap": 60},
    ]
    
    for strategy in strategies:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=strategy["chunk_size"],
            chunk_overlap=strategy["chunk_overlap"],
        )
        
        chunks = splitter.split_text(long_text)
        
        print(f"分块策略：size={strategy['chunk_size']}, overlap={strategy['chunk_overlap']}")
        print(f"  分块数量：{len(chunks)}")
        print(f"  平均长度：{sum(len(c) for c in chunks) / len(chunks):.1f} 字符\n")


def multi_vector_retrieval():
    """多向量检索"""
    print("\n" + "=" * 60)
    print("多向量检索 - 不同粒度")
    print("=" * 60)
    
    # 文档
    documents = [
        Document(page_content="Python 是一种高级编程语言，由 Guido van Rossum 于 1989 年发明。", metadata={"source": "intro", "level": "basic"}),
        Document(page_content="Python 广泛应用于 Web 开发、数据分析、人工智能、自动化等领域。", metadata={"source": "apps", "level": "intermediate"}),
        Document(page_content="Django 和 Flask 是 Python 最流行的两个 Web 框架。", metadata={"source": "web", "level": "advanced"}),
    ]
    
    print("文档库:")
    for doc in documents:
        print(f"  [{doc.metadata['level']}] {doc.page_content[:50]}...")
    
    print("\n多向量检索策略:")
    print("1. 文档级向量 - 整体语义")
    print("2. 段落级向量 - 段落语义")
    print("3. 句子级向量 - 细粒度匹配")
    print("\n检索时合并多个粒度的结果，提高召回率。")


def reranking():
    """重排序 - 提高检索质量"""
    print("\n" + "=" * 60)
    print("检索重排序 (Reranking)")
    print("=" * 60)
    
    # 初始检索结果
    initial_results = [
        {"doc": "Python 编程入门教程", "score": 0.95, "relevance": "高"},
        {"doc": "Python Web 开发实战", "score": 0.88, "relevance": "中"},
        {"doc": "Python 数据分析指南", "score": 0.82, "relevance": "低"},
        {"doc": "Python 机器学习", "score": 0.78, "relevance": "中"},
    ]
    
    print("初始检索结果 (按向量相似度):")
    for i, result in enumerate(initial_results, 1):
        print(f"  {i}. {result['doc']} (score: {result['score']}, 相关性：{result['relevance']})")
    
    print("\n重排序后 (考虑相关性):")
    reranked = sorted(initial_results, key=lambda x: {"高": 3, "中": 2, "低": 1}[x["relevance"]], reverse=True)
    for i, result in enumerate(reranked, 1):
        print(f"  {i}. {result['doc']} (相关性：{result['relevance']}, 新排名：{i})")
    
    print("\n重排序方法:")
    print("1. Cross-Encoder 模型")
    print("2. LLM 重排序")
    print("3. 规则重排序 (如本例)")


def query_expansion():
    """查询扩展 - 提高召回率"""
    print("\n" + "=" * 60)
    print("查询扩展 (Query Expansion)")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 查询扩展 prompt
    expand_prompt = ChatPromptTemplate.from_template("""
    为以下查询生成 3 个相关的变体查询：
    
    原始查询：{query}
    
    要求:
    1. 保持原意
    2. 使用不同措辞
    3. 覆盖不同角度
    
    返回格式:
    变体 1: ...
    变体 2: ...
    变体 3: ...
    """)
    
    expand_chain = expand_prompt | llm | StrOutputParser()
    
    # 测试查询
    query = "Python 学习路线"
    
    print(f"原始查询：{query}\n")
    
    # 生成变体
    expansions = expand_chain.invoke({"query": query})
    
    print("扩展查询:")
    print(expansions)
    
    print("\n检索策略:")
    print("1. 用原始查询检索")
    print("2. 用每个变体查询检索")
    print("3. 合并所有结果")
    print("4. 去重和重排序")


def contextual_compression():
    """上下文压缩检索"""
    print("\n" + "=" * 60)
    print("上下文压缩检索")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 压缩 prompt
    compress_prompt = ChatPromptTemplate.from_template("""
    根据问题压缩文档内容：
    
    问题：{question}
    文档：{document}
    
    要求:
    1. 只保留与问题相关的信息
    2. 删除无关内容
    3. 保持关键信息完整
    
    压缩后:
    """)
    
    compress_chain = compress_prompt | llm | StrOutputParser()
    
    # 测试
    document = """
    Python 是一种高级编程语言，由 Guido van Rossum 于 1989 年发明，1991 年首次发布。
    Python 的设计哲学强调代码可读性，使用缩进来定义代码块。
    Python 支持多种编程范式，包括面向对象、函数式、过程式编程。
    Python 广泛应用于 Web 开发、数据分析、人工智能、科学计算、自动化脚本等领域。
    流行的 Python 框架包括 Django、Flask( Web 开发)、Pandas、NumPy(数据分析)、
    TensorFlow、PyTorch(机器学习)等。
    """
    
    question = "Python 应用于哪些领域？"
    
    print(f"问题：{question}\n")
    print(f"原始文档长度：{len(document)} 字符\n")
    
    # 压缩
    compressed = compress_chain.invoke({"question": question, "document": document})
    
    print(f"压缩后内容:\n{compressed}")
    print(f"\n压缩后长度：{len(compressed)} 字符")


def rag_evaluation():
    """RAG 系统评估"""
    print("\n" + "=" * 60)
    print("RAG 系统评估指标")
    print("=" * 60)
    
    print("""
    评估维度:
    
    1. 检索质量
       - Recall@K: 相关文档召回率
       - MRR: 第一个相关结果排名
       - NDCG: 排序质量
    
    2. 生成质量
       - 答案准确性 (与标准答案对比)
       - 答案相关性 (是否回答问题)
       - 事实一致性 (是否有幻觉)
       - 流畅度 (语言质量)
    
    3. 端到端指标
       - 用户满意度
       - 任务完成率
       - 响应时间
    
    4. 常见问题检测
       - 空检索检测
       - 上下文不相关
       - 答案长度异常
    """)


if __name__ == "__main__":
    print("\n🦙 Ollama 高级 RAG 示例\n")
    
    advanced_chunking()
    multi_vector_retrieval()
    reranking()
    query_expansion()
    contextual_compression()
    rag_evaluation()
    
    print("\n✅ Ollama 高级 RAG 示例完成！")
