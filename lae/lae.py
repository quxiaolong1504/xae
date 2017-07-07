#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import absolute_import

import glob
import os
import sys
import logging
import pkg_resources
from argparse import ArgumentParser
from .utils.colorlog import ColorizingStreamHandler
from .utils import find_app_root


logger = logging.getLogger(__name__)


def verify_command_module(mod):
    name = getattr(mod, "COMMAND_NAME", None)
    desc = getattr(mod, "COMMAND_DESCRIPTION", None)
    if not name:
        return False

    assert desc, "invalid %s.COMMAND_DESCRIPTION" % mod.__name__
    return True


def loadmodules():
    fpths = glob.iglob(os.path.join(os.path.dirname(__file__), "*.py"))
    for fpth in fpths:
        if fpth.endswith("__init__.py"):
            continue

        modname = os.path.splitext(os.path.basename(fpth))[0]
        print modname
        try:
            mod = __import__("lae." + modname, fromlist=["*"])
        except ImportError:
            raise
            continue

        if verify_command_module(mod):
            yield mod


def loadplugins():
    mods = []
    for ep in pkg_resources.iter_entry_points("lae.plugins"):
        try:
            load = ep.load()
            plugins_mods = load()
        except ImportError:
            continue

        mods.extend(plugins_mods)
    return mods


def setup_logging(verbose=False):
    root = logging.getLogger()
    root.setLevel(level=logging.DEBUG if verbose else logging.INFO)

    color_hdl = ColorizingStreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(message)s")
    color_hdl.setFormatter(formatter)
    root.addHandler(color_hdl)


def setup_env():
    approot = find_app_root(raises=False)
    if approot:
        appcfg = {'application': 'application'}
        appname = appcfg['application']
        os.environ['DAE_APPNAME'] = appname


def checkrootpath(args):
    rootpath = getattr(args, "root_path", None)
    if rootpath and not os.path.isdir(rootpath):
        logging.error("root_path doesn't exist: %s", rootpath)
        sys.exit(1)


def add_default_args(subparser, cmdmod=None):
    if not cmdmod or cmdmod.COMMAND_NAME not in ("install", "uninstall"):
        subparser.add_argument("-v", "--verbose", action="store_true",
                               help="enable additional output")

    if not cmdmod or getattr(cmdmod, "COMMAND_AUTHENTICATION", False):
        subparser.add_argument("-u", "--username", dest="user",
                               help="LDAP username")
        subparser.add_argument("--user", dest="user",
                               help="Same as -u/--username")
        subparser.add_argument("--ldap", dest="user",
                               help="Same as -u/--username")


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="commands",
                                       dest='subparser_command')

    mods = list(loadmodules()) + list(loadplugins())
    names = [mod.COMMAND_NAME for mod in mods]
    for mod in mods:
        delegator = mod.COMMAND_NAME in ("install", "uninstall")
        subparser = subparsers.add_parser(name=mod.COMMAND_NAME,
                                          help=mod.COMMAND_DESCRIPTION,
                                          add_help=not delegator)
        add_default_args(subparser, mod)

        mod.populate_argument_parser(subparser)
        subparser.set_defaults(func=mod.main)

    argv = sys.argv[1:] or ['--help']
    args, _ = parser.parse_known_args(argv)
    setup_logging(verbose=getattr(args, "verbose", False))
    setup_env()

    if args.subparser_command in ('install', 'uninstall'):
        # dae install is a delegator for pip install/uninstall
        return args.func(args, argv)

    args = parser.parse_args(argv)
    checkrootpath(args)
    return args.func(args)
