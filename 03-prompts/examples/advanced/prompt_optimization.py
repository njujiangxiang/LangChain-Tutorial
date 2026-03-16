"""
示例 1: 提示优化技巧

演示高级提示优化技术和最佳实践
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def test_chain_of_thought():
    """测试思维链 (Chain of Thought)"""
    print("=" * 60)
    print("思维链 (Chain of Thought)")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 普通提示
    simple_prompt = ChatPromptTemplate.from_template(
        "问题：{question}\n答案："
    )
    
    # 思维链提示
    cot_prompt = ChatPromptTemplate.from_template(
        "问题：{question}\n\n"
        "让我们一步步思考:\n"
        "1. 首先分析问题的关键信息\n"
        "2. 然后列出已知条件\n"
        "3. 接着推导中间步骤\n"
        "4. 最后得出结论\n\n"
        "思考过程："
    )
    
    question = "小明有 5 个苹果，他给了小红 2 个，又买了 3 个，现在他有几个苹果？"
    
    print(f"问题：{question}\n")
    
    # 普通回答
    print("普通提示:")
    simple_response = (simple_prompt | llm | StrOutputParser()).invoke({"question": question})
    print(f"{simple_response}\n")
    
    # 思维链回答
    print("思维链提示:")
    cot_response = (cot_prompt | llm | StrOutputParser()).invoke({"question": question})
    print(f"{cot_response}\n")


def test_few_shot_optimization():
    """测试优化的少样本提示"""
    print("=" * 60)
    print("优化的少样本提示")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 精心设计的少样本示例
    few_shot_template = ChatPromptTemplate.from_template(
        "任务：将口语转换为正式书面语\n\n"
        "示例 1:\n"
        "输入：这东西贼好用\n"
        "输出：该产品非常实用\n\n"
        "示例 2:\n"
        "输入：我贼喜欢这个\n"
        "输出：我非常喜欢这个产品\n\n"
        "示例 3:\n"
        "输入：这玩意儿太贵了\n"
        "输出：该产品的价格较高\n\n"
        "现在请转换:\n"
        "输入：{input}\n"
        "输出："
    )
    
    test_inputs = [
        "这电影贼好看",
        "那家店的东西贼难吃",
        "今天天气贼好"
    ]
    
    for input_text in test_inputs:
        response = (few_shot_template | llm | StrOutputParser()).invoke({"input": input_text})
        print(f"输入：{input_text}")
        print(f"输出：{response}\n")


def test_role_playing():
    """测试角色扮演提示"""
    print("=" * 60)
    print("角色扮演 (Role Playing)")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    roles = [
        ("严厉的老师", "指出以下代码的问题，语气要严格："),
        ("鼓励的导师", "对以下代码给予建设性反馈，语气要鼓励："),
        ("挑剔的客户", "从客户角度评价以下代码，关注用户体验：")
    ]
    
    code = """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""
    
    for role_name, instruction in roles:
        print(f"角色：{role_name}")
        print("-" * 60)
        
        role_prompt = ChatPromptTemplate.from_template(
            f"你是一位{role_name}。{instruction}\n\n代码:\n{{code}}"
        )
        
        response = (role_prompt | llm | StrOutputParser()).invoke({"code": code})
        print(f"{response[:250]}...\n")


def test_constraint_optimization():
    """测试约束优化"""
    print("=" * 60)
    print("约束优化")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 带明确约束的提示
    constrained_prompt = ChatPromptTemplate.from_template(
        "请解释什么是 API，遵循以下约束:\n"
        "- 使用比喻说明\n"
        "- 不超过 100 字\n"
        "- 包含 1 个生活例子\n"
        "- 避免技术术语\n"
        "- 以问句结束\n\n"
        "解释："
    )
    
    response = (constrained_prompt | llm | StrOutputParser()).invoke({})
    print(f"{response}\n")
    
    # 验证约束
    print(f"字数：{len(response)} 字符")
    print(f"包含问号：{'?' in response or '？' in response}")


def test_negative_prompting():
    """测试否定提示 (告诉模型不要做什么)"""
    print("=" * 60)
    print("否定提示 (Negative Prompting)")
    print("=" * 60)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置，跳过")
        return
    
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
    
    # 包含否定指令的提示
    negative_prompt = ChatPromptTemplate.from_template(
        "请介绍 Python 编程语言。\n\n"
        "请注意:\n"
        "- 不要提及 Java\n"
        "- 不要使用代码示例\n"
        "- 不要超过 150 字\n"
        "- 不要使用'首先'、'其次'等序数词\n\n"
        "介绍："
    )
    
    response = (negative_prompt | llm | StrOutputParser()).invoke({})
    print(f"{response}\n")
    
    # 验证
    print(f"检查：{'Java' not in response and 'def ' not in response}")


if __name__ == "__main__":
    print("\n✨ 提示优化技巧示例\n")
    
    test_chain_of_thought()
    test_few_shot_optimization()
    test_role_playing()
    test_constraint_optimization()
    test_negative_prompting()
    
    print("✅ 所有测试完成！")
