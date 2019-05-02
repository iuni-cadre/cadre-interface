#!/bin/bash

#rebuild node app
pushd ../frontend
if [ ! -d "./node_modules" ]; then
    exec npm ci &
    wait
fi
exec npm run build &
wait

pushd ../deployment