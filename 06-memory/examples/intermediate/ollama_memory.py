"""
示例：Ollama 记忆系统 - 中级

演示使用 Ollama 模型实现对话记忆功能
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()


def buffer_memory_example():
    """对话缓冲记忆示例"""
    print("=" * 60)
    print("对话缓冲记忆 (Buffer Memory)")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 简单记忆 - 保存所有历史
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )
    
    # 模拟对话
    conversations = [
        ("你好，我叫小明。", "你好小明！很高兴认识你。"),
        ("我今年 25 岁。", "好的，我记住了你今年 25 岁。"),
        ("我喜欢编程。", "编程很有趣！你主要用什么语言？"),
    ]
    
    print("存储对话历史:\n")
    for user_msg, ai_msg in conversations:
        memory.save_context({"input": user_msg}, {"output": ai_msg})
        print(f"用户：{user_msg}")
        print(f"助手：{ai_msg}\n")
    
    # 获取历史
    history = memory.load_memory_variables({})
    print(f"记忆中的对话轮数：{len(history['chat_history']) // 2}")
    
    # 使用历史进行新对话
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个友好的助手。记住用户的信息。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    # 测试记忆
    print("\n测试记忆:")
    result = chain.invoke({
        "chat_history": history["chat_history"],
        "input": "我叫什么？"
    })
    print(f"Q: 我叫什么？\nA: {result}")


def summary_memory_example():
    """对话摘要记忆示例"""
    print("\n" + "=" * 60)
    print("对话摘要记忆 (Summary Memory)")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 摘要记忆 - 自动总结对话
    memory = ConversationSummaryMemory(
        llm=llm,
        return_messages=True,
        memory_key="summary"
    )
    
    # 模拟长对话
    print("进行多轮对话并自动摘要:\n")
    
    topics = [
        "我想学习 Python 编程。",
        "Python 可以用来做什么？",
        "如何开始学习？",
        "有什么推荐的资源吗？",
        "学习 Python 需要多长时间？",
    ]
    
    for topic in topics:
        memory.save_context({"input": topic}, {"output": "助手给出了建议。"})
        print(f"  - {topic}")
    
    # 获取摘要
    summary = memory.load_memory_variables({})
    print(f"\n对话摘要:\n{summary['summary'][:300]}...")


def custom_memory_example():
    """自定义记忆示例"""
    print("\n" + "=" * 60)
    print("自定义记忆 - 带用户信息")
    print("=" * 60)
    
    class UserProfileMemory:
        """用户画像记忆"""
        
        def __init__(self):
            self.profile = {
                "name": None,
                "age": None,
                "interests": [],
                "preferences": {},
            }
            self.history = []
        
        def extract_info(self, text: str):
            """从对话中提取用户信息"""
            # 简单规则提取 (实际可用 LLM)
            if "我叫" in text:
                name = text.split("我叫")[1].split("。")[0]
                self.profile["name"] = name
            if "岁" in text and "今年" in text:
                age = text.split("今年")[1].split("岁")[0]
                self.profile["age"] = age
            if "喜欢" in text:
                interest = text.split("喜欢")[1].split("。")[0]
                if interest not in self.profile["interests"]:
                    self.profile["interests"].append(interest)
        
        def add_message(self, role: str, content: str):
            """添加消息"""
            self.history.append({"role": role, "content": content})
            if role == "user":
                self.extract_info(content)
        
        def get_profile(self) -> dict:
            """获取用户画像"""
            return self.profile
        
        def get_context(self) -> str:
            """获取对话上下文"""
            return "\n".join([
                f"{m['role']}: {m['content']}" 
                for m in self.history[-10:]
            ])
    
    # 测试
    memory = UserProfileMemory()
    
    messages = [
        ("user", "你好，我叫小明。"),
        ("assistant", "你好小明！很高兴认识你。"),
        ("user", "我今年 25 岁。"),
        ("assistant", "好的，25 岁是很好的年纪。"),
        ("user", "我喜欢编程和音乐。"),
        ("assistant", "编程和音乐都是很棒爱好！"),
    ]
    
    print("记录用户信息:\n")
    for role, content in messages:
        memory.add_message(role, content)
        print(f"{role}: {content}")
    
    profile = memory.get_profile()
    print(f"\n用户画像:")
    print(f"  姓名：{profile['name']}")
    print(f"  年龄：{profile['age']}")
    print(f"  兴趣：{', '.join(profile['interests'])}")


def memory_with_context():
    """带上下文的记忆对话"""
    print("\n" + "=" * 60)
    print("带上下文的记忆对话")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 对话历史
    history = []
    
    def chat(user_input: str):
        history.append(HumanMessage(content=user_input))
        
        # 构建 prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="你是有帮助的助手。记住之前的对话。"),
        ] + history[-8:])  # 保留最近 8 条消息
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({})
        
        history.append(AIMessage(content=response))
        
        return response
    
    # 多轮对话测试
    print("多轮对话测试:\n")
    
    questions = [
        "我想买一台笔记本电脑，预算 5000 元。",
        "主要用来办公和看电影。",  # 上下文相关
        "有什么推荐的吗？",  # 上下文相关
        "电池续航重要吗？",  # 上下文相关
    ]
    
    for q in questions:
        print(f"用户：{q}")
        response = chat(q)
        print(f"助手：{response[:150]}...\n")


def save_load_memory():
    """记忆的保存与加载"""
    print("\n" + "=" * 60)
    print("记忆的保存与加载")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 对话历史
    history = [
        {"role": "user", "content": "我叫小红。"},
        {"role": "assistant", "content": "你好小红！"},
        {"role": "user", "content": "我喜欢画画。"},
        {"role": "assistant", "content": "画画是很棒的爱好！"},
    ]
    
    # 保存到文件
    filepath = "./memory_export.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "history": history,
        }, f, ensure_ascii=False, indent=2)
    
    print(f"记忆已保存到：{filepath}")
    
    # 从文件加载
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n加载的记忆:")
    print(f"  时间：{data['timestamp']}")
    print(f"  对话轮数：{len(data['history']) // 2}")
    
    # 使用加载的记忆继续对话
    messages = [SystemMessage(content="记住之前的对话。")]
    for msg in data["history"]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    
    messages.append(HumanMessage(content="我叫什么？我喜欢什么？"))
    
    response = llm.invoke(messages)
    print(f"\n测试记忆：{response.content}")


if __name__ == "__main__":
    print("\n🦙 Ollama 记忆系统 - 中级示例\n")
    
    buffer_memory_example()
    summary_memory_example()
    custom_memory_example()
    memory_with_context()
    save_load_memory()
    
    print("\n✅ Ollama 记忆示例完成！")
