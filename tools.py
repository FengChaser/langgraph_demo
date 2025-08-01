"""
LangGraph 工具集合 - 结构化工具函数

这个模块包含了多种工具函数，每个工具都使用结构化的方式定义，
确保大模型能够准确识别参数类型和含义。
"""

import json
import math
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# ================================
# 1. 天气查询工具
# ================================

class WeatherInput(BaseModel):
    """天气查询输入参数"""
    city: str = Field(
        description="要查询天气的城市名称，例如：北京、上海、广州"
    )
    days: int = Field(
        default=1,
        description="查询天数，1表示今天，3表示未来3天，最大7天",
        ge=1,
        le=7
    )

@tool("weather_query", args_schema=WeatherInput)
def get_weather(city: str, days: int = 1) -> str:
    """
    查询指定城市的天气信息
    
    Args:
        city: 城市名称
        days: 查询天数（1-7天）
    
    Returns:
        天气信息的JSON字符串
    """
    # 模拟天气数据（实际使用时可以接入真实的天气API）
    weather_conditions = ["晴天", "多云", "阴天", "小雨", "中雨", "大雨", "雪"]
    temperatures = list(range(-10, 35))
    
    weather_data = {
        "city": city,
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "forecast": []
    }
    
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        weather_data["forecast"].append({
            "date": date,
            "condition": random.choice(weather_conditions),
            "temperature": f"{random.choice(temperatures)}°C",
            "humidity": f"{random.randint(30, 90)}%",
            "wind": f"{random.randint(1, 8)}级"
        })
    
    return json.dumps(weather_data, ensure_ascii=False, indent=2)


# ================================
# 2. 计算器工具
# ================================

class CalculatorInput(BaseModel):
    """计算器输入参数"""
    expression: str = Field(
        description="要计算的数学表达式，支持基本运算符 +, -, *, /, **, (), 以及数学函数如 sin, cos, tan, log, sqrt 等"
    )

@tool("calculator", args_schema=CalculatorInput)
def calculate(expression: str) -> str:
    """
    执行数学计算
    
    Args:
        expression: 数学表达式
    
    Returns:
        计算结果
    """
    try:
        # 安全的数学函数映射
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
        }
        
        # 替换常用数学函数
        expression = expression.replace("^", "**")  # 支持 ^ 作为幂运算
        
        result = eval(expression, safe_dict)
        return f"计算结果: {expression} = {result}"
    
    except Exception as e:
        return f"计算错误: {str(e)}"


# ================================
# 3. 时间日期工具
# ================================

class DateTimeInput(BaseModel):
    """时间日期查询输入参数"""
    query_type: str = Field(
        description="查询类型：'current'(当前时间), 'format'(格式化时间), 'calculate'(时间计算)"
    )
    format_string: Optional[str] = Field(
        default=None,
        description="时间格式字符串，例如：'%Y-%m-%d %H:%M:%S'"
    )
    days_offset: Optional[int] = Field(
        default=None,
        description="天数偏移量，正数表示未来，负数表示过去"
    )

@tool("datetime_query", args_schema=DateTimeInput)
def get_datetime_info(query_type: str, format_string: str = None, days_offset: int = None) -> str:
    """
    查询时间日期信息
    
    Args:
        query_type: 查询类型
        format_string: 时间格式
        days_offset: 天数偏移
    
    Returns:
        时间信息
    """
    now = datetime.now()
    
    if query_type == "current":
        return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    elif query_type == "format":
        if format_string:
            try:
                return f"格式化时间: {now.strftime(format_string)}"
            except Exception as e:
                return f"格式化错误: {str(e)}"
        else:
            return "请提供格式字符串"
    
    elif query_type == "calculate":
        if days_offset is not None:
            target_date = now + timedelta(days=days_offset)
            return f"计算结果: {target_date.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return "请提供天数偏移量"
    
    else:
        return "不支持的查询类型"


