import sys

from loguru import logger


def configure_logger():
    file_name = "log.log"

    logger.remove()
    logger.add(sys.stderr,
               colorize=True,
               enqueue=True,
               format="<magenta>{process}</magenta>| "
               "<level>{level}</level>| "
               "<level>{message}</level>",
               level="INFO")
    logger.add(
        file_name,
        format="{time:MM-DD at HH:mm:ss}| {process}| {level}| {message}",
        enqueue=True,
        encoding='utf-8',
        level="DEBUG",
        rotation="2 days")
