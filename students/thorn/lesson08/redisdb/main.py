"""
Main control of mailroom.py
"""

import redis_mailroom


def main():
    db = redis_mailroom.Mailroom()

    while True:
        prompt =\
        """
        Please Choose:
        '1: Get a donor's info
        '2: Add a donation and/or donor
        '3: Get a donors email
        '4: Create report
        '5: Create a formatted report
        '6: Delete a donor
        'Q or q to Quit
        '>> 
        """
        choice = input(prompt)

        if choice.lower() == 'q':
            quit()
        elif choice == '1':
            db.get_donor_info()
        elif choice == '2':
            db.add_donation()
        elif choice == '3':
            db.get_donor_email()
        elif choice == '4':
            db.all_donors_all_donation()
        elif choice == '5':
            db.create_report()
        elif choice == '6':
            db.delete_donor()
        else:
            print("Please enter a valid command.")
            continue

    



    
if __name__ == "__main__":
    main()