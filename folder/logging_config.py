import logging


def configure_logger():
    # create logger
    logger = logging.getLogger('logger1')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to handler
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch, fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
