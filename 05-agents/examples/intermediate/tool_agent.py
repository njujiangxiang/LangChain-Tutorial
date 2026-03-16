"""
示例：工具增强 Agent - 使用外部工具

演示如何为 Agent 添加工具使用能力，扩展其功能边界
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import tool, AgentExecutor, create_openai_tools_agent
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import Optional

load_dotenv()


# ==================== 自定义工具定义 ====================

@tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculate(expression: str) -> str:
    """计算数学表达式
    
    Args:
        expression: 数学表达式，如 "2+2" 或 "10*5"
    """
    try:
        # 安全计算
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"


@tool
def search_knowledge_base(query: str) -> str:
    """搜索知识库
    
    Args:
        query: 搜索关键词
    """
    # 模拟知识库
    knowledge = {
        "python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。",
        "langchain": "LangChain 是一个用于开发 LLM 应用的框架，提供链式调用、Agent 等功能。",
        "ollama": "Ollama 是一个本地运行大语言模型的工具，支持 Llama、Mistral 等模型。",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"未找到关于'{query}'的信息。可用主题：python, langchain, ollama"


@tool
def get_weather(city: str) -> str:
    """查询天气 (模拟)
    
    Args:
        city: 城市名称
    """
    # 模拟天气数据
    weather_data = {
        "北京": "晴，15-25°C，东北风 2 级",
        "上海": "多云，18-26°C，东南风 3 级",
        "广州": "小雨，22-28°C，南风 2 级",
        "深圳": "晴，24-30°C，西南风 1 级",
        "南京": "阴，16-24°C，东风 2 级",
    }
    
    return weather_data.get(city, f"暂无{city}的天气数据")


def create_agent_with_tools():
    """创建带工具的 Agent"""
    print("=" * 60)
    print("创建工具增强 Agent")
    print("=" * 60)
    
    # 可用工具列表
    tools = [
        get_current_time,
        calculate,
        search_knowledge_base,
        get_weather,
    ]
    
    print(f"可用工具 ({len(tools)} 个):")
    for t in tools:
        print(f"  - {t.name}: {t.description}")
    
    return tools


def manual_tool_execution():
    """手动工具执行示例"""
    print("\n" + "=" * 60)
    print("手动工具执行")
    print("=" * 60)
    
    tools = create_agent_with_tools()
    tool_dict = {t.name: t for t in tools}
    
    # 模拟 Agent 决策过程
    print("\n模拟对话:")
    
    # 用户问题
    user_query = "现在几点了？北京天气如何？"
    print(f"用户：{user_query}")
    
    # Agent 思考并调用工具
    print("\nAgent 思考：需要调用 get_current_time 和 get_weather 工具")
    
    # 调用时间工具
    time_result = tool_dict["get_current_time"].invoke({})
    print(f"工具 [get_current_time]: {time_result}")
    
    # 调用天气工具
    weather_result = tool_dict["get_weather"].invoke({"city": "北京"})
    print(f"工具 [get_weather]: {weather_result}")
    
    # 综合回答
    print(f"\nAgent: 现在是{time_result}。北京天气：{weather_result}")


def llm_with_tools():
    """LLM 决定工具调用"""
    print("\n" + "=" * 60)
    print("LLM 自主工具调用")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    tools = create_agent_with_tools()
    tool_dict = {t.name: t for t in tools}
    
    # 系统提示 - 告诉 LLM 可用工具
    system_prompt = """你是一个智能助手，可以使用以下工具：

可用工具:
1. get_current_time - 获取当前时间
2. calculate - 计算数学表达式
3. search_knowledge_base - 搜索知识库
4. get_weather - 查询天气

当用户问题时，如果需要工具帮助，请按格式回复:
[TOOL: 工具名] {"参数": "值"}

否则直接回答问题。
"""
    
    # 测试问题
    test_questions = [
        "123 乘以 456 等于多少？",
        "现在几点了？",
        "Python 是什么？",
        "上海天气怎么样？",
    ]
    
    for question in test_questions:
        print(f"\n用户：{question}")
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]
        
        response = llm.invoke(messages)
        print(f"Agent: {response.content[:200]}...")


def structured_tool_example():
    """结构化示例"""
    print("\n" + "=" * 60)
    print("结构化输入工具")
    print("=" * 60)
    
    # 带参数验证的工具
    def create_user_profile(name: str, age: int, city: str = "未知") -> str:
        """创建用户档案
        
        Args:
            name: 姓名
            age: 年龄 (必须>0)
            city: 城市 (可选)
        """
        if age <= 0:
            return "错误：年龄必须大于 0"
        
        profile = {
            "name": name,
            "age": age,
            "city": city,
            "created_at": datetime.now().isoformat()
        }
        
        return json.dumps(profile, ensure_ascii=False, indent=2)
    
    # 创建结构化工具
    profile_tool = StructuredTool.from_function(
        func=create_user_profile,
        name="create_user_profile",
        description="创建用户档案"
    )
    
    # 测试
    result = profile_tool.invoke({"name": "小明", "age": 25, "city": "北京"})
    print(f"用户档案：{result}")
    
    # 错误处理
    result = profile_tool.invoke({"name": "小红", "age": -1})
    print(f"错误处理：{result}")


if __name__ == "__main__":
    print("\n🤖 工具增强 Agent 示例\n")
    
    manual_tool_execution()
    llm_with_tools()
    structured_tool_example()
    
    print("\n✅ 工具 Agent 示例完成！")