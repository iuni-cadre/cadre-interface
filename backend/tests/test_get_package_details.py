import pytest
import os
import requests
import sys

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from library import readconfig
from datetime import datetime

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_cursor, patch_user




def test_get_package_details_from_package_id_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/packages/get-package/123456789', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500



def test_get_package_details_from_package_id_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''
    now = datetime.now()
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

    patch_cursor(mocker, rows)

    rv = client.get('/rac-api/packages/get-package/1234567890', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })
    # pprint(rv.data)
    assert rv.status_code == 200
    assert rv.get_json() == expected_output


def test_get_package_details_from_package_id_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''
    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/packages/get-package/<package_id>', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500
