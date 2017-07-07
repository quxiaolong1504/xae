# -*- coding: utf-8 -*-

import logging
import pkg_resources

COMMAND_NAME = "plugin"
COMMAND_DESCRIPTION = "Plugin install"

logger = logging.getLogger(__name__)


def populate_argument_parser(parser):
    parser.add_argument('action', choices=['list'], default='list', help="list all installed plugins")


def main(args):
    if args.action not in ['list']:
        logger.error('action error')
        return 0

    for ep in pkg_resources.iter_entry_points('lae.plugins'):
        logger.info(ep.name)

    return 0


class PluginCommand(object):
    def run(self):
        raise NotImplementedError
