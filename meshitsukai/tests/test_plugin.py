# -*- coding:utf-8 -*-
import unittest
from meshitsukai.plugin import Plugin


# plugin definition. usually plugin implementation is separated from test code.
class LineStripPlugin(Plugin):
    def line_strip(self, message):
        return "".join(line.strip() for line in message.split("\n"))

    def process_message(self, data):
        result = self.line_strip(data["text"])
        self.outputs.append((data["channel"], result))


class PluginTestSampleTests(unittest.TestCase):
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
section
  subsection
  subsection
"""
        source.generate_channel("general")
        source.generate_message(text, user="foo", channel="general")

        bot.run()

        result = source.find_channel("general").getvalue()
        self.assertEqual(result, ["sectionsubsectionsubsection"])
