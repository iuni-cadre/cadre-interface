
import pytest
import os
import requests
import sys

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from backend.library import readconfig

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse


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


# def test_get_data_archives_ep_fails_without_proper_headers(client):
#     """
#     End point needs at least the auth-auth and auth-user headers
#     """
#     rv = client.get('/rac-api/get-data-archives')
#     json = rv.get_json()
#     assert rv.status_code == 401
#     assert json["error"] and json["error"] == "auth headers are missing"

#     rv = client.get('/rac-api/get-data-archives', headers={
#         'auth-username': "SOME USERNAME"
#     })
#     json = rv.get_json()
#     assert rv.status_code == 401
#     assert json["error"] and json["error"] == "auth headers are missing"

#     rv = client.get('/rac-api/get-data-archives', headers={
#         'auth-token': "SOME TOKEN"
#     })
#     json = rv.get_json()
#     assert rv.status_code == 401
#     assert json["error"] and json["error"] == "auth headers are missing"


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
           'archive_id': "11234221137",
            's3_location': "/cadre-file-archive/yan30",
            'archive_description': "tar file",
            'archive_name': "ISSIDemoData.tar.gz",
            'archive_created_on': "2019-08-23 17:17:34.196818+00:00"
        }
    ]

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)
    # mock_response.set_json({
    #     "archive_id": "11234221137",
    #     "s3_location": "/cadre-file-archive/yan30",
    #     "archive_description": "tar file",
    #     "archive_name": "ISSIDemoData.tar.gz",
    #     "archive_created_on": "2019-08-23 17:17:34.196818+00:00"
    # })

    mock_connection = MockPsycopgConnection(rows=rows)
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    # pprint(rv.get_json())
    # pprint(rows);
    assert rv.get_json() == (rows)
