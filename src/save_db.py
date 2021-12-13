#!/usr/bin/env python3
"""
This code is not include AWS Sensor, only Visibility
"""

import traceback
import binascii
import struct
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
                "fields": {"visbility": float(vis_value)},
                "time": save_time}]
        client.write_points(points=points, protocol="json")
        client.close()

        # Save every 1 minute.
        # time.sleep(3)
        return

    except TypeError:
        pass


def main():
    for i in range(10000):
        num = i % 10
        SaveDB(num)

if __name__ == '__main__':
    main()