"""
示例：阿里云百炼链式调用

演示使用阿里云模型创建各种链式调用
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
import os

load_dotenv()


def get_aliyun_llm(**kwargs):
    """获取阿里云 LLM 实例"""
    api_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not api_key:
        return None
    
    return ChatOpenAI(
        model="qwen-plus",
        openai_api_key=api_key,
        openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        **kwargs
    )


def sequential_chain_example():
    """顺序链示例"""
    print("=" * 60)
    print("顺序链 - 文章生成 (阿里云)")
    print("=" * 60)
    
    llm = get_aliyun_llm(temperature=0.7)
    
    if llm is None:
        print("⚠️  API Key 未配置，显示示例代码")
        print("""
        # 顺序链示例代码
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        llm = ChatOpenAI(
            model="qwen-plus",
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        # 步骤 1: 生成大纲
        outline_prompt = ChatPromptTemplate.from_template(
            "为'{topic}'生成 3 个要点的大纲"
        )
        
        # 步骤 2: 扩展内容
        expand_prompt = ChatPromptTemplate.from_template(
            "扩展以下要点：\\n{outline}"
        )
        
        # 创建链
        outline_chain = outline_prompt | llm | StrOutputParser()
        full_chain = (
            {"topic": RunnablePassthrough()}
            | outline_chain
            | (lambda x: {"outline": x})
            | expand_prompt
            | llm
            | StrOutputParser()
        )
        
        result = full_chain.invoke("人工智能")
        """)
        return
    
    # 实际执行
    outline_prompt = ChatPromptTemplate.from_template(
        "为'{topic}'生成 3 个要点的大纲。"
    )
    
    expand_prompt = ChatPromptTemplate.from_template(
        "扩展以下要点：\n{outline}"
    )
    
    outline_chain = outline_prompt | llm | StrOutputParser()
    full_chain = (
        {"topic": RunnablePassthrough()}
        | outline_chain
        | (lambda x: {"outline": x})
        | expand_prompt
        | llm
        | StrOutputParser()
    )
    
    topic = "人工智能的发展"
    print(f"主题：{topic}\n")
    
    result = full_chain.invoke(topic)
    print(f"结果：{result[:300]}...")


def parallel_analysis():
    """并行分析示例"""
    print("\n" + "=" * 60)
    print("并行链 - 多维度分析 (阿里云)")
    print("=" * 60)
    
    llm = get_aliyun_llm(temperature=0.5)
    
    if llm is None:
        print("⚠️  API Key 未配置")
        return
    
    # 并行执行多个分析
    parallel_chain = RunnableParallel({
        "summary": ChatPromptTemplate.from_template("总结：{text}") | llm | StrOutputParser(),
        "sentiment": ChatPromptTemplate.from_template("情感分析：{text}") | llm | StrOutputParser(),
        "keywords": ChatPromptTemplate.from_template("关键词：{text}") | llm | StrOutputParser(),
    })
    
    text = "阿里云百炼大模型提供强大的 AI 能力，支持多种应用场景。"
    
    print(f"分析文本：{text}\n")
    
    results = parallel_chain.invoke({"text": text})
    
    for key, value in results.items():
        print(f"{key}: {value}")


def model_routing():
    """模型路由 - 根据任务选择模型"""
    print("\n" + "=" * 60)
    print("模型路由 - 智能选择 (阿里云)")
    print("=" * 60)
    
    # 定义不同模型
    models = {
        "fast": get_aliyun_llm(model="qwen-turbo", temperature=0.5),
        "standard": get_aliyun_llm(model="qwen-plus", temperature=0.7),
        "advanced": get_aliyun_llm(model="qwen-max", temperature=0.8),
    }
    
    print("""
    阿里云模型路由策略:
    
    - qwen-turbo: 简单任务，快速响应
    - qwen-plus: 通用任务，平衡性能
    - qwen-max: 复杂任务，最强性能
    
    示例代码:
    
    def route_by_complexity(text):
        if len(text) < 20:
            return models["fast"]
        elif len(text) < 100:
            return models["standard"]
        else:
            return models["advanced"]
    """)


if __name__ == "__main__":
    print("\n☁️ 阿里云百炼链式调用示例\n")
    
    sequential_chain_example()
    parallel_analysis()
    model_routing()
    
    print("\n✅ 阿里云链式示例完成！")
