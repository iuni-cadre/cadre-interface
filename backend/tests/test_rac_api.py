import pytest
import os
import requests
import sys

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from library import readconfig

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_cursor, patch_user



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


def test_no_unknown_endpoints(client):
    """
    All endpoints exist are not a 404
    """
    failed_paths = []
    for path in ALL_ENDPOINTS:
        p = '{0}'.format(path)
        rv = client.get(p)
        ENDPOINT_METHODS[path] = "GET"
        result_json = rv.get_json()
        if result_json is None:
            result_json = {}
    
        if rv.status_code == 404 and result_json.get("error", "None") == "Unknown endpoint.":
            rv = client.post(p)
            ENDPOINT_METHODS[path] = "POST"

        json_results = {}
        try: 
            json_results = rv.get_json()
        except:
            pass

        if rv.status_code == 405: #method must be allowed
            failed_paths.append('{0} - {1}'.format(p, rv.status_code))
        # if rv.status_code == 404:
        #     failed_paths.append('{0} - {1} - Some other problem'.format(p, rv.status_code))
        if rv.status_code == 404 and json_results and json_results.get("error") == "Unknown endpoint.": #if returns 404, it must not be because of an unknown endpoint error
            failed_paths.append('{0} - {1}'.format(p, rv.status_code))
            pprint(json_results)
    assert failed_paths == ['/api/failonme - 404']


def test_for_401_on_invalid_credentials(client, mocker):
    auth_token = "FAKE_TOKEN"
    headers_options = [
        {},
        {
            "auth-token": auth_token
        },
        {
            "auth-username": "fakeUser"
        }
    ]
    json_to_send = {
        "username": "some username",
        "password": "fake password",
    }
    failed_paths = []

    for path in ALL_ENDPOINTS:
        rv = None
        p = "{0}".format(path)
        for headers in headers_options:
            if ENDPOINT_METHODS[path] == "GET":
                rv = client.get(p, headers=headers, content_type='application/json', data=json.dumps(json_to_send))
            else:
                rv = client.post(p, headers=headers, content_type='application/json', data=json.dumps(json_to_send))
            if rv.status_code != 401:
                error = '{0} - {1}'.format(p, rv.status_code)
                failed_paths.append(error)
    assert failed_paths == ['/api/failonme - 404','/api/failonme - 404','/api/failonme - 404']

    #doesn't fail with 401 if has headers
    failed_paths = []
    headers = {
        "auth-token": auth_token,
        "auth-username": "fake_username"
    }
    for path in ALL_ENDPOINTS:
        rv = None
        p = "{0}".format(path)
        if ENDPOINT_METHODS[path] == "GET":
            rv = client.get(p, headers=headers, content_type='application/json', data=json.dumps(json_to_send))
        else:
            rv = client.post(p, headers=headers, content_type='application/json', data=json.dumps(json_to_send))
        if rv.status_code == 401:
            error = '{0} - {1}'.format(p, rv.status_code)
            failed_paths.append(error)
    assert failed_paths == []


    # rv = client.get('/qi-api/user-jobs')
    # json = rv.get_json()
    # assert rv.status_code == 401
    # assert json["error"] and json["error"] == "auth headers are missing"

    # rv = client.get('/qi-api/user-jobs', headers= {
    #     'auth-username': "SOME USERNAME"
    # })
    # json = rv.get_json()
    # assert rv.status_code == 401
    # assert json["error"] and json["error"] == "auth headers are missing"

    # rv = client.get('/qi-api/user-jobs', headers= {
    #     'auth-token': "SOME TOKEN"
    # })
    # json = rv.get_json()
    # assert rv.status_code == 401
    # assert json["error"] and json["error"] == "auth headers are missing"

def test_for_403_on_invalid_user(client, mocker):

    #doesn't fail with 401 if has headers
    failed_paths = []
    headers = {
        "auth-token": "fake_token",
        "auth-username": "fake_username"
    }
    json_to_send = {}
    
    # mock_response = MockResponse()
    # mock_response.set_status_code(401)
    # mocker.patch("requests.post", return_value=mock_response)
    patch_cursor(mocker)
    patch_user(mocker, status_code = 401)
    for path in ALL_ENDPOINTS:
        rv = None
        p = "{0}".format(path)
        if ENDPOINT_METHODS[path] == "GET":
            rv = client.get(p, headers=headers, content_type='application/json', data=json.dumps(json_to_send))
        else:
            rv = client.post(p, headers=headers, content_type='application/json', data=json.dumps(json_to_send))
        if rv.status_code != 403:
            error = '{0} - {1}'.format(p, rv.status_code)
            failed_paths.append(error)
    assert failed_paths == ['/api/failonme - 404']


ENDPOINT_METHODS = {}

ALL_ENDPOINTS = [
    '/api/failonme',
    # "/api/auth/authenticate-token",
    # "/api/auth/logout",
    # "/api/cognito/callback",
    # "/api/cognito/logout",
    # "/api/data/publications-async",
    # "/api/data/publications-sync",
    "/qi-api/user-jobs",
    "/rac-api/packages/run-package",
    "/rac-api/packages/get-packages",
    "/rac-api/packages/get-package/:package_id",
    "/rac-api/packages/new",
    "/rac-api/get-tools",
    "/rac-api/get-tools/user",
    "/rac-api/get-tool/:tool_id",
    # "/rac-api/tools/new", #not yet implemented
    "/rac-api/get-data-archives",
    # "/rac-api/archive-user-file", #not yet implemented
    "/rac-api/user-files",
    "/rac-api/new-notebook/<username>",
    "/rac-api/notebook-status/<username>",
    "/rac-api/get-new-notebook-token/<username>",
    # "/api/rac/jobs/{job_id}",
    # "/api/rac/teams",
    # "/api/rac/teams/{team_id}" ,
    # "/api/rac/teams/new",
    # "/api/rac/teams/user-add/<user_id>",
    # "/api/rac/teams/user-remove/<user_id>",
    # "/api/rac/datasets",
    # "/api/rac/notebooks",
    # "/api/rac/notebooks/user/<user_id>",
    # "/api/rac/notebooks/team/<team_id>",
    # "/api/rac/notebooks/{notebook_id}",
    # "/api/rac/data-assets/",
    # "/api/rac/data-assets/{data-set}",
    # "/api/rac/data-assets/{asset-id}/move-to-notebook/{notebook-id}",
    # "/api/rac/institutions/",
    # "/api/rac/institutions/{institution}",
    # "/api/notebook/new-token",
    # "/api/notebook/new",
    # "/api/notebook/new/team/{team-id}",
    # "/api/notebook/status",
    # "/api/notebook/publish",
    # "/rac-api/packages/run-package",
    # "/rac-api/packages/get-packages"
]
