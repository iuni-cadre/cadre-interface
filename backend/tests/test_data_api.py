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

import routefunctions.data_api as data_api
    # wos_filter_string = {"job_name": "", "filters": [{"field": "year", "value": "2005", "operation": ""}], "output": [
    #     {"field": "wos_id", "type": "single"}, {"field": "year", "type": "single"}, {"field": "authors_full_name", "type": "single"}], "dataset": "wos"}


def test_gen_wos_query_exists(client):
    query, value_array = data_api.generate_wos_query('string', [])
    assert query == 'SELECT string FROM wos_core.interface_table WHERE  LIMIT 10'
    assert value_array == []

def test_gen_mag_query_exists(client):
    query, value_array = data_api.generate_mag_query('string', [])
    assert query == 'SELECT string FROM mag_core.interface_table WHERE LIMIT 10'
    assert value_array == []

# def test_gen_wos_query_exists(client):
#     data_api.generate_wos_query('string', [])

    # for path in ALL_ENDPOINTS:
    #     p = '{0}'.format(path)
    #     rv = client.get(p)
    #     ENDPOINT_METHODS[path] = "GET"
    #     result_json = rv.get_json()
    #     if result_json is None:
    #         result_json = {}

    #     if rv.status_code == 404 and result_json.get("error", "None") == "Unknown endpoint.":
    #         rv = client.post(p)
    #         ENDPOINT_METHODS[path] = "POST"

    #     json_results = {}
    #     try:
    #         json_results = rv.get_json()
    #     except:
    #         pass

    #     if rv.status_code == 405: #method must be allowed
    #         failed_paths.append('{0} - {1}'.format(p, rv.status_code))
    #     # if rv.status_code == 404:
    #     #     failed_paths.append('{0} - {1} - Some other problem'.format(p, rv.status_code))
    #     if rv.status_code == 404 and json_results and json_results.get("error") == "Unknown endpoint.": #if returns 404, it must not be because of an unknown endpoint error
    #         failed_paths.append('{0} - {1}'.format(p, rv.status_code))
    #         pprint(json_results)
    # assert failed_paths == ['/api/failonme - 404']
