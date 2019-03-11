"""tests connecting to mongodb"""
from pathlib import Path
import configparser
import mongoengine
from mongoengine import Document, StringField, EmailField

config = configparser.ConfigParser()
config_file = Path.cwd() / 'config' / 'config_mongodb'
config.read(config_file)
user = config["default"]["user"]
pw = config["default"]["pw"]
conn = config["default"]["connect"]

RUN_MODE = 'test'

# used to test different mongo engine connections
client = mongoengine.connect(
            db=run_mode,
            username=config.get('default','user'),
            password=config.get('default', 'pw'),
            host=config.get('default', 'connect')
        )


class Donor(Document):
    """donor giving to organization"""
    donor_name = StringField(required=True, max_length=55, unique=True)
    email = EmailField(required=False, max_length=55)


d = Donor(donor_name='Paul Jasdfasf')
d.save()

client.close()