# ================================
# 4. 文本处理工具
# ================================

class TextProcessInput(BaseModel):
    """文本处理输入参数"""
    text: str = Field(description="要处理的文本内容")
    operation: str = Field(
        description="处理操作：'count'(统计), 'upper'(转大写), 'lower'(转小写), 'reverse'(反转), 'split'(分割)"
    )
    separator: Optional[str] = Field(
        default=" ",
        description="分割符，用于split操作"
    )

@tool("text_processor", args_schema=TextProcessInput)
def process_text(text: str, operation: str, separator: str = " ") -> str:
    """
    处理文本内容
    
    Args:
        text: 文本内容
        operation: 处理操作
        separator: 分割符
    
    Returns:
        处理结果
    """
    if operation == "count":
        return f"文本统计:\n字符数: {len(text)}\n单词数: {len(text.split())}\n行数: {len(text.splitlines())}"
    
    elif operation == "upper":
        return f"转大写: {text.upper()}"
    
    elif operation == "lower":
        return f"转小写: {text.lower()}"
    
    elif operation == "reverse":
        return f"反转文本: {text[::-1]}"
    
    elif operation == "split":
        parts = text.split(separator)
        return f"分割结果: {parts}"
    
    else:
        return "不支持的操作类型"


# ================================
# 5. 随机数生成工具
# ================================

class RandomInput(BaseModel):
    """随机数生成输入参数"""
    type: str = Field(
        description="随机类型：'int'(整数), 'float'(浮点数), 'choice'(从列表选择), 'uuid'(UUID)"
    )
    min_value: Optional[int] = Field(default=1, description="最小值（用于int类型）")
    max_value: Optional[int] = Field(default=100, description="最大值（用于int类型）")
    choices: Optional[List[str]] = Field(default=None, description="选择列表（用于choice类型）")

@tool("random_generator", args_schema=RandomInput)
def generate_random(type: str, min_value: int = 1, max_value: int = 100, choices: List[str] = None) -> str:
    """
    生成随机数或随机选择
    
    Args:
        type: 随机类型
        min_value: 最小值
        max_value: 最大值
        choices: 选择列表
    
    Returns:
        随机结果
    """
    if type == "int":
        result = random.randint(min_value, max_value)
        return f"随机整数: {result}"
    
    elif type == "float":
        result = random.uniform(min_value, max_value)
        return f"随机浮点数: {result:.2f}"
    
    elif type == "choice":
        if choices and len(choices) > 0:
            result = random.choice(choices)
            return f"随机选择: {result}"
        else:
            return "请提供选择列表"
    
    elif type == "uuid":
        import uuid
        result = str(uuid.uuid4())
        return f"UUID: {result}"
    
    else:
        return "不支持的随机类型"


# ================================
# 6. 单位转换工具
# ================================

class ConversionInput(BaseModel):
    """单位转换输入参数"""
    value: float = Field(description="要转换的数值")
    from_unit: str = Field(description="源单位")
    to_unit: str = Field(description="目标单位")
    category: str = Field(
        description="转换类别：'length'(长度), 'weight'(重量), 'temperature'(温度), 'area'(面积)"
    )

