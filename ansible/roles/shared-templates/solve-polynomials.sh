#!/usr/bin/env sh

mkdir ~/polynomial-builds/

readable_date=$(date +"%H:%M_%m-%d-%Y")

screen -dmS "solve-polynomials-$readable_date" bash run_script.sh $readable_date
