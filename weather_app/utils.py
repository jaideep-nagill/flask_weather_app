import os
import logging
from sqlalchemy.sql import text
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from time import time
from datetime import datetime


from weather_app.models import Weather_Data, Weather_Stats


def list_dir(path):
    try:
        files = os.listdir(path)
        return files
    except Exception as e:
        print(e)


def construct_data_query(
    query,
    station_code=None,
    date=None,
    year=None,
    page_no=1,
    page_size=10
):
    condition = " where "
    if station_code:
        condition = condition + f"station_code= {station_code} "
    if date:
        condition = condition + \
            ("and " if station_code else "") + f"date={date}"
    if year:
        condition = condition + \
            ("and " if station_code else "") + f" year={year}"

    if station_code or date or year:
        query = query + condition
    query = query + f" limit {page_size} offset {page_size*(page_no - 1)}"
    return query


def construct_response(res, page_no, page_size, stats_or_data):
    records = []
    keys_data = ['id', 'station_code', 'date', 'max_temp', 'min_temp', 'prcp']
    keys_stats = ['id', 'year', 'station_code''avg_max_temp',
                  'avg_min_temp', 'total_acc_prcp']
    for row in res:
        row = list(row)
        data_dict = None
        if stats_or_data == 'data':
            data_dict = zip(keys_data, row)
        else:
            data_dict = zip(keys_stats, row)
        records.append(dict(data_dict))

    return records


def get_file_data(path):
    try:

        with open(path, 'r') as file:
            file_data = file.read().strip(' ').strip('\n').split('\n')
            return file_data

    except Exception as e:
        print(e)


def construct_weather_data(file, data):
    single_reading = [x.strip(" ") for x in data.split('\t')]
    obj = Weather_Data(
        file.replace('.txt', ''),
        None if single_reading[0] == '' or single_reading[0] == '-9999' else datetime.strptime(
            single_reading[0], '%Y%m%d'),
        None if single_reading[1] == '' or single_reading[1] == '-9999' else single_reading[1],
        None if single_reading[2] == '' or single_reading[2] == '-9999' else single_reading[2],
        None if single_reading[3] == '' or single_reading[3] == '-9999' else single_reading[3]
    )

    return obj


def check_duplicate(file, db, last_date):

    try:
        res = db.session.execute(text('SELECT * FROM weather__data WHERE weather__data.station_code = :code AND weather__data.date = :date'),
                                 {
            'code': file.replace('.txt', ''),
            'date': last_date[:4] + '-'+last_date[4:6]+'-'+last_date[6:]
        }
        )
        res.one()
        print('Duplicate Entry!!!')
    except NoResultFound as e:
        return False
    except MultipleResultsFound as e:
        print('Duplicate Entry!!!')
    return True


def insert_data(path, db):

    files = list_dir(path)
    if not files:
        return
    for file in files:
        if file[:3] != 'USC':
            continue
        file_data = get_file_data(os.path.join(path, file))
        if not file_data:
            return
        # Check if file data is already inserted in the table
        last_date = file_data[-1].split('\t')[0].strip(' ')

        if check_duplicate(file, db, last_date):
            return False

        # insert data
        records = []
        for data in file_data:
            if len(data) == 0:
                continue
            records.append(construct_weather_data(file, data))

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[
                                # Specify the log file
                                logging.FileHandler('my_log_file.log'),
                                logging.StreamHandler()  # Display logs on the console as well
                            ]
                            )
        log_message = f'File: {file} | Number of Records: {len(records)} | Record ingestion start'
        start_time = time()
        logging.info(log_message)
        db.session.add_all(records)
        db.session.commit()
        log_message = f'File: {file} | Record ingestion finished, time consumed: {time() - start_time} seconds'
        logging.info(log_message)
    return True


def calculate_stats(db):
    query = "Select strftime('%Y', weather__data.date) as year, weather__data.station_code,  avg(weather__data.max_temp), avg(weather__data.min_temp), sum(prcp) from weather__data group by weather__data.station_code, strftime('%Y', weather__data.date)"
    res = db.session.execute(text(query))
    records = []
    for row in res:
        records.append(Weather_Stats(
            year=int(row[0]),
            station_code=row[1],
            avg_max_temp=row[2],
            avg_min_temp=row[3],
            total_acc_prcp=row[4]
        )
        )
    db.session.add_all(records)
    db.session.commit()

# file_data('./data/wx_data/USC00110072.txt')
