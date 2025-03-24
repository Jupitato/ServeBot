import json
import re


def extract_answer(input_str, keys=None):
    """
    从输入字符串中提取JSON数据，并返回指定键的值

    Args:
        input_str: 包含JSON数据的字符串
        keys: 要提取的键列表，如果为None则提取所有键值

    Returns:
        如果指定了keys，返回按keys顺序排列的值列表
        如果未指定keys，返回整个解析后的字典
    """
    try:
        #  先去除 <think> </think> 标签
        cleaned = re.sub(r"<think>.*?</think>", "", input_str, flags=re.DOTALL).strip()

        # 使用正则表达式匹配被```json包裹的JSON内容
        match = re.search(r'```json(.*?)```', cleaned, re.DOTALL)
        if not match:
            return None if keys else {}
        json_str = match.group(1).strip()

        # 解析JSON字符串为字典
        data = json.loads(json_str)

        # 如果没有指定keys，返回整个字典
        if keys is None:
            return data

        # 如果指定了keys，返回对应的值列表
        return [data.get(key) for key in keys]
    except (json.JSONDecodeError, AttributeError) as e:
        # 处理可能的异常，如JSON解析错误、正则未匹配
        print(f"Error occurred: {e}")
        return None if keys else {}
