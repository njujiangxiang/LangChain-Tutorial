"""
示例：提示模板基础

演示 LangChain 提示模板的基本用法
"""

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取 LLM 实例"""
    if os.getenv('ANTHROPIC_API_KEY'):
        return ChatAnthropic(model="claude-3-sonnet-20240229")
    return ChatOllama(model="qwen3.5:9b")


def test_chat_prompt_template():
    """测试聊天提示模板"""
    print("=" * 60)
    print("ChatPromptTemplate 基础")
    print("=" * 60)
    
    llm = get_llm()
    
    # 创建聊天提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，擅长{expertise}。"),
        ("human", "{question}")
    ])
    
    print(f"输入变量：{prompt.input_variables}")
    
    # 创建链
    chain = prompt | llm | StrOutputParser()
    
    # 测试
    result = chain.invoke({
        "role": "Python 专家",
        "expertise": "解释编程概念",
        "question": "什么是装饰器？"
    })
    
    print(f"\n结果：{result[:200]}...")


def test_prompt_template():
    """测试基础提示模板"""
    print("\n" + "=" * 60)
    print("PromptTemplate 基础")
    print("=" * 60)
    
    llm = get_llm()
    
    # 创建简单提示模板
    prompt = PromptTemplate.from_template(
        "翻译以下内容为{language}: {text}"
    )
    
    print(f"输入变量：{prompt.input_variables}")
    
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({
        "language": "英文",
        "text": "你好，世界"
    })
    
    print(f"\n结果：{result}")


def test_few_shot_prompting():
    """测试少样本提示"""
    print("\n" + "=" * 60)
    print("少样本提示 (Few-Shot)")
    print("=" * 60)
    
    llm = get_llm()
    
    from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
    
    # 示例
    examples = [
        {"input": "高兴", "output": "开心"},
        {"input": "悲伤", "output": "难过"},
        {"input": "快速", "output": "迅速"},
    ]
    
    example_prompt = PromptTemplate.from_template(
        "近义词：{input} → {output}"
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="请给出以下词语的近义词:",
        suffix="近义词：{input} →",
        input_variables=["input"]
    )
    
    chain = few_shot_prompt | llm | StrOutputParser()
    
    result = chain.invoke({"input": "美丽"})
    print(f"输入：美丽")
    print(f"结果：{result}")


def test_system_message():
    """测试系统消息"""
    print("\n" + "=" * 60)
    print("系统消息提示")
    print("=" * 60)
    
    llm = get_llm()
    
    # 创建带系统消息的提示
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "你是一个{personality}的助手。{constraint}"
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    # 测试不同人设
    test_cases = [
        {
            "personality": "幽默风趣",
            "constraint": "回答要简短有趣",
            "question": "什么是编程？"
        },
        {
            "personality": "严谨专业",
            "constraint": "回答要准确详细",
            "question": "什么是编程？"
        }
    ]
    
    for case in test_cases:
        print(f"\n人设：{case['personality']}")
        result = chain.invoke(case)
        print(f"结果：{result[:150]}...")


def test_prompt_formatting():
    """测试提示格式化"""
    print("\n" + "=" * 60)
    print("提示格式化技巧")
    print("=" * 60)
    
    # 使用 f-string 风格的模板
    prompt = ChatPromptTemplate.from_template(
        """请分析以下内容:

主题：{topic}
要点:
{points}

要求:
- 语言：{language}
- 长度：{length}"""
    )
    
    print(f"模板变量：{prompt.input_variables}")
    
    # 格式化
    formatted = prompt.format(
        topic="人工智能",
        points="1. 机器学习\n2. 深度学习\n3. 自然语言处理",
        language="中文",
        length="简洁"
    )
    
    print("\n格式化后的提示:")
    print(formatted)


if __name__ == "__main__":
    print("\n📝 提示模板基础示例\n")
    
    test_chat_prompt_template()
    test_prompt_template()
    test_few_shot_prompting()
    test_system_message()
    test_prompt_formatting()
    
    print("\n✅ 所有测试完成！")
