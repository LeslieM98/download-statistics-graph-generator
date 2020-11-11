from measurement import load_data, Measurement, load_data_as_set
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas

def main(argv):
    measurement_set = load_data_as_set(argv[1])
    plot_total_downloadspeed(measurement_set)

def plot_total_downloadspeed(measurement_set):
    measurements = measurement_set.get_as_dict('inexio')
    x = []
    y = []
    for key in measurements.keys():
        date = matplotlib.dates.date2num(key)
        x.append(date)
    for value in measurements.values():
        y.append(value.get_download())
    df = pandas.DataFrame({'x': x, 'y': y})
    plt.plot('y', 'x', data=df, color='skyblue')



    plt.show()
    
        

if __name__ == "__main__":
    main(sys.argv)