import logging


def get_logger(name: str):
    name = name.split('.')[-1]
    a_logger = logging.getLogger(name)

    return a_logger
