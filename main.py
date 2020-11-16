import measurement
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas


def generate_filename(date, server_name):
    return f'{server_name}_{date}'.replace(' ', '_')


def get_measurements(db_name, server_name, date):
    results = measurement.get_all_with_server_name_and_date(db_name, server_name, date)
    results_parsed = []
    for result in results:
        results_parsed.append(measurement.Measurement.from_tuple(result))
    return results_parsed


def main(argv):
    db_name = "tmp.sqlite"
    measurement.create_db(db_name)
    measurements = measurement.load_data_as_set(argv[1])
    data = map(lambda x: x.as_db_tuple(), measurements.get_all())
    # measurement.insert_into_db(db_name, data)
    # measurement.query_db(db_name, "SELECT * FROM measurements WHERE date = '2020-11-04' AND server_name like '%%inexio%%' ")
    results = get_measurements(db_name, 'inexio', '2020-11-03')
    for result in results:
        print(result)

if __name__ == "__main__":
    main(sys.argv)
