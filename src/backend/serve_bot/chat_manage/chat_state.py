from enum import Enum
from typing import Annotated

from langchain_core.messages import AnyMessage

from langgraph.graph.message import MessagesState, add_messages
class ChatState(MessagesState):
    # 每次更新只增加messages
    messages: Annotated[list[AnyMessage], add_messages]