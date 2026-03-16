# 09-Output-Parsers 项目实战 - 结构化数据提取工具

> 从非结构化文本中提取结构化数据的通用工具

---

## 🎯 项目目标

构建一个能够从各种文本中提取结构化数据的工具，支持多种输出格式。

**核心功能**:
- ✅ JSON 提取
- ✅ 表格解析
- ✅ 列表提取
- ✅ 实体识别
- ✅ 自定义格式

---

## 📁 项目结构

```
project/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── json_extractor.py    # JSON 提取
│   ├── table_parser.py      # 表格解析
│   ├── entity_extractor.py  # 实体提取
│   └── custom_parser.py     # 自定义解析
├── tests/
│   └── test_extractors.py
└── examples/
    └── demo.py
```

---

## 🚀 快速开始

```bash
cd project
pip install -r requirements.txt
python examples/demo.py
```

---

## 💻 核心功能

### 1. JSON 提取器

```python
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class ProductInfo(BaseModel):
    name: str = Field(description="产品名称")
    price: float = Field(description="价格")
    description: str = Field(description="产品描述")
    features: list[str] = Field(description="功能列表")

class JSONExtractor:
    def __init__(self):
        self.llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
        self.parser = JsonOutputParser(pydantic_object=ProductInfo)
    
    def extract(self, text: str) -> dict:
        prompt = ChatPromptTemplate.from_template("""
        从文本中提取产品信息：
        
        {text}
        
        {format_instructions}
        """)
        
        chain = prompt | self.llm | self.parser
        return chain.invoke({
            "text": text,
            "format_instructions": self.parser.get_format_instructions()
        })
```

### 2. 实体提取器

```python
class EntityExtractor:
    def __init__(self):
        self.llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    
    def extract_entities(self, text: str) -> dict:
        """提取命名实体"""
        prompt = ChatPromptTemplate.from_template("""
        从文本中提取实体：
        
        文本：{text}
        
        返回 JSON 格式:
        {{
            "persons": ["人名"],
            "organizations": ["组织名"],
            "locations": ["地点"],
            "dates": ["日期"]
        }}
        """)
        
        chain = prompt | self.llm | JsonOutputParser()
        return chain.invoke({"text": text})
```

---

## 📝 使用示例

```python
from src.json_extractor import JSONExtractor
from src.entity_extractor import EntityExtractor

# JSON 提取
json_ext = JSONExtractor()
product_text = "iPhone 15 Pro，售价 7999 元，搭载 A17 芯片..."
result = json_ext.extract(product_text)
print(f"产品：{result['name']}, 价格：{result['price']}")

# 实体提取
entity_ext = EntityExtractor()
news_text = "马云于 2024 年在杭州参加了阿里巴巴的年会..."
entities = entity_ext.extract_entities(news_text)
print(f"人物：{entities['persons']}")
print(f"组织：{entities['organizations']}")
```

---

## 🎓 学习目标

- ✅ 结构化数据提取
- ✅ Pydantic 数据验证
- ✅ JSON 解析
- ✅ 命名实体识别
- ✅ 自定义解析器

---

**祝你学习愉快！🚀**
