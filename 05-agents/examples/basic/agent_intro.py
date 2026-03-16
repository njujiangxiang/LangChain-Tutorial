"""
示例：Agent 基础入门

演示 LangChain Agent 的基本概念和用法
"""

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取 LLM 实例"""
    if os.getenv('ANTHROPIC_API_KEY'):
        return ChatAnthropic(model="claude-3-sonnet-20240229")
    return ChatOllama(model="qwen3.5:9b")


# 定义工具
@tool
def add(a: int, b: int) -> int:
    """两个数相加"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """两个数相乘"""
    return a * b


@tool
def get_weather(city: str) -> str:
    """获取城市天气 (模拟)"""
    weather_data = {
        "北京": "晴，25°C",
        "上海": "多云，28°C",
        "广州": "小雨，30°C",
        "深圳": "晴，32°C"
    }
    return weather_data.get(city, f"{city}天气未知")


def test_tools():
    """测试工具定义"""
    print("=" * 60)
    print("工具 (Tools) 基础")
    print("=" * 60)
    
    tools = [add, multiply, get_weather]
    
    print(f"定义的工具数量：{len(tools)}")
    print("\n工具列表:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # 测试工具调用
    print("\n测试工具调用:")
    print(f"  add(5, 3) = {add.invoke({'a': 5, 'b': 3})}")
    print(f"  multiply(4, 7) = {multiply.invoke({'a': 4, 'b': 7})}")
    print(f"  get_weather('北京') = {get_weather.invoke({'city': '北京'})}")


def test_react_agent():
    """测试 ReAct Agent"""
    print("\n" + "=" * 60)
    print("ReAct Agent")
    print("=" * 60)
    
    llm = get_llm()
    tools = [add, multiply, get_weather]
    
    # 检查是否支持 Agent
    try:
        from langchain.agents import create_tool_calling_agent, AgentExecutor
        
        # 创建提示
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个有帮助的助手，可以使用工具回答问题。"),
            ("human", "{input}"),
        ])
        
        # 创建 Agent
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        # 测试
        print("\n测试 1 - 使用计算工具:")
        result = agent_executor.invoke({"input": "5 加 3 等于多少？"})
        print(f"结果：{result['output']}")
        
        print("\n测试 2 - 使用天气工具:")
        result = agent_executor.invoke({"input": "北京天气怎么样？"})
        print(f"结果：{result['output']}")
        
    except ImportError as e:
        print(f"需要安装：pip install langchain-agents")
        print(f"错误：{e}")
        
        # 演示模式
        print("\n演示：ReAct Agent 工作流程")
        print("""
        1. 思考 (Thought): 我需要使用工具来回答这个问题
        2. 行动 (Action): 调用 get_weather 工具
        3. 观察 (Observation): 北京：晴，25°C
        4. 回答 (Answer): 北京今天晴朗，温度 25 度
        """)


def test_custom_tool():
    """测试自定义工具"""
    print("\n" + "=" * 60)
    print("自定义工具")
    print("=" * 60)
    
    from langchain_core.tools import BaseTool
    
    class CalculatorTool(BaseTool):
        """自定义计算器工具"""
        name: str = "calculator"
        description: str = "执行数学计算"
        
        def _run(self, expression: str) -> str:
            """执行计算"""
            try:
                # 简单实现，实际使用需要更安全的解析
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"计算错误：{e}"
    
    calc = CalculatorTool()
    
    print(f"工具名称：{calc.name}")
    print(f"工具描述：{calc.description}")
    
    # 测试
    result = calc.invoke({"expression": "10 + 20 * 3"})
    print(f"\n计算 10 + 20 * 3 = {result}")


def agent_use_cases():
    """Agent 使用场景"""
    print("\n" + "=" * 60)
    print("Agent 使用场景")
    print("=" * 60)
    
    print("""
    💡 Agent 适用场景:
    
    1. 需要多步推理的任务:
       - 复杂问题分解
       - 多轮对话
       - 任务规划
    
    2. 需要外部工具的任务:
       - 搜索网络信息
       - 调用 API
       - 数据库查询
       - 文件操作
    
    3. 需要动态决策的任务:
       - 根据情况选择不同策略
       - 错误恢复
       - 自适应流程
    
    4. 自动化工作流:
       - 数据处理流水线
       - 报告生成
       - 客户服务
    
    📋 常见 Agent 类型:
    - ReAct Agent: 思考 - 行动 - 观察循环
    - Tool Calling Agent: 直接调用工具
    - Plan-and-Execute: 先规划后执行
    - Self-Reflective: 自我反思改进
    """)


if __name__ == "__main__":
    print("\n🤖 Agent 基础入门示例\n")
    
    test_tools()
    test_react_agent()
    test_custom_tool()
    agent_use_cases()
    
    print("\n✅ 所有测试完成！")
