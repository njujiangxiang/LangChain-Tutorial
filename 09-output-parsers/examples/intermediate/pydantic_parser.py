"""
示例：Pydantic 输出解析 - 中级

演示使用 Pydantic 进行结构化输出
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()


def article_analysis():
    """文章分析"""
    print("=" * 60)
    print("文章结构化分析")
    print("=" * 60)
    
    # 定义输出格式
    class ArticleAnalysis(BaseModel):
        title: str = Field(description="文章标题")
        author: Optional[str] = Field(description="作者，如果有的话")
        main_points: List[str] = Field(description="主要观点列表")
        sentiment: str = Field(description="情感倾向", enum=["positive", "negative", "neutral"])
        summary: str = Field(description="100 字以内的摘要")
        reading_time: int = Field(description="预计阅读时间 (分钟)")
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    parser = JsonOutputParser(pydantic_object=ArticleAnalysis)
    
    prompt = ChatPromptTemplate.from_template("""
    分析以下文章：
    
    {article}
    
    {format_instructions}
    """)
    
    chain = prompt | llm | parser
    
    # 测试文章
    article = """
    《人工智能的未来》
    
    人工智能技术正在快速发展，大语言模型如 GPT-4、Claude 展现出惊人能力。
    这些模型可以理解自然语言、生成文本、编写代码，甚至进行推理。
    
    然而，AI 也面临挑战：幻觉问题、偏见、安全性、就业影响等。
    专家建议，需要建立 AI 治理框架，确保技术向善发展。
    
    未来 5-10 年，AI 将在医疗、教育、科研等领域发挥更大作用，
    但人类智慧和创造力仍然不可替代。
    """
    
    print(f"分析文章：{article[:100]}...\n")
    
    try:
        result = chain.invoke({
            "article": article,
            "format_instructions": parser.get_format_instructions()
        })
        
        print("分析结果:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"解析失败：{e}")
        print("\n演示期望输出:")
        print("""
        {
            "title": "人工智能的未来",
            "author": null,
            "main_points": [
                "AI 技术快速发展",
                "面临幻觉、偏见等挑战",
                "需要建立治理框架",
                "未来将在多领域发挥作用"
            ],
            "sentiment": "neutral",
            "summary": "AI 技术发展迅速但面临挑战，需要治理确保向善，未来将发挥更大作用。",
            "reading_time": 2
        }
        """)


def product_comparison():
    """产品对比分析"""
    print("\n" + "=" * 60)
    print("产品对比分析")
    print("=" * 60)
    
    class ProductComparison(BaseModel):
        products: List[str] = Field(description="产品名称列表")
        comparison_table: List[dict] = Field(description="对比表格数据")
        recommendation: str = Field(description="推荐建议")
        best_for: dict = Field(description="各自最适合的场景")
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    parser = JsonOutputParser(pydantic_object=ProductComparison)
    
    prompt = ChatPromptTemplate.from_template("""
    对比以下产品：
    
    {text}
    
    {format_instructions}
    """)
    
    chain = prompt | llm | parser
    
    text = """
    MacBook Pro vs Dell XPS 15 vs ThinkPad X1 Carbon
    
    MacBook Pro: Apple 自研 M 芯片，优秀性能续航，macOS 系统，适合创意工作，价格较高。
    Dell XPS 15: Intel/AMD 处理器，4K OLED 屏幕，Windows 系统，适合多媒体，性价比高。
    ThinkPad X1: 轻薄便携，优秀键盘，商务定位，稳定可靠，适合商务人士。
    """
    
    print(f"产品对比：{text[:80]}...\n")
    
    try:
        result = chain.invoke({
            "text": text,
            "format_instructions": parser.get_format_instructions()
        })
        
        print("对比结果:")
        print(f"  产品：{result['products']}")
        print(f"  推荐：{result['recommendation']}")
    except Exception as e:
        print(f"解析失败：{e}")


if __name__ == "__main__":
    print("\n📋 Pydantic 输出解析 - 中级示例\n")
    
    article_analysis()
    product_comparison()
    
    print("\n✅ Pydantic 解析示例完成！")
