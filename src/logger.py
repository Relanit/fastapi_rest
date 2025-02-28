import logging

from config import config

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger("fastapi_rest")
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
