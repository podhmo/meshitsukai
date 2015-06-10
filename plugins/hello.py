# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin
from meshitsukai.view import as_view


class HelloPlugin(Plugin):
    def in_hello(self, request):
        return "hello" in request.body.lower()

    @as_view(predicate="in_hello")
    def process_message(self, request):
        return "<@{user}> `*hello*`".format(user=request.user)
