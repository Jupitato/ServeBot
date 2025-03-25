from __future__ import annotations

import uuid
from typing import Dict, Union

from fastapi import APIRouter, HTTPException
from langgraph.types import Command
from pydantic import BaseModel, Field

from src.backend.serve_bot.workflow.serve_bot import ServeBot

chat_router = APIRouter()


# 定义请求体数据模型
class ChatRequest(BaseModel):
    session_id: Union[str, None] = Field(
        default=None,
        # alias="sessionId",  # 支持前端使用camelCase
        description="会话ID（首次请求不需要传）"
    )
    messages: list = Field(..., min_length=1, description="用户输入的消息内容")
    interrupt_flag: Union[bool, None] = Field(
        default=None,
        description="和前端交互判断是回复中断还是新的"
    )


sessions: Dict[str, ServeBot] = {}


@chat_router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        prompt = request.messages[-1]['content']
        # 获取或创建会话
        if not request.session_id or request.session_id not in sessions:
            # 新会话初始化
            session_id = str(uuid.uuid4())
            bot = ServeBot(user_id="luxun")
            sessions[session_id] = bot
            # 执行任务
            await bot.run_chat(task_id=session_id, prompt=prompt)

        else:
            # 恢复已有会话
            session_id = request.session_id
            bot = sessions[session_id]
            config = bot.graph.config
            # 中断中恢复
            if request.interrupt_flag:
                await bot.graph.ainvoke(
                    Command(resume=request.messages[-1]['content']),
                    config=config
                )
            else:
                # 新任务
                await bot.graph.ainvoke({"prompt": prompt},
                                        config=config
                                        )

        # 所有的任务结果状态统一从state获取
        agent_state = await bot.graph.aget_state(config=bot.graph.config)
        if agent_state.tasks:
            reply = agent_state.tasks[0].interrupts[0].value["question"]
            interrupt_flag = True
        else:
            # 消息列表中的最后一条消息应该是机器人最后一次回复
            reply = agent_state.values["messages"][-1].content
            interrupt_flag = False
        return {
            "session_id": session_id,
            "reply": reply.replace("<think>", "[思考开始]").replace("</think>", "[思考结束]"),
            "interrupt_flag": interrupt_flag
        }

    except KeyError as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"无效的会话ID: {request.session_id}")
    except Exception as e:
        sessions.pop(session_id, None)  # 清理异常会话
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
