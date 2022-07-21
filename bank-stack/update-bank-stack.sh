#!/bin/bash

################################################################################
# runs the Hermes & Angelia services needed to get API 1 & 2 up & running
# TODO: Pelops
# Requires:
#     hermes, angelia & metis code, postgres database etc etc 
#     tmux
################################################################################

# This script will install, set environments, git pull Hermes, Hermes database & Angelia
# - git (authenticated in cli via either HTTPS or SSH (see below parameters))

#Options:
#-d <directory> : directory in which to install/run merchant services
#-u <username> : database username to be stored in .env
#-p <password> : database password to be stored in .env
#-i true : installs and updates services from staging (including git branch, .envs, databases (if -r true)). Otherwise just runs services
#-r true : reads and copies in latest databases from staging (if omitted, but -i true, will install/update without affecting database)
#-s true : uses SSH to clone git repositories (if omitted defaults to HTTPS)

# If you do not have an existing hermes admin account in staging, you will need to create a superuser for access 
# From hermes root directory > pipenv run python manage.py createsuperuser & follow the prompts

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
    i) install_or_update="$OPTARG"
    ;;
    s) ssh="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&6
    exit 1
    ;;
  esac
done

 if [[ ! $directory ]] ; then
    directory="${PWD}"
  fi

  if [[ ! $username ]] ; then
  db_username="postgres"
  fi

if [[ ! $db_password ]] ; then
  db_password=""
  fi

if [[ $ssh = "true"  ]] ; then
    github_prefix="git@github.com:"
  else
    github_prefix="https://github.com/"
  fi

setup_services() {

HERMES_ENV_FILE=$(
        cat <<EOF
HERMES_DATABASE_HOST=localhost
HERMES_DATABASE_PORT=5432
MIDAS_URL=http://0.0.0.0:8001
MASTER_LOG_LEVEL=INFO
UBIQUITY_LOG_LEVEL=INFO
METIS_URL=http://127.0.0.1:8095
VAULT_URL=https://bink-uksouth-dev-com.vault.azure.net/
SSO_OFF=True
LOCAL_SECRETS=False
PROMETHEUS_LOG_LEVEL=ERROR
HERMES_LOCAL=True

EOF
    )


ANGELIA_ENV_FILE=$(
        cat <<EOF

LOG_LEVEL=DEBUG
LOCAL_SECRETS=False
POSTGRES_READ_DSN=postgresql://postgres@127.0.0.1:5432/hermes
POSTGRES_WRITE_DSN=postgresql://postgres@127.0.0.1:5432/hermes
RABBIT_PASSWORD=guest
RABBIT_USER=guest
RABBIT_HOST=127.0.0.1
RABBIT_PORT=5672
HERMES_URL=http://127.0.0.1:8000
METRICS_SIDECAR_DOMAIN=localhost
METRICS_PORT=4000
PERFORMANCE_METRICS=0
VAULT_URL=https://bink-uksouth-dev-com.vault.azure.net/
QUERY_LOGGING=False

EOF
    )

# Set up services
echo "- Setting up services in directory: $directory"

echo $directory
echo $exclude

# Hermes

cd $directory

if [[ ! -d "hermes" ]] ; then
  echo "- Cloning Hermes..." && git clone "${github_prefix}binkhq/hermes.git"
  fi

cd hermes

echo "- (Hermes) Checking out and updating master branch..."
git checkout master
git pull --ff-only origin master

echo "- (Hermes) Synching .env and pipenv..."
echo "$HERMES_ENV_FILE" > .env && pipenv sync --dev


# Angelia

cd $directory

if [[ ! -d "Angelia" ]] ; then
  echo "- Cloning angelia..." && git clone "${github_prefix}binkhq/angelia.git"
  fi

cd angelia

echo "- (Angelia) Checking out and updating master branch..."
git checkout master
git pull --ff-only origin master

echo "- (Angelia) Synching .env and pipenv..."
echo "$ANGELIA_ENV_FILE" > .env && pipenv sync --dev

# Create/update databases

cd $directory

if [[ $db_update = "true" ]] ; then

  kubectl config use-context uksouth-staging

  kubectl port-forward deploy/proxy-postgres 5432:5432 &
  sleep 3

  pg_dump $(kubectl get secret azure-pgfs -o json | jq -r .data.common_hermes | base64 --decode | sed 's/bink-uksouth-.*.postgres.database.azure.com/127.0.0.1/g') > $directory/hermes.sql
  sleep 4

  kill %1
  wait

  uri=postgresql://$db_username:$db_password@localhost:5432

  psql $uri -c 'DROP DATABASE IF EXISTS hermes';

  psql postgresql://$db_username:$db_password@localhost:5432/midas < $directory/hermes.sql
  sleep 4

  rm hermes.sql

fi
}

if [[ $install_or_update = "true" ]] ; then
setup_services
fi

