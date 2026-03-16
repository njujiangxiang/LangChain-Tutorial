"""
示例：Ollama 高级 Agent

演示复杂的 Agent 模式和高级技巧
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

load_dotenv()


# ==================== 定义工具集 ====================

@tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"错误：{e}"


@tool
def search_knowledge(query: str) -> str:
    """搜索知识库"""
    # 模拟知识库
    knowledge = {
        "python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1989 年发明。",
        "ai": "人工智能 (AI) 是计算机科学的一个分支，致力于创建智能机器。",
        "langchain": "LangChain 是用于开发 LLM 应用的框架，提供组件和工具。",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"未找到关于'{query}'的信息"


@tool
def get_weather(city: str = "南京") -> str:
    """获取天气"""
    weathers = {
        "南京": "晴，25°C，湿度 60%",
        "北京": "多云，28°C",
        "上海": "小雨，23°C",
        "深圳": "晴，30°C",
    }
    return weathers.get(city, f"{city}: 晴，26°C")


@tool
def recommend_restaurant(cuisine: str = "中餐") -> str:
    """推荐餐厅"""
    restaurants = {
        "中餐": "南京大牌档 - 传统江苏菜，人均 100 元",
        "西餐": "王品牛排 - 高端西餐厅，人均 500 元",
        "日料": "将太无二 - 创意日本料理，人均 300 元",
        "火锅": "海底捞 - 知名连锁火锅，人均 150 元",
    }
    return restaurants.get(cuisine, "推荐：本地特色餐厅")


def create_react_agent():
    """创建 ReAct Agent"""
    print("=" * 60)
    print("ReAct Agent - 推理与行动")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    tools = [
        get_current_time,
        calculate,
        search_knowledge,
        get_weather,
        recommend_restaurant,
    ]
    
    # ReAct prompt
    react_prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个智能助手，可以使用以下工具：

{tools}

使用以下格式：

Question: 用户的问题
Thought: 你的思考过程
Action: 要采取的行动，从 [{tool_names}] 中选择
Action Input: 行动的输入
Observation: 行动的结果
... (可重复 Thought/Action/Observation)
Thought: 我有足够信息回答
Answer: 最终答案

开始!"""),
        ("human", "{input}"),
    ])
    
    print("可用工具:")
    for t in tools:
        print(f"  - {t.name}: {t.description}")
    
    print("\n示例问题:")
    questions = [
        "现在几点了？",
        "计算 123 * 456",
        "南京天气怎么样？",
        "推荐一个中餐厅",
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        # 简化处理
        print(f"A: [Agent 会使用工具回答这个问题]")


def multi_agent_collaboration():
    """多 Agent 协作"""
    print("\n" + "=" * 60)
    print("多 Agent 协作 - 专家系统")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 定义不同角色的 Agent
    roles = {
        "研究员": "你是一名研究员，负责查找和分析信息。",
        "分析师": "你是一名数据分析师，负责计算和统计。",
        "顾问": "你是一名专业顾问，负责给出建议。",
    }
    
    print("多 Agent 协作系统:\n")
    
    for role, system_prompt in roles.items():
        print(f"【{role}】")
        print(f"  职责：{system_prompt}\n")
    
    # 协作流程示例
    print("协作流程示例:")
    print("""
    用户问题："我想去南京旅游，预算 3000 元，有什么建议？"
    
    1. 研究员 Agent:
       - 查询南京景点信息
       - 查询酒店价格
       - 查询交通费用
    
    2. 分析师 Agent:
       - 计算总预算
       - 分配各项支出
       - 优化预算分配
    
    3. 顾问 Agent:
       - 综合所有信息
       - 给出旅行建议
       - 提供注意事项
    
    最终答案：完整的旅行计划
    """)


def agent_with_memory():
    """带长期记忆的 Agent"""
    print("\n" + "=" * 60)
    print("带长期记忆的 Agent")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 长期记忆存储
    long_term_memory = {
        "user_profile": {
            "name": "小明",
            "age": 25,
            "location": "南京",
            "interests": ["编程", "音乐", "旅行"],
        },
        "conversation_history": [],
    }
    
    def agent_with_ltm(user_input: str):
        """带长期记忆的 Agent"""
        # 从记忆中提取上下文
        profile = long_term_memory["user_profile"]
        history = long_term_memory["conversation_history"][-5:]
        
        context = f"""用户信息:
- 姓名：{profile['name']}
- 年龄：{profile['age']}
- 城市：{profile['location']}
- 兴趣：{', '.join(profile['interests'])}

对话历史:
{chr(10).join([f"{h['role']}: {h['content']}" for h in history])}
"""
        
        prompt = f"""{context}
用户：{user_input}
助手："""
        
        response = llm.invoke([("human", prompt)])
        
        # 更新记忆
        long_term_memory["conversation_history"].append({
            "role": "user",
            "content": user_input
        })
        long_term_memory["conversation_history"].append({
            "role": "assistant",
            "content": response.content
        })
        
        return response.content
    
    # 测试
    print("带记忆的对话:\n")
    
    conversations = [
        "你好",
        "我最近想学习编程，有什么建议？",  # 基于兴趣
        "我在南京，有什么好玩的地方？",  # 基于位置
        "你还记得我叫什么吗？",  # 测试记忆
    ]
    
    for msg in conversations:
        response = agent_with_ltm(msg)
        print(f"用户：{msg}")
        print(f"助手：{response.content[:100]}...\n")


def agent_planning():
    """Agent 规划能力"""
    print("\n" + "=" * 60)
    print("Agent 规划 - 任务分解")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 规划 prompt
    plan_prompt = ChatPromptTemplate.from_template("""
将以下任务分解为可执行的步骤：

任务：{task}

要求:
1. 每个步骤清晰具体
2. 步骤之间有逻辑顺序
3. 标注每个步骤需要的工具

格式:
步骤 1: [描述] (工具：xxx)
步骤 2: [描述] (工具：xxx)
...
""")
    
    chain = plan_prompt | llm | StrOutputParser()
    
    # 测试任务
    tasks = [
        "计划一次 3 天的南京旅行",
        "学习 Python 编程",
        "准备一顿晚餐",
    ]
    
    print("任务规划示例:\n")
    
    for task in tasks:
        print(f"任务：{task}")
        plan = chain.invoke({"task": task})
        print(f"计划:\n{plan}\n")


def agent_self_reflection():
    """Agent 自我反思"""
    print("\n" + "=" * 60)
    print("Agent 自我反思 - 质量改进")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 生成 prompt
    generate_prompt = ChatPromptTemplate.from_template(
        "回答以下问题：{question}"
    )
    
    # 反思 prompt
    reflect_prompt = ChatPromptTemplate.from_template("""
评估以下回答的质量：

问题：{question}
回答：{answer}

评估标准:
1. 准确性
2. 完整性
3. 清晰度

评分 (1-10): 
改进建议:
""")
    
    generate_chain = generate_prompt | llm | StrOutputParser()
    reflect_chain = reflect_prompt | llm | StrOutputParser()
    
    # 测试
    question = "什么是机器学习？"
    
    print(f"问题：{question}\n")
    
    # 生成初始回答
    print("初始回答:")
    answer = generate_chain.invoke({"question": question})
    print(f"{answer}\n")
    
    # 自我反思
    print("自我反思:")
    reflection = reflect_chain.invoke({"question": question, "answer": answer})
    print(f"{reflection}\n")


if __name__ == "__main__":
    print("\n🦙 Ollama 高级 Agent 示例\n")
    
    create_react_agent()
    multi_agent_collaboration()
    agent_with_memory()
    agent_planning()
    agent_self_reflection()
    
    print("\n✅ Ollama 高级 Agent 示例完成！")
