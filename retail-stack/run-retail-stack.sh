#!/bin/bash

# This script will install, set environments, git pull and run Midas API, Midas consumer, Europa, API Reflector and Callbacca.

# For full instructions, please see 'Installing and running the retail stack with run-retail-stack.sh' on Confluence.

# Requirements:
# - tmux
# - poetry
# - git (authenticated in cli via either HTTPS or SSH (see below parameters))

#Options:
#-d <directory> : directory in which to install/run retail services
#-u <username> : database username to be stored in .env
#-p <password> : database password to be stored in .env
#-i true : installs and updates services from staging (including git branch, .envs, databases (if -r true)). Otherwise just runs services
#-r true : reads and copies in latest databases from staging (if omitted, but -i true, will install/update without affecting database)
#-s true : uses SSH to clone git repositories (if omitted defaults to HTTPS)

# You can update europa configurations at localhost:8050/config-service/admin
# If you do not have an existing user account in staging, you will need to create a superuser for access to europa.
# From europa root directory > pipenv run python manage.py createsuperuser

while getopts ":d:u:p:r:i:s:" opt; do
  case $opt in
  d)
    directory="$OPTARG"
    ;;
  u)
    username="$OPTARG"
    ;;
  p)
    db_password="$OPTARG"
    ;;
  r)
    db_update="$OPTARG"
    ;;
  i)
    install_or_update="$OPTARG"
    ;;
  s)
    ssh="$OPTARG"
    ;;
  \?)
    echo "Invalid option -$OPTARG" >&6
    exit 1
    ;;
  esac
done

if [[ ! $directory ]]; then
  directory="${PWD}"
fi

if [[ ! $username ]]; then
  db_username="postgres"
fi

if [[ ! $db_password ]]; then
  db_password=""
fi

if [[ $ssh = "true" ]]; then
  github_prefix="git@github.com:"
else
  github_prefix="https://github.com/"
fi

setup_services() {

  MIDAS_ENV_FILE=$(
    cat <<EOF
  HERMES_URL=http://127.0.0.1:8000
  HADES_URL=http://0.0.0.0:8005/
  VAULT_TOKEN=<o0q2cx/pcbtWWNSQnLJtJhflyyw570Zkbr2kYQGasvNW>
  VAULT_URL=https://uksouth-dev-2p5g.vault.azure.net/
  TXM_API_AUTH_ENABLED=False
  CREDENTIALS_LOCAL=False
  CONFIG_SERVICE_URL=http://127.0.0.1:8050/config_service
  POSTGRES_DSN="postgresql+psycopg2://$db_username:$db_password@localhost:5432/midas"
  PUSH_PROMETHEUS_METRICS=false
  AZURE_AAD_TENANT_ID=a6e2367a-92ea-4e5a-b565-723830bcc095
EOF
  )

  EUROPA_ENV_FILE=$(
    cat <<EOF
  EUROPA_DATABASE_URI="postgresql://$db_username:$db_password@localhost:5432/europa"
EOF
  )

  API_REFLECTOR_ENV_FILE=$(
    cat <<EOF
  FLASK_APP=wsgi
  FLASK_ENV=development
  FLASK_RUN_PORT=6400
  FLASK_SKIP_DOTENV=true

  secret_key=f98034hqvp9nqpfn32p9f8hp3298fn3l3wwer343fc3fv9p80p2u95r023ikhfgm
  postgres_dsn=postgresql://$db_username:$db_password@localhost:5432/api_reflector
  log_json=false
  log_level=debug
  trace_query_descriptions=true
  OAUTHLIB_INSECURE_TRANSPORT=true
EOF
  )

  CALLBACCA_ENV_FILE=$(
    cat <<EOF
  bpl_callback_oauth2_resource=http://foo.url
  bpl_azure_oauth2_token_url=http://foo.url
  redis_url=redis://localhost:6379/0
EOF
  )

  # Set up services
  echo "- Setting up services in directory: $directory"

  echo $directory
  echo $exclude

  # MIDAS

  cd $directory

  if [[ ! -d "midas" ]]; then
    echo "- Cloning Midas..." && git clone "${github_prefix}binkhq/midas.git"
  fi

  cd midas

  echo "- (Midas) Checking out and updating master branch..."
  git checkout master
  git pull --ff-only origin master

  echo "- (Midas) Synching .env and pipenv..."
  echo "$MIDAS_ENV_FILE" >.env && pipenv sync --dev

  # EUROPA

  cd $directory

  if [[ ! -d "europa" ]]; then
    echo "- Cloning Europa..." && git clone "${github_prefix}binkhq/europa.git"
  fi

  cd europa

  echo "- (Europa) Checking out and updating master branch..."
  git checkout master
  git pull --ff-only origin master

  echo "- (Europa) Synching .env and pipenv..."
  echo "$EUROPA_ENV_FILE" >.env && pipenv sync --dev

  # API-REFLECTOR

  cd $directory

  if [[ ! -d "api-reflector" ]]; then
    echo "- Cloning api-reflector..." && git clone "${github_prefix}binkhq/api-reflector.git"
  fi

  cd api-reflector

  echo "- (API-Reflector) Checking out and updating master branch..."
  git checkout master
  git pull --ff-only origin master

  echo "- (API-Reflector) Synching .env and poetry..."
  echo "$API_REFLECTOR_ENV_FILE" >.env && poetry install --sync
  poetry plugin add poetry-dotenv-plugin

  # Callbacca

  cd $directory

  if [[ ! -d "callbacca" ]]; then
    echo "- Cloning callbacca..." && git clone "${github_prefix}binkhq/callbacca.git"
  fi

  cd callbacca

  echo "- (API-Reflector) Checking out and updating master branch..."
  git checkout master
  git pull --ff-only origin master

  echo "- (API-Reflector) Synching .env and poetry..."
  echo "$CALLBACCA_ENV_FILE" >.env && poetry install --sync
  poetry install --sync

  # Create/update databases

  cd $directory

  if [[ $db_update = "true" ]]; then

    kubectl config use-context uksouth-staging

    kubectl -n devops port-forward deploy/proxy-postgres 5432:5432 &
    sleep 3

    pg_dump $(kubectl get secret azure-postgres -o json | jq -r .data.common_midas | base64 --decode | sed 's/uksouth-.*.postgres.database.azure.com/127.0.0.1/g') >$directory/midas.sql
    sleep 4

    pg_dump $(kubectl get secret azure-postgres -o json | jq -r .data.common_api_reflector | base64 --decode | sed 's/uksouth-.*.postgres.database.azure.com/127.0.0.1/g') >$directory/api_reflector.sql
    sleep 4

    pg_dump $(kubectl get secret azure-postgres -o json | jq -r .data.common_europa | base64 --decode | sed 's/uksouth-.*.postgres.database.azure.com/127.0.0.1/g') >$directory/europa.sql
    sleep 4

    kill %1
    wait

    uri=postgresql://$db_username:$db_password@localhost:5432

    psql $uri -c 'DROP DATABASE IF EXISTS midas' -c 'DROP DATABASE IF EXISTS europa;' -c 'DROP DATABASE IF EXISTS api_reflector;' -c 'CREATE DATABASE midas;' -c 'CREATE DATABASE europa;' -c 'CREATE DATABASE api_reflector;'

    psql postgresql://$db_username:$db_password@localhost:5432/midas <$directory/midas.sql
    sleep 4

    psql postgresql://$db_username:$db_password@localhost:5432/api_reflector <$directory/api_reflector.sql
    sleep 4

    psql postgresql://$db_username:$db_password@localhost:5432/europa <$directory/europa.sql
    sleep 4

    rm midas.sql
    rm europa.sql
    rm api_reflector.sql

  fi
}

