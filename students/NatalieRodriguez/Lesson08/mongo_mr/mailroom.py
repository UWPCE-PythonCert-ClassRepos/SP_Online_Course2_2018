from mongodb_script import *
import donor_db

choices = {1: send_thankyou,
           2: create_report,
           3: send_letters,
           4: delete_donor,
           5: close_program
           }


def user_input():
    try:
        action = int(input("\nChoose an action: \n" +
                           "1. Send a Thank You \n" +
                           "2. Create a Report \n" +
                           "3. Send Thank Yous to All Donors \n" +
                           "4. Delete a Donor \n" +
                           "5. Quit\n"
                           ))
    except ValueError:
        print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Thank Yous to All Donors', " +
              "4 to 'Delete a Donor', or 5 to 'Quit'\n")
    else:
        if action not in choices:
            print("\nEnter 1 to 'Send a Thank You', 2 to 'Create a Report',3 to 'Send Thank Yous to All Donors', " +
                  "4 to 'Delete a Donor', or 5 to 'Quit'\n")
    return action


def main():
    log = utilities.configure_logger('default', '../logs/nosql_dev.log')

    log.info("Retrieving donor data.")
    d = donor_db.get_donor_data()

    donor = run_example(d)

    action = 0

    while action != 5:
        try:
            action = user_input()
            choices[action](donor)
        except KeyError:
            print("Please choose a valid entry.")


if __name__ == "__main__":
    main()