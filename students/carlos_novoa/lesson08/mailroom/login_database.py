"""
Module to connect to databases
"""

import configparser
from pathlib import Path
import utilities
import pymongo
import redis
from neo4j.v1 import GraphDatabase, basic_auth

log = utilities.configure_logger('default', './logs/login_databases_dev.log')
config_file = Path().resolve().parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_mongodb_cloud():
    """
    connect to mongodb and login
    """

    try:
        config.read(config_file)
        connection = config["mongodb_cloud"]["connection"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(connection)
    return client


def login_redis_cloud():
    """
    connect to redis and login
    """
    try:
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    try:
        r = redis.StrictRedis(host=host, port=port, password=pw, decode_responses=True)

    except Exception as e:
        print(f'error: {e}')

    return r


def login_neo4j_cloud():
    """
    connect to neo4j and login
    """
    config.read(config_file)
    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-hjelmnlpgbimgbkefcpmfbbl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver
