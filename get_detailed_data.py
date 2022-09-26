#!/usr/bin/python3

import requests
from datetime import date

import pandas as pd

from solaredge import SOLAR_EDGE_DETAIL_URL, SOLAR_EDGE_START

if __name__ == '__main__':
    pr = pd.period_range(start=SOLAR_EDGE_START,end=date.today(), freq='W')

    for d in pr:
        url = f'{SOLAR_EDGE_DETAIL_URL}&format=csv&startTime={d.start_time.date()} 00:00:00&endTime={d.end_time.date()} 23:59:59'
        data = requests.get(url)
        with open(f'data/details_{str(d.start_time.date())}.csv', 'wb') as file:
            file.write(data.content)