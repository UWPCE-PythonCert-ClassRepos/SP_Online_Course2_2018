#!/usr/bin/env python3
# Lesson 4, JSON-based Mailroom (decorators)

from json_save_dec import json_save, from_json
from saveables import String, List, Float

@json_save
class Donor:
    _name = String()
    _donations = List()
    
    """
    Defines a single donor with their individual donation information
    """
    def __init__(self, name, donations=None):
        self._name = name
        if donations is None:
            self._donations = []
        else:
            self._donations = donations
            
    @property
    def name(self):
        """
        Get donor name
        """
        return self._name
        
    def donate(self, amt):
        """
        Record a new donation for this donor
        """
        self._donations.append(amt)
        
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
        return len(self._donations)
        
    @property
    def total_donations(self):
        """
        Return the total donations for this donor
        """
        total = 0;
        for donation in self._donations:
            total += donation
        return total
    
    @property
    def avg_donation(self):
        """
        Return the average donation for this donor
        """
        return self.total_donations / self.num_donations
 
 
    def __lt__(self, other):
        """
        Less-than comparator for this donor's total donations to anothers
        """
        return self.total_donations < other.total_donations
        
    def __eq__(self, other):
        """
        Equality comparator for this donor's total donations to another
        """
        return self.total_donations == other.total_donations
        
    
@json_save    
class DonationRecords:
    _donors = List()
    
    """
    Maintains record of all donors
    """
    ltr_template = ("\n\nDear {donor_name},"
                    "\n\nThank you for your generous donation of ${amt}."
                    "\nThis brings your to-date total of donations to ${total}!"
                    "\nYour kind help is greatly appreciated."
                    "\n\nKindest regards, Monty Burns\n\n"
                    )

    def __init__(self, donors=None):
        if donors is None:
            self._donors = []
        else:
            self._donors = donors
            
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
            donor = Donor(name)
            self.add_donor(donor)
        donor.donate(donation)
        return donor
        
    def clear_donations(self):
        """
        Clear all donor records
        """
        self._donors.clear()
        
    def create_report(self):
        """
        Return a formatted report of all donors
        """
        # print the report header
        header_row = "\n\n{:25} | {:11} | {:9} | {:12}\n".format("Donor Name", "Total Given", "Num Gifts", "Average Gift")
        report = header_row + ("-" * len(header_row)) + "\n"
        # create sorted list of row data from donors
        sorted_donors = sorted(self._donors, reverse=True)
        # add a report row for each sorted donor row
        for donor in sorted_donors:
            report +=  ("{:28}${:>10.2f}{:>12}   ${:>12.2f}\n"
                        .format(donor.name, donor.total_donations, donor.num_donations, donor.avg_donation))
        report += "\n\n"
        return report

    def send_thanx(self, donor, donation):
        """
        Return formatted thank you
        :param - donor - donor to thank
        :param - donation - donation amount to thank them for
        :return - formatted thank you letter
        """
        record = {'donor_name' : donor.name, 'amt' : "{:.2f}".format(donation), 'total' : "{:.2f}".format(donor.total_donations)}
        return self.ltr_template.format(**record)
        
    def thank_all(self):
        """
        Write thank you letters for all donors to separate files
        """
        for donor in self._donors:
            f = open(donor.name.replace(' ',  '_') + ".txt", 'w')
            last_donation = donor.donations[-1:][0]
            f.write(self.send_thanx(donor, last_donation))
            
    def save(self, filename):
        """
        Saves the donors as a json file
        """
        with open(filename, 'w') as f:
            self.to_json(f)

    def load(self, filename):
        """
        Loads the donors from a json file
        """
        json_donors = ""
        with open(filename, 'r') as f:
            for l in f:
                json_donors = json_donors + l
        temp = from_json(json_donors)
        self._donors = temp._donors






        
    