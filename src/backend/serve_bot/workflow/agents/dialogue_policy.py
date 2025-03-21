

import logging

from langchain_core.runnables import RunnableConfig

from backend.serve_bot.chat_manage.chat_state import ChatState
from langgraph.types import Command
from typing import Literal

logger = logging.getLogger(__name__)

class DialoguePolicyAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal["ActionRunnerAgent"]]:
        logger("DialoguePolicyAgent run: ", config["configurable"]["user_id"])

        try:
            return Command(goto="ActionRunnerAgent")
        except BaseException as e:
            logger(e)