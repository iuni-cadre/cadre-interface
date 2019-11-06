import pytest
from backend import application

class MockResponse:
    # Mocks up a response object and lets you set the error code
    def __init__(self):
        # default is a 200 success response
        self.status_code = 200
        self.json_data = None

    def set_status_code(self, status_code):
        self.status_code = status_code

    def json(self):
        return self.json_data

    def set_json(self, fake_json):
        self.json_data = fake_json


class MockPsycopgCursor:
    def __init__(self, rowcount, raise_exception=False, rows=[], **kwargs):
        self.rows = rows
        self.raise_exception = raise_exception
        self.rowcount = rowcount

    def close(self):
        return True

    def execute(self, query, variables=None):
        if(self.raise_exception):
            raise Exception('Fake Exception')
        pass

    def fetchall(self):
        vals = []
        
        for row in self.rows:
            if type(row) is dict:
                vals.append(list(row.values()))
            else:
                vals.append(row)
        
        return vals

    def fetchone(self):
        return self.rows

    def set_rows(self, rows):
        self.rows = rows

    def set_exception(self, raise_exception):
        self.raise_exception = raise_exception


class MockPsycopgConnection:
    def __init__(self, rowcount=10, raise_exception=False, rows=[], **kwargs):
        self.raise_exception = raise_exception
        self.rows = rows
        self.rowcount = rowcount
        pass

    def cursor(self):
        return MockPsycopgCursor(rowcount=self.rowcount, raise_exception=self.raise_exception, rows=self.rows)

    def close(self):
        return True



@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """
    Sets the environment to testing.
    """

    monkeypatch.setenv('TEST', 'testing-mode')

@pytest.fixture
def client():
    """Fixture allowing us to mock requests and test endpoints."""
  # application.app.config["TESTING"] = True
    client = application.app.test_client()

    yield client
    return client