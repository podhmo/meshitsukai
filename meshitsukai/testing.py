# -*- coding:utf-8 -*-
from .bot import Bot
from .plugin import PluginHandler


class DummyChannel(object):
    def __init__(self, name, cont=None):
        self.name = name
        self.outputs = []
        self.cont = cont

    def send_message(self, message):
        self.outputs.append(message)
        if self.cont is not None:
            self.cont(message)

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

    def __iter__(self):
        for ch in sorted(self.pool.values(), key=lambda ch: ch.name):
            yield ch


class DummyTimeKeeper(object):
    def wait(self):
        pass

    def __next__(self):
        return None

    def __iter__(self):
        return self


class DummyMediator(object):
    def __init__(self, source, time_keeper=None):
        self.source = source
        self.time_keeper = time_keeper or DummyTimeKeeper()

    def time_keeping(self):
        return iter(self.time_keeper)

    def wait(self):
        self.time_keeper.wait()

    def read(self):
        return self.source.shift_message()

    def send(self, output, wait_itr):
        channel_id, message = output
        channel = self.find_channel(channel_id)
        if channel is not None and message is not None:
            next(wait_itr)
            channel.send_message(message)

    def ping(self):
        pass

    def find_channel(self, name):
        return self.source.find_channel(name)

    def connect(self):
        pass


class DummySource(object):
    def __init__(self, pool):
        self.pool = pool
        self.queue = [[]]

    def find_channel(self, name):
        return self.pool.find_channel(name)

    def shift_message(self):
        item = self.queue[-1]
        if item:
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


class DummyContext(object):
    debug = True


def dummy_source(pool=None, Channel=DummyChannel):
    pool = pool or ChannelPool(Channel)
    return DummySource(pool)


def dummy_bot(plugins, source, time_keeper=None):
    mediator = DummyMediator(source, time_keeper=time_keeper)
    return Bot(mediator, plugins)


def dummy_plugin(cls, *args, _context=None, **kwargs):
    context = _context or DummyContext()
    plugin = cls(*args, **kwargs)
    return PluginHandler(plugin, context)
