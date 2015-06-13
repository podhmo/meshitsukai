# -*- coding:utf-8 -*-
from . import logger
from .job import Job
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager


class Plugin(IPlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.crontable = []
        self.outputs = []
        self.config = None

    @property
    def section_name(self):
        return self.__class__.__name__.lower()

    def setup(self, context):
        self.context = context
        try:
            self.settings = context.config[self.section_name]
        except KeyError:
            self.settings = {}

    def catch_all(self, data):
        pass


class PluginHandler(object):
    def __init__(self, plugin, context):
        self.context = context

        self.plugin = plugin
        self.jobs = []
        self.outputs = []

        self.setup()

    def setup(self):
        self.plugin.setup(self.context)
        self.register_jobs()

    def register_jobs(self):
        for interval, function in self.plugin.crontable:
            self.jobs.append(Job(interval, getattr(self.plugin, function), self.context))
            logger.info(self.plugin.crontable)
            self.plugin.crontable = []

    def do(self, function_name, data):
        logger.debug("do -- %s (plugin=%s)", function_name, self.plugin.__class__.__name__)
        if hasattr(self.plugin, function_name):
            if not self.context.debug:
                try:
                    getattr(self.plugin, function_name)(data)
                except:
                    logger.debug("problem in module {} {}".format(function_name, data))
            else:
                getattr(self.plugin, function_name)(data)
        if hasattr(self.plugin, "catch_all"):
            try:
                self.plugin.catch_all(data)
            except:
                logger.debug("problem in catch all")

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        for out in self.plugin.outputs:
            output.append(out)
        self.plugin.outputs = []
        return output
