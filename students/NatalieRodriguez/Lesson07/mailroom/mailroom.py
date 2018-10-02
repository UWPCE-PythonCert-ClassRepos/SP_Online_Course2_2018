from ops_db import *


choices = {1: send_thankyou,
           2: create_report,
           3: send_letters,
           4: close_program
           }

def user_input():
    try:
        action = int(input("\nChoose an action: \n"+
                           "1. Send a Thank You, Update or Remove a Donor \n" +
                           "2. Create a Report \n"+
                           "3. Send Thanks Yous to Everyone \n"+
                           "4. Quit \n"

                           ))
    except ValueError:
        print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Thank Yous to All Donors', " +
               "4 to 'Quit'\n")
    else:
        if action not in choices:
            print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Thank Yous to All Donors', " +
               "4 to 'Quit'\n")
    return action

def main():
    action = 0

    while action != 6:
        try:
            action = user_input()
            choices[action]()
        except KeyError:
            print("Please enter a number from the available choices.")

if __name__ == "__main__":
    main()
    user_input()
