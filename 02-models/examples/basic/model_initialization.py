"""
示例：模型初始化与配置

演示如何初始化和配置不同的语言模型
"""

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


def test_anthropic_model():
    """测试 Anthropic Claude 模型"""
    print("=" * 60)
    print("Anthropic Claude 模型")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    # 基础配置
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0.7,
        max_tokens=1024,
        timeout=60
    )
    
    print(f"模型：{llm.model_name}")
    print(f"温度：{llm.temperature}")
    print(f"最大 token: {llm.max_tokens}")
    
    # 测试调用
    messages = [
        HumanMessage(content="你好，请用一句话介绍自己。")
    ]
    
    response = llm.invoke(messages)
    print(f"\n响应：{response.content}")


def test_openai_model():
    """测试 OpenAI GPT 模型"""
    print("\n" + "=" * 60)
    print("OpenAI GPT 模型")
    print("=" * 60)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY 未配置，跳过")
        return
    
    # 基础配置
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1024,
        timeout=60
    )
    
    print(f"模型：{llm.model_name}")
    print(f"温度：{llm.temperature}")
    
    # 测试调用
    messages = [
        HumanMessage(content="你好，请用一句话介绍自己。")
    ]
    
    response = llm.invoke(messages)
    print(f"\n响应：{response.content}")


def test_ollama_model():
    """测试 Ollama 本地模型"""
    print("\n" + "=" * 60)
    print("Ollama 本地模型")
    print("=" * 60)
    
    # 本地模型，不需要 API Key
    llm = ChatOllama(
        model="qwen3.5:9b",
        temperature=0.7,
        num_ctx=4096
    )
    
    print(f"模型：{llm.model}")
    print(f"温度：{llm.temperature}")
    print(f"上下文窗口：{llm.num_ctx}")
    
    # 测试调用
    messages = [
        HumanMessage(content="你好，请用一句话介绍自己。")
    ]
    
    try:
        response = llm.invoke(messages)
        print(f"\n响应：{response.content}")
    except Exception as e:
        print(f"\n⚠️  调用失败：{e}")
        print("请确保 Ollama 已安装并运行：ollama pull qwen3.5:9b")


def test_model_parameters():
    """测试不同模型参数的影响"""
    print("\n" + "=" * 60)
    print("模型参数对比")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    question = "用 3 个词描述人工智能"
    
    # 低温：更确定、更保守
    print("\n🌡️  低温 (temperature=0.1) - 更确定:")
    llm_low = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.1)
    response = llm_low.invoke([HumanMessage(content=question)])
    print(f"响应：{response.content}")
    
    # 高温：更随机、更有创意
    print("\n🌡️  高温 (temperature=0.9) - 更有创意:")
    llm_high = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.9)
    response = llm_high.invoke([HumanMessage(content=question)])
    print(f"响应：{response.content}")


def test_model_comparison():
    """对比不同模型"""
    print("\n" + "=" * 60)
    print("模型对比总结")
    print("=" * 60)
    
    print("""
    | 模型提供商   | 模型名称              | 特点                          | 使用场景          |
    |--------------|----------------------|-------------------------------|------------------|
    | Anthropic    | claude-3-sonnet      | 平衡性能和成本                | 通用任务          |
    | Anthropic    | claude-3-opus        | 最强性能                      | 复杂推理          |
    | Anthropic    | claude-3-haiku       | 快速、经济                    | 简单任务          |
    | OpenAI       | gpt-4-turbo          | 强大、多模态                  | 高级应用          |
    | OpenAI       | gpt-3.5-turbo        | 快速、经济                    | 日常任务          |
    | Ollama       | qwen3.5:9b           | 本地运行、免费                | 开发测试          |
    | Ollama       | llama3:8b            | 轻量、快速                    | 简单任务          |
    """)
    
    print("\n💡 选择建议:")
    print("- 开发测试：使用 Ollama 本地模型，节省成本")
    print("- 生产环境：根据预算和性能需求选择")
    print("- 敏感数据：优先本地模型或私有部署")


if __name__ == "__main__":
    print("\n🤖 模型初始化与配置示例\n")
    
    test_anthropic_model()
    test_openai_model()
    test_ollama_model()
    test_model_parameters()
    test_model_comparison()
    
    print("\n✅ 所有测试完成！")
