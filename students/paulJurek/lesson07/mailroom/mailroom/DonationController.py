"""donation organization congroller

Expected to have one controller created for each non-profit organization.
This controller contains information about organization and manages creation
and management of donations"""

import copy
import datetime
import logging

from peewee import *

from . Donor import Donor
from . Donation import Donation


class DonationController():
    """organization controller for donations
    upon initiation, the Donation controller will first look if the file
    already exists in the directory.  If so, this will be loaded.
    If not, a new one will be created.  The application is initalized with
    empty donors.

    Through the controller new donors, donation and reports are created.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def find_donor(self, donor_name: str):
        """searches through donor list and returns donor
        returns none if not found.  Search is performed on donor_name.
        args:
            donor_name: donors name.
        returns:
            donor object"""
        try:
            return Donor.get(Donor.donor_name == donor_name)
        except Donor.DoesNotExist:
            return None

    def create_donor(self, donor_name: str, donor_email: str = None) -> Donor:
        """creates donor in donation controller.  Accepts donor_name and email
        then creates object.  This first checks if donor already exists and
        raises error to avoid duplication.
        args:
            donor_name: name for donor
            donor_email: contact email for donor
        returns:
            donor inctance
            """
        self.logger.info('creating new donor')
        return Donor.create(donor_name=donor_name, donor_email=donor_email)

    def create_donation(self, amount, donor, date=datetime.datetime.utcnow()):
        """creates donation in input donor
        the donation amount should be in dollar cents (eg ###.##)
        the donor name should be full name of donor.
        Optional parameter is date which should be datetime object."""
        self.logger.info(f'creating donation of amount {amount}')
        if not self.find_donor(donor_name=donor):
            self.logger.info('donor not found, creating donor')
            self.create_donor(donor_name=donor)
        self.logger.info('creating donation finally')
        return Donation.create(donation_donor=donor,
                               donation_amount=amount,
                               date=date)

    def get_total_donations(self):
        """returns total donations in controller"""
        return (Donation
                .select(fn.Sum(Donation.donation_amount)
                .alias('total_donation')))

    def display_donors(self):
        """displays a list of donors in printed format"""
        print("\n".join([donor.donor_name for donor in
                         Donor.select(Donor.donor_name)]))

    def display_donor_donations(self, donor: str):
        """displays donor donations with most recent first"""
        query = (Donation
                 .select(Donation.id,
                         Donation.donation_amount_cents,
                         Donation.donation_date)
                 .where(Donation.donation_donor == donor).dicts()
                 .order_by(-Donation.donation_date)
                 )
        for i in query:
            print(i)


    def donor_report(self):
        """handles process for main screens report selection

        If the user (you) selected “Create a Report”, print a list of your
        donors,
        sorted by total historical donation amount.
        Include Donor Name, total donated, number of donations and average
        donation amount as values in each row. You do not need to print out all
        their donations, just the summary info.
        Using string formatting, format the output rows as nicely as possible.
        The end result should be tabular (values in each column should align
        with those above and below)
        After printing this report, return to the original prompt.
        At any point, the user should be able to quit their current task and
        return to the original prompt.
        From the original prompt, the user should be able to quit the script
        cleanly.
        Your report should look something like this:
        Donor Name                | Total Given | Num Gifts | Average Gift
        ------------------------------------------------------------------
        William Gates, III         $  653784.49           2  $   326892.24
        Mark Zuckerberg            $   16396.10           3  $     5465.37
        Jeff Bezos                 $     877.33           1  $      877.33
        Paul Allen                 $     708.42           3  $      236.14
        """
        print(f"{'Donor Name':<26}|{'Total Given':^15}|"
            f"{'Num Gifts':^11}|{'Average Gift':^15}")
        print('-'*70)
        donor_stats = self.summarize_donors()
        for person, stats in donor_stats.items():
            print(f"{person:<26} ${stats['donation_total']:>13.2f}  "
                f"{stats['donation_count']:>10}  ${stats['average_donation']:>14.2f}")

    def summarize_donors(self):
        """creats summar report of donors.  Default values to 0 if no donations present.
        returns:
            dict of donors summary
                donor_name: key str of donors name
                total_donations: float of total given to date
                donation_count: int of total gifts
                average_donation: float of average amount per donation"""
        query = (Donor
                 .select(Donor.donor_name,
                 fn.sum(Donation.donation_amount_cents).alias('donation_total')
                 , fn.count(Donation.donation_amount_cents).alias('donation_count')
                 , fn.avg(Donation.donation_amount_cents).alias('average_donation')
                 )
                .join(Donation, JOIN.LEFT_OUTER)
                .group_by(Donor).dicts()
                .order_by(-fn.sum(Donation.donation_amount_cents))
                )
        results = {i['donor_name']: i for i in query}

        # normailze results to have 0s in place of None
        results_mod = {}
        for key, value in results.items():
            inner_results = {}
            for key_, value_ in value.items():
                if value_ is None:
                    value_ = 0
                inner_results[key_] = value_
            results_mod[key] = inner_results
        return results_mod


    def create_donation_thank_you(self, donor, amount):
        """prints thank you message to terminal for donation"""
        return f"""Dear {donor},

            Thank you for your very kind donation of ${amount:.2f}.

            It will be put to very good use.

                        Sincerely,
                            -The Team"""

    def send_donation_thank_you(self, message):
        """sends donation thank you to donor"""
        pass

    def send_letters_to_everyone(self):
        pass

    def update_donation(self, donation, value, field='donation_amount'):
        """update interface to update donation field in database
        args:
            donation: id for donation to update
            field: filed in donation database to update
            value: new value for update"""
        donation = Donation.get(Donation.id == donation)
        setattr(donation, field, value)
        donation.save()

    def update_donor(self, donor, value, field='email'):
        """update interface to update donor field in database.
        Defaults to email only but setup to easily expand in future.
        args:
            donor: donor name to adjust
            field: filed in donation database to update
            value: new value for update"""
        donor = Donor.get(Donor.donor_name == donor)
        setattr(donor, field, value)
        donor.save()

    def delete_donation(self, donation):
        """deletes donation from database.  Has
        not impact on donors"""
        donation = Donation.get(Donation.id == donation)
        donation.delete_instance()

    def delete_donor(self, donor):
        """deletes donor from database.  deletes all donations
        associated with donor as well"""
        donor = Donor.get(Donor.donor_name == donor)
        donor.delete_instance(recursive=True)
