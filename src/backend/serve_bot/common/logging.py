import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

# 确保日志目录存在
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../temp/logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 定义日志格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def init_logging():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="D", interval=1, backupCount=7, encoding="utf-8")
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        handlers=[
                            file_handler,
                            logging.StreamHandler(sys.stdout)
                        ])
