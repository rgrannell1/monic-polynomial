#!/usr/bin/env python3

import os
import sys
import json
import time
from prompter import prompt




with open('security/ip_address','r') as fconn:
    ip_address = fconn.read( ).strip( )

inventory = {
	'target_vm': {
		'hosts': ['target_vm'],
		'vars': {
			'start_time':   int(time.time( )),
			'ansible_host': ip_address,
			'args': {
				'draw': [
					{
						'width':  2000,
						'height': 2000,
						'xrange': 10,
						'yrange': 10
					}
				],
				'solve': [
					{
						'range': 5,
						'order': 5
					}
				]
			}
		}
	}
}






print(json.dumps(inventory))
