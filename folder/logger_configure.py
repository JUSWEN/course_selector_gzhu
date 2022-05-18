import logging


def logger_configure():
    file_name = "course_selector_gzhu.log"

    file = open(file_name, "w")
    file.close()

    logger = logging.getLogger(__name__)

    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=file_name, mode="a")
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    c_format = logging.Formatter(
        '%(processName)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s - %(processName)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)


def get_logger():
    return logging.getLogger(__name__)
