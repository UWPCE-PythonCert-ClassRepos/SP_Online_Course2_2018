"""tests connecting to mongodb"""
from pathlib import Path
import configparser
import pymongo
import mongoengine

config = configparser.ConfigParser()
config_file = Path.cwd() / 'config' / 'config_mongodb'
config.read(config_file)
user = config["default"]["user"]
pw = config["default"]["pw"]
conn = config["default"]["connect"]

client = mongoengine.connect(f'mongodb://{user}:{pw}'
                                 '@cluster0-shard-00-00-wphqo.mongodb.net:27017,'
                                 'cluster0-shard-00-01-wphqo.mongodb.net:27017,'
                                 'cluster0-shard-00-02-wphqo.mongodb.net:27017/test'
                                 '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
print(client)