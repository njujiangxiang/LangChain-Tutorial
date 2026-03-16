# 05-Agents 项目实战 - 智能研究助手

## 📋 项目概述

构建一个智能研究助手，能够自主搜索信息、整理资料、生成报告。

### 项目目标
- 掌握 LangChain Agent 的设计和使用
- 学会为 Agent 添加工具能力
- 理解 ReAct 模式和自主决策

### 功能特性
- ✅ 自主搜索信息
- ✅ 多源信息整合
- ✅ 智能总结报告
- ✅ 工具调用能力
- ✅ 对话式交互

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd 05-agents/project
pip install -r requirements.txt
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 配置模型
```

### 3. 运行演示

```bash
# 交互式对话
python examples/chat.py

# 生成研究报告
python examples/research.py --topic "人工智能发展"
```

---

## 📁 项目结构

```
project/
├── README.md
├── requirements.txt
├── src/
│   ├── agent.py          # Agent 核心
│   ├── tools.py          # 工具定义
│   └── report.py         # 报告生成
├── tests/
│   └── test_agent.py
└── examples/
    ├── chat.py           # 对话演示
    └── research.py       # 研究演示
```

---

## 💡 核心功能

### 1. 智能对话

```python
from src.agent import ResearchAgent

agent = ResearchAgent()

# 对话
response = agent.chat("帮我研究一下量子计算的最新进展")
print(response)
```

### 2. 研究报告

```python
# 生成完整报告
report = agent.generate_report(
    topic="人工智能",
    sections=["概述", "技术", "应用", "趋势"]
)
report.save("ai_report.md")
```

---

## 🔧 可扩展工具

- 网页搜索
- 文档检索
- 代码执行
- API 调用
- 数据库查询

---

**开始你的智能助手之旅！🚀**
