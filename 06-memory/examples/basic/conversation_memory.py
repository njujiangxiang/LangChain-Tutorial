"""
示例：对话记忆基础

演示 LangChain 记忆系统的基本用法
"""

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取 LLM 实例"""
    if os.getenv('ANTHROPIC_API_KEY'):
        return ChatAnthropic(model="claude-3-sonnet-20240229")
    return ChatOllama(model="qwen3.5:9b")


def test_buffer_memory():
    """测试缓冲记忆"""
    print("=" * 60)
    print("缓冲记忆 (Buffer Memory)")
    print("=" * 60)
    
    llm = get_llm()
    
    from langchain.memory import ConversationBufferMemory
    
    # 创建记忆
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # 模拟对话
    conversations = [
        ("你好，我叫小明", "你好小明！很高兴认识你。"),
        ("我喜欢编程", "编程很有趣！你最喜欢什么语言？"),
        ("我喜欢 Python", "Python 是个很好的选择！"),
    ]
    
    print("存储对话历史:\n")
    for human, ai in conversations:
        memory.save_context({"input": human}, {"output": ai})
        print(f"用户：{human}")
        print(f"助手：{ai}\n")
    
    # 获取历史
    history = memory.load_memory_variables({})
    print(f"记忆中的消息数：{len(history['chat_history'])}")


def test_buffer_window_memory():
    """测试窗口记忆"""
    print("\n" + "=" * 60)
    print("窗口记忆 (Buffer Window Memory)")
    print("=" * 60)
    
    from langchain.memory import ConversationBufferWindowMemory
    
    # 只保留最近 K 轮对话
    memory = ConversationBufferWindowMemory(
        k=2,  # 保留最近 2 轮
        memory_key="chat_history",
        return_messages=True
    )
    
    print("保留最近 2 轮对话:\n")
    
    # 添加 5 轮对话
    for i in range(5):
        memory.save_context(
            {"input": f"问题{i+1}"},
            {"output": f"回答{i+1}"}
        )
    
    # 查看记忆
    history = memory.load_memory_variables({})
    print(f"保留的消息数：{len(history['chat_history'])}")
    print("(只保留最近的 2 轮，早期的已自动遗忘)")


def test_summary_memory():
    """测试摘要记忆"""
    print("\n" + "=" * 60)
    print("摘要记忆 (Summary Memory)")
    print("=" * 60)
    
    from langchain.memory import ConversationSummaryMemory
    
    llm = get_llm()
    
    # 创建摘要记忆
    memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="summary",
        return_messages=True
    )
    
    print("长对话自动摘要:\n")
    
    # 添加多轮对话
    conversations = [
        ("我想学习 Python", "Python 是很好的入门语言。"),
        ("有什么学习资源推荐？", "官方文档、Codecademy、Coursera 都不错。"),
        ("学多久能找到工作？", "通常 3-6 个月系统学习可以达到入门水平。"),
        ("需要学哪些内容？", "基础语法、数据结构、常用库、项目实践。"),
    ]
    
    for human, ai in conversations:
        memory.save_context({"input": human}, {"output": ai})
    
    # 获取摘要
    summary = memory.load_memory_variables({})
    print(f"对话摘要：{summary['summary'][:200]}...")


def test_memory_with_chain():
    """测试带记忆的链"""
    print("\n" + "=" * 60)
    print("带记忆的对话链")
    print("=" * 60)
    
    llm = get_llm()
    
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    
    # 创建带记忆的对话链
    memory = ConversationBufferMemory()
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    print("多轮对话测试:\n")
    
    # 对话
    responses = []
    questions = [
        "你好，我最近想学习编程",
        "你觉得 Python 怎么样？",
        "我刚才问的是什么？"  # 测试记忆
    ]
    
    for question in questions:
        print(f"用户：{question}")
        response = conversation.predict(input=question)
        print(f"助手：{response}\n")
        responses.append(response)


def memory_comparison():
    """记忆类型对比"""
    print("\n" + "=" * 60)
    print("记忆类型对比")
    print("=" * 60)
    
    print("""
    | 记忆类型              | 特点                      | 适用场景          |
    |----------------------|--------------------------|------------------|
    | Buffer Memory        | 保存所有历史              | 短对话，上下文重要 |
    | Buffer Window Memory | 只保留最近 K 轮            | 长对话，节省 token |
    | Summary Memory       | 自动摘要历史              | 超长对话，保留要点 |
    | Vector Memory        | 向量存储，语义检索         | 需要精准回忆      |
    | Entity Memory        | 记忆实体和信息            | 需要记住用户信息  |
    
    💡 选择建议:
    - 短对话 (<10 轮): Buffer Memory
    - 中等对话：Buffer Window Memory (k=5-10)
    - 长对话：Summary Memory
    - 需要精准回忆：Vector Memory
    """)


if __name__ == "__main__":
    print("\n🧠 对话记忆基础示例\n")
    
    test_buffer_memory()
    test_buffer_window_memory()
    test_summary_memory()
    test_memory_with_chain()
    memory_comparison()
    
    print("\n✅ 所有测试完成！")
