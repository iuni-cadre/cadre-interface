import pytest
import os
import requests
import sys
import datetime

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from library import readconfig

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_cursor, patch_user, patch_settings


def test_publish_packages_ep_exists(client, mocker):
    """
    test that /rac-api/packages/publish endpoint exists
    """


    rv = client.post('/rac-api/packages/publish', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    },
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_publish_packages_ep_fails_if_missing_params(client, mocker):
    """
    test that /rac-api/packages/publish fails if missing header, params (package_id)
    """
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    patch_user(mocker, json={"user_id":"FAKEUSERID"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])

    #not missing params
    rv = client.post('/rac-api/packages/publish', headers=headers,
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))
    assert rv.status_code != 400
    assert rv.status_code == 200

    #params absent
    rv = client.post('/rac-api/packages/publish', headers=headers)
    assert rv.status_code == 500
    
    #headers absent
    rv = client.post('/rac-api/packages/publish',
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))
    assert rv.status_code == 401

    #headers malformed
    rv = client.post('/rac-api/packages/publish', headers={},
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))
    assert rv.status_code == 401
    
    # #empty json
    # rv = client.post('/rac-api/packages/publish', headers=headers,
    # content_type='application/json', data=json.dumps({
    #     "package_id": "1234567890"
    # }))
    # assert rv.status_code == 500



def test_publish_tools_ep_exists(client, mocker):
    """
    test that '/rac-api/tools/publish' endpoint exists
    """


    rv = client.post('/rac-api/tools/publish', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    },
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_publish_tools_ep_fails_if_missing_params(client, mocker):
    """
    test that '/rac-api/tools/publish' fails if missing header, params (package_id)
    """
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    patch_user(mocker, json={"user_id":"FAKEUSERID"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])

    #not missing params
    rv = client.post('/rac-api/tools/publish', headers=headers,
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))
    assert rv.status_code != 400
    assert rv.status_code == 200

    #params absent
    rv = client.post('/rac-api/tools/publish', headers=headers)
    assert rv.status_code == 500
    
    #headers absent
    rv = client.post('/rac-api/tools/publish',
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))
    assert rv.status_code == 401

    #headers malformed
    rv = client.post('/rac-api/tools/publish', headers={},
    content_type='application/json', data=json.dumps({
        "package_id": "1234567890"
    }))
    assert rv.status_code == 401
    
    # #empty json
    # rv = client.post('/rac-api/tools/publish', headers=headers,
    # content_type='application/json', data=json.dumps({
    #     "package_id": "1234567890"
    # }))
    # assert rv.status_code == 500



