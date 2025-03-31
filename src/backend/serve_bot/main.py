import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from langchain.globals import set_debug, set_verbose

from src.backend.serve_bot.common.logging import init_logging
from src.backend.serve_bot.rag.context import init_rag_settings
from src.backend.serve_bot.web_server.api.endpoint.chat import chat_router

init_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPII应用程序 生命周期事件"""
    logger.info("🚀初始化RAG上下文配置...")
    init_rag_settings()

    yield  # 这里会进入 FastAPI 运行阶段

    logger.info("🛑FastAPI应用程序结束...")


set_debug(True)
set_verbose(True)
app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, tags=["chat"])

# 通过mitmproxy代理拦截流量
os.environ["HTTP_PROXY"] = "http://localhost:8080"
# os.environ["HTTPS_PROXY"] = "http://localhost:8080"

if __name__ == "__main__":
    # 启动服务，默认监听 http://127.0.0.1:8000
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
