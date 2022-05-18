import sys

from loguru import logger


def configure_logger():
    file_name = "log.log"

    file = open(file_name, "w")
    file.close()

    logger.remove()
    logger.add(sys.stderr,
               colorize=True,
               enqueue=True,
               format="<level>{level}</level>| "
               "<magenta>{time:YYYY-MM-DD}</magenta>| "
               "<level>{message}</level>",
               level="INFO")
    logger.add(file_name,
               format="{time}| {process}| {level}| {message}",
               enqueue=True,
               encoding='utf-8',
               level="DEBUG")


def get_logger():
    return logger
