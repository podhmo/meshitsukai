# -*- coding:utf-8 -*-
import unittest
from meshitsukai.plugin import Plugin
from meshitsukai.view import as_view


# plugin definition. usually plugin implementation is separated from test code.
class LineStripPlugin(Plugin):
    def starts_from_bot(self, request):
        return request.body.startswith("bot:")

    @as_view(predicate="starts_from_bot")
    def process_message(self, request):
        return request.Response(self.line_strip(request.body[4:]))

    def line_strip(self, message):
        return "".join(line.strip() for line in message.split("\n"))


class UsuallyUnitTestSampleTests(unittest.TestCase):
    def _makeOne(self):
        return LineStripPlugin()

    def test_linestrip__nostrip(self):
        message = "@foo@"
        target = self._makeOne()
        result = target.line_strip(message)
        self.assertEqual(result, "@foo@")

    def test_linestrip__strip(self):
        message = " foo "
        target = self._makeOne()
        result = target.line_strip(message)
        self.assertEqual(result, "foo")


class PluginUnitTestSampleTests(unittest.TestCase):
    def _makeOne(self):
        return LineStripPlugin()

    def test_it(self):
        data = {"text": "bot:\n foo ", "channel": "*general*"}
        target = self._makeOne()
        target.process_message(data)

        self.assertEqual(len(target.outputs), 1)
        self.assertEqual(target.outputs[-1], ("*general*", "foo"))

    def test_not_match(self):
        data = {"text": "hmm:\n foo ", "channel": "*general*"}
        target = self._makeOne()
        target.process_message(data)

        self.assertEqual(len(target.outputs), 0)


class PluginIntegrationTestSampleTests(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from meshitsukai.testing import dummy_plugin
        return dummy_plugin(self._getTarget(), *args, **kwargs)

    def _getTarget(self):
        return LineStripPlugin

    def test_it(self):
        from meshitsukai.testing import dummy_source, dummy_bot
        plugin = self._makeOne()
        source = dummy_source()
        bot = dummy_bot([plugin], source)
        text = """\
bot:
section
  subsection
  subsection
"""
        source.generate_channel("general")
        source.generate_message(text, user="foo", channel="general")

        bot.run()

        result = source.find_channel("general").getvalue()
        self.assertEqual(result, ["sectionsubsectionsubsection"])
