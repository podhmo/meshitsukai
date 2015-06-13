# -*- coding:utf-8 -*-
from .langhelpers import reify


class Response(object):
    def __init__(self, request, body=None, channel=None):
        self.request = request
        self.channel = channel or self.request.channel
        self.buf = []
        if body:
            self.write(body)

    def write(self, line, channel=None):
        channel = channel or self.channel
        self.buf.append((channel, line))

    def on_finish(self, plugin):
        for message in self.buf:
            plugin.outputs.append(message)


class Request(object):
    def __init__(self, data):
        self._rawdata = data

    @property
    def body(self):
        return self._rawdata.get("text") or ""

    @property
    def user(self):
        return self._rawdata.get("user")

    @property
    def type(self):
        return self._rawdata.get("type")

    @property
    def channel(self):
        return self._rawdata.get("channel")

    @reify
    def response(self):
        return Response(self)

    def Response(self, *args, **kwargs):
        self.response = Response(self, *args, **kwargs)
        return self.response


def _always_true(*args, **kwargs):
    return True


class AsView(object):
    def __init__(self, method, predicate=_always_true, transform=Request):
        self.method = method
        self.transform = transform
        self.predicate = predicate

    def get_predicate(self, ob):
        if callable(self.predicate):
            return self.predicate
        else:
            return getattr(ob, self.predicate)

    def __get__(self, ob, type=None):
        if ob is None:
            return self

        def closure(data):
            request = self.transform(data)
            if self.get_predicate(ob)(request):
                response = self.method(ob, request)
            else:
                response = None

            if response is None:
                response = request.response
            elif isinstance(response, str):
                response = request.Response(response)
            return response.on_finish(ob)
        return closure


def as_view(*args, **kwargs):
    def _as_view(method):
        return AsView(method, *args, **kwargs)
    return _as_view
