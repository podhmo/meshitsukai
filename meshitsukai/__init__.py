# -*- coding:utf-8 -*-
import sys
import logging
import yaml
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
    args = parser.parse_args(sys_args)
    setup_logging(args)

    with open(args.config) as rf:
        settings = yaml.load(rf)

    configurator = Configurator(settings)
    bot = configurator.make_app()

    logger.debug("running as daemon? .. %s", settings.get("DAEMON", False))
    if "DAEMON" in settings:
        if settings["DAEMON"]:
            import daemon
            with daemon.DaemonContext():
                main_loop(bot)
    else:
        main_loop(bot)


if __name__ == "__main__":
    main()
