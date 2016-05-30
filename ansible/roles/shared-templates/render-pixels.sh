#!/usr/bin/env sh

mkdir -p ~/polynomial-builds/

screen -dmS "render-pixels-{{start_time}}" bash run_script.sh
