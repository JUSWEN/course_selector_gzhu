import logging


def configure_logger():
    # Create a logger
    logger = logging.getLogger()

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("course_selector_gzhu.log")
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter(
        ' %(threadName)s -%(levelname)s - %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s  -%(threadName)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
