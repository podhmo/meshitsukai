# -*- coding:utf-8 -*-
import sys
import os
import logging
import yaml
logger = logging.getLogger(__name__)


class UnknownChannel(Exception):
    pass

directory = None

config = {
}


def main_loop(bot):
    if "LOGFILE" in config:
        logger.basicConfig(filename=config["LOGFILE"], level=logger.INFO, format='%(asctime)s %(message)s')
    logger.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logger.exception('OOPS')

if __name__ == "__main__":
    from meshitsukai.bot import RtmBot

    directory = os.getcwd()
    with open(os.path.join(directory, 'rtmbot.conf')) as rf:
        config = yaml.load(rf)

    debug = config["DEBUG"]
    bot = RtmBot(config["SLACK_TOKEN"])
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}

    if "DAEMON" in config:
        if config["DAEMON"]:
            import daemon
            with daemon.DaemonContext():
                main_loop(bot)
    main_loop(bot)
