#!/usr/bin/env python3
# from create_mailroom_db import *
import mailroom_data
import login_database
import pymongo
import redis
import random


class MyDonations():

    def load_initial_donors(self):

        with login_database.login_mongodb_cloud() as client:
            db = client['dev']

            mailroom = db['mailroom']

            # Drop current DB
            db.drop_collection('mailroom')
            # Load initial list of donors
            mailroom.insert_many(mailroom_data.get_donor_data())

            print("\nInitial donors have been loaded...")

    def add_donation(self, name, amount):
        """
            Adds a new donor and donation contribution
        """

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                mailroom.insert({'donor': name, 'donation': amount})

        except IntegrityError as IE:
            pass
        except Exception as e:
            print(e)

    def challenge(self, donor, factor=1, min=50, max=9999999):
        """
            Returns estimated predictions of current donations
        """
        total = 0
        new_total = 0

        try:

            with login_database.login_mongodb_cloud() as client:
                db = client['dev']
                mailroom = db['mailroom']

                # Return donations within the specified range
                query = {"donor": {"$eq": donor}, "donation": {"$gte": min, "$lte": max}}

                result = mailroom.find(query)

                for row in result:
                    new_total += round(float(row['donation']), 2) * factor

                total_query = {"donor": {"$eq": donor}}
                total_result = mailroom.find(total_query)

                for i in total_result:
                    total += i['donation']

            proj_str = ("\nIf donations between ${0} and ${1} are multiplied by a factor of {2}, "
                        "\nthe total contribution for {3} "
                        "will be: $").format(min, max, factor, donor)

            return proj_str + str(new_total + total)

        except Exception as e:
            print(e)

    def update_donor(self, name, new_name):
        """
            Updates the specified donor's name
        """

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                mailroom.update_many({"donor": {"$eq": name}}, {"$set": {"donor": new_name}})

                print("\n{0} has been updated to {1} ".format(name, new_name))

        except Exception as e:
            print(e)

    def update_donation(self, name, donation, new_donation):
        """
            Updates a donor's donation amount
        """

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                mailroom.update_one({"donor": {"$eq": name},
                                     "donation": {"$eq": donation}},
                                    {"$set": {"donation": new_donation}})

                print("\n${0} has been updated to ${1}".format(donation, new_donation))

        except Exception as e:
            print(e)

    def delete_donor(self, name):
        """
            Deletes a donor and donations
        """
        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                mailroom.remove({"donor": {"$eq": name}})

                print("\n{0} has been deleted... ".format(name))

        except IntegrityError as IE:
            pass
        except Exception as e:
            print(e)

    def delete_donation(self, name, donation):
        """
            Deletes a donor's donations
        """

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                mailroom.delete_one({"donor": {"$eq": name},
                                     "donation": {"$eq": donation}})

                print("\n{0}'s donation of ${1} has been deleted... ".format(name, donation))

        except Exception as e:
            print(e)

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
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                results = mailroom.distinct('donor')

                return results

        except Exception as e:
            print(e)

    def get_formatted_list_of_donors(self):
        """
            Returns a formatted list of donor names
        """

        donor_list = self.get_list_of_donors()
        names = []

        for row in donor_list:
            names.append(row)

        print("\nList of current donors: ")
        print(*names, sep=", ")

    def get_list_of_donations(self, name):
        """
            Returns a list of donations from the donor specified
        """

        donations = []

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                query = {"donor": {"$eq": name}}

                result = mailroom.find(query)

                for row in result:
                    donations.append(row['donation'])

                return donations

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

            with login_database.login_mongodb_cloud() as client:
                db = client['dev']
                mailroom = db['mailroom']

                query = {}
                output = mailroom.find(query).sort([("donation", pymongo.DESCENDING)])
                donors = []

                for row in output:
                    donors.append(row['donor'])

                unique_donors = self.unique(donors)

                for row in unique_donors:
                    sum = 0
                    num = []

                    query = {"donor": {"$eq": row}}
                    result = mailroom.find(query)

                    for i in result:
                        num.append(i['donation'])
                        sum += i['donation']

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

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']
                mailroom = db['mailroom']

                query = {"donor": {"$eq": name}}
                result = mailroom.find(query).sort([("_id", pymongo.DESCENDING)]).limit(1)

                for row in result:
                    summary["donor_name"] = row['donor']
                    summary["last_donation"] = row['donation']

                total_result = mailroom.find(query)

                for i in total_result:
                    total += i['donation']

                summary["total"] = round(total, 2)

            return summary
        except Exception as e:
            print(e)

    def get_last_donation(self, name):
        """
            Returns the last donation for the specified donor
        """
        summary = {}

        try:
            with login_database.login_mongodb_cloud() as client:
                db = client['dev']

                mailroom = db['mailroom']

                query = {"donor": {"$eq": name}}

                result = mailroom.find(query).sort([("_id", pymongo.DESCENDING)]).limit(1)

            for row in result:
                summary["donor_name"] = row['donor']
                summary["amount"] = row['donation']
        except Exception as e:
            print(e)

        return summary

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
