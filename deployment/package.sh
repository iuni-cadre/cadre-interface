#!/bin/bash

pushd ..

# create the bundle
rm -rf ./bundle
mkdir ./bundle
# mkdir ./bundle/.ebextensions
mkdir ./bundle/conf
# cp -r ./conf/.ebextensions ./bundle
cp -r ./frontend/dist ./bundle/frontend
cp ./conf/backend.config ./bundle/conf/backend.config
cp ./backend/requirements.txt ./bundle/requirements.txt
cp ./backend/application.py ./bundle/application.py
cp -r ./.ebextensions ./bundle

pushd deployment