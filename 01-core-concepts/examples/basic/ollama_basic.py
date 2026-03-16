"""
示例：使用 Ollama 本地模型

演示如何使用 LangChain 调用本地 Ollama 模型 (qwen3.5:9b)
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def test_ollama_basic():
    """测试 Ollama 基础调用"""
    print("=" * 60)
    print("Ollama 本地模型基础调用")
    print("=" * 60)
    
    # 创建 Ollama 模型实例
    # 确保已安装并运行 Ollama: ollama pull qwen3.5:9b
    llm = ChatOllama(
        model="qwen3.5:9b",
        temperature=0.7,
        num_ctx=4096  # 上下文窗口大小
    )
    
    print(f"模型：{llm.model}")
    print(f"温度：{llm.temperature}")
    print(f"上下文窗口：{llm.num_ctx}")
    
    # 发送简单消息
    messages = [
        SystemMessage(content="你是一个友好的 AI 助手。"),
        HumanMessage(content="你好！请用一句话介绍你自己。")
    ]
    
    print("\n发送消息...")
    response = llm.invoke(messages)
    print(f"响应：{response.content}")


def test_ollama_with_prompt_template():
    """使用提示模板调用 Ollama"""
    print("\n" + "=" * 60)
    print("Ollama + 提示模板")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_template(
        "请用{style}的风格解释什么是{concept}。"
    )
    
    # 创建链
    chain = prompt | llm | StrOutputParser()
    
    # 测试不同风格
    test_cases = [
        {"style": "简单易懂", "concept": "机器学习"},
        {"style": "专业严谨", "concept": "深度学习"},
        {"style": "幽默风趣", "concept": "神经网络"},
    ]
    
    for case in test_cases:
        print(f"\n📝 用{case['style']}的风格解释{case['concept']}:")
        result = chain.invoke(case)
        print(f"结果：{result[:200]}...")


def test_ollama_streaming():
    """测试 Ollama 流式输出"""
    print("\n" + "=" * 60)
    print("Ollama 流式输出")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", streaming=True)
    
    messages = [
        HumanMessage(content="请写一首关于春天的短诗，4 句即可。")
    ]
    
    print("流式输出：")
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
    print()


def test_ollama_batch_processing():
    """测试 Ollama 批量处理"""
    print("\n" + "=" * 60)
    print("Ollama 批量处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b")
    
    questions = [
        "1+1 等于几？",
        "地球是什么形状？",
        "水的化学式是什么？"
    ]
    
    print("批量处理多个问题:\n")
    
    for i, question in enumerate(questions, 1):
        print(f"问题{i}: {question}")
        response = llm.invoke([HumanMessage(content=question)])
        print(f"答案：{response.content}\n")


def compare_ollama_vs_cloud():
    """对比 Ollama 和云端模型"""
    print("=" * 60)
    print("Ollama vs 云端模型对比")
    print("=" * 60)
    
    print("\n📊 对比维度:")
    print("""
    | 维度         | Ollama (本地)           | 云端模型 (Anthropic/OpenAI) |
    |--------------|------------------------|---------------------------|
    | 成本         | 免费 (使用本地 GPU/CPU)  | 按 token 计费              |
    | 隐私         | 数据完全本地            | 数据发送到云端             |
    | 速度         | 取决于本地硬件          | 通常较快，受网络影响        |
    | 模型质量     | 中等 (取决于模型)        | 通常较高                  |
    | 离线使用     | ✅ 支持                 | ❌ 需要网络                |
    | 配置复杂度   | 需要安装 Ollama         | 只需 API Key              |
    """)
    
    print("\n💡 使用建议:")
    print("- 开发测试：优先使用 Ollama，节省成本")
    print("- 生产环境：根据需求选择，敏感数据用本地")
    print("- 高质量要求：使用云端先进模型")


if __name__ == "__main__":
    print("\n🦙 Ollama 本地模型示例\n")
    print("前提：确保已安装 Ollama 并下载模型")
    print("安装：brew install ollama (macOS) 或访问 ollama.ai")
    print("下载模型：ollama pull qwen3.5:9b\n")
    
    try:
        test_ollama_basic()
        test_ollama_with_prompt_template()
        test_ollama_streaming()
        test_ollama_batch_processing()
        compare_ollama_vs_cloud()
        print("\n✅ Ollama 示例完成！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n请确保:")
        print("1. Ollama 已安装并运行")
        print("2. 已下载模型：ollama pull qwen3.5:9b")
        print("3. Ollama 服务在 http://localhost:11434 运行")
