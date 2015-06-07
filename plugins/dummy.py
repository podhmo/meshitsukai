# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin


class DummyPlugin(Plugin):
    # ## instance variables ##
    # self.outputs
    # self.crontable

    def process_message(self, data):
        print("---------- incomming: ----------")
        print(data)
        print("--------------------------------")
        self.outputs.append((data["channel"], "`*dummy*`"))
