#!/usr/bin/python3

import json
import sys
import requests

from influxdb import InfluxDBClient
from datetime import date, datetime

from solaredge import INFLUX_DATABASE, INFLUX_HOST, SOLAR_EDGE_DETAIL_URL, SOLAR_EDGE_ENERGY_URL, csv_to_influx, telemetries_to_influx

if __name__ == '__main__':
    influx = InfluxDBClient(host=INFLUX_HOST, port=8086, database=INFLUX_DATABASE)

    url = f'{SOLAR_EDGE_ENERGY_URL}&startDate={date.today()}&endDate={date.today()}'
    response = requests.get(url)

    data = json.loads(response.content)

    if response.status_code != 200:
        print(f'Error {response.status_code} fetching data: {data}', file=sys.stderr)
        exit()

    pts = csv_to_influx(data['energy']['values'])
    influx.write_points(pts)

    today = date.today()
    start = datetime(today.year, today.month, today.day)
    end = datetime.now().replace(microsecond=0)
    detail_url = f'{SOLAR_EDGE_DETAIL_URL}&startTime={start}&endTime={end}'
    response = requests.get(detail_url)

    data = json.loads(response.content)
    if response.status_code != 200:
        print(f'Error {response.status_code} fetching data: {data}', file=sys.stderr)
        exit()

    pts = telemetries_to_influx(data['data']['telemetries'])
    influx.write_points(pts)