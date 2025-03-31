import logging
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, interrupt

from src.backend.serve_bot.chat_manage.chat_state import ChatState

logger = logging.getLogger(__name__)


class HumanInterruptAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal["KeyInformationExtractionAgent"]]:
        logger.info("HumanInterruptAgent run: %s ", config["configurable"]["user_id"])
        human_response = interrupt({"question": state["to_human_question"]})
        logger.info("human_response: %s", human_response)
        return Command(
            goto=state['interrupt_from_agent'],
            update={
                "messages": [
                    {
                        "role": "user",
                        "content": human_response,
                    },
                ],
            }
        )
