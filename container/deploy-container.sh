#!/usr/bin/env sh





container_name=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

lxc init ubuntu:16.04 "$container_name"
lxc config set "$container_name" user.user_data - < cloud-init-config.yaml
lxc start "$container_name"
