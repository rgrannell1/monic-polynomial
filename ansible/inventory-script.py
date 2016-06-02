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
			'start_time':      int(time.time( )),
			'ansible_host':    ip_address,
			'argument_script': 'arguments.py'
		}
	}
}





print(json.dumps(inventory))
