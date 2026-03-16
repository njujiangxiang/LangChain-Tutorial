"""
示例：Ollama 高级链式调用

演示复杂的链式调用模式和高级技巧
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import (
    RunnableLambda, 
    RunnableParallel, 
    RunnablePassthrough,
    RunnableBranch
)
from pydantic import BaseModel, Field
from typing import List, Dict
import time
from dotenv import load_dotenv
import os

load_dotenv()


def branched_chain_example():
    """分支链 - 根据条件选择不同路径"""
    print("=" * 60)
    print("分支链 - 智能路由")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 定义不同分支的 prompt
    code_prompt = ChatPromptTemplate.from_template(
        "生成实现以下功能的 Python 代码：{input}"
    )
    
    explain_prompt = ChatPromptTemplate.from_template(
        "用简单语言解释以下概念：{input}"
    )
    
    translate_prompt = ChatPromptTemplate.from_template(
        "将以下内容翻译成英文：{input}"
    )
    
    # 分类函数
    def classify(x):
        text = x.get("input", "").lower()
        if "代码" in text or "python" in text or "function" in text:
            return "code"
        elif "解释" in text or "什么是" in text or "explain" in text:
            return "explain"
        elif "翻译" in text or "translate" in text:
            return "translate"
        else:
            return "default"
    
    # 分支链
    branch_chain = (
        RunnableLambda(classify)
        | {
            "code": code_prompt | llm | StrOutputParser(),
            "explain": explain_prompt | llm | StrOutputParser(),
            "translate": translate_prompt | llm | StrOutputParser(),
            "default": ChatPromptTemplate.from_template("回答：{input}") | llm | StrOutputParser(),
        }
        | RunnableLambda(lambda x: x.get("code") or x.get("explain") or x.get("translate") or x.get("default"))
    )
    
    # 测试
    test_cases = [
        "写一个 Python 函数计算阶乘",
        "解释什么是机器学习",
        "翻译：你好世界",
        "今天天气如何？",
    ]
    
    print("测试分支链:\n")
    for case in test_cases:
        print(f"输入：{case}")
        result = branch_chain.invoke({"input": case})
        print(f"输出：{result[:100]}...\n")


def map_reduce_chain():
    """Map-Reduce 链 - 批量处理+汇总"""
    print("\n" + "=" * 60)
    print("Map-Reduce 链 - 批量分析与汇总")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # Map: 分析每个项目
    analyze_prompt = ChatPromptTemplate.from_template(
        "分析以下产品的优缺点（各 2 点）：\n产品：{product}"
    )
    
    analyze_chain = analyze_prompt | llm | StrOutputParser()
    
    # Reduce: 汇总所有分析
    summary_prompt = ChatPromptTemplate.from_template(
        "基于以下产品分析，给出购买建议：\n\n{analyses}"
    )
    
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    # 产品列表
    products = [
        "MacBook Pro",
        "Dell XPS 15",
        "ThinkPad X1 Carbon",
    ]
    
    print("产品对比分析:\n")
    
    # Map 阶段
    analyses = []
    for product in products:
        print(f"分析 {product}...")
        analysis = analyze_chain.invoke({"product": product})
        analyses.append(f"{product}:\n{analysis}")
        print(f"  完成\n")
    
    # Reduce 阶段
    print("生成汇总建议...")
    summary = summary_chain.invoke({"analyses": "\n\n".join(analyses)})
    print(f"\n购买建议:\n{summary[:300]}...")


def recursive_chain():
    """递归链 - 迭代改进"""
    print("\n" + "=" * 60)
    print("递归链 - 迭代改进文本")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 改进 prompt
    improve_prompt = ChatPromptTemplate.from_template(
        "改进以下文本，使其更清晰、专业：\n\n{text}"
    )
    
    improve_chain = improve_prompt | llm | StrOutputParser()
    
    # 初始文本
    text = "这个产品好用，但是贵，不过质量不错。"
    
    print(f"初始文本：{text}\n")
    
    # 迭代改进 3 次
    for i in range(3):
        print(f"第 {i+1} 次改进:")
        text = improve_chain.invoke({"text": text})
        print(f"  {text}\n")
    
    print(f"最终版本：{text}")


def stateful_chain():
    """有状态链 - 维护上下文"""
    print("\n" + "=" * 60)
    print("有状态链 - 对话上下文")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 维护对话状态
    state = {
        "history": [],
        "user_info": {},
    }
    
    def process_with_state(x):
        user_input = x["input"]
        history = x["state"]["history"]
        
        # 构建完整上下文
        context = "\n".join([f"{h['role']}: {h['content']}" for h in history[-6:]])
        
        prompt = f"""对话历史：
{context}

