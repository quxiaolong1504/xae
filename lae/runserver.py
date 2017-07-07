# -*- coding: utf8 -*-
import os
import sys
from .utils import find_app_root
from .utils.log import logger

COMMAND_NAME = "runserver"
COMMAND_DESCRIPTION = "Run a web server."


def populate_argument_parser(parser):
    parser.add_argument('-H', '--host', default='localhost', help='web server host. Default: localhost')
    parser.add_argument('-p', '--port', default='5000', help='web server port. Default: 5000')


def main(arg):
    pwd = find_app_root()
    if not os.path.exists(pwd + "/env"):
        logger.error('please run "lae env first!"')
        return -1

    sys.path.insert(0, pwd + '/env/lib/python2.7/site-packages')
    sys.path.insert(0, pwd)

    app = __import__('app')
    if app and getattr(app, 'app'):
        app.app.run(port=int(arg.port), host=arg.host)
    else:
        logger.error('failed import app')
