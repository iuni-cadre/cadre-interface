import pytest
from backend import application
from psycopg2 import extensions
from contextlib import contextmanager

class MockResponse:
    # Mocks up a response object and lets you set the error code
    def __init__(self):
        # default is a 200 success response
        self.status_code = 200
        self.json_data = None
        self.text = ""

    def set_status_code(self, status_code):
        self.status_code = status_code

    def json(self):
        return self.json_data

    def set_json(self, fake_json):
        self.json_data = fake_json
    
    def get_json(self):
        return self.json_data



class MockPsycopgCursor:
    def __init__(self, raise_exception = False, rows = [], **kwargs):
        self.rowcount = len(rows)
        self.rows = rows
        self.raise_exception = raise_exception
        self.queries = []
        self.row_sets = []
        self.current_index = 0
    def close(self):
        return True
    def execute(self, query, variables):
        #mogrify the query and the variables
        full_query = query
        x = ()
        for variable in variables:
            x = x + (extensions.adapt(str(variable)).getquoted().decode('utf-8'),)
        full_query = full_query % x
        print("QUERY TO EXECUTE: " + (full_query.replace('    ', ' ')))
        #put the query on the list so we can check later if need be
        self.queries.append(full_query)

        #if there are multiple sets of rows, set the next set of rows
        #    and increase the current counter
        if len(self.row_sets) > 0:
            self.rows = self.row_sets[self.current_index]
            self.rowcount = len(self.rows)
            self.current_index += 1
            if self.current_index >= len(self.row_sets):
                self.current_index = 0

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
        all_rows = self.fetchall()
        return all_rows[0]
    def set_rows(self, rows):
        self.rows = rows
    def set_exception(self, raise_exception):
        self.raise_exception = raise_exception
    def add_row_set(self, rows):
        self.row_sets.append(rows)
    

class MockPsycopgConnection:
    def __init__(self, raise_exception = False, rows = [], **kwargs):
        self.raise_exception = raise_exception
        self.rows = rows
        self.my_cursor = MockPsycopgCursor(raise_exception = self.raise_exception, rows = self.rows)
        pass
    def cursor(self):
        return self.my_cursor
    def close(self):
        return True
    def commit(self):
        return True
    def set_cursor(self, cursor):
        self.my_cursor = cursor



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

def patch_cursor(mocker, rows=[], **kwargs):
    """
    Adds all the required mocking for DB connections
    """
    mock_connection = MockPsycopgConnection(rows=rows)
    # mock_cursor = mock_connection.cursor()
    mock_cursor = MockPsycopgCursor(rows=rows)
    if 'result_sets' in kwargs:
        for result_set in kwargs.get('result_sets'):
            mock_cursor.add_row_set(result_set)
    mock_connection.set_cursor(mock_cursor)

    mocker.patch("psycopg2.connect", return_value=mock_connection)
    return mock_cursor, mock_connection

def patch_user(mocker, **kwargs):
    """
    Adds all required mocking for a logged in user
    """
    
    mock_response = MockResponse()
    # if 'status_code' in kwargs:
    mock_response.set_status_code(kwargs.get('status_code', 200))
    mock_response.set_json(kwargs.get("json", {}))
    mocker.patch("requests.post", return_value=mock_response)
    # mock_user = user_model.User(user_id=1, token="token")
    # mocker.patch('middleware.api.views.user_model.User.query', user_model.Query())
    # mocker.patch('middleware.api.views.user_model.User.verify_auth_token', return_value=mock_user)
