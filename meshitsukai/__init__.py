# -*- coding:utf-8 -*-
import sys
import logging
import argparse
logger = logging.getLogger(__name__)
from meshitsukai.configurator import Configurator


class UnknownChannel(Exception):
    pass


def main_loop(bot):
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logger.exception('OOPS')


def setup_logging(args):
    if args.logging is None:
        return
    else:
        level = getattr(logging, args.logging)
        logging.basicConfig(level=level)


def main(sys_args=None):
    sys_args = sys_args or sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")
    parser.add_argument("--console", default=False, action="store_true")
    parser.add_argument("-p", "--plugins", default=None, help="',' separated plugin name list")
    args = parser.parse_args(sys_args)
    setup_logging(args)

    configurator = Configurator.from_ini_file(args.config)
    plugin_names = args.plugins and [e.strip() for e in args.plugins.split(",")]
    plugins = configurator.load_plugins(plugin_names)

    if not args.console:
        bot = configurator.make_app(plugins)
        serve(bot, configurator.context)
    else:
        from meshitsukai.console import main as console_main
        console_main(configurator, plugins)


def serve(bot, context):
    DAEMON = context.is_daemon
    logger.debug("running as daemon? .. %s", DAEMON)
    if DAEMON:
        import daemon
        with daemon.DaemonContext():
            main_loop(bot)
    else:
        main_loop(bot)

if __name__ == "__main__":
    main()
