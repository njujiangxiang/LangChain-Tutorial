"""
示例：Ollama 高级记忆系统

演示复杂的记忆管理和优化技巧
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
    VectorStoreRetrieverMemory,
)
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import List, Dict

load_dotenv()


def sliding_window_memory():
    """滑动窗口记忆 - 保留最近 N 轮"""
    print("=" * 60)
    print("滑动窗口记忆 (Sliding Window)")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 只保留最近 5 轮对话
    memory = ConversationBufferWindowMemory(
        k=5,
        return_messages=True,
        memory_key="chat_history"
    )
    
    print("滑动窗口记忆：保留最近 5 轮对话\n")
    
    # 模拟多轮对话
    for i in range(8):
        user_msg = f"这是第{i+1}条消息"
        ai_msg = f"我记住了第{i+1}条消息"
        
        memory.save_context({"input": user_msg}, {"output": ai_msg})
        
        history = memory.load_memory_variables({})
        msg_count = len(history["chat_history"]) // 2
        
        print(f"第{i+1}轮 - 记忆中的对话数：{msg_count}")
    
    print(f"\n最终记忆：保留最近 5 轮")


def entity_memory():
    """实体记忆 - 记住关键信息"""
    print("\n" + "=" * 60)
    print("实体记忆 - 提取和存储关键信息")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 实体提取 prompt
    extract_prompt = ChatPromptTemplate.from_template("""
    从对话中提取用户信息：
    
    对话：{conversation}
    
    提取以下实体:
    - 姓名
    - 年龄
    - 城市
    - 兴趣爱好
    - 职业
    
    返回 JSON 格式。
    """)
    
    extract_chain = extract_prompt | llm | StrOutputParser()
    
    # 对话历史
    conversations = [
        "你好，我叫小明。",
        "我今年 25 岁。",
        "我住在南京。",
        "我喜欢编程和音乐。",
        "我是一名软件工程师。",
    ]
    
    print("从对话中提取实体:\n")
    
    full_conversation = "\n".join(conversations)
    
    entities = extract_chain.invoke({"conversation": full_conversation})
    
    print("提取的实体信息:")
    print(entities)


def hierarchical_memory():
    """分层记忆 - 短期 + 长期"""
    print("\n" + "=" * 60)
    print("分层记忆系统")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    class HierarchicalMemory:
        def __init__(self):
            self.short_term = []  # 短期记忆 (最近 10 轮)
            self.long_term = {}   # 长期记忆 (关键信息)
            self.summary = ""     # 对话摘要
        
        def add_message(self, role: str, content: str):
            """添加消息"""
            self.short_term.append({"role": role, "content": content})
            
            # 保持短期记忆大小
            if len(self.short_term) > 20:
                self.short_term = self.short_term[-20:]
        
        def extract_long_term(self, text: str):
            """提取长期记忆"""
            # 简单规则提取
            if "我叫" in text:
                name = text.split("我叫")[1].split("。")[0]
                self.long_term["name"] = name
            if "喜欢" in text:
                interest = text.split("喜欢")[1].split("。")[0]
                if "interests" not in self.long_term:
                    self.long_term["interests"] = []
                self.long_term["interests"].append(interest)
        
        def get_context(self, user_input: str) -> str:
            """获取完整上下文"""
            context_parts = []
            
            # 长期记忆
            if self.long_term:
                context_parts.append(f"用户信息：{json.dumps(self.long_term, ensure_ascii=False)}")
            
            # 短期记忆 (最近 10 轮)
            if self.short_term:
                history = "\n".join([
                    f"{m['role']}: {m['content']}"
                    for m in self.short_term[-10:]
                ])
                context_parts.append(f"对话历史:\n{history}")
            
            return "\n\n".join(context_parts)
    
    # 测试
    mem = HierarchicalMemory()
    
    print("分层记忆测试:\n")
    
    messages = [
        ("user", "你好，我叫小明。"),
        ("assistant", "你好小明！很高兴认识你。"),
        ("user", "我喜欢编程和音乐。"),
        ("assistant", "编程和音乐都是很好的爱好！"),
        ("user", "我是一名软件工程师。"),
        ("assistant", "软件工程师是很棒的职业！"),
    ]
    
    for role, content in messages:
        mem.add_message(role, content)
        mem.extract_long_term(content)
        print(f"{role}: {content}")
    
    print(f"\n长期记忆：{json.dumps(mem.long_term, ensure_ascii=False, indent=2)}")
    print(f"\n短期记忆：{len(mem.short_term)} 条消息")


def memory_compression():
    """记忆压缩 - 摘要压缩"""
    print("\n" + "=" * 60)
    print("记忆压缩 - 对话摘要")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 摘要 prompt
    summary_prompt = ChatPromptTemplate.from_template("""
    将以下对话压缩成简洁的摘要：
    
    {conversation}
    
    摘要要求:
    1. 保留关键信息
    2. 简洁明了
    3. 50 字以内
    """)
    
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    # 长对话
    long_conversation = """
    用户：我想学习编程，有什么建议？
    助手：建议从 Python 开始，它语法简单，适合初学者。
    用户：Python 可以用来做什么？
    助手：Web 开发、数据分析、人工智能、自动化脚本等。
    用户：学习 Python 需要多长时间？
    助手：基础语法 2-4 周，熟练掌握 3-6 个月。
    用户：有什么好的学习资源？
    助手：推荐《Python 编程：从入门到实践》、Codecademy、Coursera 等。
    用户：需要安装什么工具？
    助手：Python 解释器、VS Code 或 PyCharm 编辑器。
    """
    
    print(f"原始对话长度：{len(long_conversation)} 字符\n")
    
    # 压缩
    summary = summary_chain.invoke({"conversation": long_conversation})
    
    print(f"压缩后摘要:\n{summary}")
    print(f"\n摘要长度：{len(summary)} 字符")
    print(f"压缩率：{(1 - len(summary)/len(long_conversation))*100:.1f}%")


def memory_persistence():
    """记忆持久化 - 保存和加载"""
    print("\n" + "=" * 60)
    print("记忆持久化 - 保存到文件")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 对话记忆
    memory_data = {
        "timestamp": datetime.now().isoformat(),
        "user_profile": {
            "name": "小明",
            "age": 25,
            "location": "南京",
        },
        "conversation_history": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么可以帮助你的？"},
            {"role": "user", "content": "推荐一个周末活动"},
            {"role": "assistant", "content": "可以去中山陵散步，或者参观南京博物院。"},
        ],
        "preferences": {
            "cuisine": "中餐",
            "activities": ["阅读", "运动"],
        }
    }
    
    # 保存到文件
    filepath = "./memory_export.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)
    
    print(f"记忆已保存到：{filepath}")
    
    # 从文件加载
    with open(filepath, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    
    print(f"\n加载的记忆:")
    print(f"  时间：{loaded['timestamp']}")
    print(f"  用户：{loaded['user_profile']['name']}")
    print(f"  对话：{len(loaded['conversation_history'])} 条")
    print(f"  偏好：{loaded['preferences']}")


if __name__ == "__main__":
    print("\n🦙 Ollama 高级记忆系统示例\n")
    
    sliding_window_memory()
    entity_memory()
    hierarchical_memory()
    memory_compression()
    memory_persistence()
    
    print("\n✅ Ollama 高级记忆示例完成！")
