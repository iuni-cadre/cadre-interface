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
