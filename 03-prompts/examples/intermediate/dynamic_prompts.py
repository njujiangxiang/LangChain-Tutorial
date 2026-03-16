"""
示例 1: 动态提示生成

演示如何根据上下文动态生成提示
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


def test_context_aware_prompt():
    """测试上下文感知的提示"""
    print("=" * 60)
    print("上下文感知的动态提示")
    print("=" * 60)
    
    # 根据时间生成不同的问候
    hour = datetime.now().hour
    if hour < 12:
        greeting = "早上好"
    elif hour < 18:
        greeting = "下午好"
    else:
        greeting = "晚上好"
    
    # 动态创建系统提示
    system_prompt = f"""你是一位友好的 AI 助手。
当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
请用{greeting}开始你的回答。"""
    
    chat_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    if os.getenv('ANTHROPIC_API_KEY'):
        llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
        
        messages = chat_template.format_messages(question="今天有什么建议？")
        response = llm.invoke(messages)
        
        print(f"动态系统提示：{system_prompt[:100]}...")
        print(f"用户问题：今天有什么建议？")
        print(f"模型响应：{response.content[:300]}...\n")


def test_conversation_history():
    """测试带对话历史的提示"""
    print("=" * 60)
    print("带对话历史的提示")
    print("=" * 60)
    
    # 创建带历史消息的模板
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个有帮助的 AI 助手，记住对话历史。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # 模拟对话历史
    history = [
        HumanMessage(content="我叫小明"),
        AIMessage(content="你好小明！很高兴认识你。"),
        HumanMessage(content="我喜欢编程"),
        AIMessage(content="编程很有趣！你最喜欢什么编程语言？")
    ]
    
    if os.getenv('ANTHROPIC_API_KEY'):
        llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
        
        # 新问题 (应该记住历史)
        messages = chat_template.format_messages(
            history=history,
            input="你觉得我应该学习什么编程语言？"
        )
        
        response = llm.invoke(messages)
        
        print(f"对话历史：{len(history)} 条消息")
        print(f"新问题：我应该学习什么编程语言？")
        print(f"模型响应：{response.content[:300]}...\n")


def test_conditional_prompt():
    """测试条件提示"""
    print("=" * 60)
    print("条件提示 (根据输入类型)")
    print("=" * 60)
    
    def create_prompt_for_type(input_type: str, content: str):
        """根据类型创建不同的提示"""
        if input_type == "code":
            system = "你是一位资深程序员，擅长代码审查和优化。"
            user = f"请审查以下代码并提供改进建议：\n\n{content}"
        elif input_type == "writing":
            system = "你是一位专业编辑，擅长文字润色。"
            user = f"请润色以下文字，使其更流畅：\n\n{content}"
        elif input_type == "analysis":
            system = "你是一位数据分析师，擅长洞察分析。"
            user = f"请分析以下内容并提供洞察：\n\n{content}"
        else:
            system = "你是一位通用的 AI 助手。"
            user = f"请回答以下问题：\n\n{content}"
        
        return ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", user)
        ])
    
    if os.getenv('ANTHROPIC_API_KEY'):
        llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
        
        # 测试代码审查
        code_prompt = create_prompt_for_type(
            "code",
            "def add(a,b):\n    return a+b"
        )
        messages = code_prompt.format_messages()
        response = llm.invoke(messages)
        print("📝 代码审查:")
        print(f"响应：{response.content[:200]}...\n")
        
        # 测试文字润色
        writing_prompt = create_prompt_for_type(
            "writing",
            "这个产品很好用，我非常喜欢，推荐给大家。"
        )
        messages = writing_prompt.format_messages()
        response = llm.invoke(messages)
        print("✏️ 文字润色:")
        print(f"响应：{response.content[:200]}...\n")


def test_progressive_refinement():
    """测试渐进式细化提示"""
    print("=" * 60)
    print("渐进式细化 (多轮优化)")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 第 1 轮：粗略回答
    prompt1 = ChatPromptTemplate.from_messages([
        ("system", "简洁回答，不超过 50 字。"),
        ("human", "什么是机器学习？")
    ])
    response1 = llm.invoke(prompt1.format_messages())
    print(f"第 1 轮 (简洁): {response1.content}\n")
    
    # 第 2 轮：详细解释
    prompt2 = ChatPromptTemplate.from_messages([
        ("system", "详细解释，包含例子。"),
        ("human", "什么是机器学习？")
    ])
    response2 = llm.invoke(prompt2.format_messages())
    print(f"第 2 轮 (详细): {response2.content[:200]}...\n")
    
    # 第 3 轮：专业角度
    prompt3 = ChatPromptTemplate.from_messages([
        ("system", "从工程师角度解释，包含技术细节。"),
        ("human", "什么是机器学习？")
    ])
    response3 = llm.invoke(prompt3.format_messages())
    print(f"第 3 轮 (专业): {response3.content[:200]}...\n")


if __name__ == "__main__":
    print("\n🔄 动态提示生成示例\n")
    
    test_context_aware_prompt()
    test_conversation_history()
    test_conditional_prompt()
    test_progressive_refinement()
    
    print("✅ 所有测试完成！")
