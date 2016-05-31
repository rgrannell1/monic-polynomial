#!/usr/bin/env python3

import os
import json
import time
from sh import screen





timestamp = int(time.time())

screen(
	'-d',
	'-S ', 'ansible-job-' + str(timestamp),
	'-m', "'python3 run.py'"
)
