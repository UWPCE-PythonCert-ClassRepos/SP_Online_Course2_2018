#!/usr/bin/env python3

# from donor_model import *
import donor_model as dm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def challenge_report(self):
#     factor = challenge_prompt()
#     try:
#         min_donation = min_donation_prompt()
#     except ValueError:
#         min_donation = 1000

#     print("Challenge Report: \n")

#     for donor in self.donors:
#         new_db.append(Donor(donor.name, donor.mult_donations(factor, donor.list_min_donations(min_donation))))
#         print("{}: {}".format(donor.name, donor.mult_donations(factor, donor.list_min_donations(min_donation))))

# def send_letters(self):
#     for donor in self.donors:
#         file_name = donor.name.lower().replace(' ', '_', 3) + '.txt'
#         with open(file_name, "w") as fh: # fh: file handle
#             fh.write("Dear {},\n\tThank you for your very kind donations: {}\n\tIt will "
#                     "be put to very good use.\n\t\tSincerely,\n\t\t\t-The Team".format(donor.name, donor.donations))

# def projections(self):
#     for donor in self.donors:
#         print("{}:'s list of current donations: {}".format(donor.name, donor.donations))
#         print("Current total donation so far is: {}".format(donor.total_donation))
#         print("{}'s total donation projection if double the donations that are less than $100: {}".
#             format(donor.name, donor.total_donation + sum(donor.donations_to_double(100))))
#         print("If double the donations that are less than $50: {}\n".
#             format(donor.total_donation + sum(donor.donations_to_double(50))))

def group_donations():
        report = []  # initialize report
        for donor in self.donors:
            report.append([donor.name, sum(donor.donations), len(donor.donations)])

        # Sort the report based on donations
        return sorted(report, key=lambda r: r[1], reverse=True)


def create_report():
    database = dm.SqliteDatabase('donors.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (dm.Donor
                .select(dm.Donor, dm.Donation)
                .join(dm.Donation, dm.JOIN.INNER)
                )

        donor_names = []
        donor_record_list = []
        report = []

        for donor in dm.Donor.select():
            donor_names.append(donor.donor_name)
        # print(donor_names)

        
        for name in donor_names:
            gift_values = []
            for each_query in query:
                if each_query.donor_name == name:
                    gift_values.append(each_query.donation.gift_value)
            
            report.append([name, sum(gift_values), len(gift_values)])

            sorted_report = sorted(report, key=lambda r: r[1], reverse=True)
            # print('{}, Donations: {}'.format(name, gift_values))
        # print(sorted_report)

        # Create the report
        print("\nDonor Name           |  Total Given | Num Gifts | Average Gift")
        print("---------------------------------------------------------------\n")

        for donor_report in sorted_report:
            print("{:23}${:12.2f}{:10}   ${:12.2f}".format(donor_report[0],
                donor_report[1],
                donor_report[2],
                donor_report[1] / donor_report[2]))
        print("\n")

    except Exception as e:
        logger.info(e)
    finally:
        database.close()

def send_thank_you():
    input_donor_name = None
    while not input_donor_name:
        input_donor_name = donor_name_prompt()
        if input_donor_name.lower() == "list":
            print(list_all_donor_names_sorted())
            input_donor_name = None

    donation = None
    while not donation:
        try:
            donation = donation_prompt()
        except ValueError:
            print("Not a valid number! Please enter a valid number:\n")

    # If the donnor doesn't exist in the donor list - add his info
    # if input_donor_name not in get_all_donor_names():
    try:
        # first, last = donor_name.split(" ")
        add_donor(input_donor_name, donation)
    except ValueError:
        print("Please enter both of your \"First Name\" and \"Last Name\"")
    # else:
    #     for donor in self.donors:
    #         if donor.name == input_donor_name:
    #             donor.add_donation(donation)

    print("Thank You Email:  Thanks for the donation!\n\n")


