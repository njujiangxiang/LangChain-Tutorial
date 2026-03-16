"""
示例：自定义 LangChain 组件

演示如何创建自定义的 Prompt、Model、Chain 和 OutputParser
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import re
import json

# 加载环境变量
load_dotenv()

def get_llm():
    """获取 LLM 实例"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY 未配置")
        return None
    return ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)


# ============================================================
# 1. 自定义输出解析器
# ============================================================

class NumberedListOutputParser(BaseOutputParser[list]):
    """解析编号列表输出为 Python 列表"""
    
    def parse(self, text: str) -> list:
        """
        解析文本中的编号列表
        
        示例输入:
        1. 第一项
        2. 第二项
        3. 第三项
        
        输出：["第一项", "第二项", "第三项"]
        """
        # 使用正则表达式匹配编号项
        pattern = r'^\s*\d+[\.\)]\s*(.+)$'
        items = []
        
        for line in text.strip().split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                items.append(match.group(1).strip())
        
        # 如果没有匹配到编号列表，尝试按行分割
        if not items:
            items = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        return items
    
    @property
    def _type(self) -> str:
        return "numbered_list_output_parser"


class JSONOutputParser(BaseOutputParser[dict]):
    """解析 JSON 格式输出为字典"""
    
    def parse(self, text: str) -> dict:
        """解析 JSON 文本"""
        # 尝试提取 JSON 块
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group()
        
        return json.loads(text)
    
    @property
    def _type(self) -> str:
        return "json_output_parser"


# ============================================================
# 2. 自定义 Prompt 模板
# ============================================================

def create_role_playing_prompt():
    """创建角色扮演提示模板"""
    
    template = """你是一位{role}，具有以下特征：
- 专业领域：{expertise}
- 沟通风格：{style}
- 经验水平：{experience}

请基于你的角色回答以下问题：

问题：{question}

回答:"""
    
    return ChatPromptTemplate.from_template(template)


def create_chain_of_thought_prompt():
    """创建思维链提示模板"""
    
    template = """请逐步思考以下问题，然后给出答案。

问题：{question}

思考步骤：
1. 首先，分析问题的关键点
2. 然后，考虑相关的知识和信息
3. 接着，推理出可能的答案
4. 最后，验证答案的合理性

思考过程：
{thinking}

最终答案："""
    
    return ChatPromptTemplate.from_template(template)


# ============================================================
# 3. 自定义链
# ============================================================

def create_self_reflection_chain(llm):
    """
    创建自我反思链
    
    流程：生成答案 → 反思质量 → 改进答案
    """
    # 第一步：生成初始答案
    initial_prompt = ChatPromptTemplate.from_template(
        "回答以下问题：{question}"
    )
    initial_chain = initial_prompt | llm
    
    # 第二步：反思和改进
    reflection_prompt = ChatPromptTemplate.from_template(
        """以下是问题的初始答案：
{initial_answer}

请评估这个答案的质量，并提供改进版本。
考虑以下方面：
- 准确性
- 完整性
- 清晰度

改进后的答案："""
    )
    reflection_chain = reflection_prompt | llm
    
    # 组合链
    full_chain = (
        initial_chain
        | RunnableLambda(lambda x: {"initial_answer": x.content, "question": x.content})
        | reflection_chain
    )
    
    return full_chain


def create_multi_step_reasoning_chain(llm):
    """
    创建多步推理链
    
    流程：分解问题 → 逐步解答 → 综合结论
    """
    # 步骤 1: 分解问题
    decompose_prompt = ChatPromptTemplate.from_template(
        "将以下复杂问题分解为 3-5 个子问题：\n{question}"
    )
    decompose_chain = decompose_prompt | llm
    
    # 步骤 2: 回答子问题
    answer_prompt = ChatPromptTemplate.from_template(
        "基于以下子问题，逐一回答：\n{sub_questions}"
    )
    answer_chain = answer_prompt | llm
    
    # 步骤 3: 综合结论
    synthesize_prompt = ChatPromptTemplate.from_template(
        "基于以下分析和答案，给出最终结论：\n{answers}"
    )
    synthesize_chain = synthesize_prompt | llm
    
    # 组合链
    full_chain = (
        decompose_chain
        | RunnableLambda(lambda x: {"sub_questions": x.content})
        | answer_chain
        | RunnableLambda(lambda x: {"answers": x.content})
        | synthesize_chain
    )
    
    return full_chain


