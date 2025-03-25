import logging
import traceback
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from src.backend.serve_bot.chat_manage.chat_state import ChatState
from src.backend.serve_bot.llm_manage.llm_provider import getLLM
from src.backend.serve_bot.rag.context import MyStorageContext
from src.backend.serve_bot.workflow.agent_tools.business_tools import order_query_tool, logistics_query_tool, refund_apply_tool, complaint_feedback_tool

logger = logging.getLogger(__name__)

storage_context = MyStorageContext.storageContext()


class BusinessLogicProcessAgent:
    def __init__(self, llm):
        # deepseek暂时不支持工具调用，改成qwen
        llm = getLLM(model="qwen2:7b-instruct")
        self.business_agent = create_react_agent(llm, tools=[order_query_tool, logistics_query_tool, refund_apply_tool, complaint_feedback_tool])

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal[END]]:
        logger.info("BusinessLogicProcessAgent run: %s", config["configurable"]["user_id"])

        try:
            intent = state['current_intent']
            user_key_info = state['user_key_info']
            request = {
                "messages": [
                    SystemMessage(content="你是一个客服专家，请根据用户的意图和关键信息选择合适的工具完成业务查询，根据查询结果，友好的回复用户”"),
                    HumanMessage(content=f"用户意图是{intent}，关键信息是{user_key_info}")
                ]
            }
            response = await self.business_agent.ainvoke(request)
            # 模拟处理结果
            state.setdefault("messages", []).extend([
                AIMessage(content=response["messages"][-1].content)  # 添加AI响应
            ])
            return Command(goto=END, update={"messages": state['messages']})
        except BaseException as e:
            traceback_info = traceback.format_exc()
            logger.info(traceback_info)
