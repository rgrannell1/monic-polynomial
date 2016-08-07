#!/usr/bin/env python3

import os
import sys
import json
import time





ansible_folder = os.path.dirname(os.path.realpath(__file__))
connect_path   = os.path.realpath(os.path.join(ansible_folder, '../security/ip_address'))
ssh_key        = '~/.ssh/id_rsa.nuc'





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
			'start_time':                   int(time.time( )),
			'ansible_host':                 ip_address,
			'ansible_user':                 ansible_user,
			'ansible_ssh_private_key_file': ssh_key,
			'argument_script':              'arguments.py'
		}
	}
}





print(json.dumps(inventory))
