"""
示例：LLMChain 基础

演示 LangChain 链的基础用法
"""

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取 LLM 实例"""
    if os.getenv('ANTHROPIC_API_KEY'):
        return ChatAnthropic(model="claude-3-sonnet-20240229")
    return ChatOllama(model="qwen3.5:9b")


def test_basic_chain():
    """测试基础链"""
    print("=" * 60)
    print("基础链 (Prompt | LLM | OutputParser)")
    print("=" * 60)
    
    llm = get_llm()
    
    # 最简单的链
    prompt = ChatPromptTemplate.from_template(
        "解释什么是{concept}"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({"concept": "机器学习"})
    print(f"概念：机器学习")
    print(f"解释：{result[:200]}...")


def test_chain_with_history():
    """测试带历史的链"""
    print("\n" + "=" * 60)
    print("带对话历史的链")
    print("=" * 60)
    
    llm = get_llm()
    
    from langchain_core.messages import HumanMessage, AIMessage
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有帮助的助手。记住对话历史。"),
        ("human", "{input}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    # 多轮对话
    history = []
    
    questions = [
        "你好，我叫小明",
        "我叫什么名字？",
        "我喜欢什么？"
    ]
    
    for question in questions:
        result = chain.invoke({"input": question})
        print(f"问：{question}")
        print(f"答：{result[:100]}...\n")
        history.append(("human", question))
        history.append(("ai", result))


def test_chained_operations():
    """测试链式操作"""
    print("\n" + "=" * 60)
    print("链式操作")
    print("=" * 60)
    
    llm = get_llm()
    
    # 多步处理链
    step1_prompt = ChatPromptTemplate.from_template(
        "列出{topic}的 3 个关键点"
    )
    
    step2_prompt = ChatPromptTemplate.from_template(
        "详细解释以下关键点:\n{points}"
    )
    
    # 组合链
    chain = (
        step1_prompt 
        | llm 
        | StrOutputParser()
        | (lambda x: {"points": x})
        | step2_prompt
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke({"topic": "Python 编程"})
    print(f"主题：Python 编程")
    print(f"结果：{result[:300]}...")


def test_parallel_chains():
    """测试并行链"""
    print("\n" + "=" * 60)
    print("并行链")
    print("=" * 60)
    
    llm = get_llm()
    
    from langchain_core.runnables import RunnableParallel
    
    # 创建多个并行链
    explain_prompt = ChatPromptTemplate.from_template("解释{topic}")
    example_prompt = ChatPromptTemplate.from_template("给{topic}一个例子")
    analogy_prompt = ChatPromptTemplate.from_template("为{topic}打个比方")
    
    parallel_chain = RunnableParallel(
        explanation=explain_prompt | llm | StrOutputParser(),
        example=example_prompt | llm | StrOutputParser(),
        analogy=analogy_prompt | llm | StrOutputParser()
    )
    
    results = parallel_chain.invoke({"topic": "递归"})
    
    print(f"主题：递归")
    print(f"\n解释：{results['explanation'][:100]}...")
    print(f"\n例子：{results['example'][:100]}...")
    print(f"\n比方：{results['analogy'][:100]}...")


def test_conditional_chain():
    """测试条件链"""
    print("\n" + "=" * 60)
    print("条件链")
    print("=" * 60)
    
    llm = get_llm()
    
    from langchain_core.runnables import RunnableLambda
    
    # 根据输入选择不同处理
    def route(input_data):
        text = input_data.get("text", "")
        if len(text) > 20:
            # 长文本：总结
            return ChatPromptTemplate.from_template(
                "总结以下内容：{text}"
            )
        else:
            # 短文本：翻译
            return ChatPromptTemplate.from_template(
                "翻译成英文：{text}"
            )
    
    chain = (
        RunnableLambda(route)
        | llm
        | StrOutputParser()
    )
    
    # 测试
    test_cases = [
        {"text": "你好"},
        {"text": "这是一个比较长的文本，需要被总结一下主要内容。"}
    ]
    
    for case in test_cases:
        result = chain.invoke(case)
        print(f"输入：{case['text']}")
        print(f"输出：{result}\n")


if __name__ == "__main__":
    print("\n🔗 LLMChain 基础示例\n")
    
    test_basic_chain()
    test_chain_with_history()
    test_chained_operations()
    test_parallel_chains()
    test_conditional_chain()
    
    print("\n✅ 所有测试完成！")
