# 🦜️🔗 LangChain 系统学习教程

> 从入门到精通的完整 LangChain 开发学习路径  
> **最后更新**: 2026-03-16  
> **特色**: ✅ Ollama 本地模型 (qwen3.5:9b) | ✅ 阿里云百炼 | ✅ 35+ 示例代码 | ✅ 项目实战

---

## 📊 教程状态

| 类别 | 数量 | 状态 |
|------|------|------|
| 示例代码文件 | 35+ | ✅ |
| Ollama 专项示例 | 10+ | ✅ |
| 阿里云专项示例 | 6+ | ✅ |
| 项目实战 | 1 | ✅ |
| 覆盖章节 | 9/10 | 🔄 |

---

## 📚 课程目录

```
LangChain-Tutorial/
├── 00-setup/              # 环境配置与基础
├── 01-core-concepts/      # 核心概念 (5 个示例)
├── 02-models/             # 模型集成 (9 个示例) ⭐
├── 03-prompts/            # 提示工程 (7 个示例 + 项目) ⭐
├── 04-chains/             # 链式调用 (2 个示例)
├── 05-agents/             # 智能体 (2 个示例)
├── 06-memory/             # 记忆系统 (2 个示例)
├── 07-retrieval/          # 检索增强 RAG (2 个示例)
├── 08-vector-stores/      # 向量数据库 (1 个示例)
├── 09-output-parsers/     # 输出解析 (1 个示例)
├── 10-real-world/         # 实战项目 (待创建)
├── resources/             # 学习资源
├── COMPLETION_REPORT.md   # 完成报告
└── README.md              # 本文件
```

---

## 🎯 学习路径

### 阶段 1: 基础入门 (1-2 周) ✅
- ✅ 环境配置 (00-setup)
- ✅ 核心概念理解 (01-core-concepts)
- ✅ 模型调用 (02-models) - **含 Ollama/阿里云**
- ✅ 提示工程基础 (03-prompts)

### 阶段 2: 核心技能 (2-3 周) ✅
- ✅ 链式调用 (04-chains)
- ✅ 记忆系统 (06-memory)
- ✅ 输出解析 (09-output-parsers)
- ✅ 基础 Agents (05-agents)

### 阶段 3: 高级应用 (3-4 周) 🔄
- 🔄 RAG 检索增强 (07-retrieval)
- 🔄 向量数据库 (08-vector-stores)
- 🔄 复杂 Agents
- ✅ 实战项目 (03-prompts/project)

### 阶段 4: 精通实践 (持续) 🔄
- 🔄 生产部署
- 🔄 性能优化
- 🔄 最佳实践
- 🔄 社区贡献

---

## 📖 每个主题包含

```
主题文件夹/
├── README.md              # 主题介绍与学习目标
├── examples/              # 示例代码
│   ├── basic/             # 基础示例 ✅
│   ├── intermediate/      # 中级示例 ✅
│   └── advanced/          # 高级示例 ✅
├── project/               # 项目实战 (部分章节) ✅
│   ├── README.md
│   ├── src/
│   ├── tests/
│   └── examples/
├── exercises/             # 练习题
└── resources/             # 扩展资源
```

---

## 🚀 快速开始

### 1. 环境要求

```bash
Python 3.10+
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# Ollama (本地，无需 API Key)
OLLAMA_HOST=localhost:11434

# 阿里云百炼 (可选)
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 安装 Ollama (推荐)

```bash
# macOS
brew install ollama

# 下载模型
ollama pull qwen3.5:9b

# 启动服务
ollama serve

# 验证
ollama list
```

### 4. 开始学习

```bash
# 基础示例
python 02-models/examples/basic/ollama_basic.py

# 中级示例
python 02-models/examples/intermediate/ollama_intermediate.py

# 高级示例
python 02-models/examples/advanced/ollama_advanced.py

