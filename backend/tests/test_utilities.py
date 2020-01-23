import pytest
import hashlib
import os
# import requests
# import sys

from flask import Flask, render_template, request, json, jsonify
from pprint import pprint
from backend import application
from library import readconfig, utilities

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

def test_calc_checksum():
    """
    check that calc_checksum gets called correctly
    """
    content = "this is a temp file".encode('utf-8')
    checksum = hashlib.md5(content).hexdigest()

    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
    except Exception as err:
        print(str(err))
        pass

    new_checksum = utilities.calc_checksum("/tmp/username/temp_file.txt")

    assert new_checksum == checksum
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")



def test_calc_checksum():
    """
    check that validate_checksum works gets called correctly
    """
    content = "this is a temp file".encode('utf-8')
    checksum = hashlib.md5(content).hexdigest()

    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
    except Exception as err:
        print(str(err))
        pass

    assert utilities.validate_checksum("/tmp/username/temp_file.txt", checksum)
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")


