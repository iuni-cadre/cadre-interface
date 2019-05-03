#!/bin/bash
pushd scripts
exec ./compile.sh &
wait
pushd ..

pushd scripts
exec ./package.sh &
wait
pushd ..

rm -rf ../eb_bundle*.zip

pushd bundle
today=`date '+%Y-%m-%d--%H-%M-%S'`
zip -r ../eb_bundle.zip -r * .[^.]*
# zip -r ../eb_bundle-$today.zip -r * .[^.]*

#remove the temporary bundle directory
pushd ..
rm -rf ./bundle

exec eb deploy -v &
wait
exec eb status -v 
