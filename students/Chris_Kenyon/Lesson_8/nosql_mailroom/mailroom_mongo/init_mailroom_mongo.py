import login_database
import utilities
import os

log = utilities.configure_logger('default', '../mongo_mailroom.log')

   
def donor_data():
    """
    donor data
    """
    donations = [
        {
            'donor_name': 'Justin Thyme',
            'donations': [
                1,
                1,
                1
            ]

        },
        {
            'donor_name': 'Beau Andarrow',
            'donations': [
                207.12,
                400.32,
                12345
            ]

        },
        {
            'donor_name': 'Crystal Clearwater',
            'donations': [
                80082
            ]

        },
        {
            'donor_name': 'Harry Shins',
            'donations': [
                1,
                2,
                3
            ]

        },
        {
            'donor_name': 'Bob Zuruncle',
            'donations': [
                0.53,
                7.00
            ]

        },
        {
            'donor_name': 'Al Kaseltzer',
            'donations': [
                1010101,
                666
            ]

        },
        {
            'donor_name': 'Joe Somebody',
            'donations': [
                25
            ]

        }
    ]
    return donations


def init_mongo():
    """
    connect to mongodb and setup inital data
    """
    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called donor_chart')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['donor_chart']
    
        log.info('And in that database use a collection called mailrrom')
        log.info('If it doesnt exist mongodb creates it')
    
        mailroom = db['mailroom']
    
        log.info('Step 2: Now we add the donor information')
        donors = donor_data()
        mailroom.insert_many(donors)
        log.info('Mongo db populated')

if __name__ == '__main__':
    init_mongo()