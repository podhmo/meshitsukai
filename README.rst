meshitsukai
========================================

slack client library.

hevily inspired by `python-rtmbot <https://github.com/slackhq/python-rtmbot>`_

WIP.

install
----------------------------------------

::

  pip install -e git+https://github.com/podhmo/meshitsukai.git@master#egg=meshitsukai

how to use
----------------------------------------

writing config file. such as below. ::

  [app]
  slack_token = xoxb-xxxxxxxxxxxXxxxXxxxxxXXxXxxXxxxXxXX
  plugin_directory = %(here)s/plugins
  DEBUG = false
  DAEMON = false

- `slack_token` is api token of slack.
- `plugin_directory` is a location of directory stored your plugins

run `meshitsukai` ::

  $ meshitsukai --logging=DEBUG config.ini

writing your plugin
----------------------------------------

if you will write a plugin by your own hands, at least two files is needed.

- plugin implemntation (.py)
- info file. (.plugin)

file structure ::

  .
  ├── plugins
  │   ├── __init__.py
  │   ├── dummy.plugin
  │   └── dummy.py
  └── config.ini


plugin implemntation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(todo: gentle instruction)

::


  from meshitsukai.plugin import Plugin


  class DummyPlugin(Plugin):
      # ## instance variables ##
      # self.outputs
      # self.crontable

      def process_message(self, data):
          print("---------- incomming: ----------")
          # data : {'ts': '1433670154.000003', 'type': 'message', 'team': 'XxxXXXXXX', 'text': 'aa', 'user': 'XxxXXxxXX', 'channel': 'XxxXXXXXx'}
          print(data)
          print("--------------------------------")
          self.outputs.append((data["channel"], "`*dummy*`"))

info file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(todo: gentle instruction)

::

  [Core]
  name = dummy
  module = dummy

  [Document]
  author = podhmo
  description = simple dummy plugin