# ============================================================
# 4. 演示函数
# ============================================================

def test_custom_output_parser():
    """测试自定义输出解析器"""
    print("=" * 60)
    print("自定义输出解析器")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("\n演示：NumberedListOutputParser")
        print("输入：'1. 苹果\\n2. 香蕉\\n3. 橙子'")
        print("输出：['苹果', '香蕉', '橙子']")
        return
    
    # 测试编号列表解析器
    list_prompt = ChatPromptTemplate.from_template(
        "列出 3 个学习 Python 的建议，使用编号格式 (1. 2. 3.)"
    )
    
    list_chain = list_prompt | llm | NumberedListOutputParser()
    
    print("\n📋 测试编号列表解析器:")
    result = list_chain.invoke({})
    print(f"解析结果：{result}")
    print(f"类型：{type(result)}")


def test_custom_prompt():
    """测试自定义提示模板"""
    print("\n" + "=" * 60)
    print("自定义提示模板")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("\n演示：角色扮演提示模板")
        return
    
    # 角色扮演提示
    role_prompt = create_role_playing_prompt()
    
    chain = role_prompt | llm
    
    print("\n🎭 测试角色扮演提示:")
    result = chain.invoke({
        "role": "资深软件工程师",
        "expertise": "Python 和系统设计",
        "style": "清晰、实用",
        "experience": "10 年",
        "question": "如何设计一个可扩展的 API？"
    })
    print(f"回答:\n{result.content}")
    
    # 思维链提示
    cot_prompt = create_chain_of_thought_prompt()
    cot_chain = cot_prompt | llm
    
    print("\n🧠 测试思维链提示:")
    result = cot_chain.invoke({
        "question": "如果所有程序员都改用 AI 编程，会发生什么？",
        "thinking": ""  # 留空让模型填充
    })
    print(f"回答:\n{result.content}")


def test_custom_chain():
    """测试自定义链"""
    print("\n" + "=" * 60)
    print("自定义链")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("\n演示：自我反思链和多步推理链")
        return
    
    # 测试自我反思链
    print("\n🔄 测试自我反思链:")
    reflection_chain = create_self_reflection_chain(llm)
    result = reflection_chain.invoke({"question": "什么是机器学习？"})
    print(f"改进后的答案:\n{result.content}")
    
    # 测试多步推理链
    print("\n🔗 测试多步推理链:")
    reasoning_chain = create_multi_step_reasoning_chain(llm)
    result = reasoning_chain.invoke({"question": "人工智能会取代人类工作吗？"})
    print(f"最终结论:\n{result.content}")


def test_composable_patterns():
    """测试可组合模式"""
    print("\n" + "=" * 60)
    print("可组合模式")
    print("=" * 60)
    
    llm = get_llm()
    if not llm:
        print("\n演示：链的组合和复用")
        return
    
    # 创建一个可复用的基础链
    base_prompt = ChatPromptTemplate.from_template("解释：{concept}")
    base_chain = base_prompt | llm
    
    # 组合不同的后处理
    def add_summary(text):
        return f"总结：{text.content[:100]}..."
    
    def add_emoji(text):
        return f"💡 {text.content}"
    
    # 不同的组合
    summary_chain = base_chain | RunnableLambda(add_summary)
    emoji_chain = base_chain | RunnableLambda(add_emoji)
    
    print("\n🧩 测试链组合:")
    concept = "递归"
    
    print(f"\n基础解释:")
    result = base_chain.invoke({"concept": concept})
    print(f"{result.content}")
    
    print(f"\n带总结:")
    result = summary_chain.invoke({"concept": concept})
    print(f"{result}")
    
    print(f"\n带表情:")
    result = emoji_chain.invoke({"concept": concept})
    print(f"{result}")


if __name__ == "__main__":
    print("\n🦜️🔗 LangChain 自定义组件示例\n")
    
    test_custom_output_parser()
    test_custom_prompt()
    test_custom_chain()
    test_composable_patterns()
    
    print("\n✅ 所有演示完成！")
