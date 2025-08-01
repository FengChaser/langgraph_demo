"""
LangGraph Studio 入口文件
为 LangGraph Studio 提供标准化的图形接口
"""

import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent

# 导入工具
from tools import AVAILABLE_TOOLS
from langchain_tools import get_available_tools

# 加载环境变量
load_dotenv()

def create_graph():
    """
    创建 LangGraph 图形，供 LangGraph Studio 使用
    注意：LangGraph API 会自动处理持久化，不需要自定义 checkpointer
    """
    # 初始化大模型
    model = ChatDeepSeek(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        model=os.getenv("MODEL_NAME", "deepseek-chat"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("MAX_TOKENS", "2000"))
    )
    
    # 组合工具列表
    all_tools = AVAILABLE_TOOLS.copy()
    
    try:
        langchain_tools = get_available_tools()
        all_tools.extend(langchain_tools)
        print(f"✅ 已加载 {len(langchain_tools)} 个 LangChain 内置工具")
    except Exception as e:
        print(f"⚠️ LangChain 工具加载失败: {e}")
    
    # 创建 ReAct 智能体图形（不使用自定义 checkpointer）
    graph = create_react_agent(
        model=model,
        tools=all_tools
        # 注意：移除了 checkpointer 参数，LangGraph API 会自动处理持久化
    )
    
    return graph

# LangGraph Studio 会自动查找这个变量
graph = create_graph()