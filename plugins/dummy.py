# -*- coding:utf-8 -*-
from meshitsukai.plugin import Plugin
from meshitsukai.view import as_view
import logging
logger = logging.getLogger(__name__)


class Dummy(Plugin):
    @as_view()
    def process_message(self, request):
        # data : {'ts': '1433670154.000003', 'type': 'message', 'team': 'XxxXXXXXX', 'text': 'aa', 'user': 'XxxXXxxXX', 'channel': 'XxxXXXXXx'}
        logger.debug("incomming: %s", request._rawdata)
        return "`*dummy*`"
