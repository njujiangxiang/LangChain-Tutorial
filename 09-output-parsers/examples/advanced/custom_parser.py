"""
示例：自定义输出解析 - 高级

演示创建自定义输出解析器
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional, Any
import re
import json
from dotenv import load_dotenv
import os

load_dotenv()


class CustomListParser(BaseOutputParser[List[str]]):
    """自定义列表解析器"""
    
    def parse(self, text: str) -> List[str]:
        """解析文本为列表"""
        # 匹配列表项
        patterns = [
            r'[-•*]\s*(.+)',      # 无序列表
            r'\d+\.\s*(.+)',      # 有序列表
            r'^(.+)$',            # 每行一项
        ]
        
        items = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    item = match.group(1).strip()
                    if item:
                        items.append(item)
                    break
        
        return items if items else [text.strip()]


class TableParser(BaseOutputParser[List[dict]]):
    """表格解析器"""
    
    def parse(self, text: str) -> List[dict]:
        """解析 Markdown 表格"""
        rows = []
        lines = text.strip().split('\n')
        
        # 跳过表头分隔线
        data_lines = [l for l in lines if not l.startswith('|---')]
        
        if len(data_lines) < 2:
            return [{"raw": text}]
        
        # 解析表头
        headers = [h.strip() for h in data_lines[0].split('|') if h.strip()]
        
        # 解析数据行
        for line in data_lines[1:]:
            if line.startswith('|'):
                values = [v.strip() for v in line.split('|')[1:-1]]
                if len(values) == len(headers):
                    rows.append(dict(zip(headers, values)))
        
        return rows if rows else [{"raw": text}]


def custom_list_parser_example():
    """自定义列表示例"""
    print("=" * 60)
    print("自定义列表解析器")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    parser = CustomListParser()
    
    prompt = ChatPromptTemplate.from_template("""
    列出{topic}的 5 个关键点，使用无序列表格式（每行以 - 开头）：
    
    {topic}:
    """)
    
    chain = prompt | llm | parser
    
    topic = "学习 Python 的建议"
    
    print(f"主题：{topic}\n")
    
    try:
        result = chain.invoke({"topic": topic})
        
        print("解析结果:")
        for i, item in enumerate(result, 1):
            print(f"  {i}. {item}")
        
        print(f"\n共 {len(result)} 项")
    except Exception as e:
        print(f"解析失败：{e}")


def table_parser_example():
    """表格解析示例"""
    print("\n" + "=" * 60)
    print("表格解析器")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    parser = TableParser()
    
    prompt = ChatPromptTemplate.from_template("""
    对比以下产品，返回 Markdown 表格格式：
    
    产品：iPhone 15, Samsung S24, Pixel 8
    
    表格列：品牌，价格，屏幕，电池
    """)
    
    chain = prompt | llm | parser
    
    print("产品对比表格:\n")
    
    try:
        result = chain.invoke({})
        
        if result and "raw" not in result[0]:
            print("解析的表格:")
            for row in result:
                print(f"  {row}")
        else:
            print("表格格式不标准，返回原始内容")
    except Exception as e:
        print(f"解析失败：{e}")


class StructuredOutput(BaseModel):
    """结构化输出模型"""
    title: str
    points: List[str]
    summary: str
    rating: float = Field(ge=0, le=10)
    tags: List[str]


def pydantic_with_validation():
    """Pydantic 带验证的解析"""
    print("\n" + "=" * 60)
    print("Pydantic 带验证解析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    
    from langchain_core.output_parsers import JsonOutputParser
    parser = JsonOutputParser(pydantic_object=StructuredOutput)
    
    prompt = ChatPromptTemplate.from_template("""
    评价以下产品：
    
    产品：{product}
    
    {format_instructions}
    
    要求:
    - title: 评价标题
    - points: 3 个主要特点
    - summary: 50 字以内总结
    - rating: 0-10 分评分
    - tags: 3 个标签
    """)
    
    chain = prompt | llm | parser
    
    product = "MacBook Pro M3"
    
    print(f"产品评价：{product}\n")
    
    try:
        result = chain.invoke({
            "product": product,
            "format_instructions": parser.get_format_instructions()
        })
        
        print("评价结果:")
        print(f"  标题：{result.get('title', 'N/A')}")
        print(f"  评分：{result.get('rating', 'N/A')}/10")
        print(f"  特点：{result.get('points', [])}")
        print(f"  标签：{result.get('tags', [])}")
        print(f"  总结：{result.get('summary', 'N/A')}")
        
    except Exception as e:
        print(f"解析失败：{e}")
        print("\n演示期望输出:")
        print("""
        {
            "title": "MacBook Pro M3 - 专业创作者的利器",
            "points": [
                "M3 芯片性能强劲",
                "Mini-LED 屏幕出色",
                "续航优秀"
            ],
            "summary": "M3 MacBook Pro 性能强大，适合专业创作者和开发者，但价格较高。",
            "rating": 9.0,
            "tags": ["笔记本", "苹果", "专业"]
        }
        """)


def error_handling_parser():
    """错误处理解析器"""
    print("\n" + "=" * 60)
    print("带错误处理的解析")
    print("=" * 60)
    
    class SafeJsonParser(BaseOutputParser[Any]):
        """安全的 JSON 解析器"""
        
        def parse(self, text: str) -> Any:
            try:
                # 尝试提取 JSON
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return {"raw": text}
            except json.JSONDecodeError:
                return {"error": "JSON 解析失败", "raw": text}
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    parser = SafeJsonParser()
    
    prompt = ChatPromptTemplate.from_template("返回 JSON：{{\"name\": \"测试\", \"value\": 123}}")
    
    chain = prompt | llm | parser
    
    print("测试安全 JSON 解析:\n")
    
    result = chain.invoke({})
    print(f"解析结果：{result}")


def chain_of_thought_parser():
    """思维链解析"""
    print("\n" + "=" * 60)
    print("思维链解析")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.5)
    
    # 要求 LLM 展示思考过程
    prompt = ChatPromptTemplate.from_template("""
    解答以下数学问题，展示思考过程：
    
    问题：{question}
    
    请按以下格式回答:
    思考过程：[你的推理步骤]
    最终答案：[简洁的答案]
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    question = "一个农场有鸡和兔子共 35 个头，94 只脚。鸡和兔子各有多少只？"
    
    print(f"问题：{question}\n")
    
    result = chain.invoke({"question": question})
    print(f"解答:\n{result}")


if __name__ == "__main__":
    print("\n📋 自定义输出解析 - 高级示例\n")
    
    custom_list_parser_example()
    table_parser_example()
    pydantic_with_validation()
    error_handling_parser()
    chain_of_thought_parser()
    
    print("\n✅ 自定义解析器示例完成！")
