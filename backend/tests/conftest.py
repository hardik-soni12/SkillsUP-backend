import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db

# first fixture
@pytest.fixture(scope='module')
def app():
    # creates new flask app for session
    test_app = create_app('testing')

    with test_app.app_context():
        db.create_all() #setup brand new, empty database

        yield test_app #runs the tests

        # after all the tests are done , they completely clean the test.data base
        db.session.remove()
        db.drop_all()

# second fixture, depends on the first one.
@pytest.fixture(scope='module')
def client(app):
    # creates test client
    return app.test_client()