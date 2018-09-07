from redis_script import *
import redis_script

choices = {1: send_thankyou,
           2: create_report,
           3: send_letters,
           4: lookup_email,
           5: delete_donor,
           6: close_program
           }

def user_input():
    try:
        action = int(input("\nChoose one of four actions: \n"+
                           "1. Send a Thank You \n" +
                           "2. Create a Report \n"+
                           "3. Send Letter to Everyone \n"+
                           "4. Lookup Email Address \n"+
                           "5. Delete Donor \n"+
                           "6. Quit\n"
                           ))
    except ValueError:
        print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Letter to Everyone', " +
               "4 to 'Lookup Email Address', 5 to 'Delete a Donor', or 6 to 'Quit'\n")
    else:
        if action not in choices:
            print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Letter to Everyone', " +
               "4 to 'Lookup Email Address' 5 to 'Delete a Donor', or 6 to 'Quit'\n")
    return action

def main():
    log = utilities.configure_logger('default', '../logs/mailroom_redis.log')

    redis_script.run_example()
    
    action = 0

    while action != 6:
        try:
            action = user_input()
            choices[action]()
        except KeyError:
            print("Please enter a number from the options given")

if __name__ == "__main__":
    main()
