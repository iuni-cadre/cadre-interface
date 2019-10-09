import pytest
import os
import requests
import sys

from flask import Flask, render_template, request, json, jsonify

from pprint import pprint

abspath = os.path.abspath(os.path.dirname(__file__))
middleware = abspath + '\\cadre-interface'
backend = middleware + '\\backend'
library = backend + '\\library'
sys.path.append(backend)
sys.path.append(library)

from backend import application

from library import readconfig

test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API


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
        return self.rows

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


@pytest.fixture
def client():
    """Fixture allowing us to mock requests and test endpoints."""
  # application.app.config["TESTING"] = True
    client = application.app.test_client()

    yield client
    return client


def test_api_endpoints():
    """
    This is a method to test if the get notebook api endpoint is working correctly
    """
    # response = requests.get(url + '/')
    # assert response.status_code == 200
    pass


def test_notebook_status():
    """
    This is a method to test whether the notebook status api endpoint is working correctly
    """
    # response = requests.get(url + '/rac-api/notebook-status/m52xa5dbmfsg')
    # assert response.status_code == 200
    pass


def test_get_tools_ep_exists(client):
    """
    This is a method to test if the get tools api endpoint is working correctly
    """
    rv = client.get('/rac-api/get-tools')
    json = rv.get_json()
    unknown_endpoint = False
    if json["error"] and rv.status_code == 404 and json["error"] == "Unknown endpoint.":
        unknown_endpoint = True

    assert not unknown_endpoint


def test_get_tools_ep_fails_without_proper_headers(client):
    """
    The end point needs at least the auth-auth and auth-user headers
    """

    rv = client.get('/rac-api/get-tools')
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/get-tools', headers= {
        'auth-username': "SOME USERNAME"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/get-tools', headers= {
        'auth-token': "SOME TOKEN"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"


