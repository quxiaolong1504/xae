# -*- coding: utf8 -*-
import os

import errno


def mkdir(path):
    if not os.path.exists(path):
        mkdir_p(path)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise