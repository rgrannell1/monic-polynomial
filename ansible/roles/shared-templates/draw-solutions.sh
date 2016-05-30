#!/usr/bin/env sh

mkdir -p /home/root/tasks/

screen -dmS "draw-solutions-{{start_time}}" bash run_script.sh
