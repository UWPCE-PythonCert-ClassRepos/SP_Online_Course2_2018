"""
    clears database for testing
"""

import login_mongodb

def clear_database():
    """
        mongo data removal
    """
    
    with login_mongodb.login_mongodb_cloud() as client:
        db = client['dev']
        db.drop_collection('donor_data')
        
if __name__ == '__main__':
    clear_database()