# -*- coding:utf-8 -*-
from . import logger
from .job import Job


class PluginManager(object):
    def __init__(self, name, context):
        self.context = context

        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        settings = context.settings
        if name in settings:
            logger.info("config found for: " + name)
            self.module.config = settings[name]
        if 'setup' in dir(self.module):
            self.module.setup()

    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module." + function), self.context))
            logger.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []

    def do(self, function_name, data):
        if function_name in dir(self.module):
            # this makes the plugin fail with stack trace in debug mode
            if not self.settings.get("debug"):
                try:
                    eval("self.module." + function_name)(data)
                except:
                    logger.debug("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module." + function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                logger.debug("problem in catch all")

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logger.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output
