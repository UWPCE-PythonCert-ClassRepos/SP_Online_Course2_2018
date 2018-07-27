import configparser
import pymongo
from pathlib import Path
config_file = Path(__file__).parent.parent / '../.config/config.ini'
config = configparser.ConfigParser()


def create_donor_data(name, gifts):
    return {'name': name, 'key': name.lower(), 'gifts': gifts}


def get_donor_data():
    donor_data = [
        create_donor_data('Sleve McDichael', [86457.89,2346.43,9099.09]),
        create_donor_data('Willie Dustice', [505.05,43.21]),
        create_donor_data('Rey McScriff', [666.0]),
        create_donor_data('Mike Truk', [70935.3,12546.7,312.0]),
        create_donor_data('Bobson Dugnutt', [1234.56,789.0]),
        create_donor_data('Todd Bonzalez', [10352.07,2394.32]),
        create_donor_data('andrew', [9473.65],)
    ]
    return donor_data


def connect():
    user = None
    pw = None
    uri = None
    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]
        uri = config["mongodb_cloud"]["connection"]

    except Exception as e:
        print(f'error: {e}')

    client = None
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=10000, authMechanism='SCRAM-SHA-1', username=user, password=pw)

    return client


def populate_donors():
    with connect() as client:
        donors = client.get_database()['donors']
        donors.insert_many(get_donor_data())


def purge_donor_db():
    with connect() as client:
        db = client.get_database()
        db.drop_collection('donors')

if __name__ == '__main__':
    user_in = None
    while user_in not in ['1', '2']:
        print('input 1 to populate donor db, input 2 to drop donor collection')
        user_in = input('>')
    if user_in == '1':
        populate_donors()
    else:
        purge_donor_db()
