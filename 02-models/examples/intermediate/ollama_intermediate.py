"""
示例：Ollama 中级使用 - 高级配置与优化

演示 Ollama 模型的高级配置、性能优化和实用技巧
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import time
from typing import List, Dict

load_dotenv()


def custom_model_parameters():
    """自定义模型参数"""
    print("=" * 60)
    print("自定义模型参数")
    print("=" * 60)
    
    # Ollama 支持丰富的参数配置
    llm = ChatOllama(
        model="qwen3.5:9b",
        temperature=0.7,        # 创造性：0-1，越高越有创造性
        top_p=0.9,              # 核采样：0-1
        top_k=40,               # 采样池大小
        num_ctx=4096,           # 上下文窗口大小
        num_predict=1024,       # 最大生成 token 数
        repeat_penalty=1.1,     # 重复惩罚
        seed=42,                # 随机种子 (可复现结果)
    )
    
    print(f"模型配置:")
    print(f"  - model: {llm.model}")
    print(f"  - temperature: {llm.temperature}")
    print(f"  - num_ctx: {llm.num_ctx}")
    
    # 测试不同 temperature
    messages = [HumanMessage(content="今天天气真好")]
    
    for temp in [0.1, 0.5, 0.9]:
        llm_temp = ChatOllama(model="qwen3.5:9b", temperature=temp)
        response = llm_temp.invoke(messages)
        print(f"\ntemperature={temp}: {response.content[:50]}...")


def conversation_with_history():
    """带历史记录的对话"""
    print("\n" + "=" * 60)
    print("带历史记录的对话")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 模拟多轮对话
    messages = [
        SystemMessage(content="你是一个有帮助的助手。记住用户的信息。"),
        HumanMessage(content="我叫小明，喜欢编程。"),
        AIMessage(content="好的，小明！我记住了你喜欢编程。有什么我可以帮助你的吗？"),
        HumanMessage(content="我喜欢什么？"),  # 测试记忆
    ]
    
    response = llm.invoke(messages)
    print(f"用户问题：我喜欢什么？")
    print(f"AI 回答：{response.content}")


def batch_processing():
    """批量处理多个请求"""
    print("\n" + "=" * 60)
    print("批量处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    questions = [
        "Python 是什么？",
        "Java 是什么？",
        "JavaScript 是什么？",
    ]
    
    print("批量处理多个问题...\n")
    
    # 方式 1: 顺序处理
    start = time.time()
    for q in questions:
        response = llm.invoke([HumanMessage(content=q)])
        print(f"Q: {q}")
        print(f"A: {response.content[:80]}...\n")
    print(f"顺序处理耗时：{time.time() - start:.2f}s")


def prompt_chaining():
    """提示链 - 多步骤处理"""
    print("\n" + "=" * 60)
    print("提示链示例")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 步骤 1: 生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为'{topic}'主题生成一个包含 3 个要点的大纲。只返回要点，每行一个。"
    )
    
    # 步骤 2: 扩展内容
    expand_prompt = ChatPromptTemplate.from_template(
        "扩展以下要点为详细说明：\n{outline}\n\n要求：每个要点 2-3 句话。"
    )
    
    # 创建链
    outline_chain = outline_prompt | llm | StrOutputParser()
    expand_chain = expand_prompt | llm | StrOutputParser()
    
    # 执行
    topic = "人工智能"
    print(f"主题：{topic}\n")
    
    print("步骤 1: 生成大纲")
    outline = outline_chain.invoke({"topic": topic})
    print(outline)
    
    print("\n步骤 2: 扩展内容")
    result = expand_chain.invoke({"outline": outline})
    print(result)


def error_handling_with_retry():
    """错误处理与重试"""
    print("\n" + "=" * 60)
    print("错误处理与重试")
    print("=" * 60)
    
    def invoke_with_retry(llm, messages, max_retries=3):
        """带重试的调用"""
        for i in range(max_retries):
            try:
                return llm.invoke(messages)
            except Exception as e:
                if i < max_retries - 1:
                    print(f"重试 {i+1}/{max_retries}: {e}")
                    time.sleep(1)
                else:
                    raise
        return None
    
    llm = ChatOllama(model="qwen3.5:9b")
    messages = [HumanMessage(content="你好")]
    
    try:
        response = invoke_with_retry(llm, messages)
        print(f"成功：{response.content}")
    except Exception as e:
        print(f"失败：{e}")


def structured_output():
    """结构化输出"""
    print("\n" + "=" * 60)
    print("结构化输出")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    
    # 要求 JSON 格式输出
    prompt = ChatPromptTemplate.from_template("""
    请分析以下文本并返回 JSON 格式：
    文本：{text}
    
    返回格式：
    {{
        "sentiment": "positive/negative/neutral",
        "keywords": ["关键词 1", "关键词 2"],
        "summary": "一句话总结"
    }}
    
    只返回 JSON，不要其他内容。
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    text = "这个产品非常好用，界面友好，但是价格有点贵。"
    print(f"分析文本：{text}\n")
    
    result = chain.invoke({"text": text})
    print(f"结果:\n{result}")


def model_comparison():
    """模型对比"""
    print("\n" + "=" * 60)
    print("模型性能对比")
    print("=" * 60)
    
    models = [
        ("qwen3.5:9b", "通义千问 - 平衡性能"),
        ("llama3:8b", "Llama 3 - 轻量快速"),
        ("mistral:7b", "Mistral - 高效"),
    ]
    
    question = "用一句话解释什么是机器学习。"
    messages = [HumanMessage(content=question)]
    
    print(f"问题：{question}\n")
    
    for model_id, model_desc in models:
        try:
            llm = ChatOllama(model=model_id)
            start = time.time()
            response = llm.invoke(messages)
            elapsed = time.time() - start
            
            print(f"{model_desc} ({model_id})")
            print(f"  耗时：{elapsed:.2f}s")
            print(f"  回答：{response.content}\n")
        except Exception as e:
            print(f"{model_id}: 不可用 - {e}\n")


def caching_example():
    """缓存示例"""
    print("\n" + "=" * 60)
    print("缓存优化")
    print("=" * 60)
    
    # 简单的内存缓存
    cache: Dict[str, str] = {}
    
    def cached_invoke(llm, prompt_key, messages):
        if prompt_key in cache:
            print(f"[缓存命中] {prompt_key}")
            return cache[prompt_key]
        
        print(f"[缓存未命中] 调用模型...")
        response = llm.invoke(messages)
        cache[prompt_key] = response.content
        return response.content
    
    llm = ChatOllama(model="qwen3.5:9b")
    messages = [HumanMessage(content="1+1 等于几？")]
    
    print("第一次调用:")
    result1 = cached_invoke(llm, "math_1", messages)
    print(f"结果：{result1}\n")
    
    print("第二次调用 (相同问题):")
    result2 = cached_invoke(llm, "math_1", messages)
    print(f"结果：{result2}\n")
    
    print(f"缓存大小：{len(cache)} 条")


if __name__ == "__main__":
    print("\n🦙 Ollama 中级示例 - 高级配置与优化\n")
    
    custom_model_parameters()
    conversation_with_history()
    batch_processing()
    prompt_chaining()
    error_handling_with_retry()
    structured_output()
    model_comparison()
    caching_example()
    
    print("\n✅ Ollama 中级示例完成！")
