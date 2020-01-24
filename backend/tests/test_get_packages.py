import pytest
import os
import requests
import sys
import datetime

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from library import readconfig

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_user, patch_cursor




def test_get_packages_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/packages/get-packages?limit=50&page=1&order=name&search=', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500


def test_get_packages_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''
    rows = sample_rows
    patch_user(mocker)
    patch_cursor(mocker, rows)

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
    now = global_now

    rows = sample_rows

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


# def test_packages_new_fails_if_missing_params(client, mocker):
#     headers = {
#         'auth-token': "Some Token",
#         'auth-username': "Some Username"
#     }
#     patch_user(mocker)
#     rv = client.post('/rac-api/packages/new', headers=headers) 
#     assert rv.status_code == 400

#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         "name": "somename",
#         "description": "fake_data",
#         "tools": "fake_data",
#         "input_files": "fake.csv",
#         "archive_id": "1234",
#         "type": "sometype"
#     })) 
#     assert rv.status_code != 400

#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         # "name": "somename",
#         "description": "fake_data",
#         "tools": "fake_data",
#         "input_files": "fake.csv",
#         "archive_id": "1234",
#         "type": "sometype"
#     })) 
#     assert rv.status_code == 400
    
#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         "name": "somename",
#         # "description": "fake_data",
#         "tools": "fake_data",
#         "input_files": "fake.csv",
#         "archive_id": "1234",
#         "type": "sometype"
#     })) 
#     assert rv.status_code == 400
#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         "name": "somename",
#         "description": "fake_data",
#         # "tools": "fake_data",
#         "input_files": "fake.csv",
#         "archive_id": "1234",
#         "type": "sometype"
#     })) 
#     assert rv.status_code == 400
#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         "name": "somename",
#         "description": "fake_data",
#         "tools": "fake_data",
#         # "input_files": "fake.csv",
#         "archive_id": "1234",
#         "type": "sometype"
#     })) 
#     assert rv.status_code == 400
#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         "name": "somename",
#         "description": "fake_data",
#         "tools": "fake_data",
#         "input_files": "fake.csv",
#         # "archive_id": "1234",
#         "type": "sometype"
#     })) 
#     assert rv.status_code == 400
#     rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
#         "name": "somename",
#         "description": "fake_data",
#         "tools": "fake_data",
#         "input_files": "fake.csv",
#         "archive_id": "1234",
#         # "type": "sometype"
#     })) 
#     assert rv.status_code == 400

def test_packages_new_sends_correct_user_id(client, mocker):
    patch_user(mocker, json={"user_id":"FAKEUSERID"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    mocker.patch("uuid.uuid4", return_value="uuid_test")
    rv = client.post('/rac-api/packages/new', headers=headers, content_type='application/json', data=json.dumps({
        "name": "string_1",
        "description": "string_2",
        "tools": "string_3",
        "input_files": "string_4",
        "archive_id": "string_5",
        "type": "string_6"
    })) 

    #query index 0 should be the index query
    assert mock_cursor.queries[0].count('FAKEUSERID') > 0
    assert mock_cursor.queries[0].count('uuid_test') > 0
    assert mock_cursor.queries[0].count('string_1') > 0
    assert mock_cursor.queries[0].count('string_2') > 0
    assert mock_cursor.queries[0].count('string_6') > 0

 ######     ###    ##     ## ########  ##       ########    ########     ###    ########    ###    
##    ##   ## ##   ###   ### ##     ## ##       ##          ##     ##   ## ##      ##      ## ##   
##        ##   ##  #### #### ##     ## ##       ##          ##     ##  ##   ##     ##     ##   ##  
 ######  ##     ## ## ### ## ########  ##       ######      ##     ## ##     ##    ##    ##     ## 
      ## ######### ##     ## ##        ##       ##          ##     ## #########    ##    ######### 
##    ## ##     ## ##     ## ##        ##       ##          ##     ## ##     ##    ##    ##     ## 
 ######  ##     ## ##     ## ##        ######## ########    ########  ##     ##    ##    ##     ## 
global_now = datetime.datetime.now()
sample_rows = [
    [
        '1234567890', #package_id, 
        'type', #type, 
        'some description', #description, 
        'package_name', #name, 
        'doi_number', #doi, 
        global_now, #created_on, 
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
        global_now, #created_on, 
        'cadre team', #created_by, 
        'tool_2', #tool_id, 
        'tool_desc2', #tool_description, 
        'tool_name2', #tool_name, 
        'tool_script2.py', #tool_script_name, 
        'input1.csv,input2.csv'#input_files 
    ]
]