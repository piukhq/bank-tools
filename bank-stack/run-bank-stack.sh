#!/bin/bash

################################################################################
# runs the Hermes & Angelia services needed to get API 1 & 2 up & running
# TODO: Pelops
# Requires:
#     hermes, angelia & metis code, postgres database etc etc 
#     tmux
################################################################################


directory="~/dev"

TMUX_SESSION_NAME='bank_stack'

tmux -2 new-session -d -s $TMUX_SESSION_NAME
tmux new-window -t $TMUX_SESSION_NAME -n 'bank'

for p in {0..7}; do
  tmux split-pane -v
  tmux select-layout tiled
done

# tmux gui formatting
tmux set -g mouse on
tmux set -g pane-border-status top
tmux set -g pane-border-format "[#[fg=white]#{?pane_active,#[bold],} #P - #T #[fg=default,nobold]]"

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
tmux send-keys -t 2 "cd $directory/hermes && pipenv run celery -A hermes worker --loglevel=INFO --concurrency=1 --queues=ubiquity-async-midas,record-history -E" C-m
##
tmux select-pane -t 3 -T Celery-beat
tmux send-keys -t 3 "echo '** Launching Hermes celery-beat **'" C-m
tmux send-keys -t 3 "cd $directory/hermes && pipenv run celery -A hermes beat --loglevel=INFO" C-m

##
tmux select-pane -t 4 -T Angelia
tmux send-keys -t 4 "echo '** Launching Angelia **'" C-m
tmux send-keys -t 4 "cd $directory/angelia && pipenv run python commands.py run-api-server" C-m

##
tmux select-pane -t 5 -T Metis-runserver
tmux send-keys -t 5 "echo '** Launching Metis Runserver **'" C-m
tmux send-keys -t 5 "cd $directory/metis && pipenv run flask run -p 8095" C-m

##
tmux select-pane -t 6 -T Metis-celery
tmux send-keys -t 6 "echo '** Launching Metis celery **'" C-m
tmux send-keys -t 6 "cd $directory/metis && pipenv run celery -A app.tasks worker --loglevel=INFO --concurrency=1 " C-m

tmux attach-session -t 'bank'
