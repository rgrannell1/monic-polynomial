#!/usr/bin/env sh

mkdir -p ~/polynomial-builds/

screen -dmS "draw-solutions-{{start_time}}" bash run_script.sh
