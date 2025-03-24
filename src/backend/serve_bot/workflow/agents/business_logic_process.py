import logging
import traceback
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langgraph.types import Command

from src.backend.serve_bot.chat_manage.chat_state import ChatState
from src.backend.serve_bot.rag.context import MyStorageContext

logger = logging.getLogger(__name__)

storage_context = MyStorageContext.storageContext()


class BusinessLogicProcessAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal[END]]:
        logger.info("BusinessLogicProcessAgent run: %s", config["configurable"]["user_id"])

        try:
            intent = state['current_intent']
            user_key_info = state['user_key_info']

            # 模拟处理结果
            state.setdefault("messages", []).extend([
                AIMessage(content="这是我出来的结果，你看下")  # 添加AI响应
            ])
            return Command(goto=END, update={"messages": state['messages']})
        except BaseException as e:
            traceback_info = traceback.format_exc()
            logger(traceback_info)
