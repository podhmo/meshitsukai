# -*- coding:utf-8 -*-
import glob
import sys
import os
from .plugin import PluginHandler, PluginManager
from .bot import RtmBot
from . import logger


class Context(object):
    def __init__(self, settings):
        self.settings = settings
        self.debug = settings.get("DEBUG", False)


class Configurator(object):
    def __init__(self, settings):
        self.settings = settings
        self.context = Context(settings)
        self.manager = PluginManager(plugin_info_ext="plugin")
        self.setup()

    def setup(self):
        self.manager.setPluginPlaces([os.path.join(self.directory, "plugins")])
        self.manager.collectPlugins()

    @property
    def directory(self):
        return self.settings["directory"]

    @property
    def token(self):
        return self.settings["SLACK_TOKEN"]

    def load_plugins(self):
        loaded = []

        for plugin in self.manager.getAllPlugins():
            logger.info("loaded plugin: %s", plugin.name)
            loaded.append(PluginHandler(plugin.plugin_object, self.context))
        return loaded

    def make_app(self):
        plugins = self.load_plugins()
        return RtmBot(self.token, plugins)
