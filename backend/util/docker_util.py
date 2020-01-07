import os

import jinja2

conf_path = os.path.abspath(os.path.dirname(__file__))

docker_info = {
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


def create_python_dockerfile():
    template_loader = jinja2.FileSystemLoader(searchpath=conf_path)
    template_env = jinja2.Environment(loader=template_loader)
    TEMPLATE_FILE = "python3.7_dockerfile_template"
    template = template_env.get_template(TEMPLATE_FILE)
    outputText = template.render(docker_info=docker_info)  # this is where to put args to the template renderer

    print(outputText)


if __name__ == "__main__":
    create_python_dockerfile()
