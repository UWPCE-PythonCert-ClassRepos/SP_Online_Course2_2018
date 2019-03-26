#!/usr/bin/env python
# This script maintains a databse of donors including name and donation amounts
import statistics
import datetime
from mailroom_model import *
from peewee import *

# Define exception to exit script
class ExitScript(Exception): pass




    @property
    def filename(self):
        """Return filename for a thankyou letter to a donor."""
        d = datetime.date.today()
        # Build file name using donor name and today's date separated by _
        filename = '_'.join([self.name.replace(' ','_'), str(d.month),
            str(d.day), str(d.year)])+'.txt'
        return filename




    def names_by_donations(self):
        """Return a list of donor objects sorted by total donation amount."""
        return sorted(self, key=self.sort_key, reverse=True)

    @staticmethod
    def sort_key(x):
        return x.total_donations

    @property
    def donors(self):
        return self._donors

    @property
    def names(self):
        """Return a list of Donors in DonorDict object sorted by name."""
        return sorted([donor.name for donor in self])



    def thank_all_donors(self):
        """Send letters to all donors thanking them for most recent donation."""
        for donor in self:
            with open(donor.filename, 'w') as f:
                f.write(donor.thank(donor.donations[-1]))
            f.closed


# Define main menu functions
def add_donation():
    """Add a donation to donors dict and compose a thank you email."""

    with database.transaction():
        while True:
            name = input("Enter the donor's Full Name, or 'list': ").lower()
            if name == 'return':
                return
            elif name == 'list':
                for donor in (Donor.select()):
                    print(donor.name)
            else:
                try:
                    new_donor = Donor.create(name=name)
                    new_donor.save()
                except Exception as e:
                    raise e
                break

        while True:
            amount = input('Enter the donation amount: ')
            if amount.lower() == 'return':
                return
            try:
                new_donation = Donation.create(
                    amount=amount,
                    donor=name
                    )
                new_donation.save()
                break
            except ValueError:
                print('Please enter a number value for donation amount.')

        print(); print(thank(name, amount))


def create_report():
    """Print a report of donors with a summary of their donation history."""
    donors = (Donor.select().order_by(Donor.donation_total))

    # Determine table size_report
    table_size = size_report(donors)

    # Build format strings for header and table rows
    head_string = '{:{}s} | {:^{}s} | {:^{}s} | {:^{}s}'
    row_string = '{:{}s} | $ {:>{}.2f} | {:>{}d} | $ {:>{}.2f}'

    # Table header - Add 2 to width of dollar value fields to account for
    # dollar sign and space
    report_str = head_string.format('Donor Name', table_size[0],
                                    'Total Given', table_size[1] + 2, 'Num Gifts', table_size[2],
                                    'Average Gift', table_size[3] + 2) + '\n'
    # report_str = report_str +  ('-'*(sum(table_size) + 13)) + '\n')

    # Table rows
    report_list = []
    for donor in donors:
        report_list.append(row_string.format(donor.name, table_size[0],
                                             donor.donation_total, table_size[1], donor.donation_count,
                                             table_size[2], donor.donation_average, table_size[3]))
    print(report_str + '\n'.join(report_list))



def send_letters():
    """Send letters to all donors thanking them for most recent donation."""
    donors.thank_all_donors()


def delete_donor():
    """
    Delete a donor from the database.
    """
    pass


def quit():
    database.close()
    raise ExitScript


# Define helper functions
def thank(name, amount):
    """Return a string thanking donor name for a donation of amount."""
    donor = Donor.get(Donor.name == name)
    return f"Dear {name},\n\n" + \
        "Thank you so much for your generous donation of " + \
        f"${amount:.2f}.\n\nWe really appreciate your donations " + \
        f"totalling ${donor.total_donations:.2f}.\n" + \
        f"You are ${1000000000-donor.total_donations:.2f} away from a" + \
        " gift of Spaceballs: The Flamethrower!\n\n" + \
        "Sincerely, The Wookie Foundation"


def size_report(donors):
    """Determine column widths for a donor report."""
    # Determine width of columns based on data in donors data structure
    # Convert numbers to strings to determine their length in characters
    # Convert the dollar amounts to an integer to remove decimal places (since
        # there are an unknown number of them), then add 3 to the length to
        # accomodate for a period and 2 decimal places
    # Ensure column size is at least as wide as header text

    name_width = max(len(donor.name) for donor in donors)
    name_width = max(name_width, len('Donor Name'))

    total_width = max(len(str(int(donor.donation_total))) for donor in
        donors)+3
    total_width = max(total_width, len('Total Given'))

    num_width = max(len(str(donor.donation_count)) for donor in donors)
    num_width = max(num_width, len('Num Gifts'))

    avg_width = max(len(str(int(donor.donation_average))) for donor in
        donors)+3
    avg_width = max(avg_width, len('Average Gift'))

    return [name_width, total_width, num_width, avg_width]





if __name__ == '__main__':

    database = SqliteDatabase('mailroom.db', pragmas={'foreign_keys': 1})
    database.connect()

    donors = DonorDict()
    donors.add_donor('han solo', [3468.34, 457, 34.2])
    donors.add_donor('luke skywalker', [5286286.3, 567, 23.5678])
    donors.add_donor('chewbacca', [432, 679.4553])
    donors.add_donor('princess leia', [5.3434])
    donors.add_donor('bobba fett, bounty hunter', [67])

    actions = {
    '1': add_donation,
    '2': create_report,
    '3': send_letters,
    '4': delete_donor,
    '5': quit
    }

    # User interaction
    while True:
        try:
            # Main menu - prompt user for an action
            print('''
                \nSelect an action to perform...\n
                Type "return" at any time to return to main menu.\n
                ''')
            action = input('''
                1: Add a Donation & Send Thank You
                2: Create a Report
                3: Send Letters to Everyone
                4: Delete a Donor
                5: Quit\n
                ''')
            actions.get(action)()
        except ExitScript:
            break
        except TypeError:
            if action not in actions:
                continue