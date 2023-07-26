#!/bin/bash

################################################################################
# runs the Hermes & Angelia services needed to get API 1 & 2 up & running
# TODO: Pelops
# Requires:
#     hermes, angelia & metis code, postgres database etc etc
#     tmux
################################################################################

RUN=${1}
RUN2=${2}

directory="~/dev"

TMUX_SESSION_NAME='wallet-stack'

tmux -2 new-session -d -s $TMUX_SESSION_NAME
tmux new-window -t $TMUX_SESSION_NAME -n 'wallet'

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

## display menu to switch sessions
tmux bind -r C-s run-shell $abs_path/tmux-session-menu.sh
################################################################################

for p in {0..7}; do
  tmux split-pane -v
  tmux select-layout tiled
done

# Launch services in panes
## Hermes
tmux select-pane -t 0 -T Hermes-runserver
tmux send-keys -t 0 "echo '** Launching Hermes Server **'" C-m
tmux send-keys -t 0 "cd $directory/hermes && pipenv run python manage.py runserver" C-m
##
tmux select-pane -t 1 -T Hermes-api-messaging
tmux send-keys -t 1 "echo '** Launching Hermes api-messaging **'" C-m
tmux send-keys -t 1 "cd $directory/hermes && pipenv run python api_messaging/run.py" C-m
##
tmux select-pane -t 2 -T Celery
tmux send-keys -t 2 "echo '** Launching Hermes celery **'" C-m
tmux send-keys -t 2 "cd $directory/hermes && pipenv run celery -A hermes worker --loglevel=INFO --concurrency=1 --queues=ubiquity-async-midas,record-history,retry-tasks -E" C-m
##
tmux select-pane -t 3 -T Celery-beat
tmux send-keys -t 3 "echo '** Launching Hermes celery-beat **'" C-m
tmux send-keys -t 3 "cd $directory/hermes && pipenv run celery -A hermes beat --loglevel=INFO" C-m

##
tmux select-pane -t 4 -T Angelia
tmux send-keys -t 4 "echo '** Launching Angelia **'" C-m
tmux send-keys -t 4 "cd $directory/angelia && pipenv run gunicorn --workers=2 --logger-class=app.report.CustomGunicornLogger --bind=0.0.0.0:6502 main:app" C-m

##
tmux select-pane -t 5 -T Metis-runserver
tmux send-keys -t 5 "echo '** Launching Metis Runserver **'" C-m
tmux send-keys -t 5 "cd $directory/metis && poetry run gunicorn --logger-class=metis.reporting.CustomGunicornLogger --bind=0.0.0.0:9000 wsgi:app" C-m

##
tmux select-pane -t 6 -T Metis-celery
tmux send-keys -t 6 "echo '** Launching Metis celery **'" C-m
tmux send-keys -t 6 "cd $directory/metis && poetry run celery -A metis.tasks worker --loglevel=INFO --concurrency=1" C-m

if [ $RUN = "with_midas" ]; then
  ##
  tmux select-pane -t 7 -T Midas_API
  tmux send-keys -t 7 "echo '** Launching Midas API **'" C-m
  tmux send-keys -t 7 "cd $directory/midas && pipenv run flask run -p 8001" C-m
fi

if [ $RUN2 = "with_reflector" ]; then
  ##
  tmux select-pane -t 8 -T API_Reflector
  tmux send-keys -t 8 "echo '** Launching API Reflector **'" C-m
  tmux send-keys -t 8 "cd $directory/api-reflector && poetry run flask run" C-m
fi

tmux attach-session -t 'wallet'
