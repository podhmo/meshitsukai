# -*- coding:utf-8 -*-
import time
from slackclient import SlackClient
from . import logger


class RtmBot(object):
    def __init__(self, token, plugins):
        self.last_ping = 0
        self.token = token
        self.bot_plugins = plugins or []
        self.slack_client = None

    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()

    def start(self):
        self.connect()
        while True:
            for reply in self.slack_client.rtm_read():
                self.input(reply)
            self.crons()
            self.output()
            self.autoping()
            time.sleep(.1)

    def autoping(self):
        # hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.slack_client.server.ping()
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
                channel = self.slack_client.server.channels.find(output[0])
                if channel is not None and output[1] is not None:
                    if limiter is True:
                        time.sleep(.1)
                        limiter = False
                    message = output[1].encode('ascii', 'ignore')
                    channel.send_message("{}".format(message))
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
