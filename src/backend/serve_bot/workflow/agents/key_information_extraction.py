import logging
import traceback
from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.errors import GraphInterrupt
from langgraph.types import Command

from src.backend.serve_bot.chat_manage.chat_state import ChatState
from src.backend.serve_bot.common.utils.llm_response_parse import extract_answer

logger = logging.getLogger(__name__)


class KeyInformationExtractionAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal["BusinessLogicProcessAgent"]]:
        try:
            logger.info("BusinessLogicProcessAgent run: %s", config["configurable"]["user_id"])
            # 获取过滤后的对话历史（仅保留用户消息）
            chat_history = [
                msg for msg in state.get("messages", [])
                if isinstance(msg, HumanMessage)
            ]

            messages = [
                SystemMessage(content=KeyInformationExtractionPrompt),  # 当前最新系统提示
                HumanMessage(content="current_intent=" + state["current_intent"]),  # 当前意图
                *chat_history,  # 注入过滤后的对话历史
            ]
            response = await self.llm.ainvoke(messages)
            # 存储对话记录到state
            state.setdefault("messages", []).extend([
                AIMessage(content=response.content)  # 添加AI响应
            ])
            extracted_data = extract_answer(response.content)
            # 提取后的处理逻辑
            user_key_info = {
                "order_number": extracted_data.get("order_number", ""),
                "phone_number": extracted_data.get("phone_number", ""),
                "tracking_number": extracted_data.get("tracking_number", ""),
                "email": extracted_data.get("email", ""),
                "check_info": extracted_data.get("check_info", ""),
                "requires_additional_info": extracted_data.get("requires_additional_info", False)
            }

            if user_key_info["requires_additional_info"]:
                return Command(goto="HumanInterruptAgent",
                               update={"user_key_info": user_key_info,
                                       "to_human_question": user_key_info["check_info"],
                                       "goto": "KeyInformationExtractionAgent", "messages": state["messages"]})
            else:
                return Command(goto="BusinessLogicProcessAgent", update={"user_key_info": user_key_info, "messages": state["messages"]})
        except GraphInterrupt as e:
            logger.error("GraphInterrupt occurred")
            raise e
        except BaseException as e:
            traceback_info = traceback.format_exc()
            logger.error(traceback_info)

    def get_required_fields(self, intent: str) -> list:
        """根据意图返回必要字段列表"""
        field_map = {
            "order_inquiry": ["order_number"],
            "logistics_tracking": ["tracking_number"],
            "payment_invoice": ["order_number", "phone_number"],
            "after_sale": ["order_number", "phone_number"]
        }
        return field_map.get(intent, [])


KeyInformationExtractionPrompt = """你是客服机器人的「关键信息提取模块」。

你的任务是根据给定的 `current_intent`，从用户输入中提取所需的关键信息，并按固定格式返回一个 JSON 对象。

当前支持的意图如下（仅支持以下四种）：
  1) `order_inquiry`（订单查询） → 需要「订单号」
  2) `logistics_tracking`（物流跟踪） → 需要「物流单号」
  3) `payment_invoice`（支付发票） → 需要「订单号」和「手机号」
  4) `after_sale`（售后服务） → 需要「订单号」和「联系方式（手机号或邮箱）」

提取规则如下：
- 如果 `current_intent` **不是以上四种之一**，则不提取任何信息，所有字段填空字符串，`requires_additional_info` 为 false，`check_info` 也置空。
- 如果 `current_intent` 是上述之一：
  - 且用户输入中 **缺失所需字段**，请在 `check_info` 字段中给出**简洁自然的追问语句**，并设置 `requires_additional_info` 为 true；
  - 且用户输入中 **提供了所有所需字段**，请在 `check_info` 字段中给出**确认信息的话术**，并设置 `requires_additional_info` 为 false。

始终返回以下结构化 JSON，字段不可缺失，值不存在时填空字符串：

```json
{
    "order_number": "",
    "phone_number": "",
    "tracking_number": "",
    "email": "",
    "check_info": "",
    "requires_additional_info": true
}
"""
