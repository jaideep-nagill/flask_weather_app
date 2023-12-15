from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Weather_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(20))
    date = db.Column(db.Date, nullable=True)
    max_temp = db.Column(db.Integer, nullable=True)
    min_temp = db.Column(db.Integer, nullable=True)
    prcp = db.Column(db.Integer, nullable=True)

    def __init__(self, station_code, date, max_temp=None, min_temp=None, prcp=None):
        self.station_code = station_code
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.prcp = prcp


class Weather_Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    station_code = db.Column(db.String(20))
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_acc_prcp = db.Column(db.Integer, nullable=True)

    def __init__(self, year, station_code, avg_max_temp=None, avg_min_temp=None, total_acc_prcp=None):
        self.total_acc_prcp = total_acc_prcp
        self.year = year
        self.station_code = station_code
        self.avg_max_temp = self.avg_max_temp
        self.avg_min_temp = self.avg_min_temp
        self.total_acc_prcp = self.total_acc_prcp
