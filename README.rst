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

  [hello]
  template = <@{user}> `*hello*` !!

- `slack_token` is api token of slack.
- `plugin_directory` is a location of directory stored your plugins
- (hello section is a plugin's option describe at below)

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
  │   ├── hello.plugin
  │   └── hello.py
  └── config.ini


plugin implemntation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(todo: gentle instruction)

::

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


info file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(todo: gentle instruction)

::

  [Core]
  name = hello
  module = hello

  [Document]
  author = podhmo
  description = simple hello plugin
