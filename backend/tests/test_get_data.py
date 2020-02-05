
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

from .conftest import MockPsycopgConnection, MockPsycopgCursor, MockResponse, patch_cursor, patch_user, patch_settings, patch_boto3

headers = {
        'auth-token': "Some Token",
        'auth-username': "username"
    }

def test_get_data_archives_ep_returns_404_on_empty_results(client, mocker):
    '''
    Uses psycopg mock to mock DB call
    '''

    patch_user(mocker)
    #gets empty result
    patch_cursor(mocker, [])

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 404



def test_get_data_archives_ep_fails_on_db_exception(client, mocker):
    '''
    Uses psycopg mock to mock DB call with exception
    '''

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mock_response.set_json({
        "archive_id": "11234221137",
        "s3_location": "/cadre-file-archive/yan30",
        "archive_description": "tar file",
        "archive_name": "ISSIDemoData.tar.gz",
        "archive_created_on": "2019-08-23 17:17:34.196818+00:00"
    })
    mocker.patch("requests.post", return_value=mock_response)
    mock_connection = MockPsycopgConnection(raise_exception=True)  # raise exception
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    assert rv.status_code == 500


def test_get_data_archives_ep_returns_jsonified_jobs_from_db(client, mocker):
    '''
    Checks that the endpoint is returning json that matches the mocked up data
    '''

    rows = [
        {
           'archive_id': "11234221137",
            's3_location': "/cadre-file-archive/yan30",
            'archive_description': "tar file",
            'archive_name': "ISSIDemoData.tar.gz",
            'archive_created_on': "2019-08-23 17:17:34.196818+00:00"
        }
    ]

    mock_response = MockResponse()
    mock_response.set_status_code(200)
    mocker.patch("requests.post", return_value=mock_response)

    mock_connection = MockPsycopgConnection(rows=rows)
    mocker.patch("psycopg2.connect", return_value=mock_connection)

    rv = client.get('/rac-api/get-data-archives', headers={
        'auth-token': "Some Token",
        'auth-username': "Some Username"
    })

    # pprint(rv.get_json())
    # pprint(rows);
    assert rv.status_code == 200
    assert rv.get_json() == (rows)



