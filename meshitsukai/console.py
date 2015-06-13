# -*- coding:utf-8 -*-
from cmd import Cmd


class Console(Cmd):
    def __init__(self, source, channel, user="YOU", completekey='tab', stdin=None, stdout=None):
        self.source = source
        self.current = channel
        self.user = user
        super(Console, self).__init__(completekey, stdin, stdout)

    @property
    def prompt(self):
        return "#{}:".format(self.current.name)

    def do_EOF(self, line):
        return True

    def emptyline(self):
        pass

    def default(self, line):
        self.current.send_message(line)
        self.source.generate_message(line, channel=self.current.name, user=self.user)

    def do_list(self, line):
        for c in self.source.pool:
            print("- {}".format(c.name))

    def do_channel(self, name):
        channel = self.source.generate_channel(name)
        if channel:
            self.current = channel

    def do_history(self, line):
        for line in self.current.outputs:
            print(line)


def main(configurator, plugins):
    from meshitsukai.testing import dummy_source, DummyChannel
    from meshitsukai.console import Console
    from functools import partial
    import threading

    def cont(message):
        print("\n\t{}".format("\n\t".join(message.split("\n"))))

    source = dummy_source(Channel=partial(DummyChannel, cont=cont))
    default_channel = source.generate_channel("general")
    bot = configurator.make_console_app(plugins, source)
    t = threading.Thread(target=bot.start)
    t.start()  # orphan?
    console = Console(source, default_channel)
    console.cmdloop()


if __name__ == "__main__":
    from meshitsukai.testing import dummy_source
    source = dummy_source()
    channel = source.generate_channel("general")
    console = Console(source, channel)
    console.cmdloop()
