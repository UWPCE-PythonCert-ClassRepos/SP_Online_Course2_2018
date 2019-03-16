#!/usr/bin/env python3
# Lesson 8, Neo4J Mailroom 

import logging

from neo4j.v1 import GraphDatabase, basic_auth
from operator import itemgetter


class Donor():
    logger = logging.getLogger(__name__)
    
    """
    Defines a single donor with their individual donation information
    """
    def __init__(self, name, driver):
        self._name = name
        self._driver = driver
            
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
        with self._driver.session() as session:
            cyph = "CREATE (n:Donation {amount:%f}) RETURN id(n)" % (float(amt))
            result = session.run(cyph)
            donation_id = result.single()[0]
            cyph = "MATCH (n:Donor {name:'%s'}) RETURN id(n)" % (self._name)
            result = session.run(cyph)
            donor_id = result.single()[0]
            cyph = "MATCH (d:Donation),(d1:Donor) WHERE ID(d) = %s and ID(d1) = %s CREATE (d)-[donated:DONATED]->(d1) RETURN d, d1" % (donation_id, donor_id)
            session.run(cyph)
            cyph = "MATCH (n:Donor {name:'%s'}) RETURN n" % (self._name)
            result = session.run(cyph)
            donor = result.single()[0]
            total_donations = float(donor['total_donations']) + float(amt)
            average_donation = total_donations / self.num_donations
            cyph = "MATCH (d:Donor) WHERE ID(d) = %s SET d.average_donation = %f, d.total_donations = %f RETURN d" % (donor_id, float(average_donation), float(total_donations))
            session.run(cyph)
            
    def update_donation(self, old_amt, new_amt):
        """
        Update the given donation amount with the new amount as well as the donor aggregate values
        """
        with self._driver.session() as session:
            cyph = "MATCH (d:Donation {amount: %f}) SET d += {amount: %f}" % (float(old_amt), float(new_amt))
            session.run(cyph)
            cyph = "MATCH (n:Donor {name:'%s'}) RETURN id(n)" % (self._name)
            result = session.run(cyph)
            donor_id = result.single()[0]
            cyph = "MATCH (n:Donor {name:'%s'}) RETURN n" % (self._name)
            result = session.run(cyph)
            donor = result.single()[0]
            total_donations = float(donor['total_donations']) - float(old_amt) + float(new_amt)
            average_donation = total_donations / self.num_donations
            cyph = "MATCH (d:Donor) WHERE ID(d) = %s SET d.average_donation = %f, d.total_donations = %f RETURN d" % (donor_id, float(average_donation), float(total_donations))
            session.run(cyph)
        
    @property
    def donations(self):
        """
        Return list the donations for this donor
        """
        with self._driver.session() as session:
            cyph = "MATCH p=(d1)-[r:DONATED]->(d:Donor {name:'%s'}) RETURN d1" % (self._name)
            result = session.run(cyph)
            rtn_list = []
            for rec in result:
                for donation in rec.values():
                    rtn_list.append(donation['amount'])
            return rtn_list
        
    @property
    def num_donations(self):
        """
        Return the number of donations for this donor
        """
        with self._driver.session() as session:
            cyph = "MATCH (d:Donor {name:'%s'})-[r]-() RETURN COUNT(r)" % (self._name)
            result = session.run(cyph)
            count = result.single()[0]
            return count
        
    @property
    def total_donations(self):
        """
        Return the total donations for this donor
        """
        with self._driver.session() as session:
            cyph = "MATCH (d:Donor {name:'%s'}) RETURN d" % (self._name)
            result = session.run(cyph)
            donor = result.single()[0]
            return float(donor['total_donations'])
    
    @property
    def avg_donation(self):
        """
        Return the average donation for this donor
        """
        with self._driver.session() as session:
            cyph = "MATCH (d:Donor {name:'%s'}) RETURN d" % (self._name)
            result = session.run(cyph)
            donor = result.single()[0]
            return donor['average_donation']
        
    def __lt__(self, other):
        """
        Less-than comparator for this donor's total donations to anothers
        """
        return float(self.total_donations) < float(other.total_donations)
        
    def __eq__(self, other):
        """
        Equality comparator for this donor's total donations to another
        """
        if other == None:
            return False
        return float(self.total_donations) == float(other.total_donations)
        
    
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

    def __init__(self, driver):
        self._donors = []
        self._driver = driver
        
        with self._driver.session() as session:
            cyph = "MATCH (n:Donor) RETURN n"
            result = session.run(cyph)
            for rec in result:
                for donor in rec.values():
                    self._donors.append(Donor(donor['name'], driver))
            
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
            donor = Donor(name, self._driver)
            with self._driver.session() as session:
                cyph = "CREATE (n:Donor {name:'%s', total_donations: '%f', average_donation: '%f'})" % (name, 0.0, 0.0)
                session.run(cyph)
            self.add_donor(donor)
        donation = float(donation)
        donor.donate(donation)
        return donor
        
    def clear_donations(self):
        """
        Clear all donor records
        """
        self._donors.clear()
        with self._driver.session() as session:
            cyph = "MATCH (n) DETACH DELETE n"
            session.run(cyph)
        
    def create_report(self):
        """
        Return a formatted report of all donors
        """
        # print the report header
        header_row = "\n\n{:25} | {:11} | {:9} | {:12}\n".format("Donor Name", "Total Given", "Num Gifts", "Average Gift")
        report = header_row + ("-" * len(header_row)) + "\n"
        # create sorted list of row data from donors
        with self._driver.session() as session:
            cyph = "MATCH (n:Donor) RETURN n"
            rresult = session.run(cyph)
            donors = [donor for rec in rresult for donor in rec.values()]
            sorted_donors = sorted(donors, key=itemgetter('total_donations'), reverse=True)
            # add a report row for each sorted donor row
            for donor in sorted_donors:
                report += "{:28}${:>10.2f}{:>12}   ${:>12.2f}\n".format(donor['name'], float(donor['total_donations']), self.get_donor(donor['name']).num_donations, float(donor['average_donation']))
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
