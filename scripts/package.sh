#!/bin/bash

pushd ..

# create the bundle
rm -rf ./bundle
mkdir ./bundle
# mkdir ./bundle/.ebextensions
mkdir ./bundle/conf
# cp -r ./conf/.ebextensions ./bundle
cp -r ./frontend/dist ./bundle/frontend
cp ./conf/deploy.backend.config ./bundle/conf/backend.config
cp ./conf/example.backend.config ./bundle/conf/example.backend.config
cp ./backend/requirements.txt ./bundle/requirements.txt
cp ./backend/application.py ./bundle/application.py
mkdir ./bundle/library ./bundle/routefunctions
cp -r ./backend/library/*.py ./bundle/library
cp -r ./backend/routefunctions/*.py ./bundle/routefunctions
cp -r ./.ebextensions ./bundle

pushd deployment