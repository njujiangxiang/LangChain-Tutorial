"""
示例：Ollama Agent - 中级

演示使用 Ollama 模型创建智能 Agent
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
import subprocess

load_dotenv()


# ==================== 定义工具 ====================

@tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        # 安全计算
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"


@tool
def search_web(query: str) -> str:
    """模拟网络搜索"""
    # 实际使用时可以接入真实搜索 API
    return f"[模拟搜索] 关于'{query}'的搜索结果：暂无真实数据"


@tool
def get_weather(city: str = "南京") -> str:
    """获取天气信息"""
    # 模拟天气数据
    weathers = {
        "南京": "晴，25°C，湿度 60%",
        "北京": "多云，28°C，湿度 45%",
        "上海": "小雨，23°C，湿度 80%",
    }
    return weathers.get(city, f"{city}: 暂无数据")


def create_simple_agent():
    """创建简单 Agent"""
    print("=" * 60)
    print("简单 Agent - 工具调用")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    tools = [get_current_time, calculate, get_weather]
    
    # 创建提示模板
    system_prompt = """你是一个有帮助的助手。你可以使用以下工具：

{tools}

请使用以下格式：

Question: 用户的问题
Thought: 你的思考过程
Action: 要采取的行动，应该是 [{tool_names}] 之一
Action Input: 行动的输入
Observation: 行动的结果
... (重复 Thought/Action/Observation N 次)
Thought: 我有足够的信息回答
Answer: 最终答案

开始!

Question: {input}
Thought: {agent_scratchpad}
"""
    
    prompt = ChatPromptTemplate.from_template(system_prompt)
    
    # 创建 agent
    agent = (
        prompt 
        | llm 
        | StrOutputParser()
    )
    
    print("可用工具:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # 测试
    test_questions = [
        "现在几点了？",
        "计算 123 * 456",
        "南京天气怎么样？",
    ]
    
    print("\n测试问题:")
    for q in test_questions:
        print(f"\nQ: {q}")
        # 简单处理，实际应使用 AgentExecutor
        response = agent.invoke({
            "tools": str(tools),
            "tool_names": ", ".join([t.name for t in tools]),
            "input": q,
            "agent_scratchpad": ""
        })
        print(f"A: {response[:200]}...")


def manual_agent_loop():
    """手动 Agent 循环"""
    print("\n" + "=" * 60)
    print("手动 Agent 循环 - ReAct 模式")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    tools = {
        "get_current_time": get_current_time,
        "calculate": calculate,
        "get_weather": get_weather,
    }
    
    def run_agent(question: str, max_iterations: int = 5):
        """运行 Agent 循环"""
        messages = [
            ("system", """你是一个智能助手。你可以使用工具回答问题。
            
可用工具：
- get_current_time: 获取当前时间
- calculate: 计算数学表达式
- get_weather: 获取天气信息

请按以下格式：
Thought: 思考
Action: 工具名
Action Input: 工具输入
Observation: 工具输出
... (可重复)
Thought: 我有答案了
Answer: 最终答案"""),
            ("human", question)
        ]
        
        print(f"\n问题：{question}")
        print("-" * 60)
        
        for i in range(max_iterations):
            # 调用 LLM
            response = llm.invoke(messages)
            content = response.content
            
            print(f"Iteration {i+1}:")
            print(content[:300])
            
            # 检查是否有最终答案
            if "Answer:" in content or "最终答案" in content:
                break
            
            # 解析工具调用 (简化版)
            if "Action:" in content:
                action_line = [l for l in content.split('\n') if 'Action:' in l][0]
                action = action_line.split('Action:')[1].strip()
                
                if action in tools:
                    # 执行工具
                    observation = tools[action].invoke({})
                    messages.append(("assistant", content))
                    messages.append(("user", f"Observation: {observation}"))
                else:
                    messages.append(("assistant", content))
                    messages.append(("user", "未知工具，请重试"))
            else:
                messages.append(("assistant", content))
                break
        
        return response.content
    
    # 测试
    questions = [
        "现在几点了？",
        "计算 100 + 200",
    ]
    
    for q in questions:
        run_agent(q)


def agent_with_memory():
    """带记忆的 Agent"""
    print("\n" + "=" * 60)
    print("带记忆的 Agent")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 对话历史
    history = []
    
    def chat_with_memory(user_input: str):
        history.append(f"用户：{user_input}")
        
        # 构建包含历史的 prompt
        context = "\n".join(history[-10:])  # 保留最近 10 条
        
        prompt = f"""对话历史：
{context}

助手："""
        
        response = llm.invoke([("human", prompt)])
        
        history.append(f"助手：{response.content}")
        
        return response.content
    
    # 多轮对话测试
    print("多轮对话测试:\n")
    
    conversations = [
        "我叫小明。",
        "我喜欢什么？",  # 测试记忆
        "今天天气不错。",
        "刚才说了什么？",  # 测试记忆
    ]
    
    for msg in conversations:
        response = chat_with_memory(msg)
        print(f"用户：{msg}")
        print(f"助手：{response.content[:100]}...\n")


if __name__ == "__main__":
    print("\n🦙 Ollama Agent - 中级示例\n")
    
    create_simple_agent()
    manual_agent_loop()
    agent_with_memory()
    
    print("\n✅ Ollama Agent 示例完成！")
    print("\n💡 提示：生产环境建议使用完整的 AgentExecutor 框架。")
