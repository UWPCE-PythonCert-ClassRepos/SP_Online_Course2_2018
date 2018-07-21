# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 18:07:42 2018

@author: HP-Home
"""

import configparser
config = configparser.ConfigParser()
config['mongodb_cloud'] = {'user': 'kmsnyde',
                      'pw': 'beattle55!',
                      'connection': ''}
config['redis_cloud'] = {}
config['redis_cloud']['host'] = 'redis-13391.c8.us-east-1-4.ec2.cloud.redislabs.com'
config['redis_cloud']['pw'] = 'beattle55'
config['redis_cloud']['connection'] = ''
config['redis_cloud']['user'] = 'kmsnyder2@verizon.net'
config['redis_cloud']['port'] = '13391'
config['neo4j_cloud'] = {}
config['neo4j_cloud']['user'] = 'kmsnyde'
config['neo4j_cloud']['pw'] = 'b.l19fGz9thYZ0.ZrtiPthuOZX5DPAU'
config['neo4j_cloud']['connection'] = ''

with open('z:/uofw/repo/SP_Online_Course2_2018/students/kmsnyde/lesson08/nosql_repo/.config/config1.ini', 'w') as configfile:
   config.write(configfile)