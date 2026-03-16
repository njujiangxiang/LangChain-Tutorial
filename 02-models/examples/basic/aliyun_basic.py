"""
示例：阿里云百炼模型基础使用

演示如何使用 LangChain 调用阿里云百炼大模型
支持两种方式：
1. 使用 DashScope SDK
2. 使用兼容 OpenAI 接口的方式
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


def setup_aliyun():
    """设置阿里云百炼"""
    print("=" * 60)
    print("阿里云百炼设置指南")
    print("=" * 60)
    
    print("""
    📦 安装依赖:
      pip install dashscope
      pip install langchain-community
    
    🔑 获取 API Key:
      1. 访问 https://dashscope.console.aliyun.com/
      2. 登录阿里云账号
      3. 创建/获取 API Key
      4. 添加到 .env 文件:
         DASHSCOPE_API_KEY=your_key_here
    
    📚 可用模型:
      - qwen-turbo: 速度快，成本低
      - qwen-plus: 性能平衡
      - qwen-max: 最强性能
      - qwen-vl-max: 多模态 (图像理解)
    """)


def test_with_dashscope():
    """使用 DashScope SDK"""
    print("\n" + "=" * 60)
    print("方式 1: DashScope SDK")
    print("=" * 60)
    
    api_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not api_key:
        print("⚠️  DASHSCOPE_API_KEY 未配置")
        print("请在 .env 文件中添加：DASHSCOPE_API_KEY=your_key")
        
        # 演示模式
        print("\n演示代码:")
        print("""
        from langchain_community.chat_models import QianfanChatEndpoint
        
        llm = QianfanChatEndpoint(
            model="qwen-plus",
            dashscope_api_key="your_key"
        )
        """)
        return
    
    try:
        from langchain_community.chat_models import QianfanChatEndpoint
        
        llm = QianfanChatEndpoint(
            model="qwen-plus",
            dashscope_api_key=api_key
        )
        
        messages = [
            SystemMessage(content="你是一个友好的 AI 助手。"),
            HumanMessage(content="你好！请用一句话介绍你自己。")
        ]
        
        response = llm.invoke(messages)
        print(f"响应：{response.content}")
        
    except ImportError:
        print("⚠️  需要安装：pip install langchain-community")
    except Exception as e:
        print(f"❌ 错误：{e}")


def test_with_openai_compatible():
    """使用 OpenAI 兼容接口"""
    print("\n" + "=" * 60)
    print("方式 2: OpenAI 兼容接口")
    print("=" * 60)
    
    api_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not api_key:
        print("⚠️  DASHSCOPE_API_KEY 未配置")
        return
    
    try:
        from langchain_openai import ChatOpenAI
        
        # 阿里云百炼提供 OpenAI 兼容接口
        llm = ChatOpenAI(
            model="qwen-plus",
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        print(f"模型：qwen-plus")
        print(f"API 端点：https://dashscope.aliyuncs.com/compatible-mode/v1")
        
        messages = [
            HumanMessage(content="你好！请用一句话介绍你自己。")
        ]
        
        response = llm.invoke(messages)
        print(f"\n响应：{response.content}")
        
    except ImportError:
        print("⚠️  需要安装：pip install langchain-openai")
    except Exception as e:
        print(f"❌ 错误：{e}")


def test_with_prompt_template():
    """使用提示模板"""
    print("\n" + "=" * 60)
    print("提示模板示例")
    print("=" * 60)
    
    api_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not api_key:
        print("⚠️  API Key 未配置，显示示例代码")
        print("""
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="qwen-plus",
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        prompt = ChatPromptTemplate.from_template(
            "请用{style}的风格解释{concept}"
        )
        
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"style": "简单易懂", "concept": "机器学习"})
        """)
        return
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="qwen-plus",
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0.7
        )
        
        prompt = ChatPromptTemplate.from_template(
            "请用{style}的风格解释{concept}"
        )
        
        chain = prompt | llm | StrOutputParser()
        
        # 测试不同风格
        test_cases = [
            {"style": "简单易懂", "concept": "机器学习"},
            {"style": "专业严谨", "concept": "深度学习"},
        ]
        
        for case in test_cases:
            print(f"\n用{case['style']}的风格解释{case['concept']}:")
            result = chain.invoke(case)
            print(f"结果：{result[:150]}...")
            
    except Exception as e:
        print(f"❌ 错误：{e}")


def compare_models():
    """对比不同阿里云模型"""
    print("\n" + "=" * 60)
    print("阿里云模型对比")
    print("=" * 60)
    
    print("""
    | 模型          | 特点                      | 适用场景            | 成本     |
    |---------------|--------------------------|---------------------|----------|
    | qwen-turbo    | 速度快，成本低            | 简单任务，高并发     | 💰        |
    | qwen-plus     | 性能平衡，性价比高         | 大多数通用任务       | 💰💰      |
    | qwen-max      | 最强性能，处理复杂任务     | 复杂推理，专业场景   | 💰💰💰    |
    | qwen-vl-max   | 多模态，支持图像理解       | 图像问答，视觉分析   | 💰💰💰    |
    
    💡 选择建议:
    - 开发测试：qwen-turbo (成本低)
    - 生产通用：qwen-plus (平衡)
    - 复杂任务：qwen-max (最强)
    - 图像相关：qwen-vl-max (多模态)
    """)


def aliyun_best_practices():
    """阿里云最佳实践"""
    print("\n" + "=" * 60)
    print("最佳实践")
    print("=" * 60)
    
    print("""
    💡 阿里云百炼使用建议:
    
    1. API Key 管理:
       - 使用环境变量存储
       - 定期轮换密钥
       - 设置使用限额
    
    2. 成本控制:
       - 监控 token 使用量
       - 设置预算告警
       - 选择合适的模型
    
    3. 性能优化:
       - 使用流式输出减少等待
       - 批量处理请求
       - 实现本地缓存
    
    4. 错误处理:
       - 处理 API 限流
       - 实现重试机制
       - 记录错误日志
    
    5. 安全考虑:
       - 不发送敏感数据
       - 实现输入过滤
       - 审计 API 调用
    """)


if __name__ == "__main__":
    print("\n☁️ 阿里云百炼模型基础示例\n")
    
    setup_aliyun()
    test_with_dashscope()
    test_with_openai_compatible()
    test_with_prompt_template()
    compare_models()
    aliyun_best_practices()
    
    print("\n✅ 阿里云示例完成！")
