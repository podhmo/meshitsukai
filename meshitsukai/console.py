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

    def default(self, line):
        self.current.send_message(line)

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


if __name__ == "__main__":
    from meshitsukai.testing import dummy_source
    source = dummy_source()
    channel = source.generate_channel("general")
    console = Console(source, channel)
    console.cmdloop()
