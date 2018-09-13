"""
Main control of mailroom.py
"""

import mongo_mailroom


def main():
    db = mongo_mailroom.Mailroom()
    # db.populate_db()
    # db.list_donors()  
    # db.add_donation()

    # db.update_donor()
    # db.delete_donor()
    # db.create_report()
    db.send_letters()
    # print(db.list_donors())
    print(db.all_donors_and_donations)
    



    
if __name__ == "__main__":
    main()