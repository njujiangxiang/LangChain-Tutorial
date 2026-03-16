"""
示例：JSON 输出解析 - 基础

演示如何让 LLM 输出结构化 JSON 数据
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
import os
import json

load_dotenv()


def basic_json_parsing():
    """基础 JSON 解析"""
    print("=" * 60)
    print("基础 JSON 解析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    
    # 定义期望的 JSON 格式
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_template("""
    请分析以下文本并返回 JSON 格式：
    
    文本：{text}
    
    返回格式：
    {{
        "sentiment": "positive 或 negative 或 neutral",
        "confidence": 0-1 之间的数字，
        "keywords": ["关键词 1", "关键词 2"],
        "summary": "一句话总结"
    }}
    
    只返回 JSON，不要其他内容。
    """)
    
    chain = prompt | llm | parser
    
    # 测试
    test_texts = [
        "这个产品非常好用，我非常满意！",
        "太失望了，完全不值这个价格。",
        "还行吧，没什么特别的。",
    ]
    
    print("情感分析:\n")
    
    for text in test_texts:
        print(f"文本：{text}")
        try:
            result = chain.invoke({"text": text})
            print(f"结果：{json.dumps(result, ensure_ascii=False, indent=2)}\n")
        except Exception as e:
            print(f"解析失败：{e}\n")


def pydantic_json_parsing():
    """使用 Pydantic 的 JSON 解析"""
    print("\n" + "=" * 60)
    print("Pydantic JSON 解析")
    print("=" * 60)
    
    # 定义输出格式
    class ArticleSummary(BaseModel):
        title: str = Field(description="文章标题")
        author: str = Field(description="作者")
        publish_date: str = Field(description="发布日期")
        tags: list[str] = Field(description="标签列表")
        summary: str = Field(description="文章摘要")
        reading_time: int = Field(description="阅读时间 (分钟)")
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    parser = JsonOutputParser(pydantic_object=ArticleSummary)
    
    prompt = ChatPromptTemplate.from_template("""
    从以下文本中提取文章信息：
    
    {text}
    
    {format_instructions}
    """)
    
    chain = prompt | llm | parser
    
    # 测试文本
    article = """
    《人工智能的未来发展趋势》
    作者：李明
    发布于 2024 年 3 月 15 日
    
    本文探讨了人工智能技术在未来 5-10 年的发展趋势，
    包括大语言模型、多模态 AI、自动驾驶等领域。
    预计这些技术将深刻改变我们的生活和工作方式。
    全文约 3000 字，阅读需要 8 分钟。
    
    标签：AI、人工智能、技术趋势、机器学习
    """
    
    print("文章信息提取:\n")
    
    try:
        result = chain.invoke({
            "text": article,
            "format_instructions": parser.get_format_instructions()
        })
        print(f"提取结果:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"解析失败：{e}")
        print("\n演示期望输出:")
        print("""
        {
            "title": "人工智能的未来发展趋势",
            "author": "李明",
            "publish_date": "2024 年 3 月 15 日",
            "tags": ["AI", "人工智能", "技术趋势", "机器学习"],
            "summary": "探讨 AI 技术未来 5-10 年发展趋势",
            "reading_time": 8
        }
        """)


def list_parsing():
    """列表解析"""
    print("\n" + "=" * 60)
    print("列表解析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_template("""
    从文本中提取所有提到的事物名称，返回 JSON 列表：
    
    文本：{text}
    
    格式：{{"items": ["项目 1", "项目 2", ...]}}
    
    只返回 JSON。
    """)
    
    chain = prompt | llm | parser
    
    text = """
    我喜欢的编程语言有 Python、Java、JavaScript、Go 和 Rust。
    它们各有特点：Python 简洁，Java 稳定，JavaScript 灵活，Go 高效，Rust 安全。
    """
    
    print(f"输入：{text[:80]}...\n")
    
    try:
        result = chain.invoke({"text": text})
        print(f"提取的编程语言:")
        for item in result.get("items", []):
            print(f"  - {item}")
    except Exception as e:
        print(f"解析失败：{e}")


def nested_json_parsing():
    """嵌套 JSON 解析"""
    print("\n" + "=" * 60)
    print("嵌套 JSON 解析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_template("""
    分析产品信息，返回嵌套 JSON：
    
    产品描述：{text}
    
    格式：
    {{
        "product": {{
            "name": "产品名称",
            "price": 价格数字，
            "features": ["特性 1", "特性 2"],
            "specs": {{
                "weight": "重量",
                "size": "尺寸",
                "color": "颜色"
            }}
        }}
    }}
    
    只返回 JSON。
    """)
    
    chain = prompt | llm | parser
    
    text = """
    iPhone 15 Pro，售价 7999 元。
    特点：A17 芯片、钛金属边框、48MP 摄像头。
    规格：重量 187g，尺寸 6.1 英寸，颜色有黑色/白色/蓝色。
    """
    
    print(f"产品描述：{text[:60]}...\n")
    
    try:
        result = chain.invoke({"text": text})
        print(f"解析结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"解析失败：{e}")
        print("\n演示期望输出:")
        print("""
        {
            "product": {
                "name": "iPhone 15 Pro",
                "price": 7999,
                "features": ["A17 芯片", "钛金属边框", "48MP 摄像头"],
                "specs": {
                    "weight": "187g",
                    "size": "6.1 英寸",
                    "color": "黑色/白色/蓝色"
                }
            }
        }
        """)


def error_handling():
    """错误处理"""
    print("\n" + "=" * 60)
    print("JSON 解析错误处理")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    def safe_json_parse(text: str, max_retries: int = 3):
        """安全的 JSON 解析"""
        parser = JsonOutputParser()
        
        prompt = ChatPromptTemplate.from_template("""
        提取信息返回 JSON：{text}
        只返回有效 JSON，不要其他内容。
        """)
        
        chain = prompt | llm | parser
        
        for i in range(max_retries):
            try:
                result = chain.invoke({"text": text})
                return {"success": True, "data": result}
            except Exception as e:
                if i < max_retries - 1:
                    print(f"重试 {i+1}/{max_retries}: {e}")
                else:
                    return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "未知错误"}
    
    # 测试
    test_cases = [
        "正常文本，应该能解析。",
        "",  # 空文本
        "非常非常非常长的文本" * 100,  # 超长文本
    ]
    
    for text in test_cases:
        print(f"\n测试：{text[:30]}...")
        result = safe_json_parse(text)
        print(f"结果：{result['success']}")
        if not result['success']:
            print(f"错误：{result['error']}")


if __name__ == "__main__":
    print("\n📋 JSON 输出解析 - 基础示例\n")
    
    basic_json_parsing()
    pydantic_json_parsing()
    list_parsing()
    nested_json_parsing()
    error_handling()
    
    print("\n✅ JSON 解析示例完成！")
