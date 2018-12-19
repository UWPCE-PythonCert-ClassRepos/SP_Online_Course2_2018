# ------------------------------------------------- #
# Title: Lesson 4, Meta Mailroom
# Dev:   Craig Morton
# Date:  11/27/2018
# Change Log: CraigM, 12/5/2018, Meta Mailroom
# ------------------------------------------------- #

import os
import sys
import json_save.json_save.json_save_meta as js


class Donor(js.JsonSaveable):
    """Modify Donor data"""
    name = js.String()
    donations = js.List()

    def __init__(self, name, donations=None):
        self.name = name
        if donations is None:
            self.donations = []
        else:
            self.donations = donations

    def append_donations(self, amt):
        try:
            self.donations.append(float(amt))
        except ValueError:
            print("Error! A donation can only be an integer or float value.")

    def sum_donations(self):
        return sum(self.donations)

    def number_donations(self):
        return len(self.donations)

    def avg_donations(self):
        return self.sum_donations() / self.number_donations()


class DonorDatabase(js.JsonSaveable):
    """Modify the data of multiple Donors"""
    donors = js.List()

    def __init__(self, donors=None):
        if donors:
            self.donors = donors
        else:
            self.donors = []

    def list_donors(self):
        """Donor list"""
        return [donor.name for donor in self.donors]

    def add_new_donor(self, donor):
        self.donors.append(donor)

    def create_report(self):
        report = ""
        for donor in self.donors:
            k = donor.name
            num_gifts = donor.number_donations()
            total_given = donor.sum_donations()
            average_gifts = donor.avg_donations()
            report = report + f"{k: <26}| ${total_given:>10.2f} |{num_gifts:^11}| ${average_gifts:>11.2f}\n"
        return report

    @classmethod
    def thank_you(cls):
        """Add donation to existing donor, create a new donor, thank you letter and donor list"""
        user_input = input("Please enter the full name of a donor, type \"list\" for a full list of donors, " +
                           "or type \"exit\" to return to the main menu.\n: ").title()
        if user_input.lower() == "list":
            print(donor_db.list_donors())
            cls.thank_you()
        elif user_input.lower() == "exit":
            mailroom(donor_db)
        else:
            try:
                donation = float(input("Please enter a donation amount: "))
            except ValueError:
                print("Error! A donation can only be an integer or float value.")
                print("Returning to Menu:\n")
                cls.thank_you()
            donor_list = donor_db.list_donors()
            for donor in donor_db.donors:
                if user_input in donor_list and donor.name != user_input:
                    continue
                elif user_input in donor_list and donor.name == user_input:
                    donor.append_donations(donation)
                    print("Donor found")
                    print("Adding {0} to {1}'s file...".format(donation, user_input))
                    print("Thank you email:\n")
                    print(cls.create_letter(0, user_input, donation,), "\n")
                    print("Returning to Menu:")
                    cls.thank_you()
                else:
                    donor_db.add_new_donor(Donor(user_input, [donation]))
                    print("New Donor. Generating record for {0}".format(user_input))
                    print("Thank you email:\n")
                    print(cls.create_letter(1, user_input, donation), "\n")
                    print("Returning to Menu:\n")
                    cls.thank_you()

    @classmethod
    def create_letter(cls, donor_status, donor_name, donation_amt):
        """Format letters"""
        if donor_status == 0:
            letter_text = """
            Dear {0},
                Thank you for your contribution of ${1:.2f}.
                Your generosity will be put to good use!
                               Kind regards,
                                  Charity Services
                                  """.format(donor_name, donation_amt)
            return letter_text
        elif donor_status == 1:
            letter_text = """
            Dear {0},
                Thank you for your donation of ${1:.2f}.
                Your generosity will be put to good use!
                               Kind regards,
                                  Charity Services
                                  """.format(donor_name, donation_amt)
            return letter_text
        elif donor_status == 2:
            return ("""
            Dear {0},
                Thank you for your donation totaling ${1:.2f}.
                Your generosity will be put to good use!
                               Kind regards,
                                  Charity Services
                                  """.format(donor_name, donation_amt))

    @classmethod
    def report_printing(cls):
        """Generate report"""
        while True:
            print("Donor Name" + " " * 16 + "| Total Given | Num Gifts | Average Gift")
            print("-" * 66)
            print(donor_db.create_report())
            print("Returning to Menu:\n")
            return

    @classmethod
    def thank_all(cls):
        """Generate Donor thank you letters"""
        current_dir = os.getcwd()
        print("Saving letters to {0}...".format(current_dir))
        cls.create_txt_files()
        print("=========================")
        print("Letters generated to all donors.  Returning to Menu")
        mailroom(donor_db)

    @classmethod
    def create_txt_files(cls):
        """Write thank you letters to local directory"""
        for donor in donor_db.donors:
            name = donor.name
            donation = sum(donor.donations)
            letter = cls.create_letter(2, name, donation)
            with open("{:s}.txt".format(donor.name), "w") as f:
                f.write(letter)

    @classmethod
    def save_to_json(cls, filename):
        donor_to_json = donor_db.to_json()
        with open(filename, "w") as dbf:
            dbf.write(donor_to_json)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, "r") as dbf:
            data = dbf.read()
        return js.from_json(data)

    @classmethod
    def quit_program(cls):
        """Escape program"""
        user_input = input("Write changes to database? (Y/N)\n> ")
        if user_input.lower() == ('y' or 'yes'):
            cls.save_to_json('donor_database.json')
        print("Signing off")
        sys.exit()


def mailroom(ddb):
    """Main Menu"""
    while True:
        selection = input("Your Meta Mailroom: \n====================" +
                          "\nSelect an option:\n1> Send thank you letter" +
                          "\n2> Generate report\n3> Send letters to everyone\n4> Exit program\n> ")
        menu_dict = {"1": ddb.thank_you, "2": ddb.report_printing, "3": ddb.thank_all, "4": ddb.quit_program}
        try:
            menu_dict.get(selection)()
        except TypeError:
            print("Error!  Enter options 1-4.")
            pass


if __name__ == "__main__":
    donor_db = DonorDatabase.load_from_json("donor_database.json")
    mailroom(donor_db)
