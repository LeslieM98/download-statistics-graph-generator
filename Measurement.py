import csv
import os

def class Measurement:

    def __init__(self, file_path):
        read_csv = []

        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                read_csv.append(row)
        
        self.csv_data = read_csv[1]

    
    def get_server_Name(self):
        return read_csv[0]

    def get_server_id(self):
        return read_csv[1]

    def get_latency(self):
        return read_csv[2]

    def get_jitter(self):
        return read_csv[3]

    def get_packet_loss(self):
        return read_csv[4]

    def get_download(self):
        return read_csv[5]

    def get_upload(self):
        return read_csv[6]

    def get_download_bytes(self):
        return read_csv[7]

    def get_upload_bytes(self):
        return read_csv[8]

    def get_shared_url(self):
        return read_csv[9]

def load_data(directory_path):
    file_names = os.listdir(directory_path)
    file_paths = map(lambda file_name: os.path.join(directory_path, file_name), files)
    parsed_data = map(lambda file_path: Measurement(file_path))
    return parsed_data