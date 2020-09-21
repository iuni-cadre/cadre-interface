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

# get-user-profile

def test_get_user_profile_ep_exists(client, mocker):
    """
    test that /rac-api/profile/get-user-profile endpoint exists
    """


    rv = client.get('/rac-api/profile/get-user-profile', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    },
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_get_user_profile_ep_fails_if_missing_params(client, mocker):
    """
    test that /rac-api/profile/get-user-profilefails if missing header, params (user_id)
    """
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    patch_user(mocker, json={"user_id":"1234567890"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])

    #not missing params
    rv = client.get('/rac-api/profile/get-user-profile', headers=headers,
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code != 400
    assert rv.status_code == 200

    #params absent
    rv = client.get('/rac-api/profile/get-user-profile', headers=headers)
    assert rv.status_code == 500
    
    #headers absent
    rv = client.get('/rac-api/profile/get-user-profile',
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code == 401

    #headers malformed
    rv = client.get('/rac-api/profile/get-user-profile', headers={},
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code == 401


# create-user-profile

def test_create_user_profile_ep_exists(client, mocker):
    """
    test that /rac-api/profile/get-user-profile endpoint exists
    """


    rv = client.post('/rac-api/profile/create-user-profile', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    },
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_create_user_profile_ep_fails_if_missing_params(client, mocker):
    """
    test that /rac-api/profile/create-user-profile fails if missing header, params (user_id)
    """
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    patch_user(mocker, json={"user_id":"1234567890"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])

    #not missing params
    rv = client.post('/rac-api/profile/create-user-profile', headers=headers,
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code != 400
    assert rv.status_code == 200

    #params absent
    rv = client.post('/rac-api/profile/create-user-profile', headers=headers)
    assert rv.status_code == 500
    
    #headers absent
    rv = client.post('/rac-api/profile/create-user-profile',
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code == 401

    #headers malformed
    rv = client.post('/rac-api/profile/create-user-profile', headers={},
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code == 401

# /rac-api/profile/update-user-profile

def test_update_user_profile_ep_exists(client, mocker):
    """
    test that /rac-api/profile/update-user-profile endpoint exists
    """


    rv = client.post('/rac-api/profile/update-user-profile', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    },
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "new_display_name": "test user"
    }))

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_update_user_profile_ep_fails_if_missing_params(client, mocker):
    """
    test that /rac-api/profile/update-user-profile fails if missing header, params (user_id)
    """
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    patch_user(mocker, json={"user_id":"1234567890"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])

    #not missing params
    rv = client.post('/rac-api/profile/update-user-profile', headers=headers,
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890"
    }))
    assert rv.status_code != 400
    assert rv.status_code == 200

    #params absent
    rv = client.post('/rac-api/profile/update-user-profile', headers=headers)
    assert rv.status_code == 500
    
    #headers absent
    rv = client.post('/rac-api/profile/update-user-profile',
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "new_display_name": "test user"
    }))
    assert rv.status_code == 401

    #headers malformed
    rv = client.post('/rac-api/profile/update-user-profile', headers={},
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "new_display_name": "test user"
    }))
    assert rv.status_code == 401

# /rac-api/profile/update-user-agreement

def test_update_user_agreement_ep_exists(client, mocker):
    """
    test that /rac-api/profile/update-user-agreement endpoint exists
    """


    rv = client.post('/rac-api/profile/update-user-agreement', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    },
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "access_form_fields": '[{"first_name":"test","middle_initial":"","last_name":"test","university":"University of Toronto","department":"test","research_area":"test","university_email_address":"test","agree_access_policy":true,"agree_not_share_data":true,"agree_not_share_username":true,"agree_safeguard_username":true,"agree_unauthorized_responsibility":true,"agree_loss_control":true,"agree_publications_acknowledge":true,"agree_receive_emails":true,"agree_works_submitted":true,"agree_comply":true}]'
    }))

    response_json = rv.get_json()
    assert rv.status_code != 404
    if response_json:
        assert response_json["error"] != "Unknown endpoint."


def test_update_user_agreement_ep_fails_if_missing_params(client, mocker):
    """
    test that /rac-api/profile/update-user-agreement fails if missing header, params (user_id)
    """
    headers = {
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    }
    patch_user(mocker, json={"user_id":"1234567890"})
    mock_cursor, mock_connection = patch_cursor(mocker, [[]])

    #not missing params
    rv = client.post('/rac-api/profile/update-user-agreement', headers=headers,
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "access_form_fields": '[{"first_name":"test","middle_initial":"","last_name":"test","university":"University of Toronto","department":"test","research_area":"test","university_email_address":"test","agree_access_policy":true,"agree_not_share_data":true,"agree_not_share_username":true,"agree_safeguard_username":true,"agree_unauthorized_responsibility":true,"agree_loss_control":true,"agree_publications_acknowledge":true,"agree_receive_emails":true,"agree_works_submitted":true,"agree_comply":true}]'
    }))
    assert rv.status_code != 400
    assert rv.status_code == 200

    #params absent
    rv = client.post('/rac-api/profile/update-user-agreement', headers=headers)
    assert rv.status_code == 500
    
    #headers absent
    rv = client.post('/rac-api/profile/update-user-agreement',
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "access_form_fields": '[{"first_name":"test","middle_initial":"","last_name":"test","university":"University of Toronto","department":"test","research_area":"test","university_email_address":"test","agree_access_policy":true,"agree_not_share_data":true,"agree_not_share_username":true,"agree_safeguard_username":true,"agree_unauthorized_responsibility":true,"agree_loss_control":true,"agree_publications_acknowledge":true,"agree_receive_emails":true,"agree_works_submitted":true,"agree_comply":true}]'
    }))
    assert rv.status_code == 401

    #headers malformed
    rv = client.post('/rac-api/profile/update-user-agreement', headers={},
    content_type='application/json', data=json.dumps({
        "user_id": "1234567890",
        "access_form_fields": '[{"first_name":"test","middle_initial":"","last_name":"test","university":"University of Toronto","department":"test","research_area":"test","university_email_address":"test","agree_access_policy":true,"agree_not_share_data":true,"agree_not_share_username":true,"agree_safeguard_username":true,"agree_unauthorized_responsibility":true,"agree_loss_control":true,"agree_publications_acknowledge":true,"agree_receive_emails":true,"agree_works_submitted":true,"agree_comply":true}]'
    }))
    assert rv.status_code == 401