run_services() {

  TMUX_SESSION_NAME='retail'
  echo "Starting services in tmux session: $TMUX_SESSION_NAME"
  tmux -2 new-session -d -s $TMUX_SESSION_NAME
  tmux new-window -t $TMUX_SESSION_NAME -n 'retail_stack'

  ################################################################################
  # TMUX CONFIG
  # tmux gui formatting
  tmux set -g mouse on
  tmux set -g pane-border-status top
  tmux set -g pane-border-format "[#[fg=white]#{?pane_active,#[bold],} #P - #T #[fg=default,nobold]]"

  # tmux helpers
  # define path to tmux helpers
  main_script_dir=$(dirname "$0")
  tmux_scripts_path="../tmux-scripts"
  abs_path=$(readlink -f "$main_script_dir/$tmux_scripts_path")
  # Configure keybinds
  ## Don't exit tmux when 'tmux kill-ses ...' is run
  # tmux set -g detach-on-destroy off

  ## display menu to switch and maximize panes
  tmux bind -r C-l run-shell $abs_path/tmux-pane-menu.sh
  ################################################################################

  for p in {0..4}; do
    tmux split-pane -v
    tmux select-layout tiled
  done

  # Launch services in panes
  ## Midas
  tmux select-pane -t 0 -T Midas_API:8001
  tmux send-keys -t 0 "echo '**Launching Midas API on port 8001**'" C-m
  tmux send-keys -t 0 "cd $directory/midas && pipenv run flask run -p 8001" C-m
  tmux select-pane -t 1 -T Midas_Consumer
  tmux send-keys -t 1 "echo '**Launching Midas Consumer**'" C-m
  tmux send-keys -t 1 "cd $directory/midas && pipenv run python consumer.py" C-m

  ## Europa
  tmux select-pane -t 2 -T Europa:8050
  tmux send-keys -t 2 "echo '**Launching Europa on port 8050**'" C-m
  tmux send-keys -t 2 "cd $directory/europa && pipenv run python manage.py runserver 8050" C-m

  ## API-Reflector
  tmux select-pane -t 3 -T Api-Reflector:6400
  tmux send-keys -t 3 "echo '**Launching API-Reflector on port 6400**'" C-m
  tmux send-keys -t 3 "cd $directory/api-reflector && poetry run flask run -p 6400" C-m

  ## Callbacca
  tmux select-pane -t 4 -T Callbacca:6401
  tmux send-keys -t 4 "echo '**Launching Callbacca on port 6401**'" C-m
  tmux send-keys -t 4 "cd $directory/callbacca && poetry run uvicorn asgi:app --port 6401" C-m

  tmux attach-session -t 'retail'

}

if [[ $install_or_update = "true" ]]; then
  setup_services
fi

run_services
