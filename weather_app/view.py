from flask import request, jsonify
from sqlalchemy.sql import text
from .models import *
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')


def ingestion():
    path = './data/wx_data'
    from .utils import insert_data, calculate_stats
    if insert_data(path, db):
        calculate_stats(db)


@api.route('/')
def index():
    return "hello World!"


@api.route('/weather')
def get_weather_data():
    station_code = request.args.get('station_code')
    date = request.args.get('date')
    page_no = int(request.args.get('page_no', 1))
    page_size = int(request.args.get('page_size', 10))

    query = "select * from weather__data"
    from weather_app.utils import construct_data_query
    from weather_app.utils import construct_data_query, construct_response
    query = construct_data_query(
        query=query,
        station_code=station_code,
        date=date,
        year=None,
        page_no=page_no,
        page_size=page_size
    )
    res = db.session.execute(text(query))

    records = construct_response(res, page_no, page_size, 'data')
    if len(records) == 0:
        return jsonify(
            {
                'message': 'No data found!'
            }
        ), 404
    return jsonify(
        {
            'message': 'Success!',
            'payload': records
        }
    ), 200


@api.route('/weather/stats')
def get_weather_stats():
    station_code = request.args.get('station_code')
    year = request.args.get('year')
    year = int(year) if year else None
    page_no = int(request.args.get('page_no', 1))
    page_size = int(request.args.get('page_size', 10))

    query = "select * from weather__stats"
    from weather_app.utils import construct_data_query, construct_response
    query = construct_data_query(
        query=query,
        station_code=station_code,
        date=None,
        year=year,
        page_no=page_no,
        page_size=page_size
    )
    res = db.session.execute(text(query))
    records = construct_response(res, page_no, page_size, 'stats')
    if len(records) == 0:
        return jsonify(
            {
                'message': 'No data found!'
            }
        ), 404
    return jsonify(
        {
            'message': 'Success!',
            'payload': records
        }
    ), 200
