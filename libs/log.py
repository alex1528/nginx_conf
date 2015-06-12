#-*- coding: utf-8 -*-

import os
import logging

from web.const import LOG_DIR
from web.const import LOG_FILE


def get_logger(name):
    logger_ = logging.getLogger(name)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-8s] [%(name)-8s] %(message)s', '%Y-%m-%d %H:%M:%S',)
    handler = logging.FileHandler(LOG_DIR + "/" + LOG_FILE)
    handler.setFormatter(formatter)
    logger_.addHandler(handler)
    logger_.setLevel(logging.DEBUG)
    return logger_

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
