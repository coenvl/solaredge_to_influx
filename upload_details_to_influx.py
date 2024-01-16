#!/usr/bin/python3

from pathlib import Path
from influxdb import InfluxDBClient
from datetime import date

import pandas as pd
import csv

from solaredge import INFLUX_DATABASE, INFLUX_HOST, SOLAR_EDGE_START, csv_to_influx, telemetries_to_influx

if __name__ == '__main__':
    influx = InfluxDBClient(host=INFLUX_HOST, port=8086, database=INFLUX_DATABASE)

    files = Path('data').glob('details_*.csv')
    for file in files:
        print(file)
        with open(file, 'r', newline='', ) as fin:
            csv_reader = csv.DictReader(fin)
            pts = telemetries_to_influx(csv_reader)
            influx.write_points(pts)