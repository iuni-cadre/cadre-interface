import pytest
# import mock
# from pytest_mock import mocker
import json
from pprint import pprint

from backend import application
# import pprint
# pp = pprint.PrettyPrinter(indent = 2)

# from flask import Flask, render_template, request, json, jsonify



class MockResponse:
    #Mocks up a response object and lets you set the error code
    def __init__(self):
        #default is a 200 success response
        self.status_code = 200
        self.json_data = None
    def set_status_code(self, status_code):
        self.status_code = status_code
    def json(self):
        return self.json_data
    def set_json(self, fake_json):
        self.json_data = fake_json


class MockPsycopgCursor:
    def __init__(self, raise_exception = False, rows = [], **kwargs):
        self.rows = rows
        self.raise_exception = raise_exception
    def close(self):
        return True
    def execute(self, query, variables):
        if(self.raise_exception):
            raise Exception('Fake Exception') 
        pass
    def fetchall(self):
        return self.rows
    def set_rows(self, rows):
        self.rows = rows
    def set_exception(self, raise_exception):
        self.raise_exception = raise_exception

class MockPsycopgConnection:
    def __init__(self, raise_exception = False, rows = [], **kwargs):
        self.raise_exception = raise_exception
        self.rows = rows
        pass
    def cursor(self):
        return MockPsycopgCursor(raise_exception = self.raise_exception, rows = self.rows)
    def close(self):
        return True


@pytest.fixture
def client():
    """Fixture allowing us to mock requests and test endpoints."""
    client = application.app.test_client()

    yield client
    return client


def test_user_jobs_ep_exists(client):
    """
    If there is an error and the status code is 404 and the error message is "Unknown endpoint."
    then the endpoint is unknown, so fail.
    """

    rv = client.get('/qi-api/user-jobs')
    json = rv.get_json()
    unknown_endpoint = False
    if json["error"] and rv.status_code == 404 and json["error"] == "Unknown endpoint.":
        unknown_endpoint = True

    assert not unknown_endpoint


def test_user_jobs_ep_fails_without_proper_headers(client):
    """
    end point needs at least the auth-auth and auth-user headers
    """

    rv = client.get('/qi-api/user-jobs')
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/qi-api/user-jobs', headers= {
        'auth-username': "SOME USERNAME"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/qi-api/user-jobs', headers= {
        'auth-token': "SOME TOKEN"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    
def test_user_jobs_ep_accepts_proper_headers(client):
    """
    end point gets past the missing header check with both headers
    """

    rv = client.get('/qi-api/user-jobs', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 400



def test_user_jobs_ep_does_fail_with_invalid_credentials(client, mocker):
    """
    mocker fakes a 401 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(401)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/qi-api/user-jobs', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 403


def test_user_jobs_ep_does_not_fail_with_valid_credentials(client, mocker):
    """
    mocker fakes a 200 response from authenticator endpoint to pass verification
    """
    
    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/qi-api/user-jobs', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 403


def test_user_jobs_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "roles": "some_roles",
        "user_id": "12345"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection()
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/qi-api/user-jobs', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })
    
    assert rv.status_code == 200


def test_user_jobs_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''
    
    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "roles": "some_roles",
        "user_id": "12345"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True) #raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/qi-api/user-jobs', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })
    
    assert rv.status_code == 500



def test_user_jobs_ep_returns_jsonified_jobs_from_db(client, mocker):
    '''
    Checks that the endpoint is returning json that matches the mocked up data
    '''
    
    rows = [
        [
            12345, 
            23456, 
            'http://www.example.com', 
            'RUNNING', 
            "date", 
            "date", 
            "query", 
            "random description"
        ],
        [
            12345, 
            23456, 
            'http://www.example.com', 
            'RUNNING', 
            "date", 
            "date", 
            "query", 
            "random description"
        ],
        [
            12345, 
            23456, 
            'http://www.example.com', 
            'RUNNING', 
            "date", 
            "date", 
            "query", 
            "random description"
        ]
    ]

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "roles": "some_roles",
        "user_id": "12345"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(rows = rows)
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/qi-api/user-jobs', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })
    
    pprint(rv.get_json())
    pprint(rows);
    assert rv.get_json() == (rows)
