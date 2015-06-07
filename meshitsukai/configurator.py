# -*- coding:utf-8 -*-
import os
from configparser import ConfigParser
from .plugin import PluginHandler, PluginManager
from .bot import RtmBot
from . import logger


class Context(object):
    section_name = "app"

    def __init__(self, config):
        self.config = config
        self.manager = PluginManager(plugin_info_ext="plugin")

    def __getitem__(self, k):
        return self.config.get(self.section_name, k)

    @property
    def is_daemon(self):
        return self.config.getboolean(self.section_name, "DAEMON", fallback=False)

    @property
    def debug(self):
        return self.config.getboolean(self.section_name, "DEBUG", fallback=False)

    @property
    def plugin_directory(self):
        return self["plugin_directory"]

    @property
    def token(self):
        return self["slack_token"]

    def setup(self):
        self.manager.setPluginPlaces([self.plugin_directory])
        self.manager.collectPlugins()


class Configurator(object):
    def __init__(self, config):
        self.config = config
        self.context = Context(config)
        self.context.setup()

    @classmethod
    def from_ini_file(cls, filename):
        parser = ConfigParser(default_section=Context.section_name)
        with open(filename) as rf:
            parser.readfp(rf)
            # roughly hack, want to %(here)s behaviour of pyramid's settings file.
            parser.set(Context.section_name, "here", os.path.abspath(os.path.dirname(filename)))
        return cls(parser)

    @classmethod
    def from_dict(cls, settings, filename=""):
        parser = ConfigParser(settings, default_section=Context.section_name)
        parser.set(Context.section_name, "here", filename)
        return cls(parser)

    def load_plugins(self):
        loaded = []
        for plugin in self.context.manager.getAllPlugins():
            logger.info("loaded plugin: %s", plugin.name)
            loaded.append(PluginHandler(plugin.plugin_object, self.context))
        return loaded

    def make_app(self):
        plugins = self.load_plugins()
        return RtmBot(self.context.token, plugins)
