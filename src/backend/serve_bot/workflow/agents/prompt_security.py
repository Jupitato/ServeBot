import logging
import traceback
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.backend.serve_bot.chat_manage.chat_state import ChatState

logger = logging.getLogger(__name__)


class PromptSecurityAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal["IntentRecognitionAgent"]]:
        logger.info("PromptSecurityAgent run: %s", config["configurable"]["user_id"])
        try:
            return Command(goto="IntentRecognitionAgent")
        except BaseException as e:
            traceback_info = traceback.format_exc()
            logger(traceback_info)