@tool("unit_converter", args_schema=ConversionInput)
def convert_units(value: float, from_unit: str, to_unit: str, category: str) -> str:
    """
    单位转换
    
    Args:
        value: 数值
        from_unit: 源单位
        to_unit: 目标单位
        category: 转换类别
    
    Returns:
        转换结果
    """
    # 长度转换（以米为基准）
    length_units = {
        "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
        "inch": 0.0254, "ft": 0.3048, "yard": 0.9144, "mile": 1609.34
    }
    
    # 重量转换（以克为基准）
    weight_units = {
        "mg": 0.001, "g": 1, "kg": 1000, "ton": 1000000,
        "oz": 28.3495, "lb": 453.592
    }
    
    # 面积转换（以平方米为基准）
    area_units = {
        "cm2": 0.0001, "m2": 1, "km2": 1000000,
        "acre": 4046.86, "hectare": 10000
    }
    
    try:
        if category == "length":
            if from_unit in length_units and to_unit in length_units:
                meters = value * length_units[from_unit]
                result = meters / length_units[to_unit]
                return f"转换结果: {value} {from_unit} = {result:.4f} {to_unit}"
        
        elif category == "weight":
            if from_unit in weight_units and to_unit in weight_units:
                grams = value * weight_units[from_unit]
                result = grams / weight_units[to_unit]
                return f"转换结果: {value} {from_unit} = {result:.4f} {to_unit}"
        
        elif category == "area":
            if from_unit in area_units and to_unit in area_units:
                square_meters = value * area_units[from_unit]
                result = square_meters / area_units[to_unit]
                return f"转换结果: {value} {from_unit} = {result:.4f} {to_unit}"
        
        elif category == "temperature":
            if from_unit == "C" and to_unit == "F":
                result = (value * 9/5) + 32
                return f"转换结果: {value}°C = {result:.2f}°F"
            elif from_unit == "F" and to_unit == "C":
                result = (value - 32) * 5/9
                return f"转换结果: {value}°F = {result:.2f}°C"
            elif from_unit == "C" and to_unit == "K":
                result = value + 273.15
                return f"转换结果: {value}°C = {result:.2f}K"
            elif from_unit == "K" and to_unit == "C":
                result = value - 273.15
                return f"转换结果: {value}K = {result:.2f}°C"
        
        return "不支持的单位转换"
    
    except Exception as e:
        return f"转换错误: {str(e)}"


# ================================
# 工具列表导出
# ================================

# 所有可用工具的列表
AVAILABLE_TOOLS = [
    get_weather,
    calculate,
    get_datetime_info,
    process_text,
    generate_random,
    convert_units
]

def get_all_tools():
    """获取所有可用工具"""
    return AVAILABLE_TOOLS

def get_tool_descriptions():
    """获取所有工具的描述信息"""
    descriptions = {}
    for tool in AVAILABLE_TOOLS:
        descriptions[tool.name] = {
            "name": tool.name,
            "description": tool.description,
            "args_schema": tool.args_schema.schema() if tool.args_schema else None
        }
    return descriptions

if __name__ == "__main__":
    # 测试工具
    print("🔧 工具测试")
    print("=" * 50)
    
    # 测试天气查询
    print("1. 天气查询测试:")
    print(get_weather.invoke({"city": "北京", "days": 3}))
    print()
    
    # 测试计算器
    print("2. 计算器测试:")
    print(calculate.invoke({"expression": "2 + 3 * 4"}))
    print(calculate.invoke({"expression": "sqrt(16) + sin(pi/2)"}))
    print()
    
    # 测试时间查询
    print("3. 时间查询测试:")
    print(get_datetime_info.invoke({"query_type": "current"}))
    print(get_datetime_info.invoke({"query_type": "calculate", "days_offset": 7}))
    print()
    
    # 测试文本处理
    print("4. 文本处理测试:")
    print(process_text.invoke({"text": "Hello World", "operation": "count"}))
    print(process_text.invoke({"text": "Hello World", "operation": "reverse"}))
    print()
    
    # 测试随机数生成
    print("5. 随机数生成测试:")
    print(generate_random.invoke({"type": "int", "min_value": 1, "max_value": 10}))
    print(generate_random.invoke({"type": "choice", "choices": ["苹果", "香蕉", "橙子"]}))
    print()
    
    # 测试单位转换
    print("6. 单位转换测试:")
    print(convert_units.invoke({"value": 100, "from_unit": "cm", "to_unit": "m", "category": "length"}))
    print(convert_units.invoke({"value": 32, "from_unit": "F", "to_unit": "C", "category": "temperature"}))