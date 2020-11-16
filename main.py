import measurement
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas

def generate_filename(date, server_name):
    return f'{server_name}_{date}'.replace(' ', '_')

def main(argv):
    db_name = "tmp.sqlite"
    measurement.create_db(db_name)
    measurements = measurement.load_data_as_set(argv[1])
    data = map(lambda x: x.as_db_tuple(), measurements.get_all())
    # measurement.insert_into_db(db_name, data)
    # measurement.query_db(db_name, "SELECT * FROM measurements WHERE date = '2020-11-04' AND server_name like '%%inexio%%' ")
    results = measurement.db_get_all_servers(db_name)
    print(generate_filename('2020-11-16', 'inexio Saar'))

if __name__ == "__main__":
    main(sys.argv)
