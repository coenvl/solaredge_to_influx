#!/usr/bin/python3

from influxdb import InfluxDBClient
from datetime import date

import pandas as pd
import csv

from solaredge import INFLUX_DATABASE, SOLAR_EDGE_START, csv_to_influx

if __name__ == '__main__':
    influx = InfluxDBClient(host="192.168.178.200", port=8086, database=INFLUX_DATABASE)

    pr = pd.period_range(start=SOLAR_EDGE_START,end=date.today().replace(day=1), freq='M')
    for d in pr:
        print(d)
        with open(f'data/energy_{str(d)}.csv', 'r', newline='', ) as file:
            csv_reader = csv.DictReader(file)
            pts = csv_to_influx(csv_reader)
            influx.write_points(pts)