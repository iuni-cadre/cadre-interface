#!/bin/bash
pushd ../conf
mv frontend.config.json frontend.config.json.tmp
mv deploy.frontend.config.json frontend.config.json
#rebuild node app
pushd ../frontend
if [ ! -d "./node_modules" ]; then
    exec npm ci &
    wait
fi
exec npm run build &
wait

pushd ../conf
mv frontend.config.json deploy.frontend.config.json
mv frontend.config.json.tmp frontend.config.json

pushd ../deployment