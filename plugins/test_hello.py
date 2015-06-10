# -*- coding:utf-8 -*-
import unittest


class Test(unittest.TestCase):
    def _getTarget(self):
        from hello import HelloPlugin
        return HelloPlugin

    def _makeOne(self, *args, **kwargs):
        from meshitsukai.testing import dummy_plugin
        plugin = self._getTarget()
        return dummy_plugin(plugin, *args, **kwargs)

    def test_it(self):
        from meshitsukai.testing import dummy_source, dummy_bot
        plugin = self._makeOne()
        source = dummy_source()
        bot = dummy_bot([plugin], source)

        source.generate_channel("general")
        source.generate_message("hello", channel="general")

        bot.run()

        result = source.find_channel("general").getvalue()
        self.assertEqual(result, ["`*hello*`"])

    def test_not_reply(self):
        from meshitsukai.testing import dummy_source, dummy_bot
        plugin = self._makeOne()
        source = dummy_source()
        bot = dummy_bot([plugin], source)

        source.generate_channel("general")
        source.generate_message("bye", channel="general")

        bot.run()

        result = source.find_channel("general").getvalue()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
