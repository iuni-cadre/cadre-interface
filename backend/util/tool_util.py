import os
import traceback

import boto3
import jinja2
from library import readconfig

conf_path = os.path.abspath(os.path.dirname(__file__))
aws_config = readconfig.aws
efs_path = aws_config['efs_path']
s3_file_archive = aws_config['s3_file_archive_name']
s3_tool_location = aws_config['s3_tools_location_name']
aws_access_key_id = aws_config['aws_access_key_id']
aws_secret = aws_config['aws_secret_access_key']
aws_region = aws_config['region_name']

docker_template_json = {
    'copy_files': [
        {'name': 'requirements.txt'},
        {'name': 'xnet.py'},
        {'name': '__init__.py'}
    ],
    'entrypoint': '__init__.py',
    'commands': [
        {'name': 'apt-get update && apt-get install -y build-essential python3-dev libxml2 libxml2-dev zlib1g-dev'},
        {'name': 'pip install -r requirements.txt'}
    ]
}


def create_python_dockerfile_and_upload_s3(tool_id, docker_template_json):
    try:
        s3_client = boto3.resource('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret,
                                   region_name=aws_region)
        template_loader = jinja2.FileSystemLoader(searchpath=conf_path)
        template_env = jinja2.Environment(loader=template_loader)
        TEMPLATE_FILE = "python3.7_dockerfile_template"
        template = template_env.get_template(TEMPLATE_FILE)
        dockerfile_content = template.render(docker_info=docker_template_json)  # this is where to put args to the template renderer
        dockerfile_s3_subpath = tool_id + "/Dockerfile"
        s3_client.Object(s3_tool_location, dockerfile_s3_subpath).put(Body=dockerfile_content)
    except (Exception) as error:
        traceback.print_tb(error.__traceback__)
        print("Error while archiving files to s3")


# archive files to s3
# file paths are relative to users home directory
# need to get the efs home from config
def archive_input_files(files, username):
    try:
        s3_client = boto3.resource('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret,
                                   region_name=aws_region)

        for file in files:
            file_full_path = efs_path + "/" + file
            filename = os.path.basename(file_full_path)
            s3_archive_sub_path = username + '/' + filename
            s3_client.meta.client.upload_file(file_full_path, s3_file_archive, s3_archive_sub_path)
    except (Exception) as error:
        traceback.print_tb(error.__traceback__)
        print("Error while archiving files to s3")


# upload tool script files to s3 tool location
# file paths are relative to users home directory
# need to get the efs home from config
def upload_tool_scripts_to_s3(files, tool_id):
    try:
        s3_client = boto3.resource('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret,
                                   region_name=aws_region)

        for file in files:
            file_full_path = efs_path + "/" + file
            filename = os.path.basename(file_full_path)
            s3_tool_sub_path = tool_id + '/' + filename
            s3_client.meta.client.upload_file(file_full_path, s3_tool_location, s3_tool_sub_path)
    except (Exception) as error:
        traceback.print_tb(error.__traceback__)
        print("Error while uploading files to s3 tool location")


if __name__ == "__main__":
    create_python_dockerfile_and_upload_s3('test_tool_id', docker_template_json)
