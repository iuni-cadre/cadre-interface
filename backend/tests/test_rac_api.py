import pytest
import os
import requests
import sys

from flask import Flask, render_template, request, json, jsonify

from backend import application

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API


@pytest.fixture
def client():
    application.app.config['TESTING'] = True
    client = application.app.test_client()

    yield client


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


def test_get_tools(client):
    """
    This is a method to test if the get tools api endpoint is working correctly
    """
    rv = client.get('/rac-api/packages/get-tools')
    assert rv.status_code == 200


def test_get_packages(client):
    """
    This is a method to test if the get packages api endpoint is working correctly
    """
    rv = client.get('/rac-api/packages/get-packages')
    assert rv.status_code == 200


def test_get_user_files(client):
    """
    This is a method to test if the get all the files and folders of a single user api endpoint is working correctly
    """
    rv = client.get('/rac-api/user-files')
    assert rv.status_code == 200


def test_get_package_details_from_package_id(client):
    """
    This is a method to test if the get details of the package from the package id is working correctly
    """
    package_id = '234221133'
    rv = client.get('/rac-api/get-package/{}').format(package_id)
    assert rv.status_code == 200


def test_get_tool_details_from_tool_id(client):
    """
    This is a method to test if the get details of the tool from the tool id is working correctly
    """
    tool_id = '11234221124'
    rv = client.get('/rac-api/get-tool/{}').format(tool_id)
    assert rv.status_code == 200
