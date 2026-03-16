"""
示例：文档加载与分割

演示 RAG 中的文档加载和文本分割
"""

from dotenv import load_dotenv
import os

load_dotenv()


def test_text_loader():
    """测试文本文件加载"""
    print("=" * 60)
    print("文本文件加载")
    print("=" * 60)
    
    from langchain_community.document_loaders import TextLoader
    
    # 创建测试文件
    test_content = """
    机器学习是人工智能的一个分支。
    它使用算法来识别数据中的模式。
    这些模式可以用来做出预测或决策。
    常见的机器学习算法包括：
    1. 线性回归
    2. 决策树
    3. 神经网络
    """
    
    test_file = "/tmp/test_ml.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 加载
    loader = TextLoader(test_file, encoding="utf-8")
    documents = loader.load()
    
    print(f"加载的文档数：{len(documents)}")
    print(f"文档内容长度：{len(documents[0].page_content)}")
    print(f"前 100 字符：{documents[0].page_content[:100]}...")


def test_directory_loader():
    """测试目录加载"""
    print("\n" + "=" * 60)
    print("目录加载")
    print("=" * 60)
    
    from langchain_community.document_loaders import DirectoryLoader
    
    # 创建测试目录和文件
    os.makedirs("/tmp/test_docs", exist_ok=True)
    
    for i in range(3):
        with open(f"/tmp/test_docs/doc{i}.txt", "w", encoding="utf-8") as f:
            f.write(f"这是第{i+1}个测试文档。\n包含一些示例内容。")
    
    # 加载整个目录
    loader = DirectoryLoader(
        "/tmp/test_docs",
        glob="**/*.txt"
    )
    
    documents = loader.load()
    print(f"加载的文档数：{len(documents)}")
    
    for i, doc in enumerate(documents):
        print(f"文档{i+1}: {doc.metadata.get('source', 'unknown')}")


def test_text_splitting():
    """测试文本分割"""
    print("\n" + "=" * 60)
    print("文本分割")
    print("=" * 60)
    
    from langchain.text_splitter import CharacterTextSplitter
    
    # 长文本
    long_text = """
    机器学习是人工智能的一个重要分支，它研究如何让计算机从数据中学习。
    深度学习是机器学习的一个子领域，它使用神经网络来学习数据的表示。
    神经网络是由多层神经元组成的计算模型，可以学习复杂的模式。
    卷积神经网络 (CNN) 主要用于图像处理，循环神经网络 (RNN) 用于序列数据。
     Transformer 架构在自然语言处理领域取得了突破性进展。
    大语言模型 (LLM) 如 GPT、Claude 等都是基于 Transformer 架构。
    这些模型通过预训练和微调可以在各种任务上取得很好的效果。
    """
    
    # 创建分割器
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,  # 每块 100 字符
        chunk_overlap=20,  # 重叠 20 字符
        length_function=len
    )
    
    # 分割
    chunks = text_splitter.split_text(long_text)
    
    print(f"原文长度：{len(long_text)}")
    print(f"分割后的块数：{len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"\n块{i+1} ({len(chunk)}字符):")
        print(f"  {chunk.strip()}")


def test_recursive_splitting():
    """测试递归分割"""
    print("\n" + "=" * 60)
    print("递归文本分割")
    print("=" * 60)
    
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    long_text = """
    # 机器学习简介
    
    ## 什么是机器学习
    机器学习是人工智能的一个分支，让计算机从数据中学习而不需要明确编程。
    
    ## 主要类型
    ### 监督学习
    使用标记数据训练模型，用于分类和回归任务。
    
    ### 无监督学习
    从无标签数据中发现模式，用于聚类和降维。
    
    ### 强化学习
    通过与环境交互学习，用于决策和控制任务。
    
    ## 应用场景
    - 图像识别
    - 自然语言处理
    - 推荐系统
    - 自动驾驶
    """
    
    # 递归分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10,
        separators=["\n##", "\n###", "\n", "。", ""]
    )
    
    chunks = text_splitter.split_text(long_text)
    
    print(f"分割后的块数：{len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"\n块{i+1}:")
        print(f"  {chunk.strip()[:80]}...")


def test_code_splitting():
    """测试代码分割"""
    print("\n" + "=" * 60)
    print("代码分割")
    print("=" * 60)
    
    from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
    
    # Python 代码
    code = """
def add(a, b):
    \"\"\"两个数相加\"\"\"
    return a + b

def multiply(a, b):
    \"\"\"两个数相乘\"\"\"
    return a * b

class Calculator:
    \"\"\"计算器类\"\"\"
    
    def __init__(self):
        self.result = 0
    
    def calculate(self, expression):
        \"\"\"计算表达式\"\"\"
        self.result = eval(expression)
        return self.result
"""
    
    # 代码分割器
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=100,
        chunk_overlap=10
    )
    
    chunks = text_splitter.split_text(code)
    
    print(f"分割后的块数：{len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"\n块{i+1}:")
        print(f"  {chunk.strip()[:80]}...")


def rag_workflow_intro():
    """RAG 工作流程介绍"""
    print("\n" + "=" * 60)
    print("RAG 工作流程")
    print("=" * 60)
    
    print("""
    📚 RAG (检索增强生成) 流程:
    
    1. 文档加载 (Document Loading)
       ↓
    2. 文本分割 (Text Splitting)
       ↓
    3. 向量化 (Embedding)
       ↓
    4. 存储到向量数据库 (Vector Store)
       ↓
    5. 检索相关文档 (Retrieval)
       ↓
    6. 生成回答 (Generation)
    
    💡 每个步骤都很重要:
    - 加载：支持多种格式 (PDF, Word, HTML 等)
    - 分割：保持语义完整性
    - 向量化：选择合适的 embedding 模型
    - 检索：平衡召回率和精度
    - 生成：结合上下文生成准确回答
    """)


if __name__ == "__main__":
    print("\n📄 文档加载与分割示例\n")
    
    test_text_loader()
    test_directory_loader()
    test_text_splitting()
    test_recursive_splitting()
    test_code_splitting()
    rag_workflow_intro()
    
    print("\n✅ 所有测试完成！")
