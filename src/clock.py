#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import time


def clockclock(queue):
    """Real-time clock
    Current time to be expressed on JS-06

    :param queue: MultiProcessing Queue
    """
    while True:
        now = str(time.time())
        queue.put(now)
        time.sleep(1)
