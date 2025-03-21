import asyncio
from backend.serve_bot.workflow import serve_bot

if __name__ == "__main__":
    asyncio.run(serve_bot.main())