def test_archive_user_file_requires_params(client, mocker):
    '''
    Endpoint requires parameters
    '''

    # rows = [
    #     {
    #        'archive_id': "11234221137",
    #         's3_location': "/cadre-file-archive/yan30",
    #         'archive_description': "tar file",
    #         'archive_name': "ISSIDemoData.tar.gz",
    #         'archive_created_on': "2019-08-23 17:17:34.196818+00:00"
    #     }
    # ]

    # mock_response = MockResponse()
    # mock_response.set_status_code(200)
    # mocker.patch("requests.post", return_value=mock_response)

    # mock_connection = MockPsycopgConnection(rows=rows)
    # mocker.patch("psycopg2.connect", return_value=mock_connection)
    patch_user(mocker)
    patch_cursor(mocker)

    json_to_send = {
        # "file_path": "/some_path/some_file",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    assert rv.status_code == 400

    json_to_send = {
        "file_path": "/some_path/some_file",
        # "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    assert rv.status_code == 400

    json_to_send = {
        "file_path": "/some_path/some_file",
        "archive_name": "My Query Results",
        # "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    assert rv.status_code != 400


def test_archive_user_file_reads_a_file_from_efs(client, mocker):
    '''
    Endpoint can read a file from filesystem
    '''
    patch_user(mocker)
    patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker)

    json_to_send = {
        "file_path": "/temp_file.txt",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    assert rv.status_code == 400

    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass


    json_to_send = {
        "file_path": "/temp_file.txt",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")
    assert rv.status_code != 400



def test_archive_user_file_fails_gracefully_on_s3_error(client, mocker):
    '''
    Endpoint throws 500 error if there's an s3 error
    '''
    patch_user(mocker)
    patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker, raise_exception=True)
    
    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass

    json_to_send = {
        "file_path": "/temp_file.txt",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")

    assert rv.status_code == 502
    assert rv.get_json().get("error") == "Couldn't upload file to s3"


def test_archive_user_file_insert_into_archive_table(client, mocker):
    '''
    Endpoint generates proper sql statement for insert based on parameters
    '''
    patch_user(mocker)
    mock_cursor, mock_connection = patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker)
    mocker.patch("uuid.uuid4", return_value="some_unique_id")
    mock_cursor.add_row_set([[1, "wos"]])
    mock_cursor.add_row_set([[]])
    
    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass

    json_to_send = {
        "file_path": "/temp_file.txt",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    insert_query = """INSERT INTO archive 
        (
            archive_id,
            query_result_id,
            s3_location,
            description,
            name,
            permissions,
            created_on,
            modified_on,
            created_by,
            modified_by
        )
        VALUES
        (
            'some_unique_id',
            1,
            '/cadre-file-archive/archives/some_unique_id/temp_file.txt',
            'Some Description',
            'My Query Results',
            '{"data_type":"wos", "other":[]}',
            NOW(),
            NOW(),
            1,
            1
        )
    """

    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")
    print(mock_cursor.queries)
    assert len(mock_cursor.queries) == 2
    assert mock_cursor.queries[1].replace(' ', '').replace('\n', '') == insert_query.replace(' ', '').replace('\n', '')


def test_archive_user_file_returns_archive_id_upon_success(client, mocker):
    '''
    Endpoint returns archive id on successful archiving
    '''
    patch_user(mocker)
    mock_cursor, mock_connection = patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker)
    mocker.patch("uuid.uuid4", return_value="some_unique_id")
    mock_cursor.add_row_set([[1, "wos"]])
    mock_cursor.add_row_set([[]])
        
    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass

    json_to_send = {
        "file_path": "/temp_file.txt",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")

    assert rv.status_code == 200
    assert rv.get_json().get("archive_id") == "some_unique_id"



def test_archive_user_file_fails_gracefully_if_invalid_file(client, mocker):
    '''
    Endpoint throws 403 error if trying to archive a non cadre file
    '''
    patch_user(mocker)
    mock_cursor, mock_connection = patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker)
    mocker.patch("uuid.uuid4", return_value="some_unique_id")
    mock_cursor.add_row_set([])
    mock_cursor.add_row_set([[]])
        
    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass

    json_to_send = {
        "file_path": "/temp_file.txt",
        "archive_name": "My Query Results",
        "archive_description": "Some Description"
    }
    rv = client.post('/rac-api/archive-user-file', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")

    assert rv.status_code == 403
    assert rv.get_json().get("error") == "Attempting to archive a non-authentic file"



def test_archive_user_file_check_403_on_inauthentic(client, mocker):
    '''
    Endpoint returns 403 error if file is not authentic cadre file
    '''
    patch_user(mocker)
    mock_cursor, mock_connection = patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker)
    mocker.patch("uuid.uuid4", return_value="some_unique_id")
    mock_cursor.add_row_set([])
        
    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass

    json_to_send = {
        "file_path": "/temp_file.txt"
    }
    rv = client.post('/rac-api/archive-user-file/check', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")

    assert rv.status_code == 403
    assert rv.get_json().get("error") == "File could not be verified as authentic"


def test_archive_user_file_check_200_and_permissions(client, mocker):
    '''
    Endpoint returns a 200 and the permissions for the given file if a success
    '''
    patch_user(mocker)
    mock_cursor, mock_connection = patch_cursor(mocker)
    patch_settings(mocker)
    patch_boto3(mocker)
    mocker.patch("uuid.uuid4", return_value="some_unique_id")
    mock_cursor.add_row_set([[1, "wos"]])
        
    try:
        os.mkdir("/tmp/username")
        tmp_file = open("/tmp/username/temp_file.txt", "a")
        tmp_file.write("this is a temp file")
        tmp_file.close()
    except Exception as err:
        print(str(err))
        pass

    json_to_send = {
        "file_path": "/temp_file.txt"
    }
    rv = client.post('/rac-api/archive-user-file/check', headers = headers, content_type='application/json', data=json.dumps(json_to_send))
    
    os.remove("/tmp/username/temp_file.txt")
    os.rmdir("/tmp/username")

    assert rv.status_code == 200
    assert rv.get_json().get("data_type") == "wos"

