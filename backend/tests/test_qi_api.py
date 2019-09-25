import pytest
from backend import application
from pprint import pprint
# import pprint
# pp = pprint.PrettyPrinter(indent = 2)

# from flask import Flask, render_template, request, json, jsonify



# import boto3


@pytest.fixture
def client():
    """Fixture allowing us to mock requests and test endpoints."""
    client = application.app.test_client()

    yield client
    return client


def test_user_jobs_ep_exists(client):
    """
    If there is an error and the status code is 404 and the error message is "Unknown endpoint."
    then the endpoint is unknown, so fail.
    """
    
    rv = client.get('/qi-api/user-jobs')
    json = rv.get_json()
    unknown_endpoint = False
    if json["error"] and rv.status_code == 404 and json["error"] == "Unknown endpoint.":
        unknown_endpoint = True

    assert not unknown_endpoint
