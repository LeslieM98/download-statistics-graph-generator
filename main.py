import measurement
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas
import os


def generate_filename(measurement):
    date = measurement.get_datetime().date().isoformat()
    server_name = measurement.get_server_name()
    return f'{server_name}_{date}'.replace(' ', '_')


def get_measurements(db_name, server_name, date):
    results = measurement.get_all_with_server_name_and_date(db_name, server_name, date)
    results_parsed = []
    for result in results:
        results_parsed.append(measurement.Measurement.from_tuple(result))
    return results_parsed

def create_title(measurement):
    return f'Datum: {measurement.get_datetime().date().isoformat()} \n Server: {measurement.get_server_name()}'

def generate_graph(data):
    # x axis values  
    x = []
    
    # corresponding y axis values  
    y = []  
    y_red = []

    for measurement in data:
        y.append(measurement.get_download() * 0.000008)
        x.append(measurement.get_datetime().time().isoformat()[:5])
        y_red.append(500)

    
    plt.figure(figsize=(20,5))
    # plotting the points   
    plt.plot(x, y)  
    plt.plot(x, y_red, 'r')
    # naming the x axis  
    plt.xlabel('Uhrzeit')  
    # naming the y axis  
    plt.ylabel('Download in MBit/s')  
        
    # giving a title to my graph  
    plt.title(create_title(data[0]))  

    plt.xticks(rotation=90)
    plt.ylim(top=1000, bottom=0)
        
    # function to show the plot  
    plt.savefig(generate_filename(data[0]))  

    
def main(argv):
    db_name = "tmp.sqlite"
    measurement.create_db(db_name)
    paths = argv[1:]
    for path in paths:
        measurements = measurement.load_data_as_set(path)
        data = map(lambda x: x.as_db_tuple(), measurements.get_all())
        measurement.insert_into_db(db_name, data)

    dates = measurement.db_get_all_dates(db_name)
    servers = measurement.db_get_all_servers(db_name)

    for date in dates:
        for server in servers:
            generate_graph(get_measurements(db_name, server, date))
    os.remove(db_name)
    


if __name__ == "__main__":
    main(sys.argv)
