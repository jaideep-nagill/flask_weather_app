import pytest


@pytest.fixture
def client():
    from weather_app import create_app
    app = create_app()
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
    # app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client
