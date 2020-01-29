import pytest
import os
import requests
import sys

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from library import readconfig
import datetime

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_cursor, patch_user


def test_get_tools_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/get-tools?limit=50&page=1&order=name&search=', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500



def test_get_tools_ep_does_not_fail_with_successful_query(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    rows = sample_rows
    patch_user(mocker)
    patch_cursor(mocker, rows)

    expected_result = [
        {
            "tool_id": "123456",
            "tool_description": "some tool description",
            "tool_name": "tool name",
            "tool_script_name": "script_name.py",
            "created_on": global_now.isoformat(),
            "created_by": 1000
            
        },
        {
            "tool_id": "123456",
            "tool_description": "some tool description 2",
            "tool_name": "tool name 2",
            "tool_script_name": "script_name2.py",
            "created_on": global_now.isoformat(),
            "created_by": 1000
        }
    ]


    rv = client.get('/rac-api/get-tools', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 200
    assert rv.get_json() == expected_result


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



def test_get_tool_ep_returns_correct_json(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''
    #get first row from sample rows
    rows = [sample_rows[0]]
    patch_user(mocker)
    patch_cursor(mocker, rows)

    expected_result = {
        "tool_id": "123456",
        "description": "some tool description",
        "name": "tool name",
        "script_name": "script_name.py",
        "created_on": global_now.isoformat()
        }
    

    rv = client.get('/rac-api/get-tool/123456', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 200
    assert rv.get_json() == expected_result



# get-tools/user
 ######   ######## ########         ########  #######   #######  ##        ######        ## ##     ##  ######  ######## ########  
##    ##  ##          ##               ##    ##     ## ##     ## ##       ##    ##      ##  ##     ## ##    ## ##       ##     ## 
##        ##          ##               ##    ##     ## ##     ## ##       ##           ##   ##     ## ##       ##       ##     ## 
##   #### ######      ##    #######    ##    ##     ## ##     ## ##        ######     ##    ##     ##  ######  ######   ########  
##    ##  ##          ##               ##    ##     ## ##     ## ##             ##   ##     ##     ##       ## ##       ##   ##   
##    ##  ##          ##               ##    ##     ## ##     ## ##       ##    ##  ##      ##     ## ##    ## ##       ##    ##  
 ######   ########    ##               ##     #######   #######  ########  ######  ##        #######   ######  ######## ##     ## 



def test_get_tools_user_exists(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/get-tools/user', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_get_tools_user_ep_accepts_params(client):
    """
    End point doesn't blow up when we send parameters
    """

    rv = client.get('/rac-api/get-tools/user?limit=50&page=1&order=name&search=', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code != 500



def test_get_tools_user_ep_returns_expected_result(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    rows = sample_rows
    patch_user(mocker, json={"user_id": 1, "roles": []})
    patch_cursor(mocker, rows)

    expected_result = [
        {
            "tool_id": "123456",
            "tool_description": "some tool description",
            "tool_name": "tool name",
            "tool_script_name": "script_name.py",
            "created_on": global_now.isoformat(),
            "created_by": 1000
            
        },
        {
            "tool_id": "123456",
            "tool_description": "some tool description 2",
            "tool_name": "tool name 2",
            "tool_script_name": "script_name2.py",
            "created_on": global_now.isoformat(),
            "created_by": 1000
        }
    ]


    rv = client.get('/rac-api/get-tools/user', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })
    # pprint(rv.get_json())
    assert rv.status_code == 200
    assert rv.get_json() == expected_result


def test_get_tools_user_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''

    # mock_response = MockResponse()
    # mock_response.set_status_code(200)
    # mock_response.set_json({
    #     "tool_id": "11234221128",
    #     "tool_description": "Data for the ISSI tutorial",
    #     "tool_name": "issi_data",
    #     "tool_script_name": "issi_tutorial.py",
    #     "created_on": "2019-08-23T16:01:33.935043+00:00"
    # })
    # mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    patch_user(mocker, json={"user_id": 1, "roles": []})

    rv = client.get('/rac-api/get-tools/user', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500







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
        "123456",
        "some tool description",
        "tool name",
        "script_name.py",
        global_now,
        1000
        
    ],
    [
        "123456",
        "some tool description 2",
        "tool name 2",
        "script_name2.py",
        global_now,
        1000
        
    ]
]