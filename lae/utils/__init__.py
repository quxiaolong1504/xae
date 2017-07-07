# coding: utf-8

from __future__ import absolute_import
from .log import logger
import os


def find_app_root(start_dir=None, raises=True):
    if start_dir is None:
        start_dir = os.getcwd()
    for path in walk_up(start_dir):
        if os.path.exists(os.path.join(path, 'app.yaml')):
            return path

    if raises:
        logger.error("No app.yaml found in any parent dirs.  Please make sure "
                        "the current working dir is inside the app directory.")
        exit(-1)
    else:
        return None


def walk_up(dir_):
    while True:
        yield dir_
        olddir, dir_ = dir_, os.path.dirname(dir_)
        if dir_ == olddir:
            break
