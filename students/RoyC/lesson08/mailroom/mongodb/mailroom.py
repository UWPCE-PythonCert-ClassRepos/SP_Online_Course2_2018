#!/usr/bin/env python3
# Lesson 8, Mongodb Mailroom 

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
        self._donor_collection = db['donors']
        self._donation_record_collection = db['donation_records']
            
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
        try:
            self._donor_collection.find_one({"name": self._name})['total_donations']

            new_donation = {
                'name': self.name,
                'amount': amt
            }
            self._donation_record_collection.insert_one(new_donation)
            donor = self._donor_collection.find_one({"name": self._name})
            donor['total_donations'] = donor['total_donations'] + amt
            donor['average_donation'] = donor['total_donations'] / self.num_donations
            self._donor_collection.find_one_and_update({"name": donor['name']}, {"$set": {"total_donations": donor['total_donations'], "average_donation": donor['average_donation']}})
        except Exception as e:
            logger.error("Exception adding donation {} for {}".format(amt, self._name), e)
            
    def update_donation(self, old_amt, new_amt):
        """
        Update the given donation amount with the new amount as well as the donor aggregate values
        """
        try:
            self._donation_record_collection.update_one({"amount": old_amt}, { "$set": { "amount": new_amt }})
            donor = self._donor_collection.find_one({"name": self._name})
            donor['total_donations'] = donor['total_donations'] - float(old_amt) + float(new_amt)
            donor['average_donation'] = donor['total_donations'] / self.num_donations
            self._donor_collection.find_one_and_update({"name": donor['name']}, {"$set": {"total_donations": donor['total_donations'], "average_donation": donor['average_donation']}})
        except Exception as e:
            logger.error("Exception updating donation {} for {}".format(old_amt, self._name), e)
        
    @property
    def donations(self):
        """
        Return list the donations for this donor
        """
        return self._donation_record_collection.find({"name": self._name})
        
    @property
    def num_donations(self):
        """
        Return the number of donations for this donor
        """
        return self._donation_record_collection.count_documents({'name': self._name})
        
    @property
    def total_donations(self):
        """
        Return the total donations for this donor
        """
        return self._donor_collection.find_one({"name": self._name})['total_donations']
    
    @property
    def avg_donation(self):
        """
        Return the average donation for this donor
        """
        return self._donor_collection.find_one({"name": self._name})['average_donation']
        
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
        self._donor_collection = db['donors']
        self._donation_record_collection = db['donation_records']
        
        for donor in self._donor_collection.find():
            self._donors.append(Donor(donor['name'], db))
            
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
            try:
                new_donor = {
                    'name': name,
                    'total_donations': 0.0,
                    'average_donation': 0.0}
                self._donor_collection.insert_one(new_donor)
                self.add_donor(donor)
            except Exception as e:
                logger.error("Exception adding donor {} to database".format(name), e)
        donation = float(donation)
        donor.donate(donation)
        return donor
        
    def clear_donations(self):
        """
        Clear all donor records
        """
        self._donors.clear()
        self._donor_collection.delete_many({})
        self._donation_record_collection.delete_many({})
        
    def create_report(self):
        """
        Return a formatted report of all donors
        """
        # print the report header
        header_row = "\n\n{:25} | {:11} | {:9} | {:12}\n".format("Donor Name", "Total Given", "Num Gifts", "Average Gift")
        report = header_row + ("-" * len(header_row)) + "\n"
        # create sorted list of row data from donors
        sorted_donors = sorted(self._donor_collection.find(), key=itemgetter('total_donations'), reverse=True)
        # add a report row for each sorted donor row
        for donor in sorted_donors:
            report += "{:28}${:>10.2f}{:>12}   ${:>12.2f}\n".format(donor['name'], donor['total_donations'], self._donation_record_collection.count_documents({'name': donor['name']}), donor['average_donation'])
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







        
    