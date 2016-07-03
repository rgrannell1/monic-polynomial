#!/usr/bin/env python3

import os
import sys
import json
import time





connect_path = 'security/local_ip_address'

with open(connect_path,'r') as fconn:

	content = fconn.read( ).strip( )

	ansible_user = content.split('@')[0]
	ip_address   = content.split('@')[1]

inventory = {
	'all': {
		'hosts': [ip_address],
		'vars': {

		}
	},
	'target_vm': {
		'hosts': ['target_vm'],
		'vars': {
			'start_time':      int(time.time( )),

			'ansible_host':    ip_address,
			'ansible_user':    ansible_user,

			'argument_script': 'arguments.py'
		}
	}
}





print(json.dumps(inventory))
