#!/usr/bin/env sh

tar -xf /root/polynomial.tar
rm /root/polynomial.tar

sudo apt-get install \
	make             \
	ansible --assume-yes
