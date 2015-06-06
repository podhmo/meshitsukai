# -*- coding:utf-8 -*-
import time
from .langhelpers import debug
from . import logger


class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0

    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)

    def check(self):
        if self.lastrun + self.interval < time.time():
            if debug:
                try:
                    self.function()
                except:
                    logger.debug("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass
