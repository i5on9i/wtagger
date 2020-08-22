# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

import os
from datetime import datetime

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

# Model
STRING_LEN = 64


def get_current_time():
    return datetime.utcnow()


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e
