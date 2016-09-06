import logging
import coloredlogs

logging.getLogger("requests").setLevel(logging.ERROR)
coloredlogs.install(level="DEBUG")

logging.getLogger("logging").debug("Init logging")


def logger(name):
    log = logging.getLogger(name)
    return log
