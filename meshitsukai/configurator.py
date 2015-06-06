# -*- coding:utf-8 -*-
import glob
import sys
import os
from .plugin import PluginManager
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

    @property
    def directory(self):
        return self.settings["directory"]

    @property
    def token(self):
        return self.settings["SLACK_TOKEN"]

    def load_plugins(self):
        loaded = []
        plugin_dir = os.path.join(self.directory, 'plugins')
        if not os.path.exists(plugin_dir):
            raise RuntimeError("{} is not found. as plugins directory".format(plugin_dir))
        logger.info("load-path insert: %s", plugin_dir)
        sys.path.insert(0, plugin_dir)

        for plugin in glob.glob(os.path.join(plugin_dir, "*.py")):
            if plugin.endswith("__init__.py"):
                continue
            logger.info(plugin)
            name = "plugins.{}".format(os.path.splitext(os.path.basename(plugin))[0])
            loaded.append(PluginManager(name, self.context))
        return loaded

    def make_app(self):
        plugins = self.load_plugins()
        return RtmBot(self.token, plugins)
