#!/usr/bin/python3

import requests
from datetime import date

import pandas as pd

from solaredge import SOLAR_EDGE_START, SOLAR_EDGE_URL

if __name__ == '__main__':
    pr = pd.period_range(start=SOLAR_EDGE_START,end=date.today().replace(day=1), freq='M')

    for d in pr:
        url = f'{SOLAR_EDGE_URL}&format=csv&startDate={d.start_time.date()}&endDate={d.end_time.date()}'
        data = requests.get(url)
        with open(f'data/energy_{str(d)}.csv', 'wb') as file:
            file.write(data.content)