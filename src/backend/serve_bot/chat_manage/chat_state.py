from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import MessagesState, add_messages


class ChatState(MessagesState):
    # 每次更新只增加messages
    messages: Annotated[list[AnyMessage], add_messages]
    prompt: str
    current_intent: str
    user_key_info: str
    to_human_question: str
    interrupt_from_agent: str
