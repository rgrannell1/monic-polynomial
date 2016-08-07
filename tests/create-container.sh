#!/usr/bin/env sh


# create a test-container.
#lxc delete 'polynomial-test' --force || true
#lxc file push $temp_file 'polynomial-test/root/polynomial.tar'
#lxc exec polynomial-test 'mkdir -p /home/ubuntu/.ssh'
#lxc file push '../security/id_rsa.polynomial-test.pub' 'polynomial-test/home/ubuntu/.ssh/authorized_keys'
#lxc exec polynomial-test 'chmod 700 /home/ubuntu/.ssh'
#lxc exec polynomial-test 'chmod 600 /home/ubuntu/.ssh/authorized_keys'
#lxc file push $temp_file    'polynomial-test/root/polynomial.tar'
#lxc file push setup-test.sh 'polynomial-test/root/setup-test.sh'
#
#lxc exec polynomial-test 'bash /root/setup-test.sh'
# 	lxc delete 'polynomial-test'





lxc init ubuntu:16.04 'polynomial-test'

lxc config set polynomial-test user.user-data - < cloud-init-config.yaml

lxc start polynomial-test
