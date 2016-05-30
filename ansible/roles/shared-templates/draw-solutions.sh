#!/usr/bin/env sh

mkdir -p /root/tasks/

screen -dmS "draw-solutions-{{start_time}}" bash run_script.sh
