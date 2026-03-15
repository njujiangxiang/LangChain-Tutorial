"""
LangChain 环境验证脚本

运行此脚本验证 LangChain 是否正确安装和配置。
"""

import sys
import os
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(status: str, message: str):
    """打印状态信息"""
    if status == "success":
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
    elif status == "error":
        print(f"{Colors.RED}✗{Colors.END} {message}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")
    elif status == "info":
        print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def check_python_version():
    """检查 Python 版本"""
    print("\n" + "="*50)
    print("1. 检查 Python 版本")
    print("="*50)
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_status("success", f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    else:
        print_status("error", f"Python {version.major}.{version.minor}.{version.micro} - 需要 Python 3.10+")
        return False

def check_langchain_install():
    """检查 LangChain 安装"""
    print("\n" + "="*50)
    print("2. 检查 LangChain 安装")
    print("="*50)
    
    try:
        import langchain
        print_status("success", f"langchain {langchain.__version__} ✓")
    except ImportError:
        print_status("error", "langchain 未安装")
        return False
    
    try:
        import langchain_core
        print_status("success", f"langchain-core {langchain_core.__version__} ✓")
    except ImportError:
        print_status("error", "langchain-core 未安装")
        return False
    
    try:
        import langchain_community
        print_status("success", f"langchain-community {langchain_community.__version__} ✓")
    except ImportError:
        print_status("warning", "langchain-community 未安装 (可选)")
    
    return True

def check_model_integrations():
    """检查模型集成"""
    print("\n" + "="*50)
    print("3. 检查模型集成")
    print("="*50)
    
    # OpenAI
    try:
        from langchain_openai import ChatOpenAI
        print_status("success", "langchain-openai ✓")
        
        # 检查 API Key
        if os.getenv('OPENAI_API_KEY'):
            print_status("success", "OPENAI_API_KEY 已配置 ✓")
        else:
            print_status("warning", "OPENAI_API_KEY 未配置")
    except ImportError:
        print_status("warning", "langchain-openai 未安装 (可选)")
    
    # Anthropic
    try:
        from langchain_anthropic import ChatAnthropic
        print_status("success", "langchain-anthropic ✓")
        
        # 检查 API Key
        if os.getenv('ANTHROPIC_API_KEY'):
            print_status("success", "ANTHROPIC_API_KEY 已配置 ✓")
        else:
            print_status("warning", "ANTHROPIC_API_KEY 未配置")
    except ImportError:
        print_status("warning", "langchain-anthropic 未安装 (可选)")
    
    return True

def check_vector_stores():
    """检查向量数据库"""
    print("\n" + "="*50)
    print("4. 检查向量数据库")
    print("="*50)
    
    # FAISS
    try:
        import faiss
        print_status("success", "faiss-cpu ✓")
    except ImportError:
        print_status("warning", "faiss-cpu 未安装 (可选)")
    
    # ChromaDB
    try:
        import chromadb
        print_status("success", "chromadb ✓")
    except ImportError:
        print_status("warning", "chromadb 未安装 (可选)")
    
    return True

def check_document_loaders():
    """检查文档加载器"""
    print("\n" + "="*50)
    print("5. 检查文档处理库")
    print("="*50)
    
    # PyPDF
    try:
        import pypdf
        print_status("success", "pypdf ✓")
    except ImportError:
        print_status("warning", "pypdf 未安装 (可选)")
    
    # BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        print_status("success", "beautifulsoup4 ✓")
    except ImportError:
        print_status("warning", "beautifulsoup4 未安装 (可选)")
    
    return True

def test_basic_llm():
    """测试基础 LLM 调用"""
    print("\n" + "="*50)
    print("6. 测试基础 LLM 调用")
    print("="*50)
    
    api_key = os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print_status("warning", "没有配置 API Key，跳过测试")
        return True
    
    try:
        if os.getenv('ANTHROPIC_API_KEY'):
            from langchain_anthropic import ChatAnthropic
            
            llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.3)
            response = llm.invoke("用一句话介绍你自己")
            print_status("success", f"Anthropic API 调用成功 ✓")
            print(f"   响应：{response.content[:50]}...")
            return True
        else:
            from langchain_openai import ChatOpenAI
            
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
            response = llm.invoke("用一句话介绍你自己")
            print_status("success", f"OpenAI API 调用成功 ✓")
            print(f"   响应：{response.content[:50]}...")
            return True
    except Exception as e:
        print_status("error", f"API 调用失败：{str(e)}")
        return False

def main():
    """主函数"""
    print("\n" + "="*60)
    print(f"{Colors.BLUE}🦜️🔗 LangChain 环境验证{Colors.END}")
    print("="*60)
    
    results = []
    
    # 运行所有检查
    results.append(("Python 版本", check_python_version()))
    results.append(("LangChain 安装", check_langchain_install()))
    results.append(("模型集成", check_model_integrations()))
    results.append(("向量数据库", check_vector_stores()))
    results.append(("文档处理", check_document_loaders()))
    results.append(("LLM 测试", test_basic_llm()))
    
    # 总结
    print("\n" + "="*60)
    print("验证总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✓{Colors.END}" if result else f"{Colors.RED}✗{Colors.END}"
        print(f"{status} {name}")
    
    print("\n" + "-"*60)
    print(f"通过：{passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 恭喜！环境配置完成，可以开始学习了！{Colors.END}\n")
    else:
        print(f"\n{Colors.YELLOW}⚠️  部分检查未通过，请参考 README.md 进行配置{Colors.END}\n")

if __name__ == "__main__":
    main()
