from flask import Flask, appcontext_pushed
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/openapi.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )

    from weather_app.view import api
    app.register_blueprint(api)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    from weather_app.view import db
    db.init_app(app)
    return app


# def distroy_app():
#     global app, db
#     del app
#     del db
