# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin
from meshitsukai.view import as_view


class Hello(Plugin):
    def in_hello(self, request):
        return "hello" in request.body.lower()

    @property
    def template(self):
        return self.settings.get("template") or "hello <@{user}>"

    @as_view(predicate="in_hello")
    def process_message(self, request):
        return self.template.format(user=request.user)
