from dotenv import dotenv_values

INFLUX_DATABASE = "p1"
INFLUX_MEASUREMENT = "solaredge"

config = dotenv_values()

SOLAR_EDGE_START = '2019-04-01'
SOLAR_EDGE_ENERGY_URL = f'https://monitoringapi.solaredge.com/site/{config["location_id"]}/energy?api_key={config["api_key"]}&timeUnit=QUARTER_OF_AN_HOUR'
SOLAR_EDGE_DETAIL_URL = f'https://monitoringapi.solaredge.com/equipment/{config["location_id"]}/{config["inverter_id"]}/data?api_key={config["api_key"]}'

def parse_value(value):
    if value == 'null' or value is None:
        return None
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return value
    if isinstance(value, float) or isinstance(value, int):
        return value
    raise ValueError('Unknown type of value')

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
    return parse_value(row['value'])

def csv_to_influx(rows):
    return [{
            "measurement": INFLUX_MEASUREMENT,
            "time": x['date'],
            "fields": {
                "Wh": value_from_row(x),
            }
        } for x in rows if is_valid_row(x)]

def get_all_fields_from_row(row: dict):
    row.pop('date')
    if 'L1Data' in row:
        l1 = row.pop('L1Data')
        row.update(l1)
    return {key: parse_value(value) for key, value in row.items()}

def telemetries_to_influx(telemetries):
    return [{
            "measurement": "solaredge_details",
            "time": x['date'],
            "fields": get_all_fields_from_row(x)
        } for x in telemetries]
