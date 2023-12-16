from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


def ingestion():
    path = 'data/wx_data'

    from .utils import insert_data, calculate_stats
    from .models import db
    if insert_data(path, db):
        calculate_stats(db)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.instance_path = 'instance'
    from os import getcwd
    SWAGGER_URL = '/api/docs'
    API_URL = f'/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )
    app.register_blueprint(swaggerui_blueprint)

    from .views import api
    app.register_blueprint(api)

    from .views import db
    db.init_app(app)

    return app
