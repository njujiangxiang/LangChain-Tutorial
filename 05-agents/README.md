# 05-Agents - 智能体

> 让 LLM 能够使用工具、执行任务、自主决策

---

## 🎯 学习目标

- ✅ 理解 Agent 的工作原理
- ✅ 掌握 Tool 的使用
- ✅ 学会 ReAct 模式
- ✅ 能够创建自定义 Agent

---

## 📚 核心概念

### 什么是 Agent？

Agent = LLM + 工具 + 记忆 + 规划

```
┌─────────────┐
│    Agent    │
├─────────────┤
│   LLM Core  │
├─────────────┤
│   Tools     │ → 搜索、计算、API 调用...
├─────────────┤
│   Memory    │ → 对话历史、上下文
├─────────────┤
│   Planning  │ → 任务分解、决策
└─────────────┘
```

### ReAct 模式

**Reason + Act**

1. **Thought**: 思考下一步做什么
2. **Action**: 执行动作（使用工具）
3. **Observation**: 观察结果
4. 重复直到完成任务

---

## 💻 示例代码

### 示例 1: 基础 Agent

```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import Tool

# 定义工具
tools = [
    Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),
        description="用于数学计算"
    ),
    Tool(
        name="Search",
        func=lambda x: f"搜索结果：{x}",
        description="用于搜索信息"
    )
]

# 创建 Agent
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# 执行
result = agent_executor.invoke({"input": "计算 123 * 456"})
print(result["output"])
```

---

## 📝 练习

1. 创建一个带计算器的 Agent
2. 添加自定义工具
3. 实现多步骤任务处理

---

**继续学习：[06-Memory](../06-memory/README.md)** 🚀
