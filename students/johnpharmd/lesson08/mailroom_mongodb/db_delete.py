"""
    Use this to delete 'furniture' db
"""

import login_database


def delete_database():
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        response = input('Enter name of mongodb to drop: ')
        db.drop_collection(response)


if __name__ == '__main__':
    delete_database()
