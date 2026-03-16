"""
示例：Ollama 本地模型基础使用

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


def setup_ollama():
    """设置 Ollama 模型"""
    print("=" * 60)
    print("Ollama 设置指南")
    print("=" * 60)
    
    print("""
    📦 安装 Ollama:
    
    macOS:
      brew install ollama
    
    Linux:
      curl -fsSL https://ollama.ai/install.sh | sh
    
    Windows:
      访问 https://ollama.ai 下载安装包
    
    📥 下载模型:
      ollama pull qwen3.5:9b
    
    ▶️  启动服务:
      ollama serve
    
    🔍 验证:
      ollama list
    """)


def test_basic_chat():
    """测试基础对话"""
    print("\n" + "=" * 60)
    print("基础对话")
    print("=" * 60)
    
    # 创建 Ollama 模型实例
    llm = ChatOllama(
        model="qwen3.5:9b",
        temperature=0.7,
        num_ctx=4096
    )
    
    print(f"模型：{llm.model}")
    print(f"温度：{llm.temperature}")
    
    # 简单对话
    messages = [
        SystemMessage(content="你是一个友好的 AI 助手。"),
        HumanMessage(content="你好！请用一句话介绍你自己。")
    ]
    
    print("\n发送消息...")
    response = llm.invoke(messages)
    print(f"响应：{response.content}")


def test_with_prompt_template():
    """使用提示模板"""
    print("\n" + "=" * 60)
    print("提示模板")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_template(
        "请用{language}回答：{question}"
    )
    
    # 创建链
    chain = prompt | llm | StrOutputParser()
    
    # 测试
    print("\n测试 1 - 中文回答:")
    result = chain.invoke({
        "language": "中文",
        "question": "什么是 Python？"
    })
    print(f"结果：{result[:150]}...")
    
    print("\n测试 2 - 英文回答:")
    result = chain.invoke({
        "language": "English",
        "question": "什么是 Python？"
    })
    print(f"结果：{result[:150]}...")


def test_streaming():
    """测试流式输出"""
    print("\n" + "=" * 60)
    print("流式输出")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", streaming=True)
    
    messages = [
        HumanMessage(content="请写一首关于春天的短诗，4 句即可。")
    ]
    
    print("流式输出：")
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
    print()


def test_different_models():
    """测试不同 Ollama 模型"""
    print("\n" + "=" * 60)
    print("不同模型对比")
    print("=" * 60)
    
    models = [
        "qwen3.5:9b",
        "llama3:8b",
        "mistral:7b"
    ]
    
    question = "1+1 等于几？"
    messages = [HumanMessage(content=question)]
    
    for model_name in models:
        print(f"\n模型：{model_name}")
        try:
            llm = ChatOllama(model=model_name)
            response = llm.invoke(messages)
            print(f"响应：{response.content}")
        except Exception as e:
            print(f"错误：{e}")
            print(f"提示：运行 'ollama pull {model_name}' 下载模型")


def ollama_best_practices():
    """Ollama 最佳实践"""
    print("\n" + "=" * 60)
    print("最佳实践")
    print("=" * 60)
    
    print("""
    💡 Ollama 使用建议:
    
    1. 模型选择:
       - qwen3.5:9b: 平衡性能和速度，适合大多数任务
       - llama3:8b: 轻量快速，适合简单任务
       - codellama: 专门用于代码生成
    
    2. 性能优化:
       - 调整 num_ctx 控制上下文窗口
       - 使用 GPU 加速 (如果可用)
       - 批量处理相似请求
    
    3. 资源管理:
       - 定期清理未使用的模型：ollama rm <model>
       - 监控内存使用
       - 设置合理的并发限制
    
    4. 开发工作流:
       - 本地开发使用 Ollama
       - 生产环境根据需要选择云端或本地
       - 使用缓存减少重复调用
    """)


if __name__ == "__main__":
    print("\n🦙 Ollama 本地模型基础示例\n")
    print("前提：确保已安装 Ollama 并下载 qwen3.5:9b 模型\n")
    
    try:
        setup_ollama()
        test_basic_chat()
        test_with_prompt_template()
        test_streaming()
        test_different_models()
        ollama_best_practices()
        
        print("\n✅ Ollama 示例完成！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n请确保:")
        print("1. Ollama 已安装")
        print("2. 已下载模型：ollama pull qwen3.5:9b")
        print("3. Ollama 服务正在运行")
