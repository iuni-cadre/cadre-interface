#!/bin/bash
rm -rf ./bundle
mkdir ./bundle
mkdir ./bundle/frontend
cp -r ./frontend/dist ./bundle/frontend
cp ./backend/requirements.txt ./bundle/requirements.txt
cp ./backend/application.py ./bundle/application.py
pushd bundle

# python -m venv virt
# source ./virt/bin/activate
# pip install -r requirements.txt

pushd ..
zip -r eb_bundle.zip bundle

rm -rf ./bundle
