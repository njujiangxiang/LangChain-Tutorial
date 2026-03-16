"""
示例：使用阿里云百炼模型的提示工程

演示如何在使用阿里云百炼模型时设计有效的提示
模型：qwen-max / qwen-plus
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()


def get_aliyun_llm(model: str = "qwen-plus"):
    """获取阿里云百炼模型实例"""
    return ChatOpenAI(
        model=model,
        openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        openai_api_key=os.getenv('DASHSCOPE_API_KEY', ''),
        temperature=0.7
    )


def test_aliyun_basic_prompt():
    """测试阿里云基础提示"""
    print("=" * 60)
    print("阿里云百炼基础提示")
    print("=" * 60)
    
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置，跳过")
        return
    
    llm = get_aliyun_llm("qwen-plus")
    
    prompt = ChatPromptTemplate.from_template(
        "请用{style}的风格写一段关于{topic}的文字，{length}字左右。"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    test_cases = [
        {"style": "专业严谨", "topic": "人工智能", "length": 100},
        {"style": "生动有趣", "topic": "机器学习", "length": 100},
        {"style": "简洁明了", "topic": "深度学习", "length": 100},
    ]
    
    for case in test_cases:
        print(f"\n主题：{case['topic']} ({case['style']})")
        result = chain.invoke(case)
        print(f"响应：{result[:200]}...\n")


def test_aliyun_system_prompt():
    """测试阿里云系统提示"""
    print("=" * 60)
    print("阿里云系统提示设计")
    print("=" * 60)
    
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置，跳过")
        return
    
    llm = get_aliyun_llm("qwen-max")
    
    # 专业角色系统提示
    system_prompts = {
        "技术专家": SystemMessage(
            content="你是一位资深技术专家，擅长用通俗易懂的方式解释复杂的技术概念。"
        ),
        "商务顾问": SystemMessage(
            content="你是一位专业商务顾问，提供数据驱动的建议和洞察。"
        ),
        "创意写作": SystemMessage(
            content="你是一位创意作家，文字优美，富有想象力。"
        )
    }
    
    question = "如何理解云计算？"
    
    for role, system_prompt in system_prompts.items():
        print(f"\n角色：{role}")
        print("-" * 60)
        
        chat_template = ChatPromptTemplate.from_messages([
            system_prompt,
            ("human", question)
        ])
        
        chain = chat_template | llm | StrOutputParser()
        response = chain.invoke({})
        print(f"响应：{response[:250]}...\n")


def test_aliyun_few_shot():
    """测试阿里云少样本提示"""
    print("=" * 60)
    print("阿里云少样本提示")
    print("=" * 60)
    
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置，跳过")
        return
    
    llm = get_aliyun_llm("qwen-plus")
    
    # 少样本提示 - 文本分类
    few_shot_template = ChatPromptTemplate.from_template(
        "任务：文本分类 (科技/财经/体育/娱乐)\n\n"
        "示例 1:\n"
        "文本：新款 iPhone 发布，搭载 A17 芯片\n"
        "分类：科技\n\n"
        "示例 2:\n"
        "文本：上证指数突破 3500 点大关\n"
        "分类：财经\n\n"
        "示例 3:\n"
        "文本：湖人队赢得 NBA 总冠军\n"
        "分类：体育\n\n"
        "示例 4:\n"
        "文本：某明星新电影票房破纪录\n"
        "分类：娱乐\n\n"
        "请分类:\n"
        "文本：{text}\n"
        "分类："
    )
    
    test_texts = [
        "央行宣布降准 0.25 个百分点",
        "量子计算机取得重大突破",
        "某歌手举办世界巡回演唱会",
        "世界杯决赛即将上演"
    ]
    
    for text in test_texts:
        chain = few_shot_template | llm | StrOutputParser()
        result = chain.invoke({"text": text})
        print(f"文本：{text}")
        print(f"分类：{result}\n")


def test_aliyun_structured_output():
    """测试阿里云结构化输出"""
    print("=" * 60)
    print("阿里云结构化输出")
    print("=" * 60)
    
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置，跳过")
        return
    
    llm = get_aliyun_llm("qwen-max")
    
    # 要求 JSON 格式输出
    structured_prompt = ChatPromptTemplate.from_template(
        "请分析以下产品评论，并以 JSON 格式输出:\n\n"
        "评论：{review}\n\n"
        "输出格式:\n"
        '{{\n'
        '  "sentiment": "正面/负面/中性",\n'
        '  "score": 1-5 分,\n'
        '  "keywords": ["关键词 1", "关键词 2"],\n'
        '  "summary": "一句话总结"\n'
        '}}'
    )
    
    reviews = [
        "这个手机非常好用，拍照效果出色，电池续航也很棒，就是价格有点贵。",
        "质量太差了，用了两天就坏了，客服态度也不好，非常失望。"
    ]
    
    for review in reviews:
        chain = structured_prompt | llm | StrOutputParser()
        result = chain.invoke({"review": review})
        print(f"评论：{review}")
        print(f"分析：{result}\n")


def test_aliyun_long_context():
    """测试阿里云长上下文处理"""
    print("=" * 60)
    print("阿里云长上下文处理")
    print("=" * 60)
    
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置，跳过")
        return
    
    llm = get_aliyun_llm("qwen-max")
    
    # 创建较长的文档
    document = """
    人工智能 (AI) 是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
    
    主要应用领域包括:
    1. 机器学习：让计算机从数据中学习
    2. 自然语言处理：理解和生成人类语言
    3. 计算机视觉：让计算机"看懂"图像
    4. 语音识别：将语音转换为文本
    5. 机器人技术：创建智能机器人
    
    发展历程:
    - 1950 年代：AI 概念诞生
    - 1980 年代：专家系统兴起
    - 2010 年代：深度学习突破
    - 2020 年代：大语言模型时代
    
    未来趋势:
    - 通用人工智能 (AGI)
    - AI 与人类协作
    - AI 伦理和治理
    - 边缘 AI 和物联网
    """
    
    prompt = ChatPromptTemplate.from_template(
        "基于以下文档内容，回答问题:\n\n"
        "{document}\n\n"
        "问题：{question}\n"
        "答案："
    )
    
    questions = [
        "人工智能的主要应用领域有哪些？",
        "AI 发展经历了哪些阶段？",
        "AI 的未来趋势是什么？"
    ]
    
    for question in questions:
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"document": document, "question": question})
        print(f"问题：{question}")
        print(f"答案：{result[:200]}...\n")


def compare_aliyun_models():
    """对比阿里云不同模型"""
    print("=" * 60)
    print("阿里云模型对比")
    print("=" * 60)
    
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置，跳过")
        return
    
    models = ["qwen-plus", "qwen-max"]
    question = "请用一句话解释什么是量子计算。"
    
    for model_name in models:
        print(f"\n模型：{model_name}")
        print("-" * 60)
        
        llm = get_aliyun_llm(model_name)
        prompt = ChatPromptTemplate.from_template(question)
        
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({})
        print(f"响应：{response}\n")


if __name__ == "__main__":
    print("\n☁️ 阿里云百炼提示工程示例\n")
    print("前提：配置 DASHSCOPE_API_KEY 环境变量\n")
    
    try:
        test_aliyun_basic_prompt()
        test_aliyun_system_prompt()
        test_aliyun_few_shot()
        test_aliyun_structured_output()
        test_aliyun_long_context()
        compare_aliyun_models()
        
        print("\n✅ 阿里云提示示例完成！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