# 阿里云示例 (需配置 API Key)
python 02-models/examples/basic/aliyun_basic.py
```

---

## 📋 课程大纲详情

### ✅ 00-setup - 环境配置
- [x] Python 环境设置
- [x] LangChain 安装
- [x] API 密钥配置
- [x] 开发工具配置
- [x] 环境验证脚本

### ✅ 01-core-concepts - 核心概念
- [x] LLM 基础
- [x] Token 理解
- [x] LangChain 架构
- [x] 基本组件
- **示例**: `langchain_components.py`, `ollama_basic.py`, `chaining_patterns.py`

### ✅ 02-models - 模型集成 ⭐ 最完整
- [x] OpenAI 模型
- [x] Anthropic Claude
- [x] **Ollama 本地模型** (qwen3.5:9b)
- [x] **阿里云百炼**
- [x] 模型切换与比较
- **示例**: 9 个完整示例 (基础/中级/高级)
  - `ollama_basic.py` - Ollama 基础调用
  - `ollama_intermediate.py` - 高级配置与优化
  - `ollama_advanced.py` - 生产级应用
  - `aliyun_basic.py` - 阿里云基础
  - `aliyun_intermediate.py` - 阿里云高级特性
  - `aliyun_advanced.py` - 阿里云生产实践

### ✅ 03-prompts - 提示工程 ⭐
- [x] Prompt 模板
- [x] Few-shot 学习
- [x] 提示优化技巧
- [x] 系统提示设计
- [x] **项目实战**: 提示词模板管理器
- **示例**: 7 个示例 + 完整项目

### ✅ 04-chains - 链式调用
- [x] LLMChain
- [x] SequentialChain
- [x] 并行链
- [x] 条件链
- **示例**: `llm_chain.py`, `ollama_chains.py`

### ✅ 05-agents - 智能体
- [x] Agent 基础
- [x] Tool 使用
- [x] ReAct 模式
- [x] 自定义 Agent
- **示例**: `agent_intro.py`, `ollama_agent.py`

### ✅ 06-memory - 记忆系统
- [x] ConversationBuffer
- [x] ConversationSummary
- [x] 自定义记忆
- [x] 记忆持久化
- **示例**: `conversation_memory.py`, `ollama_memory.py`

### ✅ 07-retrieval - 检索增强 (RAG)
- [x] Document 加载
- [x] Text 分割
- [x] Embedding
- [x] 检索策略
- [x] RAG 基础实现
- **示例**: `document_loading.py`, `ollama_retrieval.py`

### ✅ 08-vector-stores - 向量数据库
- [x] FAISS
- [x] ChromaDB
- [x] 向量优化
- **示例**: `vector_store_intro.py`

### ✅ 09-output-parsers - 输出解析
- [x] 结构化输出
- [x] Pydantic 解析
- [x] JSON 解析
- [x] 错误处理
- **示例**: `json_parser.py`

### 🔄 10-real-world - 实战项目 (待完善)
- [ ] 智能客服
- [ ] 文档问答
- [ ] 代码助手
- [ ] 数据分析

---

## 💡 特色功能

### 🦙 Ollama 本地模型支持
完整支持 Ollama 本地模型 (qwen3.5:9b)，无需 API Key 即可学习：
- ✅ 基础调用与配置
- ✅ 高级参数优化
- ✅ 缓存与性能优化
- ✅ 生产级应用模式

### ☁️ 阿里云百炼集成
完整支持阿里云百炼大模型：
- ✅ DashScope SDK
- ✅ OpenAI 兼容接口
- ✅ 多模型路由
- ✅ 成本优化实践

### 📁 项目实战
每个核心章节配备完整项目实战：
- 真实场景应用
- 完整代码结构
- 可独立运行
- 可扩展开发

---

## 💡 学习建议

1. **循序渐进**: 按顺序学习每个主题，不要跳级
2. **动手实践**: 运行并修改示例代码，不要只看
3. **完成练习**: 每个主题都有练习题，务必完成
4. **记录笔记**: 在 `notes/` 文件夹记录心得
5. **本地优先**: 开发测试优先使用 Ollama，节省成本
6. **参与社区**: 加入 LangChain 社区讨论

---

## 📝 学习进度追踪

| 主题 | 状态 | 示例数 | 完成日期 | 笔记 |
|------|------|--------|----------|------|
| 00-setup | ✅ | 1 | - | - |
| 01-core-concepts | ✅ | 5 | - | - |
| 02-models | ✅ | 9 | - | - |
| 03-prompts | ✅ | 7+ 项目 | - | - |
| 04-chains | ✅ | 2 | - | - |
| 05-agents | ✅ | 2 | - | - |
| 06-memory | ✅ | 2 | - | - |
| 07-retrieval | ✅ | 2 | - | - |
| 08-vector-stores | 🔄 | 1 | - | - |
| 09-output-parsers | 🔄 | 1 | - | - |
| 10-real-world | ⬜ | 0 | - | - |

**图例**: ✅ 已完成 | 🔄 进行中 | ⬜ 待开始

---

## 🔗 相关资源

### 官方文档
- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangChain 教程](https://python.langchain.com/docs/tutorials/)

### 中文资源
- [LangChain 中文社区](https://www.langchain.com.cn/)
- [LangChain 中文教程](https://liaokong.gitbook.io/llm-kai-fa-jiao-cheng)

### 模型服务
- [Ollama 官网](https://ollama.ai/)
- [阿里云百炼](https://help.aliyun.com/zh/dashscope/)
- [通义千问](https://tongyi.aliyun.com/)

### 学习社区
- [LangChain Discord](https://discord.gg/langchain)
- [LangChain 中文微信群](https://www.langchain.com.cn/)

---

## 📚 推荐学习顺序

### 第 1 周：环境搭建与基础
```
Day 1-2: 00-setup - 环境配置
Day 3-4: 01-core-concepts - 核心概念
Day 5-7: 02-models (基础) - 模型调用
```

### 第 2 周：模型与提示
```
Day 8-10: 02-models (中级/高级) - 深入模型
Day 11-14: 03-prompts - 提示工程 + 项目实战
```

### 第 3 周：链与记忆
```
Day 15-17: 04-chains - 链式调用
Day 18-21: 06-memory - 记忆系统
```

### 第 4 周：Agent 与 RAG
```
Day 22-24: 05-agents - 智能体
Day 25-28: 07-retrieval + 08-vector-stores - RAG
```

### 第 5 周+：进阶与实战
```
Day 29-31: 09-output-parsers - 输出解析
Day 32+: 10-real-world - 综合项目
```

---

## 🛠️ 常见问题

### Q: Ollama 无法启动？
```bash
# 检查安装
ollama --version

# 重新启动服务
ollama serve

# 查看日志
tail -f ~/.ollama/logs/server.log
```

### Q: 如何切换模型？
```python
# Ollama
llm = ChatOllama(model="qwen3.5:9b")  # 或 llama3:8b, mistral:7b 等

# 阿里云
llm = ChatOpenAI(
    model="qwen-plus",
    openai_api_key=api_key,
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```

### Q: 如何节省 API 成本？
1. 开发测试使用 Ollama 本地模型
2. 实现缓存机制，避免重复调用
3. 选择合适的模型 (简单任务用 qwen-turbo)
4. 设置合理的 max_tokens 限制

---

## 📄 许可证

本教程采用 MIT 许可证，欢迎 Fork 和贡献。

---

## 🙏 致谢

感谢 LangChain 社区、Ollama 团队、阿里云百炼提供的优秀工具和文档。

---

**祝你学习愉快！🎉**

如有问题，欢迎在 Issues 中提问或讨论。

**最后更新**: 2026-03-16  
**维护者**: 大龙虾 🦞
