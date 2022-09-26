#!/bin/python3
import json
import sys
import requests

from influxdb import InfluxDBClient
from datetime import date

from solaredge import INFLUX_DATABASE, SOLAR_EDGE_URL, csv_to_influx

influx = InfluxDBClient(host="192.168.178.200", port=8086, database=INFLUX_DATABASE)

url = f'{SOLAR_EDGE_URL}&startDate={date.today()}&endDate={date.today()}'
response = requests.get(url)

data = json.loads(response.content)

if response.status_code != 200:
    print(f'Error {response.status_code} fetching data: {data}', file=sys.stderr)
    exit()

pts = csv_to_influx(data['energy']['values'])
influx.write_points(pts)