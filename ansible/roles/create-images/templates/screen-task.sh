#!/usr/bin/env sh

python3 "$HOME/tasks/current/repo/src/python/cli.py" --task-path="$HOME/tasks/current"

sudo apt-get install \
	make             \
	ansible --assume-yes
