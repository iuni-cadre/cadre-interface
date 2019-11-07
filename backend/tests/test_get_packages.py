import pytest
import os
import requests
import sys
import datetime

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from backend.library import readconfig

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse


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

    now = datetime.datetime.now()

    rows = [
        [
            '1234567890', #package_id, 
            'type', #type, 
            'some description', #description, 
            'package_name', #name, 
            'doi_number', #doi, 
            now, #created_on, 
            'cadre team', #created_by, 
            'tool_1', #tool_id, 
            'tool_desc1', #tool_description, 
            'tool_name1', #tool_name, 
            'tool_script.py', #tool_script_name, 
            'input1.csv,input2.csv'#input_files 
        ],
        [
            '1234567890', #package_id, 
            'type', #type, 
            'some description', #description, 
            'package_name', #name, 
            'doi_number', #doi, 
            now, #created_on, 
            'cadre team', #created_by, 
            'tool_2', #tool_id, 
            'tool_desc2', #tool_description, 
            'tool_name2', #tool_name, 
            'tool_script2.py', #tool_script_name, 
            'input1.csv,input2.csv'#input_files 
        ]
    ]

    expected_output = [
        {
            'package_id': '1234567890',
            'type': 'type',
            'description': 'some description',
            'name': 'package_name',
            'doi': 'doi_number',
            'created_on': now.isoformat(),
            'created_by': 'cadre team',
            'tools': [
                {
                    'tool_id': 'tool_1',
                    'description': 'tool_desc1',
                    'name': 'tool_name1',
                    'tool_script_name': 'tool_script.py',
                    # 'tool_script_name': packages[10]
                },
                {
                    'tool_id': 'tool_2',
                    'description': 'tool_desc2',
                    'name': 'tool_name2',
                    'tool_script_name': 'tool_script2.py',
                    # 'tool_script_name': packages[10]
                }
            ],
            'input_files': 'input1.csv,input2.csv'
        }
    ]

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    mock_connection = MockPsycopgConnection(rows=rows)
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/packages/get-packages', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }) 

    pprint(rv.get_json())
    pprint(expected_output)
    assert rv.get_json() == (expected_output)

