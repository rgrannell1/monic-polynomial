#!/usr/bin/env python3

import os
import sys
import json
from prompter import prompt



if not os.environ.get('MONIC_TARGET_VM_IP'):
	sys.stderr.write('the environment variable "MONIC_TARGET_VM_IP" must be set.\n')
	exit(1)



inventory = {
	'target_vm': {
		'hosts': ['target_vm'],
		'vars': {
			'ansible_host': os.environ.get('MONIC_TARGET_VM_IP'),
			'args': {
				'draw': {
					'width':  2000,
					'height': 2000,
					'xrange': 10,
					'yrange': 10
				},
				'solve': {
					'range': 10,
					'order': 5
				}
			}
		}
	}
}






print(json.dumps(inventory))
