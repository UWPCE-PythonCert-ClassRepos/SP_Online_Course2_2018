#!/usr/bin/env python3

"""
Module that contains all of the backend functionality for Mailroom.
"""


def send_thank_you(donor_db, first_name, last_name, amount):
    """
    Send a thank you to a donor for a new donation.
    :param donor_db: the Donor database.
    :param first_name: Donor's first name
    :param last_name: Donor's last name
    :param amount: Total amount of donor's donations
    :return: string
    """
    donor_db.add_donation(first_name, last_name, amount)
    return f'{first_name} {last_name} donated ${amount:.2f}. Thank you!'


def create_report(donor_db):
    """
    Print a list of all donors.
    :param donor_db: the Donor database
    :return: donor report string
    """

    def get_total(donor_data):
        """
        Return the total amount of donations from a donor.
        :param donor_data: tuple of donor data from the database
        :return: list
        """
        return donor_data[1]

    def create_row(donor):
        """
        Return the information needed to create a database entry.
        :param donor: the donor's information
        :return: list
        """
        fullname = donor.get_name()
        total = sum(donor.get_donations())
        num = len(donor.get_donations())
        avg = total / num
        return [fullname, total, num, avg]

    report = list()
    headers = ['Donor Name', 'Total', 'Count', 'Avg.']
    donor_list = [create_row(donor) for donor in donor_db.get_donors()]
    donor_list.sort(key=get_total, reverse=True)
    format_str = '{:<15} {:>10} {:^10} {:>10}'
    report.append(format_str.format(*headers))

    for donor in donor_list:
        report.append(format_str.format(donor[0], donor[1], donor[2], donor[3]))
    return '\n'.join(report)


def send_letters(donor_db):
    """
    Send letters to all donors in the database.
    :param donor_db: the Donor database
    :param template: text file
    :return: list
    """
    name_and_amounts = list()
    for donor in donor_db.get_donors():
        donations = donor.get_donations()
        total = sum(donations)
        try:
            name_and_amounts.append((donor.get_name(), total))
        except KeyError as key_error:
            print("Key Error:", key_error)
            return "Failed!"
    print(name_and_amounts)
    return name_and_amounts
