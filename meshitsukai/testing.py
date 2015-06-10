# -*- coding:utf-8 -*-
from .bot import Bot
from .plugin import PluginHandler


class DummyChannel(object):
    def __init__(self, name):
        self.name = name
        self.outputs = []

    def send_message(self, message):
        self.outputs.append(message)

    def getvalue(self):
        return self.outputs.copy()


class ChannelPool(object):
    def __init__(self, Channel, pool=None):
        self.Channel = Channel
        self.pool = pool or {}

    def find_channel(self, name):
        return self.pool.get(name)

    def create_channel(self, name):
        if self.find_channel(name) is None:
            self.pool[name] = self.Channel(name)
        return self.pool[name]


class DummyMediator(object):
    def __init__(self, source):
        self.source = source

    def read(self):
        return self.source.shift_message()

    def ping(self):
        pass

    def find_channel(self, name):
        return self.source.find_channel(name)


class DummySource(object):
    def __init__(self, pool):
        self.pool = pool
        self.queue = [[]]

    def find_channel(self, name):
        return self.pool.find_channel(name)

    def shift_message(self):
        item = self.queue[-1]
        self.queue.append([])
        return item

    def generate_channel(self, name):
        return self.pool.create_channel(name)

    def generate_message(self, text, channel="*general*", user="*user*"):
        result = {
            'ts': '1433670154.000003',
            'type': 'message',
            'team': 'XxxXXXXXX',
            'text': text,
            'user': user,
            'channel': channel
        }
        self.queue[-1].append(result)
        return result


class DummyBot(Bot):
    def _wait(self):
        pass

    def autoping(self):
        pass

    def __init__(self, mediator, plugins):
        super(DummyBot, self).__init__(mediator, plugins)


class DummyContext(object):
    debug = True


def dummy_source(pool=None):
    pool = pool or ChannelPool(DummyChannel)
    return DummySource(pool)


def dummy_bot(plugins, source):
    mediator = DummyMediator(source)
    return DummyBot(mediator, plugins)


def dummy_plugin(cls, *args, _context=None, **kwargs):
    context = _context or DummyContext()
    plugin = cls(*args, **kwargs)
    return PluginHandler(plugin, context)
