from measurement import load_data, Measurement
import sys

def main(argv):
    loaded_measurements = []
    for arg in argv[1:]:
        measurements = load_data(arg)
        loaded_measurements.extend(measurements)
    for measurement in loaded_measurements:
        print(measurement)

if __name__ == "__main__":
    main(sys.argv)