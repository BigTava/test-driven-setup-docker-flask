# src/tests/conftest.py

#Fixtures are reusable objects for tests. They have a scope associated with them, which indicates how often the fixture is invoked:

## function - once per test function (default)
## class - once per test class
## module - once per test module
## session - once per test session

import pytest

from src import create_app, db

# normal run
## $ docker-compose exec api python -m pytest "src/tests"

# disable warnings
## $ docker-compose exec api python -m pytest "src/tests" -p no:warnings

# run only the last failed tests
## $ docker-compose exec api python -m pytest "src/tests" --lf

# run only the tests with names that match the string expression
## $ docker-compose exec api python -m pytest "src/tests" -k "config and not test_development_config"

# stop the test session after the first failure
## $ docker-compose exec api python -m pytest "src/tests" -x

# enter PDB after first failure then end the test session
## $ docker-compose exec api python -m pytest "src/tests" -x --pdb

# stop the test run after two failures
## $ docker-compose exec api python -m pytest "src/tests" --maxfail=2

# show local variables in tracebacks
## $ docker-compose exec api python -m pytest "src/tests" -l

# list the 2 slowest tests
## $ docker-compose exec api python -m pytest "src/tests" --durations=2

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


