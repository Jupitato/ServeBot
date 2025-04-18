from __future__ import annotations

import logging
from typing import Dict, Union

from fastapi import APIRouter, HTTPException
from langgraph.types import Command
from pydantic import BaseModel, Field

from src.backend.serve_bot.workflow.serve_bot import ServeBot

logger = logging.getLogger(__name__)


chat_router = APIRouter()


# 定义请求体数据模型
class ChatMessageRequest(BaseModel):
    chat_id: str = Field(
        default=None,
        alias="chatId",  # 支持前端使用camelCase
        description="对话ID"
    )
    message: str = Field(description="用户输入的消息内容")
    interrupt_flag: Union[bool, None] = Field(
        default=None,
        description="和前端交互判断是回复中断还是新的"
    )


sessions: Dict[str, ServeBot] = {}

bot = ServeBot(user_id="luxun")

@chat_router.post("/chat")
async def chat_endpoint(chatMessageRequest: ChatMessageRequest):
    session_id = None
    try:
        user_message = chatMessageRequest.message
        chat_id = chatMessageRequest.chat_id
        config = {
            "configurable": {
                "thread_id": chat_id,
                "user_id": "luxun"
            }
        }

        if chatMessageRequest.interrupt_flag:
            await bot.graph.ainvoke(
                Command(resume=user_message),
                config=config
            )
        else:
            # 新任务
            await bot.graph.ainvoke({"prompt": user_message},
                                    config=config
                                    )
        
        agent_state = await bot.graph.aget_state(config=config)
        if agent_state.tasks:
            reply = agent_state.tasks[0].interrupts[0].value["question"]
            interrupt_flag = True
        else:
            # 消息列表中的最后一条消息应该是机器人最后一次回复
            reply = agent_state.values["messages"][-1].content
            interrupt_flag = False
        return {
            "response_msg": reply.replace("<think>", "[思考开始]").replace("</think>", "[思考结束]"),
            "interrupt_flag": interrupt_flag
        }

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
