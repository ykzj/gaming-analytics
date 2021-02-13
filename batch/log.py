#!/usr/bin/env python3

# Copyright 2020 ykzj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# log_format combined '$remote_addr - $remote_user [$time_local] '
#                     '"$request" $status $body_bytes_sent '
#                     '"$http_referer" "$http_user_agent"';
#
#sample log
# 192.168.33.1 - - [15/Oct/2019:19:41:46 +0000] "GET / HTTP/1.1" 200 396 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import pytz
import argparse
import time
from datetime import datetime
import random
from faker import Faker

log_fmt = '{remote_addr} - - [{time_local}] "{request}" {status} {body_bytes_sent} "{http_referer}" "{http_user_agent}"'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate synthetic gameserver logs')
	parser.add_argument('--logdir', help='where to store logs, example: /data', required=True)
	parser.add_argument('--size', help='max size per log, example: 10485760, 10MB per file', required=False, default=10485760)
	parser.add_argument('--backups', help='how many backup logs you want to keep', required=False, default=5)
	parser.add_argument('--interval', help='interval (in seconds) between events', required=False, default=1)

	args = parser.parse_args()

	logger = logging.getLogger('Gameserver Log')
	logger.setLevel(logging.INFO)
	logfile_path = os.path.join(args.logdir, 'gameserver.{}.{}.log'.format(os.environ['MY_NODE_NAME'], os.environ['MY_POD_NAME']))
	#print(logfile_path)
	handler = RotatingFileHandler(logfile_path, maxBytes = int(args.size), backupCount = int(args.backups))
	logger.addHandler(handler)

	fake = Faker()

	#run until endtime
	while True:
		log_entry = log_fmt.format(
			remote_addr = fake.ipv4(),
			time_local = datetime.now(tz=pytz.utc).strftime('%d/%b/%Y:%H:%M:%S %z'),
			request = 'GET {} HTTP/1.1'.format(fake.url()),
			status = random.choice([200, 301, 302, 401, 403, 404, 500]),
			body_bytes_sent = random.randint(1, 1000000),
			http_referer = '-',
			http_user_agent = fake.user_agent()
		)
		logger.info(log_entry)
		#print(log_entry)
		time.sleep(float(args.interval))