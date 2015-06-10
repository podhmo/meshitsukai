# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin
from meshitsukai.view import as_view


class DummyPlugin(Plugin):
    @as_view()
    def process_message(self, request):
        print("---------- incomming: ----------")
        # data : {'ts': '1433670154.000003', 'type': 'message', 'team': 'XxxXXXXXX', 'text': 'aa', 'user': 'XxxXXxxXX', 'channel': 'XxxXXXXXx'}
        print(request._rawdata)
        print("--------------------------------")
        return "`*dummy*`"
