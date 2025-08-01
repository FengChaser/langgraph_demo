"""
LangChain 内置工具集合
只保留 SerpAPI 网络搜索工具
"""

import os
from pydantic import BaseModel, Field


# ================================
# SerpAPI 网络搜索工具
# ================================

class SearchInput(BaseModel):
    """搜索输入参数"""
    query: str = Field(description="搜索关键词或问题")
    num_results: int = Field(default=5, description="返回结果数量，默认5个")

def serpapi_search(query: str, num_results: int = 5) -> str:
    """
    使用 SerpAPI 搜索互联网信息
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量
    
    Returns:
        搜索结果摘要
    """
    try:
        # 检查API密钥
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "❌ 错误: 请设置 SERPAPI_API_KEY 环境变量"
        
        # 使用 LangChain 的 SerpAPIWrapper
        from langchain_community.utilities import SerpAPIWrapper
        
        # 创建搜索包装器
        search = SerpAPIWrapper(
            serpapi_api_key=api_key,
            params={
                "engine": "google",
                "google_domain": "google.com.hk",
                "gl": "cn",
                "hl": "zh-cn",
                "num": num_results
            }
        )
        
        # 执行搜索
        result = search.run(query)
        
        return f"🔍 搜索关键词: {query}\n\n📊 搜索结果:\n{result}"
            
    except ImportError:
        return "❌ 错误: 请安装 langchain-community 包: pip install langchain-community"
    except Exception as e:
        return f"❌ 搜索失败: {str(e)}\n💡 请确保已设置正确的 SERPAPI_API_KEY"

# 为了兼容 LangChain 工具格式，添加必要属性
serpapi_search.name = "serpapi_search"
serpapi_search.description = "使用 SerpAPI 搜索互联网信息"
serpapi_search.args_schema = SearchInput


# ================================
# 工具导出
# ================================

def get_available_tools():
    """获取可用的工具列表"""
    if os.getenv("SERPAPI_API_KEY"):
        try:
            from langchain_community.utilities import SerpAPIWrapper
            return [serpapi_search]
        except ImportError:
            pass
    return []


if __name__ == "__main__":
    print("🔧 SerpAPI 搜索工具测试")
    print("=" * 50)
    
    # 检查工具可用性
    available_tools = get_available_tools()
    print(f"📊 可用工具数量: {len(available_tools)}")
    
    if available_tools:
        print(f"✅ {serpapi_search.name}: {serpapi_search.description}")
        
        print("\n🔍 测试搜索:")
        result = serpapi_search("Python编程", 3)
        print(result[:300] + "..." if len(result) > 300 else result)
    else:
        print("⚠️ SerpAPI 工具不可用")
        print("💡 请设置 SERPAPI_API_KEY 并安装 langchain-community")