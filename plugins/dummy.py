# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin


class DummyPlugin(Plugin):
    # ## instance variables ##
    # self.outputs
    # self.crontable

    def process_message(self, data):
        print("---------- incomming: ----------")
        # data : {'ts': '1433670154.000003', 'type': 'message', 'team': 'XxxXXXXXX', 'text': 'aa', 'user': 'XxxXXxxXX', 'channel': 'XxxXXXXXx'}
        print(data)
        print("--------------------------------")
        self.outputs.append((data["channel"], "`*dummy*`"))
