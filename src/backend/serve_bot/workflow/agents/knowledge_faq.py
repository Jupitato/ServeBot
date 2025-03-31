import logging
import traceback
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langgraph.types import Command

from src.backend.serve_bot.chat_manage.chat_state import ChatState
from src.backend.serve_bot.rag.context import MyStorageContext
from src.backend.serve_bot.rag.query.query_store import query_from_vector_store

logger = logging.getLogger(__name__)

storage_context = MyStorageContext.storageContext()


class KnowledgeFaqAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal[END]]:
        logger.info("KnowledgeFaqAgent run: %s", config["configurable"]["user_id"])
        try:
            response = query_from_vector_store(storage_context.vector_store, prompt=state["prompt"])
            state.setdefault("messages", []).extend([
                AIMessage(content=response)  # 添加AI响应
            ])
            return Command(goto=END, update={"messages": state['messages']})
        except BaseException as e:
            traceback_info = traceback.format_exc()
            logger(traceback_info)
