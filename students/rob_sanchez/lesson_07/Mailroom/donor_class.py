#!/usr/bin/env python3
from create_mailroom_db import *


class MyDonations():

    def __init__(self):
        self.donor_name = ""
        self.donation_amount = ""
        self.donors_list = []

    def add_donation(self, name, amount):
        """
            Adds a new donor and donation contribution
        """

        database = SqliteDatabase('mailroom.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            with database.transaction():
                new_donor = Donors.create(donor_name=name)
                new_donor.save()

        except IntegrityError as IE:
            pass
        except Exception as e:
            print(e)

        finally:
            database.close()

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            id = self.get_donor_id(name)
            with database.transaction():
                donations = Donations.create(
                    donor=id,
                    donation=amount)
                donations.save()
        except Exception as e:
            print(e)

        finally:
            database.close()

    def delete_donor(self, name):
        """
            Adds a new donor and donation contribution
        """

        database = SqliteDatabase('mailroom.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            donor_id = self.get_donor_id(name)

            Donations.delete().where(Donations.donor_id == donor_id).execute()
            Donors.delete().where(Donors.donor_name == name).execute()

            print("\n{0} has been deleted... ".format(name))

        finally:
            database.close()

    # Returns a list of donor names
    def get_list_of_donors(self):

        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        donors_query = (Donors.select(Donors.donor_name).distinct())

        return donors_query

    # Returns a list of donor ids
    def get_donor_id(self, name):

        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        id = ""

        donors_query = (Donors.select(Donors.id)
                              .where(Donors.donor_name == name))

        for row in donors_query:
            id = row.id

        return id

    # Returns a formatted list of donor names
    def get_formatted_list_of_donors(self):

        donor_list = self.get_list_of_donors()
        names = []

        for row in donor_list:
            names.append(row.donor_name)

        print("\nList of current donors: ")
        print(*names, sep=", ")

    # Returns the total donations for each donor
    @property
    def donation_totals(self):
        return {sum(self.donor_dict[key]) for key in self.donor_dict}

    # Returns donation summary ordered by donation amount
    @property
    def get_summary(self):
        """
            Returns a formatted list of donors and donations
        """
        headers = ["Donor Name", "Total Given", "Num Gifts", "Average Gift"]
        str_format = "{:<30} ${:>17} {:>16} ${:>14}"
        print(("\n{:<30} | {:^15} | {:^15} | {:^15}").format(*headers))
        print("-"*82)

        database = SqliteDatabase('mailroom.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            names_query = (Donors.select(Donors.donor_name,
                                         fn.SUM(Donations.donation).alias('total'),
                                         fn.COUNT(Donations.donation).alias('num'),
                                         fn.AVG(Donations.donation).alias('avg'))
                           .join(Donations, on=(Donors.id == Donations.donor_id))
                           .group_by(Donors.donor_name)
                           .order_by(fn.AVG(Donations.donation).desc())
                           )

            for name in names_query:
                print(str_format.format(str(name.donor_name),
                                        round(float(name.total), 2),
                                        str(name.num),
                                        round(name.avg, 2)))
        except Exception as e:
            print(e)

        finally:
            database.close()

    def get_donor_summary(self, name):
        summary = {}
        id = self.get_donor_id(name)

        query = (Donors.select(Donors.donor_name,
                               (Donations.select(Donations.donation)
                                         .where(Donations.id ==
                                (Donations.select(fn.max(Donations.id))
                                         .where(Donations.donor_id == id)))).alias('last'),
                               fn.SUM(Donations.donation).alias('total'))
                       .join(Donations, on=(Donors.id == Donations.donor_id))
                       .where(Donations.donor_id == id)
                       .namedtuples())

        for row in query:
            summary["donor_name"] = row.donor_name
            summary["last_donation"] = row.last
            summary["total"] = round(row.total, 2)

        return summary

    def get_last_donation(self, name):
        summary = {}
        id = self.get_donor_id(name)

        try:
            query = (Donors.select(Donors.donor_name.distinct(),
                                   (Donations.select(Donations.donation)
                                             .where(Donations.id ==
                                    (Donations.select(fn.max(Donations.id))
                                             .where(Donations.donor_id == id)))).alias('last')
                                   )
                           .join(Donations, on=(Donors.id == Donations.donor_id))
                           .where(Donations.donor_id == id)
                           .namedtuples())

            for row in query:
                summary["donor_name"] = row.donor_name
                summary["amount"] = row.last
        except Exception as e:
            print(e)

        return summary

    def challenge(self, donor, factor=1, min=50, max=9999999):
        new_collection = Donations()

        filtered_donations = self.filter_donations(self.donor_dict[donor], min, max)
        new_list = list(map(lambda x: x*factor, filtered_donations))

        for donations in new_list:
            new_collection.add_donation(donor, donations)

        proj_str = ("\nIf donations between ${} and ${} are multiplied by a factor of {}, "
                    "\nthe total contribution for {} "
                    "will be: $").format(min, max, factor, donor)

        return proj_str + str(new_collection.donation_totals).strip('{}')

    def filter_donations(self, donations, min, max):
        return list(filter(lambda x: min <= x <= max, donations))
