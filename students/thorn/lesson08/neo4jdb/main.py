"""
Main control of mailroom.py
"""

import neo_mailroom


def main():
    db = neo_mailroom.Mailroom()
    db.populate_db()
    # db.list_donors()
    # db.add_donation()
    db.create_report()


    # db.list_donors()
    db.all_donors_and_donations()

    # while True:
    #     prompt =\
    #     """
    #     Please Choose:
    #     '1: RepopulateDB
    #     '2: Add a donation and/or donor
    #     '4: Delete a donor by name
    #     '5: Create a formatted report
    #     '6: Send thank you letters
    #     'Q or q to Quit
    #     '>> 
    #     """
    #     choice = input(prompt)

    #     if choice.lower() == 'q':
    #         quit()
    #     elif choice == '1':
    #         db.populate_db()
    #     elif choice == '2':
    #         db.add_donation()
    #     elif choice == '3':
    #         db.update_donor()
    #     elif choice == '4':
    #         db.delete_donor()
    #     elif choice == '5':
    #         db.create_report()
    #     elif choice == '6':
    #         db.send_letters()
    #     else:
    #         print("Please enter a valid command.")
    #         continue

    



    
if __name__ == "__main__":
    main()