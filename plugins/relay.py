# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin
from meshitsukai.view import as_view
import threading
import shlex
import uuid
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import logging
logger = logging.getLogger(__name__)


"""
>>> $generate
cfce4dcf4fa549dcb28344c3a41fecf4
>>> $register cfce4dcf4fa549dcb28344c3a41fecf4
ok

# on shell
curl http://localhost:4444 -X POST -d key=cfce4dcf4fa549dcb28344c3a41fecf4 -d message="foo"
"""


class RelayPlugin(Plugin):
    def __init__(self):
        super(RelayPlugin, self).__init__()
        self.tmp = set()
        self.keys = {}
        httpd = make_server("localhost", 4444, App(self))
        self.t = threading.Thread(target=httpd.serve_forever)
        self.t.start()

    def generate(self, request):
        k = uuid.uuid4().hex
        self.tmp.add(k)
        return "`{}`".format(k)

    def register(self, request, key):
        if key not in self.tmp:
            return "ng"
        self.keys[key] = request.channel
        return "ok: `curl http://localhost:4444 -X POST -d key={key} -d message`".format(key=key)

    def relay(self, key, message):
        channel = self.keys[key]
        self.outputs.append((channel, message))  # raw api

    def predicate(self, request):
        return request.body.startswith(("$register", "$generate", "$status"))

    @as_view(predicate="predicate")
    def process_message(self, request):
        cmd, *args = shlex.split(request.body)
        return getattr(self, cmd[1:])(request, *args)


class App(object):
    def __init__(self, plugin):
        self.plugin = plugin

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)

        status = '200 OK'
        headers = [('Content-type', 'text/plain')]

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body.decode("utf-8"))
        logger.debug("POST: -- %s", d)
        start_response(status, headers)
        try:
            self.plugin.relay(d["key"][0], d["message"][0])
        except Exception as e:
            return [str(e).encode("utf-8")]
        return [b"ok"]
