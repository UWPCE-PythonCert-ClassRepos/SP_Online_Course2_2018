#!/usr/bin/env python3
# Lesson 8, Redis Mailroom 

import logging
import pymongo

from operator import itemgetter


class Donor():
    logger = logging.getLogger(__name__)
    
    """
    Defines a single donor with their individual donation information
    """
    def __init__(self, name, db):
        self._name = name
        self._db = db
        self._donations = []
            
    @property
    def name(self):
        """
        Get donor name
        """
        return self._name
        
    @property
    def email(self):
        """
        Get email address
        """
        return self._db.hget(self.name, 'email')
        
    @property
    def phone(self):
        """
        Get phone number
        """
        return self._db.hget(self.name, 'phone')
        
    def donate(self, amt):
        """
        Record a new donation for this donor
        """
        self._donations.append(amt)
            
    def update_donation(self, old_amt, new_amt):
        """
        Update the given donation amount with the new amount as well as the donor aggregate values
        """
        for i, donation in enumerate(self._donations):
            if float(donation) == float(old_amt):
                self._donations[i] = new_amt
                break
        
    @property
    def donations(self):
        """
        Return list the donations for this donor
        """
        return self._donations
        
    @property
    def num_donations(self):
        """
        Return the number of donations for this donor
        """
        return len(self.donations)
        
    @property
    def total_donations(self):
        """
        Return the total donations for this donor
        """
        total = 0;
        for donation in self.donations:
            total += float(donation)
        return total   
        
    @property
    def avg_donation(self):
        """
        Return the average donation for this donor
        """
        if self.num_donations > 0:
            return self.total_donations / self.num_donations
        else:
            return 0
        
    def __lt__(self, other):
        """
        Less-than comparator for this donor's total donations to anothers
        """
        return self.total_donations < other.total_donations
        
    def __eq__(self, other):
        """
        Equality comparator for this donor's total donations to another
        """
        if other == None:
            return False
        return self.total_donations == other.total_donations
        
    
    
class DonationRecords():
    logger = logging.getLogger(__name__)

    """
    Maintains record of all donors
    """
    ltr_template = ("\n\nDear {donor_name},"
                    "\n\nThank you for your generous donation of ${amt}."
                    "\nThis brings your to-date total of donations to ${total}!"
                    "\nYour kind help is greatly appreciated."
                    "\n\nKindest regards, Monty Burns\n\n"
                    )

    def __init__(self, db):
        self._donors = []
        self._db = db
        
        for n in self._db.keys():
            donor = Donor(n, self._db)
            self._donors.append(donor)
            
    @property
    def donors(self):
        """
        Get list of donors
        """
        return self._donors
        
    def add_donor(self, donor):
        """
        Add a donor
        :param - donor - new donor
        """
        self._donors.append(donor)
        
    def get_donor(self, name):
        """
        Return a donor
        :param - name - donor name
        :return - donor with matching name, or None if not found
        """
        for donor in self._donors:
            if donor.name == name:
                return donor
        return None
        
    def record_donation(self, name, donation):
        """
        Record a new donation
        :param - name - donor to thank
        :param - donation - donation amount
        """
        donor = self.get_donor(name)
        if donor is None:
            donor = Donor(name, self._db)
            email = input("Enter email: ")
            phone = input("Enter phone #: ")
            self._db.hmset(name, {'email':email, 'phone':phone})
            self.add_donor(donor)
        donor.donate(donation)
        return donor
        
    def clear_donations(self):
        """
        Clear all donor records
        """
        self._db.flushall()
        self._donors.clear()
        
    def create_report(self):
        """
        Return a formatted report of all donors
        """
        # print the report header
        header_row = "\n\n{:20} | {:30} | {:15} | {:11} | {:9} | {:12}\n".format("Donor Name", "Email", "Phone", "Total Given", "Num Gifts", "Average Gift")
        report = header_row + ("-" * len(header_row)) + "\n"
        # create sorted list of row data from donors
        sorted_donors = sorted(self._donors, reverse=True)
        # add a report row for each sorted donor row
        for donor in sorted_donors:
            report += "{:23}{:33}{:18}${:>10.2f}{:>12}   ${:>12.2f}\n".format(donor.name, donor.email, donor.phone, donor.total_donations, donor.num_donations, donor.avg_donation)
        report += "\n\n"
        return report

    def send_thanx(self, donor, donation):
        """
        Return formatted thank you
        :param - donor - donor to thank
        :param - donation - donation amount to thank them for
        :return - formatted thank you letter
        """
        print("donor_name: ", donor.name, ", amt: ", donation, ", total: ", donor.total_donations)
        record = {'donor_name' : donor.name, 'amt' : "{:.2f}".format(donation), 'total' : "{:.2f}".format(donor.total_donations)}
        return self.ltr_template.format(**record)
        
    def thank_all(self):
        """
        Write thank you letters for all donors to separate files
        """
        for donor in self._donors:
            f = open(donor.name.replace(' ',  '_') + ".txt", 'w')
            f.write(self.send_thanx(donor, donor.total_donations))







        
    