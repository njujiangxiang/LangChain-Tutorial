"""
示例：顺序链 - SequentialChain

演示如何使用 LangChain 的顺序链按顺序执行多个处理步骤
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()


def simple_sequential_chain():
    """简单顺序链示例"""
    print("=" * 60)
    print("简单顺序链 - 文章生成")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 步骤 1: 生成标题
    title_prompt = ChatPromptTemplate.from_template(
        "为以下主题生成一个吸引人的标题 (不超过 20 字): {topic}"
    )
    
    # 步骤 2: 根据标题生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为标题'{title}'生成一个包含 3 个要点的文章大纲"
    )
    
    # 步骤 3: 根据大纲生成简介
    intro_prompt = ChatPromptTemplate.from_template(
        "根据以下大纲写一段 100 字的简介:\n{outline}"
    )
    
    # 创建链
    title_chain = title_prompt | llm | StrOutputParser()
    outline_chain = outline_prompt | llm | StrOutputParser()
    intro_chain = intro_prompt | llm | StrOutputParser()
    
    # 顺序执行
    topic = "人工智能的未来发展"
    print(f"主题：{topic}\n")
    
    print("步骤 1: 生成标题")
    title = title_chain.invoke({"topic": topic})
    print(f"标题：{title}\n")
    
    print("步骤 2: 生成大纲")
    outline = outline_chain.invoke({"title": title})
    print(f"大纲：{outline}\n")
    
    print("步骤 3: 生成简介")
    intro = intro_chain.invoke({"outline": outline})
    print(f"简介：{intro}\n")


def multi_input_chain():
    """多输入链示例"""
    print("\n" + "=" * 60)
    print("多输入链 - 产品描述生成")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 需要多个输入的提示
    product_prompt = ChatPromptTemplate.from_template(
        """为以下产品生成营销文案：
        产品名称：{product_name}
        目标用户：{target_audience}
        核心功能：{features}
        
        要求：突出卖点，语言生动，100 字左右"""
    )
    
    chain = product_prompt | llm | StrOutputParser()
    
    # 测试不同产品
    products = [
        {
            "product_name": "智能手表 X1",
            "target_audience": "运动爱好者",
            "features": "心率监测、GPS 定位、防水设计"
        },
        {
            "product_name": "无线耳机 Pro",
            "target_audience": "商务人士",
            "features": "主动降噪、长续航、清晰通话"
        }
    ]
    
    for product in products:
        print(f"\n产品：{product['product_name']}")
        result = chain.invoke(product)
        print(f"文案：{result}\n")


def branch_chain():
    """分支链示例"""
    print("\n" + "=" * 60)
    print("分支链 - 内容分类处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 分类器
    classify_prompt = ChatPromptTemplate.from_template(
        "判断以下文本的类型 (技术/生活/娱乐): {text}\n只返回类型名称。"
    )
    
    # 不同类型的处理
    tech_prompt = ChatPromptTemplate.from_template(
        "用专业术语解释：{text}"
    )
    
    life_prompt = ChatPromptTemplate.from_template(
        "给出实用建议：{text}"
    )
    
    entertainment_prompt = ChatPromptTemplate.from_template(
        "用轻松幽默的方式评论：{text}"
    )
    
    classify_chain = classify_prompt | llm | StrOutputParser()
    tech_chain = tech_prompt | llm | StrOutputParser()
    life_chain = life_prompt | llm | StrOutputParser()
    entertainment_chain = entertainment_prompt | llm | StrOutputParser()
    
    # 测试文本
    test_texts = [
        "什么是机器学习？",
        "如何保持健康的生活方式？",
        "最近有什么好看的电影？"
    ]
    
    for text in test_texts:
        print(f"\n输入：{text}")
        
        # 分类
        category = classify_chain.invoke({"text": text})
        print(f"分类：{category}")
        
        # 根据分类选择处理链
        if "技术" in category:
            result = tech_chain.invoke({"text": text})
        elif "生活" in category:
            result = life_chain.invoke({"text": text})
        else:
            result = entertainment_chain.invoke({"text": text})
        
        print(f"处理结果：{result[:100]}...\n")


def chain_with_fallback():
    """带回退机制的链"""
    print("\n" + "=" * 60)
    print("带回退的链 - 容错处理")
    print("=" * 60)
    
    primary_llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    fallback_llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template("回答：{question}")
    
    def invoke_with_fallback(inputs):
        """主模型失败时使用备用模型"""
        try:
            print("  使用主模型...")
            chain = prompt | primary_llm | StrOutputParser()
            return chain.invoke(inputs)
        except Exception as e:
            print(f"  主模型失败：{e}")
            print("  使用备用模型...")
            chain = prompt | fallback_llm | StrOutputParser()
            return chain.invoke(inputs)
    
    # 测试
    result = invoke_with_fallback({"question": "1+1 等于几？"})
    print(f"结果：{result}")


if __name__ == "__main__":
    print("\n🔗 顺序链示例\n")
    
    simple_sequential_chain()
    multi_input_chain()
    branch_chain()
    chain_with_fallback()
    
    print("\n✅ 顺序链示例完成！")
