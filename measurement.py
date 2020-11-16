import csv
import os
import sqlite3
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

    def as_db_tuple(self):
        return (self.get_shared_url(),
                self.get_server_name(),
                self.get_server_id(),
                self.get_latency(),
                self.get_jitter(),
                self.get_packet_loss(),
                self.get_download(),
                self.get_upload(),
                self.get_download_bytes(),
                self.get_upload_bytes(),
                self.get_datetime().date().isoformat(),
                self.get_datetime().time().isoformat())


class MeasurementSet:
    def __init__(self, measurements):
        self.data = measurements

    def get_days(self):
        days = {}
        for measurement in self.data:
            measurement_date = measurement.get_datetime().date()
            if measurement_date not in days:
                days[measurement_date] = []
            days[measurement_date].append(measurement)
        return days

    def get_all(self):
        return self.data

    def get_as_dict(self, server_name):
        r = {}
        for measurement in self.data:
            if server_name.lower() in measurement.get_server_name().lower():
                r[measurement.get_datetime()] = measurement
        return r


def load_data(directory_path):
    file_names = os.listdir(directory_path)
    parsed_csvs = []
    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        parsed_csv = Measurement(file_path)
        parsed_csvs.append(parsed_csv)
    return parsed_csvs


def create_db(db_name):
    table_sql = '''
    CREATE TABLE IF NOT EXISTS measurements (
        share_url string PRIMARY KEY,
        server_name string NOT NULL,
        server_id integer NOT NULL,
        latency float NOT NULL, 
        jitter float NOT NULL,
        packet_loss float NOT NULL,
        download integer NOT NULL,
        upload integer NOT NULL,
        download_bytes integer NOT NULL,
        upload_bytes integer NOT NULL,
        date string NOT NULL,
        time string NOT NULL
    )
    '''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(table_sql)
    conn.commit()


def insert_into_db(db_name, data):
    sql = '''
    INSERT INTO 
    measurements(
        share_url,
        server_name,
        server_id,
        latency,
        jitter,
        packet_loss,
        download,
        upload,
        download_bytes,
        upload_bytes,
        date,
        time)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()

def query_db(db_name, sql):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    return results

def db_get_all_servers(db_name):
    results = query_db(db_name, "SELECT DISTINCT server_name FROM measurements")
    return results

def db_get_all_dates(db_name):
    results = query_db(db_name, "SELECT DISTINCT date FROM measurements")
    return results

def load_data_as_set(directory_path):
    return MeasurementSet(load_data(directory_path))
