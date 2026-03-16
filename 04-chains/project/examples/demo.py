#!/usr/bin/env python3
"""
文档处理流水线演示脚本

用法:
    python demo.py [--model MODEL]
    
示例:
    python demo.py                    # 使用默认模型 (Ollama qwen3.5:9b)
    python demo.py --model qwen-plus  # 使用阿里云 qwen-plus
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import DocumentPipeline, quick_process
import argparse


def demo_basic():
    """基础演示"""
    print("=" * 60)
    print("基础演示 - 单文档处理")
    print("=" * 60)
    
    text = """
    人工智能 (Artificial Intelligence, AI) 是计算机科学的一个重要分支，
    它致力于研究和开发用于创建能够执行通常需要人类智能的任务的系统和技术。
    这些任务包括但不限于：学习、推理、问题解决、感知、语言理解、甚至创造力。
    
    机器学习是 AI 的核心技术之一，它使计算机能够从数据中学习并改进性能，
    而无需进行明确的编程。深度学习则是机器学习的一个子领域，
    使用多层神经网络来模拟人脑的工作方式。
    
    当前，AI 技术已经广泛应用于各个领域，包括医疗诊断、自动驾驶、
    金融分析、客户服务、内容创作等。随着技术的不断进步，
    AI 正在深刻地改变着我们的生活方式和工作方式。
    """
    
    print(f"\n原始文本长度：{len(text)} 字符\n")
    
    # 处理文档
    pipeline = DocumentPipeline(
        model="qwen3.5:9b",
        enable_translation=True,
        enable_keyword_extraction=True
    )
    
    result = pipeline.process(text)
    
    print("📄 处理结果:")
    print(f"\n【摘要】\n{result.summary}")
    print(f"\n【关键词】\n{', '.join(result.keywords)}")
    print(f"\n【英文翻译】\n{result.translation}")
    print(f"\n【统计】")
    print(f"  - 原始字数：{result.word_count}")
    print(f"  - 处理耗时：{result.processing_time:.2f}秒")


def demo_batch():
    """批量处理演示"""
    print("\n" + "=" * 60)
    print("批量处理演示")
    print("=" * 60)
    
    documents = [
        "Python 是一种高级编程语言，以其简洁的语法和强大的功能而闻名。",
        "LangChain 是一个用于开发大语言模型应用的框架。",
        "Ollama 让你可以在本地运行各种开源大语言模型。",
    ]
    
    pipeline = DocumentPipeline(model="qwen3.5:9b")
    results = pipeline.process_batch(documents)
    
    for i, result in enumerate(results):
        print(f"\n【文档 {i+1}】")
        print(f"原文：{result.original[:50]}...")
        print(f"摘要：{result.summary}")
        print(f"关键词：{', '.join(result.keywords)}")


def demo_quick():
    """快速处理演示"""
    print("\n" + "=" * 60)
    print("快速处理 (一行代码)")
    print("=" * 60)
    
    text = "量子计算是一种基于量子力学原理的新型计算模式。"
    
    result = quick_process(text)
    
    print(f"原文：{text}")
    print(f"摘要：{result.summary}")
    print(f"关键词：{', '.join(result.keywords)}")


def main():
    parser = argparse.ArgumentParser(description="文档处理流水线演示")
    parser.add_argument(
        "--model",
        type=str,
        default="qwen3.5:9b",
        help="使用的模型 (默认：qwen3.5:9b)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="运行批量处理演示"
    )
    
    args = parser.parse_args()
    
    print(f"\n🚀 文档处理流水线演示")
    print(f"使用模型：{args.model}\n")
    
    try:
        demo_basic()
        
        if args.batch:
            demo_batch()
        
        demo_quick()
        
        print("\n✅ 演示完成！")
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n请确保:")
        print("1. Ollama 服务正在运行 (如果使用本地模型)")
        print("2. 已安装依赖：pip install -r requirements.txt")
        print("3. 已配置环境变量 (如果使用阿里云)")


if __name__ == "__main__":
    main()
