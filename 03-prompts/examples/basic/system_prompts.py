"""
示例 2: 系统提示设计

演示如何设计有效的系统提示 (System Prompts)
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def create_system_prompt(role: str, tone: str, constraints: list) -> str:
    """创建系统提示"""
    constraints_text = "\n".join([f"- {c}" for c in constraints])
    
    return f"""你是一位{role}。

沟通风格：{tone}

请遵循以下约束：
{constraints_text}

如果你不确定某件事，请诚实地说明。"""


def test_different_roles():
    """测试不同角色的系统提示"""
    print("=" * 60)
    print("不同角色的系统提示")
    print("=" * 60)
    
    scenarios = [
        {
            "role": "资深 Python 工程师",
            "tone": "专业、清晰、注重最佳实践",
            "constraints": ["只使用 Python 3.10+ 特性", "提供代码示例", "解释设计决策"]
        },
        {
            "role": "小学科学老师",
            "tone": "简单易懂、生动有趣、鼓励提问",
            "constraints": ["使用生活中的例子", "避免专业术语", "每段不超过 3 句话"]
        },
        {
            "role": "商务顾问",
            "tone": "专业、简洁、数据驱动",
            "constraints": ["提供具体建议", "引用相关数据", "考虑成本和收益"]
        }
    ]
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过模型调用")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景{i}: {scenario['role']}")
        print("-" * 60)
        
        system_prompt = create_system_prompt(
            scenario['role'],
            scenario['tone'],
            scenario['constraints']
        )
        
        chat_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "请解释什么是 API？")
        ])
        
        messages = chat_template.format_messages()
        response = llm.invoke(messages)
        
        print(f"响应：{response.content[:300]}...\n")


def test_tone_variations():
    """测试不同语气的系统提示"""
    print("=" * 60)
    print("不同语气的系统提示")
    print("=" * 60)
    
    tones = [
        "正式、专业",
        "友好、随意",
        "幽默、风趣",
        "严肃、权威"
    ]
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过模型调用")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    for tone in tones:
        print(f"\n语气：{tone}")
        print("-" * 60)
        
        system_prompt = f"你是一位 AI 助手。你的沟通风格应该是：{tone}。"
        
        chat_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "今天天气不错，有什么建议吗？")
        ])
        
        messages = chat_template.format_messages()
        response = llm.invoke(messages)
        
        print(f"响应：{response.content[:200]}...\n")


def test_constrained_output():
    """测试约束输出的系统提示"""
    print("=" * 60)
    print("约束输出的系统提示")
    print("=" * 60)
    
    system_prompt = """你是一位 AI 助手。请遵循以下约束：
1. 回答必须恰好 3 句话
2. 每句话不超过 20 个字
3. 使用中文回答
4. 不要使用专业术语"""
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过模型调用")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    chat_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "什么是人工智能？")
    ])
    
    messages = chat_template.format_messages()
    response = llm.invoke(messages)
    
    print(f"问题：什么是人工智能？")
    print(f"约束响应：{response.content}\n")


if __name__ == "__main__":
    print("\n🎯 系统提示设计示例\n")
    
    test_different_roles()
    test_tone_variations()
    test_constrained_output()
    
    print("✅ 所有测试完成！")
