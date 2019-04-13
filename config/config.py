#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 19-3-15
# Function: 


import os
import logging
import json
import random
from yaml import load, FullLoader
from log_config import log_config


config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, encoding='utf-8') as f:
    content = f.read()

facebook_json = os.path.join(os.path.dirname(__file__), 'facebook.json')
with open(facebook_json, encoding='utf-8') as f:
    fb_json = f.read()
facebook_cfg = json.loads(fb_json)

cfg = load(content, Loader=FullLoader)
log_config.init_log_config(file_prefix='facebook_auto', console_level=logging.INFO)
logger = logging.getLogger()


def get_redis_args():
    return cfg.get('redis')


def get_broker_and_backend():
    redis_info = cfg.get('redis')
    password = redis_info.get('password')
    sentinel_args = redis_info.get('sentinel', '')
    db = redis_info.get('broker', 5)
    if sentinel_args:
        broker_url = ";".join('sentinel://:{}@{}:{}/{}'.format(password, sentinel['host'], sentinel['port'], db) for
                              sentinel in sentinel_args)
        return broker_url
    else:
        host = redis_info.get('host')
        port = redis_info.get('port')
        backend_db = redis_info.get('backend', 6)
        broker_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, db)
        backend_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, backend_db)
        return broker_url, backend_url


def get_db_args():
    return cfg.get('db')


def get_account_args():
    return cfg.get('account')


def get_fb_friend_keys(limit=0):
    fks = facebook_cfg.get('friend_search_keys')
    if limit <= 0:
        return fks
    else:
        return random.sample(fks, limit)



def get_fb_posts():
    facebook_cfg.get('posts')


def get_fb_chat_msgs():
    facebook_cfg.get('chat_msgs')
