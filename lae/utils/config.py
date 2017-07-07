# -*- coding: utf8 -*-
import os
import yaml


def load_app_config(root_path):
    pwd = os.getcwd()
    app_cfg = pwd + "/app.yaml"
    config = yaml.load(file(app_cfg))
    return config
