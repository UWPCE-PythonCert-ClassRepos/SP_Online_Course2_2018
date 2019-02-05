#!/usr/bin/env python3

import mailroom_data
import login_database
import redis
import random


driver = login_database.login_neo4j_cloud()


class MyDonations():

    def load_initial_donors(self):
        mailroom_data.populate_DB()

    def add_donation(self, name, amount):
        """
            Adds a new donor and donation contribution
        """

        try:
            with driver.session() as session:

                # Add new donor
                cyph = "MERGE (n:Donor {donor_name:'%s'})" % (name)
                session.run(cyph)

                # Add new donation relationship
                don_cyph = """
                              MATCH (p1:Donor)
                              WHERE p1.donor_name='%s'
                              CREATE (p1)-[r:DONATED]->(d1:Donations {donation_amount: '%s'})
                              RETURN p1, r, d1
                            """ % (name, amount)
                session.run(don_cyph)

        except Exception as e:
            print(e)

    def challenge(self, donor, factor=1, min=50, max=9999999):
        """
            Returns estimated predictions of current donations
        """
        total = 0
        new_total = 0

        try:
            with driver.session() as session:
                cyph = """
                  MATCH (donor {donor_name:'%s'})-[:DONATED]->(donation)
                  RETURN donation
                  """ % (donor)
                result = session.run(cyph)

                for row in result:
                    for i in row.values():
                        amount = float(i['donation_amount'])
                        new_total += amount

                        if(min <= amount <= max):
                            total += amount

                new_total += (total * factor)

            proj_str = ("\nIf donations between ${0} and ${1} are multiplied by a factor of {2}, "
                        "\nthe total contribution for {3} "
                        "will be: $").format(min, max, factor, donor)

            return proj_str + str(round(new_total, 2))

        except Exception as e:
            print(e)

    def update_donor(self, name, new_name):
        """
            Updates the specified donor's name
        """

        try:
            with driver.session() as session:

                cyph = """
                        MERGE (p:Donor{donor_name:'%s'})
                        SET p.donor_name = '%s';
                       """ % (name, new_name)
                session.run(cyph)

                print("\n{0} has been updated to {1} ".format(name, new_name))

        except Exception as e:
            print(e)

    def update_donation(self, name, donation, new_donation):
        """
            Updates a donor's donation amount
        """

        try:
            with driver.session() as session:

                cyph = """
                        START n=node(*)
                        MATCH (p1)-[r:DONATED]->(d1)
                        WHERE p1.donor_name='%s' AND d1.donation_amount='%s'
                        SET d1.donation_amount='%s'
                       """ % (name, donation, new_donation)
                session.run(cyph)

        except Exception as e:
            print(e)

        print("\n${0} has been updated to ${1}".format(donation, new_donation))

    def delete_donor(self, name):
        """
            Deletes a donor and donations
        """
        try:
            with driver.session() as session:

                cyph = """
                        MATCH (p1:Donor)
                        WHERE p1.donor_name='%s'
                        DETACH DELETE p1
                       """ % (name)
                session.run(cyph)

        except Exception as e:
            print(e)

        print("\n{0} has been deleted... ".format(name))

    def delete_donation(self, name, donation):
        """
            Deletes a donor's donations
        """

        try:
            with driver.session() as session:

                cyph = """
                        START n=node(*)
                        MATCH (p1)-[r:DONATED]->(d1)
                        WHERE p1.donor_name='%s' AND d1.donation_amount='%s'
                        DETACH DELETE d1
                       """ % (name, donation)
                session.run(cyph)

        except Exception as e:
            print(e)

        print("\n{0}'s donation of ${1} has been deleted... ".format(name, donation))

    def update_cache(self):
        """
            uses non-presistent Redis to create a cache of donor values
        """
        donors = self.get_list_of_donors()

        d = login_database.login_redis_cloud()

        for value in d.keys():
            d.delete(value)

        r = login_database.login_redis_cloud()

        print("\nUpdating Donor cache...\n")

        for name in donors:
            summary = self.get_donor_summary(name)

            # Create donor cache
            r.hmset(name, {'phone': self.get_phone_number(),
                           'email': self.create_email(name),
                           'zip': self.get_zip(),
                           'last_donation': '$'+str(summary["last_donation"]),
                           'last_donation_date': self.get_date()})

    def donor_lookup(self, name, value):
        """
            uses Redis cache to validate a users value
        """

        r = login_database.login_redis_cloud()

        str_format_1 = "\n    {0}'s {1} is: {2}"
        str_format_2 = "    {0}: {1}"
        list_of_values = ['phone', 'email', 'zip', 'last_donation', 'last_donation_date']

        if(value == "all"):
            print(f"\n{name}\'s stored values:\n")
            for i in list_of_values:
                print(str_format_2.format(i.replace('_', ' ').capitalize(),
                      r.hget(name, i)))
        else:
            # Get requested value
            req_val = r.hget(name, value)

            frmt_val = value.lower().replace('_', ' ').capitalize()
            print(str_format_1.format(name, frmt_val, req_val))

    def get_list_of_donors(self):
        """
            Returns a list of donor names
        """

        try:
            return mailroom_data.get_all_donors()

        except Exception as e:
            print(e)

    def get_formatted_list_of_donors(self):
        """
            Returns a formatted list of donor names
        """

        donor_list = mailroom_data.get_all_donors()
        names = []

        for row in donor_list:
            names.append(row)

        print("\nList of current donors: ")
        print(*names, sep=", ")

    def get_list_of_donations(self, name):
        """
            Returns a list of donations from the donor specified
        """

        try:

            return mailroom_data.get_all_donations(name)

        except Exception as e:
            print(e)

    def get_formatted_list_of_donations(self, name):
        """
            Returns a formatted list of donations
            for the given donor name
        """

        donations_list = self.get_list_of_donations(name)
        donations = []

        for row in donations_list:
            donations.append("$" + str(row))

        print("\nList of current donations for {}: ".format(name))
        print(*donations, sep=", ")

    @property
    def get_summary(self):
        """
            Returns a formatted list of donors and donations
            ordered by the average total contribution
        """

        headers = ["Donor Name", "Total Given", "Num Gifts", "Average Gift"]
        str_format = "{:<30} ${:>17} {:>16} ${:>14}"
        print(("\n{:<30} | {:^15} | {:^15} | {:^15}").format(*headers))
        print("-"*82)

        try:
            with driver.session() as session:

                donors = mailroom_data.get_all_donors()

                for row in donors:
                    sum = 0
                    num = []

                    cyph = """
                      MATCH (donor {donor_name:'%s'})-[:DONATED]->(donation)
                      RETURN donation
                      """ % (row)
                    result = session.run(cyph)

                    for rec in result:
                        for i in rec.values():
                            donation = float(i['donation_amount'])
                            num.append(donation)
                            sum += donation

                    print(str_format.format(row, sum,
                                            len(num),
                                            str(self.Average(num))))

        except Exception as e:
            print(e)

    def get_donor_summary(self, name):
        """
            Returns a summary of the last donation and total
            contribution of a donor
        """
        summary = {}
        total = 0
        num = []

        try:
            with driver.session() as session:
                cyph = """
                  MATCH (donor {donor_name:'%s'})-[:DONATED]->(donation)
                  RETURN donation
                  """ % (name)
                result = session.run(cyph)

                for row in result:
                    for i in row.values():
                        num.append(float(i['donation_amount']))
                        total += float(i['donation_amount'])

                summary["donor_name"] = name
                summary["last_donation"] = num[0]
                summary["total"] = round(total, 2)

            return summary
        except Exception as e:
            print(e)

    def get_last_donation(self, name):
        """
            Returns the last donation for the specified donor
        """
        summary = {}
        num = []

        try:
            with driver.session() as session:
                cyph = """
                  MATCH (donor {donor_name:'%s'})-[:DONATED]->(donation)
                  RETURN donation
                  """ % (name)
                result = session.run(cyph)

                for row in result:
                    for i in row.values():
                        num.append(float(i['donation_amount']))

                summary["donor_name"] = name
                summary["amount"] = num[0]

            return summary

        except Exception as e:
            print(e)

    def Average(self, lst):
        """
            Returns the average of a list of values
        """
        return round(sum(lst) / len(lst), 2)

    def unique(self, sequence):
        """
            Returns unique values in the order given
        """
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]

    def create_email(self, name):
        """
            Returns an email based on the donor's name
        """
        return str(name).replace(' ', '').lower()+'@gmail.com'

    def get_phone_number(self):
        """
            Returns a randomly created phone number
        """
        n = '0000000000'
        while '9' in n[3:6] or n[3:6] == '000' or n[6] == n[7] == n[8] == n[9]:
            n = str(random.randint(10**9, 10**10-1))
        return n[:3] + '-' + n[3:6] + '-' + n[6:]

    def get_zip(self):
        """
            Returns a randomly created zip code
        """
        zips = ['85326', '07450', '91784', '38024',
                '45385', '07501', '43551', '97402']
        return zips[random.randint(0, 6)]

    def get_date(self):
        """
            Returns a randomly created date
        """
        month = random.randint(1, 12)
        day = 0
        year = 0

        if month == 2:
            day = random.randint(1, 28)
        elif month in (4, 6):
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)

        year = random.randint(2000, 2018)

        return (str(month) + '/' + str(day) + '/' + str(year))


class DonationError(Exception):
    """Raised when the donation value is not found"""
    pass
