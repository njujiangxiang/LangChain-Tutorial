"""
示例：LangChain 链式调用模式

演示不同的链式调用模式：顺序链、并行链、条件链
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def get_llm():
    """获取 LLM 实例"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置")
        return None
    return ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)

def test_sequential_chain():
    """顺序链：多个步骤依次执行"""
    print("=" * 60)
    print("顺序链模式 (Sequential Chain)")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("演示模式：步骤 1 → 步骤 2 → 步骤 3")
        print("  输入 → [处理 1] → [处理 2] → [处理 3] → 输出")
        return
    
    # 步骤 1: 生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为以下主题生成一个包含 3 个要点的大纲：{topic}"
    )
    
    # 步骤 2: 扩展每个要点
    expand_prompt = ChatPromptTemplate.from_template(
        "基于以下大纲，为每个要点添加详细说明：\n{outline}"
    )
    
    # 步骤 3: 总结
    summary_prompt = ChatPromptTemplate.from_template(
        "将以下内容总结为一句话：\n{content}"
    )
    
    # 构建顺序链
    outline_chain = outline_prompt | llm | StrOutputParser()
    expand_chain = expand_prompt | llm | StrOutputParser()
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    # 完整顺序链
    full_chain = (
        outline_chain
        | RunnableLambda(lambda x: {"outline": x, "content": x})
        | expand_chain
        | RunnableLambda(lambda x: {"content": x})
        | summary_chain
    )
    
    topic = "机器学习基础"
    print(f"\n主题：{topic}")
    print("\n执行顺序链...")
    
    result = full_chain.invoke({"topic": topic})
    print(f"\n最终总结：{result}")

def test_parallel_chain():
    """并行链：同时执行多个独立任务"""
    print("\n" + "=" * 60)
    print("并行链模式 (Parallel Chain)")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("演示模式：同时执行多个独立任务")
        print("  输入 → [任务 A] → 输出 A")
        print("       → [任务 B] → 输出 B")
        print("       → [任务 C] → 输出 C")
        return
    
    # 创建多个独立的链
    explain_prompt = ChatPromptTemplate.from_template(
        "用一句话解释：{topic}"
    )
    
    example_prompt = ChatPromptTemplate.from_template(
        "为{topic}提供一个实际例子"
    )
    
    analogy_prompt = ChatPromptTemplate.from_template(
        "为{topic}创建一个类比"
    )
    
    explain_chain = explain_prompt | llm | StrOutputParser()
    example_chain = example_prompt | llm | StrOutputParser()
    analogy_chain = analogy_prompt | llm | StrOutputParser()
    
    # 使用 RunnablePassthrough 并行执行
    from langchain_core.runnables import RunnableParallel
    
    parallel_chain = RunnableParallel(
        explanation=explain_chain,
        example=example_chain,
        analogy=analogy_chain
    )
    
    topic = "神经网络"
    print(f"\n主题：{topic}")
    print("\n并行执行三个任务...")
    
    results = parallel_chain.invoke({"topic": topic})
    
    print(f"\n解释：{results['explanation']}")
    print(f"\n例子：{results['example']}")
    print(f"\n类比：{results['analogy']}")

def test_conditional_chain():
    """条件链：根据输入选择不同路径"""
    print("\n" + "=" * 60)
    print("条件链模式 (Conditional Chain)")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("演示模式：根据条件选择不同处理路径")
        print("  输入 → [判断条件] → 路径 A 或 路径 B")
        return
    
    # 简单链：翻译
    translate_prompt = ChatPromptTemplate.from_template(
        "将以下内容翻译成英文：{text}"
    )
    translate_chain = translate_prompt | llm | StrOutputParser()
    
    # 复杂链：分析并给出建议
    analyze_prompt = ChatPromptTemplate.from_template(
        "分析以下问题并给出专业建议：{text}"
    )
    analyze_chain = analyze_prompt | llm | StrOutputParser()
    
    # 条件路由函数
    def route(input_data):
        text = input_data.get("text", "")
        # 简单判断：如果包含问号，认为是问题，需要分析
        if "?" in text or "？" in text:
            return analyze_chain
        else:
            return translate_chain
    
    # 条件链
    conditional_chain = RunnableLambda(route)
    
    # 测试 1: 翻译任务
    print("\n测试 1 - 翻译任务:")
    result1 = conditional_chain.invoke({"text": "你好，世界"})
    print(f"结果：{result1}")
    
    # 测试 2: 分析任务
    print("\n测试 2 - 分析任务:")
    result2 = conditional_chain.invoke({"text": "如何提高学习效率？"})
    print(f"结果：{result2}")

def test_branching_chain():
    """分支链：一个输入，多个输出路径"""
    print("\n" + "=" * 60)
    print("分支链模式 (Branching Chain)")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("演示模式：一个输入产生多个不同视角的输出")
        return
    
    # 创建不同视角的链
    pros_prompt = ChatPromptTemplate.from_template(
        "列出{topic}的 3 个优点"
    )
    cons_prompt = ChatPromptTemplate.from_template(
        "列出{topic}的 3 个缺点"
    )
    neutral_prompt = ChatPromptTemplate.from_template(
        "客观描述{topic}是什么"
    )
    
    pros_chain = pros_prompt | llm | StrOutputParser()
    cons_chain = cons_prompt | llm | StrOutputParser()
    neutral_chain = neutral_prompt | llm | StrOutputParser()
    
    # 分支链
    branching_chain = RunnableParallel(
        pros=pros_chain,
        cons=cons_chain,
        neutral=neutral_chain
    )
    
    topic = "远程办公"
    print(f"\n主题：{topic}")
    print("\n从三个角度分析...")
    
    results = branching_chain.invoke({"topic": topic})
    
    print(f"\n✅ 优点:\n{results['pros']}")
    print(f"\n❌ 缺点:\n{results['cons']}")
    print(f"\n📝 客观描述:\n{results['neutral']}")

if __name__ == "__main__":
    print("\n🦜️🔗 LangChain 链式调用模式示例\n")
    
    test_sequential_chain()
    test_parallel_chain()
    test_conditional_chain()
    test_branching_chain()
    
    print("\n✅ 所有演示完成！")
