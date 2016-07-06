#!/usr/bin/env sh



# create a test-container.

lxc launch ubuntu:16.04 'polynomial-test'
lxc file push '../' 'polynomial-test/polynomial'

lxc exec 'polynomial-test' 'echo hi'






lxc delete 'polynomial-test'
