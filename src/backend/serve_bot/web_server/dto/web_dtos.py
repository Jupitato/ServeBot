from typing import Union

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: Union[str, None] = Field(default=None, description="用户ID")
    content: Union[str, None] = Field(default=None, description="用户输入的消息内容")
    interrupt_flag: Union[bool, None] = Field(
        default=None,
        description="和前端交互判断是回复中断还是新的"
    )