用户：{user_input}
助手："""
        
        response = llm.invoke([("human", prompt)])
        
        # 更新状态
        x["state"]["history"].append({"role": "user", "content": user_input})
        x["state"]["history"].append({"role": "assistant", "content": response.content})
        
        return response.content
    
    state_chain = RunnableLambda(process_with_state)
    
    # 多轮对话
    print("有状态对话:\n")
    
    conversations = [
        "我叫小明。",
        "我今年 25 岁。",
        "我喜欢什么？",  # 测试记忆
        "推荐一个适合我的爱好。",  # 基于上下文
    ]
    
    for msg in conversations:
        result = state_chain.invoke({"input": msg, "state": state})
        print(f"用户：{msg}")
        print(f"助手：{result[:100]}...\n")


def parallel_execution():
    """并行执行 - 同时处理多个任务"""
    print("\n" + "=" * 60)
    print("并行执行 - 多角度分析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 定义多个并行任务
    parallel_chain = RunnableParallel({
        "summary": ChatPromptTemplate.from_template("总结以下内容：{text}") | llm | StrOutputParser(),
        "keywords": ChatPromptTemplate.from_template("提取 5 个关键词：{text}") | llm | StrOutputParser(),
        "sentiment": ChatPromptTemplate.from_template("分析情感倾向（正面/负面/中性）：{text}") | llm | StrOutputParser(),
        "questions": ChatPromptTemplate.from_template("提出 3 个相关问题：{text}") | llm | StrOutputParser(),
    })
    
    text = """
    人工智能技术正在快速发展，大语言模型如 GPT-4、Claude 等展现出惊人的能力。
    这些模型可以理解自然语言、生成文本、编写代码，甚至进行推理。
    然而，它们也面临幻觉、偏见、安全性等挑战。
    未来，AI 将在医疗、教育、科研等领域发挥更大作用。
    """
    
    print(f"分析文本：{text[:100]}...\n")
    
    results = parallel_chain.invoke({"text": text})
    
    print("并行分析结果:")
    for key, value in results.items():
        print(f"\n【{key}】")
        print(f"{value[:200]}...")


def chain_with_retry():
    """带重试的链"""
    print("\n" + "=" * 60)
    print("带重试的链 - 错误处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    def safe_invoke(x, max_retries=3):
        """安全的调用，带重试"""
        for i in range(max_retries):
            try:
                prompt = ChatPromptTemplate.from_template("回答：{question}")
                chain = prompt | llm | StrOutputParser()
                return chain.invoke({"question": x["question"]})
            except Exception as e:
                if i < max_retries - 1:
                    print(f"  重试 {i+1}/{max_retries}...")
                    time.sleep(1)
                else:
                    return f"调用失败：{e}"
        return None
    
    retry_chain = RunnableLambda(safe_invoke)
    
    # 测试
    print("测试重试机制:\n")
    result = retry_chain.invoke({"question": "1+1 等于几？"})
    print(f"结果：{result}")


if __name__ == "__main__":
    print("\n🦙 Ollama 高级链式调用示例\n")
    
    branched_chain_example()
    map_reduce_chain()
    recursive_chain()
    stateful_chain()
    parallel_execution()
    chain_with_retry()
    
    print("\n✅ Ollama 高级链式示例完成！")
