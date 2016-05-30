#!/usr/bin/env sh

mkdir -p /home/root/tasks/

screen -dmS "render-pixels-{{start_time}}" bash run_script.sh