def test_get_tools_ep_accepts_proper_headers(client):
    """
    End point gets past the missing header check with both headers
    """

    rv = client.get('/rac-api/get-tools', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 400


def test_get_tools_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/get-tools?limit=50&page=1&order=name&search=', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500


def test_get_tools_ep_does_fail_with_invalid_credentials(client, mocker):
    """
    Mocker fakes a 401 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(401)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/get-tools', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 403


def test_get_tools_ep_does_not_fail_with_valid_credentials(client, mocker):
    """
    Mocker fakes a 200 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/get-tools', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 403


def test_get_tools_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "tool_id": "11234221128",
        "tool_description": "Data for the ISSI tutorial",
        "tool_name": "issi_data",
        "tool_script_name": "issi_tutorial.py",
        "created_on": "2019-08-23T16:01:33.935043+00:00"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection()
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-tools', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 200


def test_get_tools_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "tool_id": "11234221128",
        "tool_description": "Data for the ISSI tutorial",
        "tool_name": "issi_data",
        "tool_script_name": "issi_tutorial.py",
        "created_on": "2019-08-23T16:01:33.935043+00:00"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-tools', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500


def test_get_packages_ep_exists(client):
    """
    This is a method to test if the get packages api endpoint is working correctly
    """
    rv = client.get('/rac-api/packages/get-packages')
    json = rv.get_json()
    unknown_endpoint = False
    if json["error"] and rv.status_code == 404 and json["error"] == "Unknown endpoint.":
        unknown_endpoint = True

    assert not unknown_endpoint


def test_get_packages_ep_fails_without_proper_headers(client):
    """
    The end point needs at least the auth-auth and auth-user headers
    """

    rv = client.get('/rac-api/packages/get-packages')
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/packages/get-packages', headers= {
        'auth-username': "SOME USERNAME"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/packages/get-packages', headers= {
        'auth-token': "SOME TOKEN"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"


def test_get_packages_ep_accepts_proper_headers(client):
    """
    End point gets past the missing header check with both headers
    """

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 400


def test_get_packages_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/packages/get-packages?limit=50&page=1&order=name&search=', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500


def test_get_packages_ep_does_fail_with_invalid_credentials(client, mocker):
    """
    Mocker fakes a 401 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(401)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 403


def test_get_packages_ep_does_not_fail_with_valid_credentials(client, mocker):
    """
    Mocker fakes a 200 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 403


def test_get_packages_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "package_id": "234221136",
        "type": "CADRE_DEFINED",
        "description": "package for delivering the data for the tutorial",
        "name": "issi_data_package",
        "doi": "",
        "created_on": "2019-08-23 17:17:34.196818+00:00",
        "created_by": "",
        "tools": [{"tool_id": "11234221128", "tool_description": "Data for the ISSI tutorial", "tool_name": "issi_data", 'tool_script_name': "issi_tutorial.py"}],
        "input_files": "ISSIDemoData.tar.gz"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection()
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 200


def test_get_packages_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "package_id": "234221136",
        "type": "CADRE_DEFINED",
        "description": "package for delivering the data for the tutorial",
        "name": "issi_data_package",
        "doi": "",
        "created_on": "2019-08-23 17:17:34.196818+00:00",
        "created_by": "",
        "tools": [{"tool_id": "11234221128", "tool_description": "Data for the ISSI tutorial", "tool_name": "issi_data", 'tool_script_name': "issi_tutorial.py"}],
        "input_files": "ISSIDemoData.tar.gz"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500


def test_get_packages_ep_returns_jsonified_jobs_from_db(client, mocker):
    '''
    Checks that the endpoint is returning json that matches the mocked up data
    '''

    rows = [
        [
            "234221136",
            "CADRE_DEFINED",
            "package for delivering the data for the tutorial",
            "issi_data_package",
            "",
            "2019-08-23 17:17:34.196818+00:00",
            "",
            [{"11234221128", "Data for the ISSI tutorial", "issi_data", "issi_tutorial.py"}],
            "ISSIDemoData.tar.gz"
        ],
        [
            "234221136",
            "CADRE_DEFINED",
            "package for delivering the data for the tutorial",
            "issi_data_package",
            "",
            "2019-08-23 17:17:34.196818+00:00",
            "",
            [{"11234221128", "Data for the ISSI tutorial", "issi_data", "issi_tutorial.py"}],
            "ISSIDemoData.tar.gz"
        ],
        [
            "234221136",
            "CADRE_DEFINED",
            "package for delivering the data for the tutorial",
            "issi_data_package",
            "",
            "2019-08-23 17:17:34.196818+00:00",
            "",
            [{"11234221128", "Data for the ISSI tutorial", "issi_data", "issi_tutorial.py"}],
            "ISSIDemoData.tar.gz"
        ]
    ]

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "package_id": "234221136",
        "type": "CADRE_DEFINED",
        "description": "package for delivering the data for the tutorial",
        "name": "issi_data_package",
        "doi": "",
        "created_on": "2019-08-23 17:17:34.196818+00:00",
        "created_by": "",
        "tools": [{"tool_id": "11234221128", "tool_description": "Data for the ISSI tutorial", "tool_name": "issi_data",
                   'tool_script_name': "issi_tutorial.py"}],
        "input_files": "ISSIDemoData.tar.gz"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(rows=rows)
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    pprint(rv.get_json())
    pprint(rows);
    assert rv.get_json() == (rows)


def test_get_user_files_ep_exists(client):
    """
    This is a method to test if the get user files api endpoint is working correctly
    """
    rv = client.get('/rac-api/user-files')
    json = rv.get_json()
    unknown_endpoint = False
    if json["error"] and rv.status_code == 404 and json["error"] == "Unknown endpoint.":
        unknown_endpoint = True

    assert not unknown_endpoint


def test_get_user_files_ep_fails_without_proper_headers(client):
    """
    The end point needs at least the auth-auth and auth-user headers
    """

    rv = client.get('/rac-api/user-files')
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/packages/get-packages', headers= {
        'auth-username': "SOME USERNAME"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/user-files', headers= {
        'auth-token': "SOME TOKEN"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"


def test_get_user_files_ep_accepts_proper_headers(client):
    """
    End point gets past the missing header check with both headers
    """

    rv = client.get('/rac-api/user-files', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 400


def test_get_user_files_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/user-files?level=3&path=/packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500


def test_get_user_files_ep_does_fail_with_invalid_credentials(client, mocker):
    """
    Mocker fakes a 401 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(401)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/user-files', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 403


def test_get_user_files_ep_does_not_fail_with_valid_credentials(client, mocker):
    """
    Mocker fakes a 200 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/user-files', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 403


def test_get_package_details_from_package_id_ep_accepts_proper_headers(client):
    """
    End point gets past the missing header check with both headers
    """

    rv = client.get('/rac-api/get-package/<package_id>', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 400


def test_get_package_details_from_package_id_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/get-package?package_id=234221136', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500


def test_get_package_details_from_package_id_ep_does_fail_with_invalid_credentials(client, mocker):
    """
    Mocker fakes a 401 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(401)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/get-package/<package_id>', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 403


def test_get_package_details_from_package_id_ep_does_not_fail_with_valid_credentials(client, mocker):
    """
    Mocker fakes a 200 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/get-package/<package_id>', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 403


def test_get_package_details_from_package_id_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "package_id": "234221136",
        "type": "CADRE_DEFINED",
        "description": "package for delivering the data for the tutorial",
        "name": "issi_data_package",
        "doi": "",
        "created_on": "2019-08-23 17:17:34.196818+00:00",
        "created_by": "",
        "tools": [{"tool_id": "11234221128", "tool_description": "Data for the ISSI tutorial", "tool_name": "issi_data", 'tool_script_name': "issi_tutorial.py"}],
        "input_files": "ISSIDemoData.tar.gz"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection()
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-package/<package_id>', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 200


def test_get_package_details_from_package_id_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "package_id": "234221136",
        "type": "CADRE_DEFINED",
        "description": "package for delivering the data for the tutorial",
        "name": "issi_data_package",
        "doi": "",
        "created_on": "2019-08-23 17:17:34.196818+00:00",
        "created_by": "",
        "tools": [{"tool_id": "11234221128", "tool_description": "Data for the ISSI tutorial", "tool_name": "issi_data", 'tool_script_name': "issi_tutorial.py"}],
        "input_files": "ISSIDemoData.tar.gz"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-package/<package_id>', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500


def test_get_tool_details_from_tool_id(client):
    """
    This is a method to test if the get details of the tool from the tool id is working correctly
    """
    tool_id = '11234221124'
    rv = client.get('/rac-api/get-tool/{}'.format(tool_id))
    assert rv.status_code == 401


def test_get_data_archives_ep_exists(client):
    """
    If there is an error and the status code is 404 and the error message is "Unknown endpoint."
    then the endpoint is unknown, so fail.
    """
    rv = client.get('/rac-api/get-data-archives')
    json = rv.get_json()
    unknown_endpoint = False

    if json["error"] and rv.status_code == 404 and json["error"] == "Unknown endpoint.":
        unknown_endpoint = True

    assert not unknown_endpoint


def test_get_data_archives_ep_fails_without_proper_headers(client):
    """
    End point needs at least the auth-auth and auth-user headers
    """
    rv = client.get('/rac-api/get-data-archives')
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-username': "SOME USERNAME"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "SOME TOKEN"
    })
    json = rv.get_json()
    assert rv.status_code == 401
    assert json["error"] and json["error"] == "auth headers are missing"


def test_get_data_archives_ep_accepts_proper_headers(client):
    """
    End point gets passes the missing header check with both headers
    """
    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 400


def test_get_data_archives_ep_does_fail_with_invalid_credentials(client, mocker):
    """
     Mocker fakes a 401 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(401)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 403


def test_get_data_archives_ep_does_not_fail_with_valid_credentials(client, mocker):
    """
    Mocker fakes a 200 response from authenticator endpoint to pass verification
    """

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 403


def test_get_data_archives_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "archive_id": "11234221137",
        "s3_location": "/cadre-file-archive/yan30",
        "archive_description": "tar file",
        "archive_name": "ISSIDemoData.tar.gz",
        "archive_created_on": "2019-08-23 17:17:34.196818+00:00"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection()
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 200


def test_get_data_archives_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "archive_id": "11234221137",
        "s3_location": "/cadre-file-archive/yan30",
        "archive_description": "tar file",
        "archive_name": "ISSIDemoData.tar.gz",
        "archive_created_on": "2019-08-23 17:17:34.196818+00:00"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500


def test_get_data_archives_ep_returns_jsonified_jobs_from_db(client, mocker):
    '''
    Checks that the endpoint is returning json that matches the mocked up data
    '''

    rows = [
        {
           "11234221137",
            "/cadre-file-archive/yan30",
            "tar file",
            "ISSIDemoData.tar.gz",
            "2019-08-23 17:17:34.196818+00:00"
        }
    ]

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "archive_id": "11234221137",
        "s3_location": "/cadre-file-archive/yan30",
        "archive_description": "tar file",
        "archive_name": "ISSIDemoData.tar.gz",
        "archive_created_on": "2019-08-23 17:17:34.196818+00:00"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(rows=rows)
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    pprint(rv.get_json())
    pprint(rows);
    assert rv.get_json() == (rows)
