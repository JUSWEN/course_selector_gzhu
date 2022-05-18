import logging


def logger_configure():
    logger = logging.getLogger(__name__)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename="course_selector_gzhu.log",
                                    mode="a")
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

    return logger
