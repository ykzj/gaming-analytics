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

import time
import logging
import argparse
import datetime
import random
import uuid
import json
from google.cloud import pubsub_v1

#random choose a device category
device_category = random.choice(['mobile', 'tablet', 'desktop', 'console'])

#advertising id
adid = str(uuid.uuid4())

#user_id
uid = str(uuid.uuid4())

def get_event_name():
	return random.choice(['login', 'logout', 'purchase', 'level_up', 'click_ad', 'first_install'])

def get_install_medium():
	return random.choice(['Google', 'Facebook', 'Baidu', 'Tencent', 'Bytedance', 'Other'])

def get_mobile_brand(device_category):
	if(device_category == 'mobile'):
		brand = random.choice(['Samsung', 'Apple', 'Huawei', 'Xiaomi', 'Vivo', 'Oppo', 'OnePlus'])
	elif(device_category == 'tablet'):
		brand = random.choice(['Samsung', 'Apple', 'Huawei', 'Xiaomi'])
	elif(device_category == 'desktop'):
		brand = random.choice(['HP', 'Lenovo', 'DELL', 'Asus', 'Acer'])
	elif(device_category == 'console'):
		brand = random.choice(['Microsoft', 'Nintendo', 'Sony'])
	else:
		brand = 'Unknown'
	return brand

#mock events by event_name
def get_event_parms(event_name):
	if(event_name == 'login'):
		parms = [
			{
				'key': 'battery_pct',
				'value':{
					'int_value': random.randint(20,100)
				}
			},
			{
				'key': 'login_delay',
				'value': {
					'int_value': random.randint(100, 20000)
				}
			}
		]
	elif(event_name == 'logout'):
		parms = [
			{
				'key': 'battery_pct',
				'value':{
					'int_value': random.randint(20,100)
				}
			},
			{
				'key': 'logout_delay',
				'value': {
					'int_value': random.randint(100, 20000)
				}
			}
		]
	elif(event_name == 'purchase'):
		item_id = str(random.randint(1, 1000))
		quantity = random.randint(1,10)
		unit_price = round(random.random()*10,2)
		parms = [{
			'key': 'item_id',
			'value': {
				'string_value': item_id
			}
		},
		{
			'key': 'quantity',
			'value': {
				'int_value': quantity
			}
		},
		{
			'key': 'unit_price',
			'value': {
				'float_value': unit_price
			}
		},
		{
			'key': 'total_price',
			'value': {
				'float_value': round(unit_price * quantity,2)
			}
		}
		]
	elif(event_name == 'level_up'):
		p_level = random.randint(1,100)
		parms = [
			{
				'key': 'previous_level',
				'value':{
					'int_value': p_level
				}
			},
			{
				'key': 'current_level',
				'value': {
					'int_value': p_level + 1
				}
			}
		]
	elif(event_name == 'click_ad'):
		parms = [
			{
				'key': 'imp_id',
				'value':{
					'string_value': str(uuid.uuid4())
				}
			},
			{
				'key': 'ad_revenue',
				'value': {
					'float_value': round(random.random(), 3)
				}
			}
		]
	elif(event_name == 'first_install'):
		parms = [
			{
				'key': 'install_date',
				'value':{
					'string_value': time.strftime('%Y-%m-%d')
				}
			},
			{
				'key': 'install_medium',
				'value': {
					'string_value': get_install_medium()
				}
			}
		]
	else:
		parms = {}
	return parms

device = {
	'category': device_category,
	'mobile_brand_name': get_mobile_brand(device_category),
	'advertising_id': adid,
	'language': random.choice(['zh-CN', 'en-US', 'zh-TW', 'zh-HK', 'fr-FR', 'es-ES', 'ko-KR', 'ja-JP'])
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Send simulated gaming events to Cloud Pub/Sub')
	parser.add_argument('--endTime', help='Example: 2022-01-01 00:00:00', required=False)
	parser.add_argument('--project', help='your project id, to create pubsub topic', required=True)
	parser.add_argument('--topic', help='public topic to send events', required=True)
	parser.add_argument('--interval', help='interval (in seconds) between events', required=False, default=1)

	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
	args = parser.parse_args()

	#run simulator for 1 day to save resources
	if args.endTime is None:
		end_time = datetime.datetime.now() + datetime.timedelta(days=1)
	else:
		end_time = datetime.datetime.strptime(args.endTime, '%Y-%m-%d %H:%M:%S')

	# set up cloud pub/sub client
	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path(args.project, args.topic)


	#run until endtime
	while datetime.datetime.now() < end_time:
		event_name = get_event_name()
		event = {
			'event_date': datetime.datetime.now().strftime('%Y%m%d'),
			'event_timestamp': int(time.time()*1000000),
			'event_name': event_name,
			'event_parms': get_event_parms(event_name),
			'user_id': uid,
			'device': device
		}
		event_data = json.dumps(event).encode('utf-8')
		logging.info('Sending events to {}: {}'.format(topic_path, event_data))
		future = publisher.publish(topic_path, event_data)
		logging.info('Result: {}'.format(future.result()))
		time.sleep(float(args.interval))