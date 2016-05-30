#!/usr/bin/env sh

mkdir ~/polynomial-builds/

screen -dmS "draw-solutions-{{start_time}}" bash run_script.sh
