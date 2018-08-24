from operations_database import *


choices = {1: send_thankyou,
           2: create_report,
           3: send_letters,
           4: close_program
           }

def user_input():
    try:
        action = int(input("\nChoose one of four actions: \n"+
                           "1. Send a Thank You \n" +
                           "2. Create a Report \n"+
                           "3. Send Letter to Everyone \n"+
                           "4. Quit\n"
                           ))
    except ValueError:
        print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Letter to Everyone', " +
               "4 to 'Quit'\n")
    else:
        if action not in choices:
            print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Letter to Everyone', " +
               "4 to 'Quit'\n")
    return action

def main():
    action = 0

    while action != 4:
        try:
            action = user_input()
            choices[action]()
        except KeyError:
            print("Please enter a number from the options given")

if __name__ == "__main__":
    main()
