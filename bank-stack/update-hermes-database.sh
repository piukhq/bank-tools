#!/bin/bash

################################################################################
# export staging hermes database, import it locally
################################################################################

#Options:
#-d <directory> : directory in which to install/run merchant services
#-u <username> : database username to be stored in .env
#-p <password> : database password to be stored in .env

while getopts ":d:u:p:r:i:s:" opt; do
  case $opt in
    d) directory="$OPTARG"
    ;;
    u) username="$OPTARG"
    ;;
    p) db_password="$OPTARG"
    ;;
    r) db_update="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&6
    exit 1
    ;;
  esac
done

kubectl config use-context uksouth-staging
kubectl port-forward deploy/proxy-postgres 5432:5432 &
sleep 5

pg_dump $(kubectl get secret azure-pgfs -o json | jq -r .data.common_hermes | base64 --decode | sed 's/bink-uksouth-.*.postgres.database.azure.com/127.0.0.1/g') > ~/hermes.sql
sleep 4
kill %1
wait



uri=postgresql://$db_username:$db_password@localhost:5432
psql $uri -c 'DROP DATABASE IF EXISTS hermes';

psql postgresql://$db_username:$db_password@localhost:5432/hermes < ~/hermes.sql
sleep 4

# clean up
rm hermes.sql

