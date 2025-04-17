# 存储活跃的WebSocket连接
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any

from fastapi import APIRouter
from langgraph.types import Command
from starlette.websockets import WebSocketDisconnect, WebSocket

from src.backend.serve_bot.web_server.dto.web_dtos import ChatRequestMessage
from src.backend.serve_bot.workflow.serve_bot import ServeBot

chat2_router = APIRouter()

# 存储活跃的WebSocket连接
active_connections: Dict[str, WebSocket] = {}

# 模拟消息历史记录
chat_history: Dict[str, List[Dict[str, Any]]] = {}

bot = ServeBot(user_id="luxun")



def create_welcome_message():
    return {
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": "我是ServeBot，很高兴见到你！\n\n我可以帮助你解决问题，请告诉我你需要什么帮助。",
        "timestamp": datetime.now().isoformat()
    }


@chat2_router.get("/")
async def root():
    return {"message": "欢迎使用ServeBot API"}


@chat2_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()

    if client_id not in chat_history:
        chat_history[client_id] = []
        # 添加欢迎消息
        welcome_message = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": "我是ServeBot，很高兴见到你！\n\n我可以帮助你解决问题，请告诉我你需要什么帮助。",
            "timestamp": datetime.now().isoformat()
        }
        chat_history[client_id].append(welcome_message)
        await websocket.send_text(json.dumps(welcome_message))
    else:
        # 发送历史消息
        for message in chat_history[client_id]:
            await websocket.send_text(json.dumps(message))

    active_connections[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            # 使用 ChatRequest DTO 反序列化消息数据
            chat_request = ChatRequestMessage.model_validate_json(data)

            # 生成统一的消息ID
            message_id = str(uuid.uuid4())

            # 用户消息（使用统一ID）
            user_message = {
                "id": message_id,  # 使用统一ID
                "role": "user",
                "content": chat_request.content,
                "timestamp": datetime.now().isoformat()
            }
            chat_history[client_id].append(user_message)

            # 立即发送用户消息回前端
            await websocket.send_text(json.dumps(user_message))

            config = {
                "configurable": {
                    "thread_id": client_id,
                    "user_id": "luxun"
                }
            }

            if chat_request.interrupt_flag:
                await bot.graph.ainvoke(
                    Command(resume=user_message["content"]),
                    config=config
                )
            else:
                # 新任务
                await bot.graph.ainvoke({"prompt": user_message["content"]},
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

            # AI回复
            ai_response = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": reply,
                "timestamp": datetime.now().isoformat(),
                "interrupt_flag": interrupt_flag
            }
            chat_history[client_id].append(ai_response)
            await websocket.send_text(json.dumps(ai_response))

    except WebSocketDisconnect:
        if client_id in active_connections:
            del active_connections[client_id]


@chat2_router.get("/api/history/{client_id}")
async def get_chat_history(client_id: str):
    if client_id not in chat_history:
        return {"messages": []}
    return {"messages": chat_history[client_id]}


@chat2_router.delete("/api/history/{client_id}")
async def clear_chat_history(client_id: str):
    if client_id in chat_history:
        chat_history[client_id] = []
        # 添加新的欢迎消息
        welcome_message = create_welcome_message()
        chat_history[client_id].append(welcome_message)
        # 如果客户端当前已连接，发送欢迎消息
        if client_id in active_connections:
            await active_connections[client_id].send_text(json.dumps(welcome_message))
    return {"status": "success"}
