#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
import sys


def resource_path(relative_path: str):
    """
    Get absolute path to resource, works for dev and for PyInstaller

    :param relative_path: Files to reference
    :return: os.path.join
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)
