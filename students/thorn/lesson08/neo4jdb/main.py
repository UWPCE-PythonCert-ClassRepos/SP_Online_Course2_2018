"""
Main control of mailroom.py
"""

import neo_mailroom


def main():
    db = neo_mailroom.Mailroom()

    while True:
        prompt =\
        """
        Please Choose:
        '1: List Donors
        '2: Add a donation and/or donor
        '3: Delete a donor by name
        '4: Create a formatted report
        '5: Send thank you letters
        '6: List all donors
        'Q or q to Quit
        '>> 
        """
        choice = input(prompt)

        if choice.lower() == 'q':
            quit()
        elif choice == '1':
            db.list_donors()
        elif choice == '2':
            db.add_donation()
        elif choice == '3':
            db.delete_donor()
        elif choice == '4':
            db.create_report()
        elif choice == '5':
            db.send_letters()
        elif choice == '6':
            db.all_donors_and_donations()
        else:
            print("Please enter a valid command.")
            continue

    



    
if __name__ == "__main__":
    main()