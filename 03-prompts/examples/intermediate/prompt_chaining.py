"""
示例 2: 提示链

演示如何将多个提示串联起来完成复杂任务
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def test_multi_step_analysis():
    """测试多步骤分析链"""
    print("=" * 60)
    print("多步骤分析链")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 步骤 1: 提取关键信息
    extract_prompt = ChatPromptTemplate.from_template(
        "从以下文本中提取 3 个关键点，用逗号分隔：{text}"
    )
    
    # 步骤 2: 分析情感
    analyze_prompt = ChatPromptTemplate.from_template(
        "分析以下文本的情感倾向 (正面/负面/中性): {text}"
    )
    
    # 步骤 3: 生成总结
    summarize_prompt = ChatPromptTemplate.from_template(
        "基于关键点 ({key_points}) 和情感分析 ({sentiment}), 生成一句话总结。"
    )
    
    # 创建链
    extract_chain = extract_prompt | llm | StrOutputParser()
    analyze_chain = analyze_prompt | llm | StrOutputParser()
    
    # 测试文本
    text = "这款新产品功能强大，设计精美，但是价格有点贵，性价比一般。"
    
    print(f"原文：{text}\n")
    
    # 执行链
    key_points = extract_chain.invoke({"text": text})
    print(f"关键点：{key_points}")
    
    sentiment = analyze_chain.invoke({"text": text})
    print(f"情感：{sentiment}")
    
    summary = summarize_prompt | llm | StrOutputParser()
    result = summary.invoke({"key_points": key_points, "sentiment": sentiment})
    print(f"总结：{result}\n")


def test_iterative_improvement():
    """测试迭代改进链"""
    print("=" * 60)
    print("迭代改进链")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 初始草稿
    draft = "AI 很好用。"
    print(f"初始草稿：{draft}\n")
    
    # 迭代 1: 扩展内容
    expand_prompt = ChatPromptTemplate.from_template(
        "将以下草稿扩展为 100 字左右的段落：{draft}"
    )
    expanded = (expand_prompt | llm | StrOutputParser()).invoke({"draft": draft})
    print(f"迭代 1 (扩展): {expanded}\n")
    
    # 迭代 2: 添加例子
    example_prompt = ChatPromptTemplate.from_template(
        "为以下内容添加 2 个具体例子：{content}"
    )
    with_examples = (example_prompt | llm | StrOutputParser()).invoke({"content": expanded})
    print(f"迭代 2 (加例子): {with_examples[:300]}...\n")
    
    # 迭代 3: 润色文字
    polish_prompt = ChatPromptTemplate.from_template(
        "润色以下文字，使其更专业：{content}"
    )
    polished = (polish_prompt | llm | StrOutputParser()).invoke({"content": with_examples})
    print(f"迭代 3 (润色): {polished[:300]}...\n")


def test_branching_chain():
    """测试分支链 (并行处理)"""
    print("=" * 60)
    print("分支链 (并行处理)")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    topic = "人工智能"
    print(f"主题：{topic}\n")
    
    # 并行生成不同角度的内容
    prompts = {
        "定义": ChatPromptTemplate.from_template("用一句话定义{topic}"),
        "历史": ChatPromptTemplate.from_template("简述{topic}的发展历史 (50 字)"),
        "应用": ChatPromptTemplate.from_template("列举{topic}的 3 个应用场景"),
        "未来": ChatPromptTemplate.from_template("预测{topic}的未来趋势 (50 字)")
    }
    
    chains = {
        name: (prompt | llm | StrOutputParser())
        for name, prompt in prompts.items()
    }
    
    # 并行执行 (实际是顺序，但逻辑上是并行的)
    results = {}
    for name, chain in chains.items():
        results[name] = chain.invoke({"topic": topic})
        print(f"{name}: {results[name]}")
    
    # 整合结果
    integrate_prompt = ChatPromptTemplate.from_template(
        "整合以下信息为一篇连贯的短文:\n"
        f"定义：{{definition}}\n"
        f"历史：{{history}}\n"
        f"应用：{{applications}}\n"
        f"未来：{{future}}"
    )
    
    integrated = (integrate_prompt | llm | StrOutputParser()).invoke(results)
    print(f"\n整合结果:\n{integrated[:400]}...\n")


if __name__ == "__main__":
    print("\n🔗 提示链示例\n")
    
    test_multi_step_analysis()
    test_iterative_improvement()
    test_branching_chain()
    
    print("✅ 所有测试完成！")
