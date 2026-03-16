# 06-Memory 项目实战 - 个人对话助手

## 📋 项目概述

构建一个带长期记忆的个人对话助手，能够记住用户信息、偏好和对话历史。

### 项目目标
- 掌握 LangChain 记忆系统的使用
- 学会实现对话历史管理
- 理解不同记忆类型的适用场景

### 功能特性
- ✅ 对话历史记忆
- ✅ 用户信息存储
- ✅ 长期记忆检索
- ✅ 上下文感知对话
- ✅ 记忆持久化

---

## 🚀 快速开始

```bash
cd 06-memory/project
pip install -r requirements.txt
python examples/assistant.py
```

---

## 💡 记忆类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| ConversationBuffer | 完整对话历史 | 短对话 |
| ConversationSummary | 摘要式记忆 | 长对话 |
| VectorStore | 向量检索记忆 | 大规模记忆 |
| Entity Memory | 实体信息记忆 | 知识图谱 |

---

## 📁 项目结构

```
project/
├── src/
│   ├── memory.py         # 记忆管理
│   ├── assistant.py      # 对话助手
│   └── storage.py        # 持久化存储
└── examples/
    └── assistant.py      # 演示
```

---

**打造你的专属 AI 助手！🧠**
