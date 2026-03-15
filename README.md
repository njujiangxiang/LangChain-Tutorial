# 🦜️🔗 LangChain 系统学习教程

> 从入门到精通的完整 LangChain 开发学习路径

---

## 📚 课程目录

```
LangChain-Tutorial/
├── 00-setup/              # 环境配置与基础
├── 01-core-concepts/      # 核心概念
├── 02-models/             # 模型集成
├── 03-prompts/            # 提示工程
├── 04-chains/             # 链式调用
├── 05-agents/             # 智能体
├── 06-memory/             # 记忆系统
├── 07-retrieval/          # 检索增强 (RAG)
├── 08-vector-stores/      # 向量数据库
├── 09-output-parsers/     # 输出解析
├── 10-real-world/         # 实战项目
└── resources/             # 学习资源
```

---

## 🎯 学习路径

### 阶段 1: 基础入门 (1-2 周)
- ✅ 环境配置
- ✅ 核心概念理解
- ✅ 模型调用
- ✅ 提示工程基础

### 阶段 2: 核心技能 (2-3 周)
- ✅ 链式调用
- ✅ 记忆系统
- ✅ 输出解析
- ✅ 基础 Agents

### 阶段 3: 高级应用 (3-4 周)
- ✅ RAG 检索增强
- ✅ 向量数据库
- ✅ 复杂 Agents
- ✅ 实战项目

### 阶段 4: 精通实践 (持续)
- ✅ 生产部署
- ✅ 性能优化
- ✅ 最佳实践
- ✅ 社区贡献

---

## 📖 每个主题包含

```
主题文件夹/
├── README.md          # 主题介绍与学习目标
├── theory/            # 理论知识
│   └── concepts.md    # 核心概念讲解
├── examples/          # 示例代码
│   ├── basic/         # 基础示例
│   ├── intermediate/  # 中级示例
│   └── advanced/      # 高级示例
├── exercises/         # 练习题
│   └── practice.py    # 实践代码
└── resources/         # 扩展资源
    └── links.md       # 相关链接
```

---

## 🚀 快速开始

### 1. 环境要求

```bash
Python 3.10+
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

### 3. 开始学习

```bash
# 从基础开始
cd 00-setup
python setup.py

# 逐步学习每个主题
cd ../01-core-concepts
python examples/basic/llm_call.py
```

---

## 📋 课程大纲详情

### 00-setup - 环境配置
- Python 环境设置
- LangChain 安装
- API 密钥配置
- 开发工具配置

### 01-core-concepts - 核心概念
- LLM 基础
- Token 理解
- LangChain 架构
- 基本组件

### 02-models - 模型集成
- OpenAI 模型
- Anthropic Claude
- 本地模型
- 模型切换

### 03-prompts - 提示工程
- Prompt 模板
- Few-shot 学习
- 提示优化技巧
- 系统提示设计

### 04-chains - 链式调用
- LLMChain
- SequentialChain
- TransformChain
- 自定义链

### 05-agents - 智能体
- Agent 基础
- Tool 使用
- ReAct 模式
- 自定义 Agent

### 06-memory - 记忆系统
- ConversationBuffer
- ConversationSummary
- VectorStore 记忆
- 自定义记忆

### 07-retrieval - 检索增强
- Document 加载
- Text 分割
- Embedding
- 检索策略

### 08-vector-stores - 向量数据库
- FAISS
- ChromaDB
- Pinecone
- 向量优化

### 09-output-parsers - 输出解析
- 结构化输出
- Pydantic 解析
- JSON 解析
- 错误处理

### 10-real-world - 实战项目
- 智能客服
- 文档问答
- 代码助手
- 数据分析

---

## 💡 学习建议

1. **循序渐进**: 按顺序学习每个主题
2. **动手实践**: 运行并修改示例代码
3. **完成练习**: 每个主题都有练习题
4. **记录笔记**: 在笔记文件夹记录心得
5. **参与社区**: 加入 LangChain 社区讨论

---

## 🔗 相关资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangChain 中文社区](https://www.langchain.com.cn/)
- [LangChain 教程](https://python.langchain.com/docs/tutorials/)

---

## 📝 学习进度追踪

| 主题 | 状态 | 完成日期 | 笔记 |
|------|------|----------|------|
| 00-setup | ⬜ | - | - |
| 01-core-concepts | ⬜ | - | - |
| 02-models | ⬜ | - | - |
| 03-prompts | ⬜ | - | - |
| 04-chains | ⬜ | - | - |
| 05-agents | ⬜ | - | - |
| 06-memory | ⬜ | - | - |
| 07-retrieval | ⬜ | - | - |
| 08-vector-stores | ⬜ | - | - |
| 09-output-parsers | ⬜ | - | - |
| 10-real-world | ⬜ | - | - |

---

**祝你学习愉快！🎉**

如有问题，欢迎在 Issues 中提问。
