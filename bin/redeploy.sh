#!/bin/sh

# Sample script to build and redeploy application as docker image

commit_id=$1
commiter_name=$2
commiter_email=$3

echo "Redeploying commit id $commit_id from $commiter_name ..."

#cd /usr/share/repos/IWAPharmacyDirect
git pull --force
#docker-compose down
mvn clean package
#docker build . --tag iwa:latest
#docker-compose up -d

echo "Done."
