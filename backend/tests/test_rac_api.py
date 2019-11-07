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




