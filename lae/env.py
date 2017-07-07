# -*- coding: utf8 -*-
import os

from .utils import find_app_root
from .utils.log import logger

COMMAND_NAME = "env"
COMMAND_DESCRIPTION = "Make project env. Install pip-req.txt to env"


def populate_argument_parser(parser):
    pass


def main(arg):
    pwd = find_app_root()
    env_path = pwd + "/env"
    logger.info('make virtualenv')
    os.system("virtualenv env")
    logger.info('install pip-req.txt')
    cmd = "source %s/bin/activate && pip install -r %s" % (env_path, pwd + "/pip-req.txt")
    os.system(cmd)

