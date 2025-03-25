from typing import Annotated

from fastapi import requests
from langchain_core.tools import tool


@tool(name_or_callable="order_query", description="查询订单详情")
def order_query_tool(order_id: Annotated[str, "订单号"]):
    """查询订单详情"""
    try:
        # 模拟网络延迟
        import time
        time.sleep(0.5)

        # 模拟响应数据
        mock_response = {
            "order_id": order_id,
            "status": "已发货",
            "create_time": "2024-03-24 10:30:00",
            "total_amount": "¥299.00",
            "items": [
                {
                    "name": "商品A",
                    "quantity": 1,
                    "price": "¥299.00"
                }
            ],
            "shipping_info": {
                "carrier": "顺丰快递",
                "tracking_number": "SF1234567890"
            }
        }

        return mock_response

    except requests.RequestException as e:
        # 异常时返回模拟数据
        return {
            "order_id": order_id,
            "status": "查询异常",
            "error": str(e)
        }


@tool(name_or_callable="logistics_query", description="查询物流信息")
def logistics_query_tool(tracking_number: Annotated[str, "物流单号"]):
    """查询物流信息"""
    try:
        # 模拟网络延迟
        import time
        time.sleep(0.5)

        # 模拟物流信息
        mock_logistics = {
            "tracking_number": tracking_number,
            "status": "运输中",
            "estimated_delivery": "2024-03-25",
            "tracking_details": [
                {
                    "time": "2024-03-24 18:30:00",
                    "location": "上海市浦东新区",
                    "status": "已发出",
                    "description": "包裹已由【上海浦东集散中心】发出"
                },
                {
                    "time": "2024-03-24 15:20:00",
                    "location": "上海市浦东新区",
                    "status": "运输中",
                    "description": "包裹已到达【上海浦东集散中心】"
                },
                {
                    "time": "2024-03-24 10:30:00",
                    "location": "上海市松江区",
                    "status": "已揽收",
                    "description": "快递员已揽收包裹"
                }
            ]
        }

        return mock_logistics

    except Exception as e:
        return {
            "tracking_number": tracking_number,
            "status": "查询异常",
            "error": str(e)
        }


@tool(name_or_callable="refund_apply", description="申请退货")
def refund_apply_tool(
        order_id: Annotated[str, "订单号"],
        reason: Annotated[str, "退货原因"],
        description: Annotated[str, "问题描述"] = ""
):
    """申请退货"""
    try:
        # 模拟网络延迟
        import time
        time.sleep(0.5)

        # 模拟退货申请响应
        mock_refund = {
            "refund_id": f"RF{int(time.time())}",
            "order_id": order_id,
            "status": "已受理",
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "reason": reason,
            "description": description,
            "next_step": "请在7天内将商品寄回，寄回地址：上海市浦东新区XX路XX号",
            "refund_amount": "¥299.00"
        }

        return mock_refund

    except Exception as e:
        return {
            "order_id": order_id,
            "status": "申请失败",
            "error": str(e)
        }


@tool(name_or_callable="complaint_feedback", description="提交投诉或反馈")
def complaint_feedback_tool(
        order_id: Annotated[str, "订单号"],
        feedback_type: Annotated[str, "反馈类型"],  # 投诉/建议/其他
        content: Annotated[str, "反馈内容"],
        contact: Annotated[str, "联系方式"] = ""
):
    """提交投诉或反馈"""
    try:
        # 模拟网络延迟
        import time
        time.sleep(0.5)

        # 模拟反馈处理响应
        mock_feedback = {
            "feedback_id": f"FB{int(time.time())}",
            "order_id": order_id,
            "type": feedback_type,
            "status": "已受理",
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": content,
            "contact": contact,
            "expected_response_time": "24小时内",
            "handler": "客服专员小王",
            "initial_response": "我们已收到您的反馈，专门客服会在24小时内与您联系处理。"
        }

        return mock_feedback

    except Exception as e:
        return {
            "order_id": order_id,
            "status": "提交失败",
            "error": str(e)
        }
