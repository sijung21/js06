#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

"""
This code is not include AWS Sensor, only Visibility
"""


import time
from influxdb import InfluxDBClient, exceptions


def SaveDB(vis_value):
    try:
        client = InfluxDBClient('localhost', 8086)
        save_time = time.time_ns()
        client.create_database("Sijung")
        client.switch_database("Sijung")
        points = [{"measurement": "JS06",
                   "tags": {"name": "Sijung"},
                   "fields": {"visibility": float(vis_value)},
                   "time": save_time}]
        client.write_points(points=points, protocol="json")
        client.close()

        # Save every 1 minute.
        # time.sleep(3)
        return

    except exceptions as e:
        print(e)


def main():
    for i in range(10000):
        num = i % 10
        SaveDB(num)


if __name__ == '__main__':
    main()
