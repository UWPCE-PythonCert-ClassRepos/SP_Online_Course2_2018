"""
    updated donor/donation database implementation
       for Python 220 Lesson 8 assignment (non-relational databases)

    Database implementation using MongoDB
"""

import logging
import login_database
from os import mkdir
from os.path import isdir
import pymongo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Donations():
    """
        This class defines a Donation database.
        Implemented with MongoDB.
    """

    def __init__(self, title):
        self.title = title
        self.client = login_database.login_mongodb_cloud()
        self.db = self.client['dev']
        self.mycol = self.db[self.title]


    def clear_db(self):
        self.db.drop_collection(self.title)
        self.mycol = self.db[self.title]


    def close_db(self):
        self.client.close()


    def list_donors(self):
        query = self.mycol.distinct('name')
        return '\n'.join(['   '+name for name in query])


    def add_donation(self, name, amount):
        donation = {'name': name, 'amount': float(amount)}
        self.mycol.insert_one(donation)


    def summary_report(self):
        query = self.mycol.aggregate(
            [
                {"$group": {"_id": "$name",
                            "sum": {"$sum": "$amount"},
                            "count": {"$sum": 1}}
                 },
                {"$sort": {"sum": pymongo.DESCENDING}}
            ]
        )
        report = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n"
        for item in query:
            report += f"{item['_id']:20s}   ${item['sum']:12,.2f} {item['count']:3d}" \
                    + f"               ${item['sum']/item['count']:11,.2f}\n"
        return report


    def donation_log(self):
        query = self.mycol.find({})
        report = ""
        for item in query:
            report += f"{item['name']}: ${item['amount']:.2f}\n"
        return report


    def thank_you_letter(self, name):
        last_donation = self.mycol.find_one({'name': name}, sort=[('_id', pymongo.DESCENDING)])
        return f"Dear {name},\n" \
               f"Thank you very much for your generous donation of ${last_donation['amount']:,.2f}.\n" \
               f"Sincerely,\n" \
               f"PYTHON220 Class of 2019"


    def send_all_letters(self, dir_name):
        if not isdir(dir_name):
            mkdir(dir_name)
        query = self.mycol.distinct('name')
        for donor in query:
            file_name = dir_name + '/' + donor.replace(',', '').replace(' ', '_') + '.txt'
            with open(file_name, 'w') as f:
                f.write(self.thank_you_letter(donor))


    def challenge(self, factor, min_donation=0, max_donation=1e10):
        cursor = self.mycol.aggregate(
            [
                {"$match": {"amount": {"$gte": float(min_donation), "$lte": float(max_donation)}}},
                {"$group": {"_id": "$name", "sum": {"$sum": "$amount"}}},
                {"$sort": {"_id": 1}}
            ]
        )
        total = 0
        report = ""
        for d in cursor:
            report += f"   {d['_id']}: ${factor*float(d['sum']):,.2f} = " \
                    + f"{factor} * ${float(d['sum']):,.2f}\n"
            total += factor * float(d['sum'])
        report += f"\n   Total contribution required: ${total:,.2f}\n"
        return report


    def delete_donation(self, name, amount):
        found = self.mycol.delete_one({'name': name, 'amount': float(amount)})
        return found.deleted_count


    def delete_donor(self, name):
        found = self.mycol.delete_many({'name': name})
        return found.deleted_count


    def update_donation(self, name, old_amount, new_amount):
        updated = self.mycol.replace_one(
            {'name': name, 'amount': float(old_amount)},
            {'name': name, 'amount': float(new_amount)}
        )
        return updated.modified_count


    def update_donor(self, old_name, new_name):
        if self.mycol.find_one({'name': new_name}): return 0
        updated = self.mycol.update_many(
            {'name': old_name}, {'$set': {'name': new_name}}
        )
        return updated.modified_count


def create_default_db():
    donor_data = [
        {'name': 'William Gates, III', 'amount': 653772.32},
        {'name': 'William Gates, III', 'amount': 12.17},
        {'name': 'Jeff Bezos', 'amount': 877.33},
        {'name': 'Paul Allen', 'amount': 663.23},
        {'name': 'Paul Allen', 'amount': 43.87},
        {'name': 'Paul Allen', 'amount': 1.32},
        {'name': 'Mark Zuckerberg', 'amount': 1663.23},
        {'name': 'Mark Zuckerberg', 'amount': 4300.87},
        {'name': 'Mark Zuckerberg', 'amount': 10432.0},
        {'name': 'Colleen Kaku', 'amount': 50000},
        {'name': 'Colleen Kaku', 'amount': 1000000}
    ]
    with login_database.login_mongodb_cloud() as client:
        logger.info('Create database and collection')
        db = client['dev']
        db.drop_collection('donor_db')
        donor_db = db['donor_db']

        logger.info('Add data from the dictionary')
        donor_db.insert_many(donor_data)

        logger.info('Verify data')
        cursor = donor_db.find({})
        logger.info(f'Items in database: {donor_db.estimated_document_count()}')
        for document in cursor:
            logger.info(f"{document['name']}: {document['amount']}")


def print_db():
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donor_db = db['donor_db']
        logger.info('Verify data')
        cursor = donor_db.find({})
        logger.info(f'Items in database: {donor_db.estimated_document_count()}')
        for document in cursor:
            logger.info(f"{document['name']}: {document['amount']}")


if __name__ == '__main__':
    create_default_db()
    #print_db()