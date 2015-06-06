# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
debug = True


def dbg(debug_string):
    if debug:
        logger.info(debug_string)
