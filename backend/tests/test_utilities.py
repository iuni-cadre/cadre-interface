import pytest
# import os
# import requests
# import sys

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from backend.library import readconfig, utilities

# test = readconfig.test

# url = 'http://aa36a4acbbb4311e991df02800e92ef4-1296978337.us-east-2.elb.amazonaws.com/hub/api' # This is the URL of the Jupyter Notebook API

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_cursor, patch_user



def test_validate_user_returns_403():
    """
    See if we can import and use validate_user utility function
    """
    with application.application.app_context():
        is_valid, (resp, status) = utilities.validate_user()
        
        assert status == 401
    pass
