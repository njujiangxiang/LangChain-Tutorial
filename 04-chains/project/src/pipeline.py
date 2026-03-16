"""
文档处理流水线核心模块
"""

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from dotenv import load_dotenv
import os
import time

load_dotenv()


class DocumentResult(BaseModel):
    """文档处理结果"""
    original: str = Field(description="原始文本")
    summary: str = Field(description="摘要")
    keywords: List[str] = Field(description="关键词列表")
    translation: Optional[str] = Field(default=None, description="英文翻译")
    word_count: int = Field(description="字数统计")
    processing_time: float = Field(description="处理耗时 (秒)")


class DocumentPipeline:
    """文档处理流水线"""
    
    def __init__(
        self,
        model: str = "qwen3.5:9b",
        enable_translation: bool = True,
        enable_keyword_extraction: bool = True,
    ):
        self.model_name = model
        self.enable_translation = enable_translation
        self.enable_keyword_extraction = enable_keyword_extraction
        
        # 初始化 LLM
        self.llm = self._init_llm(model)
        
        # 创建处理链
        self.summary_chain = self._create_summary_chain()
        self.keyword_chain = self._create_keyword_chain()
        self.translation_chain = self._create_translation_chain()
    
    def _init_llm(self, model: str):
        """初始化 LLM"""
        # 判断使用 Ollama 还是阿里云
        if model.startswith("qwen-") or "aliyun" in model.lower():
            api_key = os.getenv('DASHSCOPE_API_KEY')
            if api_key:
                return ChatOpenAI(
                    model=model if not model.startswith("qwen-") else "qwen-plus",
                    openai_api_key=api_key,
                    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    temperature=0.5,
                )
        
        # 默认使用 Ollama
        return ChatOllama(
            model=model if not model.startswith("qwen-") else "qwen3.5:9b",
            temperature=0.5,
        )
    
    def _create_summary_chain(self):
        """创建摘要链"""
        prompt = ChatPromptTemplate.from_template(
            "请用 100 字以内总结以下文本的核心内容：\n\n{text}"
        )
        return prompt | self.llm | StrOutputParser()
    
    def _create_keyword_chain(self):
        """创建关键词提取链"""
        prompt = ChatPromptTemplate.from_template(
            "请从以下文本中提取 3-5 个关键词，用逗号分隔：\n\n{text}"
        )
        return prompt | self.llm | StrOutputParser()
    
    def _create_translation_chain(self):
        """创建翻译链"""
        prompt = ChatPromptTemplate.from_template(
            "请将以下文本翻译成英文，保持原意：\n\n{text}"
        )
        return prompt | self.llm | StrOutputParser()
    
    def process(self, text: str) -> DocumentResult:
        """处理文档"""
        start_time = time.time()
        
        # 并行处理独立任务
        summary_future = self.summary_chain.ainvoke({"text": text})
        
        if self.enable_keyword_extraction:
            keyword_future = self.keyword_chain.ainvoke({"text": text})
        else:
            keyword_future = None
        
        if self.enable_translation:
            translation_future = self.translation_chain.ainvoke({"text": text})
        else:
            translation_future = None
        
        # 等待结果
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            summary = loop.run_until_complete(summary_future)
            
            keywords = []
            if keyword_future:
                keyword_result = loop.run_until_complete(keyword_future)
                keywords = [k.strip() for k in keyword_result.split(",")]
            
            translation = None
            if translation_future:
                translation = loop.run_until_complete(translation_future)
        finally:
            loop.close()
        
        processing_time = time.time() - start_time
        
        return DocumentResult(
            original=text,
            summary=summary,
            keywords=keywords,
            translation=translation,
            word_count=len(text),
            processing_time=processing_time
        )
    
    def process_batch(self, texts: List[str], max_concurrency: int = 3) -> List[DocumentResult]:
        """批量处理文档"""
        results = []
        
        # 简单实现：顺序处理
        # 生产环境可使用 asyncio.gather 实现并发
        for i, text in enumerate(texts):
            print(f"处理文档 {i+1}/{len(texts)}...")
            result = self.process(text)
            results.append(result)
        
        return results


# 便捷函数
def quick_process(text: str, model: str = "qwen3.5:9b") -> DocumentResult:
    """快速处理单个文档"""
    pipeline = DocumentPipeline(model=model)
    return pipeline.process(text)
