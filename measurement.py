import csv
import os
from datetime import datetime, date, time

class Measurement:
    
    def _parse_date(self, file_name):
        datetime_string = file_name[:file_name.index('CET')]
        parsed_date = date.fromisoformat(datetime_string[:datetime_string.index(' ')].strip())
        parsed_time = time.fromisoformat(datetime_string[datetime_string.index(' '):].strip())
        return datetime.combine(parsed_date, parsed_time)

    def __init__(self, file_path):
        self.read_csv = []
        self.file_name = os.path.basename(file_path)
        self.date = self._parse_date(self.file_name)

        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.read_csv.append(row)
            self.csv_header = self.read_csv[0]
            self.csv_data = self.read_csv[1]

    def get_datetime(self):
        return self.date
    
    def get_server_name(self):
        return self.csv_data[0]

    def get_server_id(self):
        return self.csv_data[1]

    def get_latency(self):
        return self.csv_data[2]

    def get_jitter(self):
        return self.csv_data[3]

    def get_packet_loss(self):
        return self.csv_data[4]

    def get_download(self):
        return self.csv_data[5]

    def get_upload(self):
        return self.csv_data[6]

    def get_download_bytes(self):
        return self.csv_data[7]

    def get_upload_bytes(self):
        return self.csv_data[8]

    def get_shared_url(self):
        return self.csv_data[9]

    def __repr__(self):
        return str(self.csv_data)

    def __str__(self):
        return str(self.csv_data)

class MeasurementSet:
    def __init__(self, measurements):
        self.data = measurements

    def get_days(self):
        pass

    def get_all(self):
        return self.data

def load_data(directory_path):
    file_names = os.listdir(directory_path)
    parsed_csvs = []
    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        parsed_csv = Measurement(file_path)
        parsed_csvs.append(parsed_csv)
    return parsed_csvs

def load_data_as_set(directory_path):
    return MeasurementSet(load_data(directory_path))