def list_all_donor_names_sorted():
        return "\n".join(sorted(get_all_donor_names()))

def get_all_donor_names():
    database = dm.SqliteDatabase('donors.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        return [donor.donor_name for donor in dm.Donor.select()]

    except Exception as e:
        logger.info(e)
    finally:
        database.close()


def add_donor(name, amount):
    # if donor not in self.donors:
    database = dm.SqliteDatabase('donors.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        if name not in get_all_donor_names():
            with database.transaction():
                new_donor = dm.Donor.create(
                    donor_name = name,
                    donor_id = 10
                    )
                logger.info("{} hasn't donated any before. Adding into Donor table.".format(name))
        with database.transaction():
            new_gift = dm.Donation.create(
                gift_value = amount,
                gift_donor = name    
                )
            new_gift.save()
            logger.info('Donation ${} added for {}'.format(amount, name))

    # except Exception as e:
    #     logger.info(e)
    finally:
        database.close()

    # self.donors.append(donor)
def delete_donation():
    delete_name = input("Whose name do you want to delete from the donation database? \n")

    database = dm.SqliteDatabase('donors.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        donor_name_list = [donor.donor_name for donor in dm.Donor.select()]

        if delete_name in donor_name_list:
            # Delete this name from Donor table
            delete_this_donor = dm.Donor.get(dm.Donor.donor_name == delete_name)
            delete_this_donor.delete_instance()

            # Delete this name from Donation table
            delete_this_donor = dm.Donation.get(dm.Donation.gift_donor == delete_name)
            delete_this_donor.delete_instance()
            print("{} has been removed from the datbase.".format(delete_name))

        else:
            print("Can't find the name you want to delete.")


    except Exception as e:
        logger.info(e)
    finally:
        database.close()

def quit_program():
    print("Thanks for using my script! Bye!")


# d1 = Donor("Bill Gates", [234.22, 45.24, 453.09, 923.01])
# d2 = Donor("Jeff Bezo", [464.23])
# d3 = Donor("Mike Dell", [299.09, 73.67])
# d4 = Donor("Harry", "Potter", [834.09, 48.04, 34.23])
# d5 = Donor("Ben", "Williams", [83.00, 1334.34])
# d6 = Donor("Guy", "James", [93.00, 34.34])

# db = DonorBook([d1, d2, d3, d4, d5, d6])
# db = DonorBook([])
# new_db =[] # New donor list for storing in Challenge Report



QUIT_OPT = '4'

selection_map = {
    "1": send_thank_you,
    "2": create_report,
    # "3": db.send_letters,
    "3": delete_donation,
    "4": quit_program
    # "5": db.challenge_report,
    # "6": db.projections
}

menu = {
    'op1': "Send a Thank You",
    'op2': "Create a Report",
    # 'op3': "Send Letters To Everyone",
    'op3': "Delete a donation",
    'op4': "Quit"
    # 'op5': "Challenge",
    # 'op6': "Run Projections"
}


def prompt():
    return input("\nPlease choose the following options:\n1) {op1}.\n2) {op2}.\n3)"
        " {op3}.\n4) {op4}.\n".format(**menu))
        # " {op3}.\n4) {op4}.\n5) {op5}.\n6) {op6}.\n".format(**menu))


def donation_prompt():
    return float(input("Please enter the donation amount:\n"))


def donor_name_prompt():
    return input("Send a Thank You - Please enter a full name or type \"list\""
        "to list the current donors:\n")

def challenge_prompt():
    return int(input("What's your challenge factor?\n"))

def min_donation_prompt():
    return int(input("What's minimum donation you want to set? (Default is $1000)\n"))


def main():
    option_value = 0
    while option_value != QUIT_OPT:
        try:
            option_value = prompt()
            selection_map[option_value]()
        except KeyError:
            print("%s is not a valid option! Please try again.\n" % option_value)


# start the script
if __name__ == "__main__":
    main()
