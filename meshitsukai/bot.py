# -*- coding:utf-8 -*-
import time
from slackclient import SlackClient
from . import logger


class SlackMediator(object):
    def __init__(self, token):
        self.token = token
        self.slack_client = SlackClient(self.token)

    def read(self):
        return self.slack_client.rtm_read()

    def ping(self):
        return self.slack_client.server.ping()

    def find_channel(self, name):
        return self.slack_client.server.channels.find(name)

    def connect(self):
        """Convenience method that creates Server instance"""
        logger.info("connect to slack ..")
        self.slack_client.rtm_connect()


class Bot(object):
    def __init__(self, mediator, plugins):
        self.last_ping = 0
        self.bot_plugins = plugins or []
        self.mediator = mediator

    def _wait(self):
        time.sleep(.1)

    def connect(self):
        self.mediator.connect()

    def start(self):
        self.connect()
        while True:
            self.run()

    def run(self):
        for reply in self.mediator.read():
            self.input(reply)
        self.crons()
        self.output()
        self.autoping()
        self._wait()

    def autoping(self):
        # hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.mediator.ping()
            self.last_ping = now

    def input(self, data):
        if "type" in data:
            function_name = "process_" + data["type"]
            logger.debug("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)

    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.mediator.find_channel(output[0])
                if channel is not None and output[1] is not None:
                    if limiter is True:
                        self._wait()
                        limiter = False
                    message = output[1]
                    channel.send_message("{}".format(message))
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
