# LangGraph 工具集成指南

## 📋 概述

本项目创建了一套完整的结构化工具集合，可以轻松集成到 LangGraph 智能体中。这些工具使用 Pydantic 模型定义参数，确保大模型能够准确识别和调用。

## 🔧 可用工具

### 1. 天气查询工具 (`weather_query`)
- **功能**: 查询指定城市的天气信息
- **参数**:
  - `city` (str): 城市名称
  - `days` (int): 查询天数 (1-7天)
- **示例**: 查询北京未来3天天气

### 2. 计算器工具 (`calculator`)
- **功能**: 执行数学计算
- **参数**:
  - `expression` (str): 数学表达式
- **支持**: 基本运算、数学函数 (sin, cos, sqrt, log等)
- **示例**: `2 + 3 * 4`, `sqrt(16) + sin(pi/2)`

### 3. 时间日期工具 (`datetime_query`)
- **功能**: 查询时间日期信息
- **参数**:
  - `query_type` (str): 查询类型 ('current', 'format', 'calculate')
  - `format_string` (str, 可选): 时间格式
  - `days_offset` (int, 可选): 天数偏移
- **示例**: 查询当前时间、格式化时间、计算未来日期

### 4. 文本处理工具 (`text_processor`)
- **功能**: 处理文本内容
- **参数**:
  - `text` (str): 要处理的文本
  - `operation` (str): 操作类型 ('count', 'upper', 'lower', 'reverse', 'split')
  - `separator` (str, 可选): 分割符
- **示例**: 统计字数、转换大小写、反转文本

### 5. 随机数生成工具 (`random_generator`)
- **功能**: 生成随机数或随机选择
- **参数**:
  - `type` (str): 随机类型 ('int', 'float', 'choice', 'uuid')
  - `min_value` (int, 可选): 最小值
  - `max_value` (int, 可选): 最大值
  - `choices` (List[str], 可选): 选择列表
- **示例**: 生成随机整数、从列表中随机选择

### 6. 单位转换工具 (`unit_converter`)
- **功能**: 各种单位转换
- **参数**:
  - `value` (float): 数值
  - `from_unit` (str): 源单位
  - `to_unit` (str): 目标单位
  - `category` (str): 转换类别 ('length', 'weight', 'temperature', 'area')
- **示例**: 长度、重量、温度、面积转换

## 🏗️ 架构设计

### 结构化工具定义
```python
class WeatherInput(BaseModel):
    city: str = Field(description="要查询天气的城市名称")
    days: int = Field(default=1, description="查询天数", ge=1, le=7)

@tool("weather_query", args_schema=WeatherInput)
def get_weather(city: str, days: int = 1) -> str:
    # 工具实现
    pass
```

### LangGraph 集成
```python
# 1. 绑定工具到大模型
self.llm = ChatDeepSeek(...).bind_tools(AVAILABLE_TOOLS)

# 2. 创建工具节点
self.tool_node = ToolNode(AVAILABLE_TOOLS)

# 3. 添加条件边决定是否调用工具
workflow.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    "end": END,
})
```

## 🚀 使用方法

### 基础使用
```python
from tools import AVAILABLE_TOOLS
from agent_with_tools import ToolEnabledAgent

# 创建智能体
agent = ToolEnabledAgent()

# 与智能体对话
response = agent.chat("北京今天天气怎么样？")
print(response)
```

### 运行示例
```bash
# 运行工具测试
python tools.py

# 运行集成智能体
python agent_with_tools.py
```

## 💡 示例对话

### 天气查询
```
用户: 北京今天天气怎么样？
助手: [调用 weather_query 工具] 根据查询结果，北京今天是晴天，温度25°C...
```

### 数学计算
```
用户: 计算 2的10次方加上144的平方根
助手: [调用 calculator 工具] 计算结果：2^10 + sqrt(144) = 1024 + 12 = 1036
```

### 单位转换
```
用户: 100厘米等于多少米？
助手: [调用 unit_converter 工具] 100厘米等于1米
```

## 🔍 工具设计原则

### 1. 结构化参数定义
- 使用 Pydantic BaseModel 定义输入参数
- 详细的字段描述帮助大模型理解
- 参数验证确保输入正确性

### 2. 清晰的工具命名
- 工具名称直观易懂
- 功能描述准确详细
- 参数说明完整

### 3. 错误处理
- 完善的异常捕获
- 友好的错误信息
- 安全的代码执行

### 4. 可扩展性
- 模块化设计
- 易于添加新工具
- 统一的接口规范

## 📦 依赖包

```
langgraph
langchain
langchain-core
langchain-deepseek
python-dotenv
httpx
typing-extensions
requests
pydantic
```

## 🔧 扩展建议

### 添加新工具
1. 定义输入参数模型
2. 使用 @tool 装饰器
3. 添加到 AVAILABLE_TOOLS 列表
4. 编写测试用例

### 工具类别扩展
- 网络请求工具 (API调用、网页抓取)
- 文件操作工具 (读写、搜索)
- 数据库工具 (查询、更新)
- 图像处理工具 (生成、编辑)
- 邮件工具 (发送、接收)

## 🎯 最佳实践

1. **参数验证**: 使用 Pydantic 进行严格的参数验证
2. **错误处理**: 提供清晰的错误信息和处理建议
3. **文档完整**: 详细的工具描述和使用示例
4. **安全考虑**: 避免执行危险操作，限制权限范围
5. **性能优化**: 合理的超时设置和资源管理

这套工具集为 LangGraph 智能体提供了强大的外部能力，让AI助手能够执行实际的任务，而不仅仅是对话。通过结构化的设计，确保了工具调用的准确性和可靠性。