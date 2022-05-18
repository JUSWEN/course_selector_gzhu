import sys

from loguru import logger


def configure_logger():
    file_name = "course_selector_gzhu.log"

    file = open(file_name, "w")
    file.close()

    logger.add(sys.stderr,
               format="{process} {level} {message}",
               filter="my_module",
               level="INFO")
    logger.add(file_name,
               format="{time} {process} {level} {message}",
               enqueue=True,
               encoding='utf-8',
               level="DEBUG")


def get_logger():
    return logger
