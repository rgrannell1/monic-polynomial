#!/usr/bin/env sh

mkdir -p /root/tasks/

screen -dmS "render-pixels-{{start_time}}" bash run_script.sh
