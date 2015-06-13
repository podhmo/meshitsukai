# -*- coding:utf-8 -*-
import time
from slackclient import SlackClient
from . import logger


class _TimeKeeper(object):
    def __init__(self, delta=0.1):
        self.need_wait = False
        self.delta = delta

    def wait(self):
        time.sleep(self.delta)

    def reset(self):
        self.need_wait = False

    def __iter__(self):
        while True:
            if self.need_wait is True:
                self.wait()
                self.need_wait = False
            yield
            self.need_wait = True


class SlackMediator(object):
    def __init__(self, token):
        self.token = token
        self.slack_client = SlackClient(self.token)
        self.time_keeper = _TimeKeeper()

    def time_keeping(self):
        self.time_keeper.reset()
        return iter(self.time_keeper)

    def wait(self):
        self.time_keeper.wait()

    def read(self):
        return self.slack_client.rtm_read()

    def send(self, output, wait_itr):
        channel_id, message = output
        channel = self.find_channel(channel_id)
        if channel is not None and message is not None:
            next(wait_itr)
            channel.send_message(message)

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
        self.mediator.wait()

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
        wait_itr = self.mediator.time_keeping()  # xxx
        for plugin in self.bot_plugins:
            for output in plugin.do_output():
                self.mediator.send(output, wait_itr)

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
