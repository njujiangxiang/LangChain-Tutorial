"""
示例 1: 基础 LLM 调用

演示如何使用 LangChain 调用不同的语言模型
"""

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def test_anthropic():
    """测试 Anthropic Claude 模型"""
    print("=" * 50)
    print("测试 Anthropic Claude")
    print("=" * 50)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    # 创建模型实例
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0.7,
        max_tokens=1024
    )
    
    # 发送消息
    messages = [
        SystemMessage(content="你是一个友好的 AI 助手"),
        HumanMessage(content="你好！请用一句话介绍你自己")
    ]
    
    response = llm.invoke(messages)
    print(f"响应：{response.content}\n")

def test_openai():
    """测试 OpenAI GPT 模型"""
    print("=" * 50)
    print("测试 OpenAI GPT")
    print("=" * 50)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY 未配置，跳过")
        return
    
    # 创建模型实例
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1024
    )
    
    # 发送消息
    messages = [
        SystemMessage(content="你是一个友好的 AI 助手"),
        HumanMessage(content="你好！请用一句话介绍你自己")
    ]
    
    response = llm.invoke(messages)
    print(f"响应：{response.content}\n")

def test_streaming():
    """测试流式输出"""
    print("=" * 50)
    print("测试流式输出")
    print("=" * 50)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0.7,
        max_tokens=500,
        streaming=True
    )
    
    messages = [
        HumanMessage(content="请写一首关于春天的短诗，4 句即可")
    ]
    
    print("流式输出：")
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    print("\n🦜️🔗 LangChain 基础 LLM 调用示例\n")
    
    test_anthropic()
    test_openai()
    test_streaming()
    
    print("✅ 所有测试完成！")
