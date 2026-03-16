"""
示例：Ollama 链式调用 - 中级

演示使用 Ollama 模型创建各种链式调用
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
import os

load_dotenv()


def sequential_chain_example():
    """顺序链示例"""
    print("=" * 60)
    print("顺序链 - 文章生成")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 步骤 1: 生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为'{topic}'生成 3 个要点的大纲。"
    )
    
    # 步骤 2: 扩展内容
    expand_prompt = ChatPromptTemplate.from_template(
        "扩展以下要点：\n{outline}"
    )
    
    # 创建链
    outline_chain = outline_prompt | llm | StrOutputParser()
    full_chain = (
        {"topic": RunnablePassthrough()}
        | outline_chain
        | (lambda x: {"outline": x})
        | expand_prompt
        | llm
        | StrOutputParser()
    )
    
    # 执行
    topic = "人工智能"
    print(f"主题：{topic}\n")
    
    result = full_chain.invoke(topic)
    print(f"结果：{result[:300]}...")


def parallel_chain_example():
    """并行链示例"""
    print("\n" + "=" * 60)
    print("并行链 - 多角度分析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 定义多个分析角度
    pros_prompt = ChatPromptTemplate.from_template("列出{topic}的优点 (3 点)")
    cons_prompt = ChatPromptTemplate.from_template("列出{topic}的缺点 (3 点)")
    summary_prompt = ChatPromptTemplate.from_template("总结{topic} (1 句话)")
    
    # 并行执行
    parallel_chain = {
        "优点": pros_prompt | llm | StrOutputParser(),
        "缺点": cons_prompt | llm | StrOutputParser(),
        "总结": summary_prompt | llm | StrOutputParser(),
    }
    
    topic = "远程办公"
    print(f"主题：{topic}\n")
    
    results = parallel_chain.invoke(topic)
    
    for key, value in results.items():
        print(f"{key}: {value}")


def conditional_chain_example():
    """条件链示例"""
    print("\n" + "=" * 60)
    print("条件链 - 根据输入选择处理路径")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    def route_input(x):
        """根据输入类型路由"""
        text = x.get("text", "")
        if "?" in text or "？" in text:
            return "question"
        elif len(text) > 100:
            return "long"
        else:
            return "short"
    
    question_prompt = ChatPromptTemplate.from_template("回答这个问题：{text}")
    long_prompt = ChatPromptTemplate.from_template("总结以下内容：{text}")
    short_prompt = ChatPromptTemplate.from_template("回应这句话：{text}")
    
    # 条件链
    conditional_chain = (
        RunnableLambda(route_input)
        | {
            "question": question_prompt | llm | StrOutputParser(),
            "long": long_prompt | llm | StrOutputParser(),
            "short": short_prompt | llm | StrOutputParser(),
        }
        | RunnableLambda(lambda x: x.get("question") or x.get("long") or x.get("short"))
    )
    
    test_cases = [
        "什么是机器学习？",
        "今天天气不错。",
        "这是一段比较长的文本，用来测试条件链的处理逻辑。" * 3,
    ]
    
    for text in test_cases:
        print(f"\n输入：{text[:50]}...")
        result = conditional_chain.invoke({"text": text})
        print(f"输出：{result[:100]}...")


def map_reduce_chain():
    """Map-Reduce 链示例"""
    print("\n" + "=" * 60)
    print("Map-Reduce - 批量处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # Map: 处理每个项目
    translate_prompt = ChatPromptTemplate.from_template("将'{word}'翻译成中文")
    translate_chain = translate_prompt | llm | StrOutputParser()
    
    # 批量处理
    words = ["apple", "computer", "programming", "algorithm", "database"]
    print(f"处理单词列表：{words}\n")
    
    results = []
    for word in words:
        result = translate_chain.invoke({"word": word})
        results.append(f"{word} -> {result}")
        print(f"  {result}")
    
    # Reduce: 汇总结果
    reduce_prompt = ChatPromptTemplate.from_template(
        "将以下翻译结果整理成表格:\n{results}"
    )
    reduce_chain = reduce_prompt | llm | StrOutputParser()
    
    print("\n汇总:")
    final = reduce_chain.invoke({"results": "\n".join(results)})
    print(final[:200])


if __name__ == "__main__":
    print("\n🦙 Ollama 链式调用 - 中级示例\n")
    
    sequential_chain_example()
    parallel_chain_example()
    conditional_chain_example()
    map_reduce_chain()
    
    print("\n✅ Ollama 链式示例完成！")
