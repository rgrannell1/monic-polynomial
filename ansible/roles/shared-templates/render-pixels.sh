#!/usr/bin/env sh

mkdir ~/polynomial-builds/

screen -dmS "render-pixels-{{start_time}}" bash run_script.sh
