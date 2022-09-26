from dotenv import dotenv_values

INFLUX_DATABASE = "p1"
INFLUX_MEASUREMENT = "solaredge"

config = dotenv_values()

SOLAR_EDGE_START = '2019-04-01'
SOLAR_EDGE_URL = f'https://monitoringapi.solaredge.com/site/{config["location_id"]}/energy?api_key={config["api_key"]}&timeUnit=QUARTER_OF_AN_HOUR'

def is_valid_row(row):
    if row is None or not isinstance(row, dict):
        return False
    if 'value' not in row:
        return False
    value = row['value']
    if value is None or value == 'null':
        return False
    return True

def value_from_row(row):
    value = row['value']
    if value == 'null' or value is None:
        return None
    if isinstance(value, str):
        return float(value)
    if isinstance(value, float) or isinstance(value, int):
        return value
    raise ValueError('Unknown type of value')

def csv_to_influx(rows):
    return [{
            "measurement": INFLUX_MEASUREMENT,
            "time": x['date'],
            "fields": {
                "Wh": value_from_row(x),
            }
        } for x in rows if is_valid_row(x)]