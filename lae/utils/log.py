# -*- coding: utf8 -*-
import logging

from .colorlog import ColorizingStreamHandler


def _init_logger(logger):
    logger.handlers = []
    logger.propagate = False
    color_hdl = ColorizingStreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(message)s")
    color_hdl.setFormatter(formatter)
    logger.addHandler(color_hdl)

logger = logging.getLogger(__name__)
_init_logger(logger)
