import traceback
import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify
from datetime import date

blueprint = Blueprint('rac_api_profile', __name__)

from library import readconfig, utilities
import boto3

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
aws_config = readconfig.aws

# Get user profile information
@blueprint.route('/rac-api/profile/get-user-profile', methods=['GET'])
def get_user_profile():
    """
    This is a method which returns the user's profile details.

    Args:
        user_id
    Returns:
        Json object of 
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json'
    }

    headers = {
        'auth-token': auth_token,
        'auth-username': username
    }
    is_valid, validate_token_response = utilities.validate_user(headers=headers)
    if not is_valid:
        return validate_token_response

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    if not user_id:
        return jsonify({"error": "Invalid user"}), 401

    #user_id: request.get_json().get("user_id", None)

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = (
            'SELECT '
                'user_id as user_id, '
                'display_name as display_name, '
                'agreement_signed as agreement_signed, '
                'date_agreement_signed as date_agreement_signed, '
                'access_form_fields as access_form_fields, '
                'university, '
                'campus, '
                'department, '
                'research_area '
            'FROM user_profile '
            'WHERE user_id=%s '
        )
        cur.execute(query, (user_id,))
        if cur.rowcount == 0:
            return jsonify({"error": "Could not find profile for user {}".format(user_id)}), 404

        results = cur.fetchall()
        user_profile = results[0]

        response = {
            "user_id": user_profile[0],
            "display_name": user_profile[1],
            "agreement_signed": user_profile[2],
            "date_agreement_signed": user_profile[3],
            "access_form_fields": user_profile[4],
            "university": user_profile[5],
            "campus": user_profile[6],
            "department": user_profile[7],
            "research_area": user_profile[8]
        }
        return jsonify(response)
    except Exception as err:
        print(err)
        return jsonify({"error": "Problem querying the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


# Create new user profile
@blueprint.route('/rac-api/profile/create-user-profile', methods=['POST'])
def create_user_profile():
    """
    This is a method that inserts a new user record

    Args:
        user_id
    Returns:
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    headers = {
        'auth-token': auth_token,
        'auth-username': username
    }
    is_valid, validate_token_response = utilities.validate_user(headers=headers)
    if not is_valid:
        return validate_token_response

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    if not user_id:
        return jsonify({"error": "Invalid user"}), 401


    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()
    # Creating/updating new record and changing display_name 
    try:
        insert_query = ("INSERT INTO user_profile (user_id) VALUES (%s)")
        cur.execute(insert_query, (user_id,))
        return jsonify({'Create': 'Successful'}), 200
    except Exception as err:
        print(err)
        return jsonify({"error":  "Problem updating the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

# Update user profile
@blueprint.route('/rac-api/profile/update-user-profile', methods=['POST'])
def update_user_profile():
    """
    This is a method that updates the user profile elements

    Args:
        user_id
        new_display_name
        university
        campus
        department
        research_area
    Returns:
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    headers = {
        'auth-token': auth_token,
        'auth-username': username
    }
    is_valid, validate_token_response = utilities.validate_user(headers=headers)
    if not is_valid:
        return validate_token_response

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    if not user_id:
        return jsonify({"error": "Invalid user"}), 401

    #If None, don't update
    response_json = request.get_json()
    new_display_name = response_json.get("new_display_name", None)

    if not new_display_name:
        return jsonify({"error": "Invalid request"}), 400

    university = response_json.get("university", "")
    campus = response_json.get("campus", "")
    department = response_json.get("department", "")
    research_area = response_json.get("research_area", "")

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()
    # Creating/updating new record and changing display_name 
    try:
        update_query = (
            "UPDATE user_profile "
            "SET "
                "display_name = %s, "
                "university = %s, "
                "campus = %s, "
                "department = %s, "
                "research_area = %s "
            "WHERE user_id = %s"
            )
        cur.execute(update_query, (new_display_name, university, campus, department, research_area, user_id,))
        return jsonify({'Update': 'Successful'}), 200
    except Exception as err:
        print(str(err))
        return jsonify({"error":  "Problem updating the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

# Update user profile
@blueprint.route('/rac-api/profile/update-user-agreement', methods=['POST'])
def update_user_agreement():
    """
    This is a method that updates the user profile elements

    Args:
        user_id
        access_form_fields
    Returns:
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    headers = {
        'auth-token': auth_token,
        'auth-username': username
    }
    is_valid, validate_token_response = utilities.validate_user(headers=headers)
    if not is_valid:
        return validate_token_response

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    if not user_id:
        return jsonify({"error": "Invalid user"}), 401

    #If None, don't update 
    access_form_fields = request.get_json().get("access_form_fields", None)
    if not access_form_fields:
        return jsonify({"error": "Invalid request"}), 400

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()
    # Creating/updating new record and changing display_name 
    try:
        update_query = ("UPDATE user_profile SET access_form_fields = %s, agreement_signed = TRUE, date_agreement_signed = NOW() WHERE user_id= %s")
        cur.execute(update_query, (json.dumps(access_form_fields), user_id,))
        return jsonify({'Update': 'Successful'}), 200
    except Exception as err:
        print(str(err))
        return jsonify({"error":  "Problem updating the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")



