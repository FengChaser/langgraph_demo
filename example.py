"""
简单的智能体使用示例
"""

from agent import LangGraphAgent

def simple_example():
    """简单使用示例"""
    print("🚀 简单示例：创建智能体并进行对话")
    
    try:
        # 创建智能体
        agent = LangGraphAgent()
        
        # 进行几轮对话
        questions = [
            "你好，你是谁？",
            "你能做什么？",
            "请介绍一下LangGraph",
            "我刚才问了什么问题？"  # 测试记忆功能
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n--- 第 {i} 轮对话 ---")
            print(f"👤 用户: {question}")
            
            response = agent.chat(question, thread_id="example_session")
            print(f"🤖 助手: {response}")
        
        # 显示对话历史
        print("\n--- 对话历史 ---")
        history = agent.get_conversation_history("example_session")
        for msg in history:
            if hasattr(msg, 'content'):
                role = "👤 用户" if msg.__class__.__name__ == "HumanMessage" else "🤖 助手"
                print(f"{role}: {msg.content}")
    
    except Exception as e:
        print(f"❌ 示例运行失败: {e}")

if __name__ == "__main__":
    simple_example()