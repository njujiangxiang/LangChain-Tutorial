"""
示例：使用 Ollama 的提示工程

演示如何在使用本地 Ollama 模型时设计有效的提示
模型：qwen3.5:9b
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()


def test_ollama_basic_prompt():
    """测试 Ollama 基础提示"""
    print("=" * 60)
    print("Ollama 基础提示")
    print("=" * 60)
    
    # 创建 Ollama 模型实例
    llm = ChatOllama(
        model="qwen3.5:9b",
        temperature=0.7,
        num_ctx=4096
    )
    
    # 简单提示
    prompt = ChatPromptTemplate.from_template(
        "请用{num_sentences}句话解释什么是{topic}。"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    test_cases = [
        {"num_sentences": 2, "topic": "机器学习"},
        {"num_sentences": 3, "topic": "深度学习"},
        {"num_sentences": 4, "topic": "神经网络"},
    ]
    
    for case in test_cases:
        print(f"\n主题：{case['topic']}")
        result = chain.invoke(case)
        print(f"响应：{result[:200]}...\n")


def test_ollama_system_prompt():
    """测试 Ollama 系统提示"""
    print("=" * 60)
    print("Ollama 系统提示设计")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 定义不同角色的系统提示
    system_prompts = {
        "助手": "你是一个友好的 AI 助手，乐于助人。",
        "老师": "你是一位耐心的老师，擅长用简单易懂的方式解释概念。",
        "工程师": "你是一位资深工程师，注重实践和最佳实践。"
    }
    
    for role, system_prompt in system_prompts.items():
        print(f"\n角色：{role}")
        print("-" * 60)
        
        chat_template = ChatPromptTemplate.from_messages([
            (SystemMessage(content=system_prompt)),
            ("human", "如何学习编程？")
        ])
        
        chain = chat_template | llm | StrOutputParser()
        response = chain.invoke({})
        print(f"响应：{response[:250]}...\n")


def test_ollama_few_shot():
    """测试 Ollama 少样本提示"""
    print("=" * 60)
    print("Ollama 少样本提示")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 少样本提示模板
    few_shot_template = ChatPromptTemplate.from_template(
        "任务：情感分析 (正面/负面)\n\n"
        "示例 1:\n"
        "文本：这个产品太好用了！\n"
        "情感：正面\n\n"
        "示例 2:\n"
        "文本：质量很差，不推荐。\n"
        "情感：负面\n\n"
        "示例 3:\n"
        "文本：还可以，中规中矩。\n"
        "情感：中性\n\n"
        "现在请分析:\n"
        "文本：{text}\n"
        "情感："
    )
    
    test_texts = [
        "非常满意，超出预期！",
        "太失望了，浪费钱",
        "一般般，没什么特别的"
    ]
    
    for text in test_texts:
        chain = few_shot_template | llm | StrOutputParser()
        result = chain.invoke({"text": text})
        print(f"文本：{text}")
        print(f"情感：{result}\n")


def test_ollama_chain_of_thought():
    """测试 Ollama 思维链"""
    print("=" * 60)
    print("Ollama 思维链 (CoT)")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    cot_prompt = ChatPromptTemplate.from_template(
        "问题：{question}\n\n"
        "让我们一步步思考:\n"
        "1. 理解问题\n"
        "2. 分析已知条件\n"
        "3. 推导解决方案\n"
        "4. 验证答案\n\n"
        "解答："
    )
    
    questions = [
        "一个房间有 3 盏灯，门外有 3 个开关，你只能进房间一次，如何确定哪个开关控制哪盏灯？",
        "如果昨天是明天的后天，那么今天是星期几？"
    ]
    
    for question in questions:
        print(f"\n问题：{question}")
        print("-" * 60)
        
        chain = cot_prompt | llm | StrOutputParser()
        response = chain.invoke({"question": question})
        print(f"解答：{response[:400]}...\n")


def test_ollama_context_window():
    """测试 Ollama 上下文窗口"""
    print("=" * 60)
    print("Ollama 长上下文处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", num_ctx=4096)
    
    # 创建长上下文
    context_parts = []
    for i in range(10):
        context_parts.append(f"事实{i + 1}: 地球是太阳系中的第三颗行星。")
    
    long_context = "\n".join(context_parts)
    
    prompt = ChatPromptTemplate.from_template(
        "基于以下信息回答问题:\n\n"
        "{context}\n\n"
        "问题：地球在太阳系中是第几颗行星？\n"
        "答案："
    )
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"context": long_context})
    
    print(f"上下文长度：{len(long_context)} 字符")
    print(f"问题：地球在太阳系中是第几颗行星？")
    print(f"答案：{response}\n")


def compare_ollama_prompts():
    """对比不同提示的效果"""
    print("=" * 60)
    print("提示对比实验")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    question = "什么是人工智能？"
    
    prompts = {
        "简单": ChatPromptTemplate.from_template("什么是人工智能？"),
        
        "带角色": ChatPromptTemplate.from_messages([
            (SystemMessage(content="你是一位科普作家，擅长用通俗语言解释概念。")),
            ("human", "什么是人工智能？")
        ]),
        
        "带约束": ChatPromptTemplate.from_template(
            "请用 50 字以内、包含 1 个比喻，解释什么是人工智能。"
        ),
        
        "思维链": ChatPromptTemplate.from_template(
            "让我们一步步解释什么是人工智能:\n"
            "1. 基本定义\n"
            "2. 核心能力\n"
            "3. 应用场景\n"
            "总结："
        )
    }
    
    for name, prompt in prompts.items():
        print(f"\n提示类型：{name}")
        print("-" * 60)
        
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({})
        print(f"响应：{response[:200]}...\n")


if __name__ == "__main__":
    print("\n🦙 Ollama 提示工程示例\n")
    print("前提：确保 Ollama 已安装并运行 qwen3.5:9b 模型\n")
    
    try:
        test_ollama_basic_prompt()
        test_ollama_system_prompt()
        test_ollama_few_shot()
        test_ollama_chain_of_thought()
        test_ollama_context_window()
        compare_ollama_prompts()
        
        print("\n✅ Ollama 提示示例完成！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n请确保:")
        print("1. Ollama 已安装并运行")
        print("2. 已下载模型：ollama pull qwen3.5:9b")
