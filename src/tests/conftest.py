# src/tests/conftest.py

#Fixtures are reusable objects for tests. They have a scope associated with them, which indicates how often the fixture is invoked:

## function - once per test function (default)
## class - once per test class
## module - once per test module
## session - once per test session

import pytest

from src import app, db


@pytest.fixture(scope='module')
def test_app():
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()