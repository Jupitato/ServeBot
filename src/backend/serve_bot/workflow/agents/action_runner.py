

import logging

from langchain_core.runnables import RunnableConfig

from backend.serve_bot.chat_manage.chat_state import ChatState
from langgraph.types import Command
from typing import Literal
from langgraph.graph import  END

logger = logging.getLogger(__name__)

class ActionRunnerAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig)-> Command[Literal[END]]:
        logger("ActionRunnerAgent run: ", config["configurable"]["user_id"])

        try:
            return Command(goto=END)
        except BaseException as e:
            logger(e)