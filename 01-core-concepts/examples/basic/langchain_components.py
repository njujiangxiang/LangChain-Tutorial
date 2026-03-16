"""
示例：LangChain 核心组件介绍

演示 LangChain 的核心组件：Model、Prompt、Chain、OutputParser
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def test_basic_components():
    """测试 LangChain 基础组件"""
    print("=" * 60)
    print("LangChain 核心组件演示")
    print("=" * 60)
    
    # 检查 API 密钥
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，使用模拟演示")
        # 演示组件结构而不实际调用
        print("\n1. Model (模型): 负责生成文本")
        print("   - ChatAnthropic, ChatOpenAI, ChatOllama 等")
        print("\n2. Prompt (提示): 定义输入模板")
        print("   - ChatPromptTemplate, PromptTemplate")
        print("\n3. Chain (链): 组合组件形成流程")
        print("   - LLMChain, SequentialChain")
        print("\n4. OutputParser (输出解析器): 解析模型输出")
        print("   - StrOutputParser, JsonOutputParser")
        return
    
    # 1. Model - 创建模型实例
    print("\n1️⃣  Model (模型)")
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0.7,
        max_tokens=1024
    )
    print(f"   模型：{llm.model_name}")
    print(f"   温度：{llm.temperature}")
    
    # 2. Prompt - 创建提示模板
    print("\n2️⃣  Prompt (提示模板)")
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个友好的 AI 助手，擅长用简洁的语言回答问题。"),
        HumanMessage(content="{question}")
    ])
    print(f"   模板变量：{prompt.input_variables}")
    
    # 3. OutputParser - 创建输出解析器
    print("\n3️⃣  OutputParser (输出解析器)")
    output_parser = StrOutputParser()
    print("   类型：StrOutputParser (字符串输出)")
    
    # 4. Chain - 组合成链
    print("\n4️⃣  Chain (链)")
    chain = prompt | llm | output_parser
    print("   链结构：Prompt → Model → OutputParser")
    
    # 执行链
    print("\n📤  执行链:")
    question = "LangChain 是什么？"
    print(f"   输入：{question}")
    
    result = chain.invoke({"question": question})
    print(f"\n📥  输出:\n{result}")

def test_message_types():
    """测试不同类型的消息"""
    print("\n" + "=" * 60)
    print("消息类型演示")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  API 未配置，跳过实际调用")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229")
    
    # SystemMessage - 系统消息
    system_msg = SystemMessage(content="你是一个专业的 Python 程序员。")
    
    # HumanMessage - 用户消息
    human_msg = HumanMessage(content="请解释什么是列表推导式。")
    
    # 发送消息
    response = llm.invoke([system_msg, human_msg])
    print(f"系统消息 + 用户消息 → 响应:\n{response.content}")

def test_invoke_vs_stream():
    """对比 invoke 和 stream 方法"""
    print("\n" + "=" * 60)
    print("Invoke vs Stream 对比")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  API 未配置，跳过实际调用")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", streaming=True)
    messages = [HumanMessage(content="请用 3 句话解释机器学习。")]
    
    # Invoke - 一次性获取完整响应
    print("\n📦 Invoke (一次性获取):")
    response = llm.invoke(messages)
    print(f"完整响应：{response.content}")
    
    # Stream - 流式获取响应
    print("\n📤 Stream (流式输出):")
    print("   ", end="")
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
    print()

if __name__ == "__main__":
    print("\n🦜️🔗 LangChain 核心组件示例\n")
    
    test_basic_components()
    test_message_types()
    test_invoke_vs_stream()
    
    print("\n✅ 所有演示完成！")
