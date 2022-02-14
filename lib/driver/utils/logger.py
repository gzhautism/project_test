import logging
import logging.handlers
import os
from Config.config import setting

LOG_PATH = setting.path.cur_log_path
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


def init_logging():
    # logger = logging.root
    # use 'driver' as root logger name to prevent changing other modules' logger
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler(setting.path.cur_log_path + "\\sys.log", mode="w",
                                                        maxBytes=setting.yaml["Parameter"]["max_log_length"],
                                                        backupCount=setting.yaml["Parameter"]["backup_count"],
                                                        encoding="UTF-8")

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s] <%(module)s %(funcName)s > %(message)s'
    )
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    return logger


logger = init_logging()






