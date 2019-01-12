#!/usr/bin/env python3
from create_mailroom_db import *


class MyDonations():

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

    def challenge(self, donor, factor=1, min=50, max=9999999):
        """
            Returns estimated predictions of current donations
        """
        new_collection = Donations()
        new_total = 0

        # Return donations within the specified range
        donor_id = self.get_donor_id(donor)
        query = (Donations.select(Donations.donation)
                          .where((Donations.donor_id == donor_id) &
                                 (Donations.donation <= max) &
                                 (Donations.donation >= min)))

        for row in query:
            new_total += round(float(row.donation), 2) * factor

        proj_str = ("\nIf donations between ${0} and ${1} are multiplied by a factor of {2}, "
                    "\nthe total contribution for {3} "
                    "will be: $").format(min, max, factor, donor)

        return proj_str + str(new_total)

    def update_donor(self, name, new_name):
        """
            Updates the specified donor's name
        """

        database = SqliteDatabase('mailroom.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            update = (Donors.update(donor_name=new_name)
                            .where(Donors.donor_name == name))

            if(update.execute()):
                print("\n'{0}' has been updated to '{1}''".format(name, new_name))
            else:
                raise ValueError

        finally:
            database.close()

    def update_donation(self, name, donation, new_donation):
        """
            Updates a donor's donation amount
        """

        database = SqliteDatabase('mailroom.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            donor_id = self.get_donor_id(name)
            donation_id = ""

            query = (Donations.select(fn.max(Donations.id).alias('id'))
                              .where((Donations.donor_id == donor_id) &
                                     (Donations.donation == donation))
                              .namedtuples())

            for row in query:
                donation_id = row.id

            update = (Donations.update(donation=new_donation)
                               .where(Donations.id == donation_id))

            if(update.execute()):
                print("\n${0} has been updated to ${1}".format(donation, new_donation))
            else:
                raise DonationError

        finally:
            database.close()

    def delete_donor(self, name):
        """
            Deletes a donor and donations
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

    def delete_donation(self, name, donation):
        """
            Deletes a donor's donations
        """

        database = SqliteDatabase('mailroom.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            donor_id = self.get_donor_id(name)
            donation_id = ""

            query = (Donations.select(fn.max(Donations.id).alias('id'))
                              .where((Donations.donor_id == donor_id) &
                                     (Donations.donation == donation))
                              .namedtuples())

            for row in query:
                donation_id = row.id

            to_del = Donations.delete().where(Donations.id == donation_id).execute()

            if (to_del):
                print("\n{0}'s donation of ${1} has been deleted... ".format(name, donation))
            else:
                raise DonationError

        finally:
            database.close()

    def get_list_of_donors(self):
        """
            Returns a list of donor names
        """

        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        donors_query = (Donors.select(Donors.donor_name).distinct())

        return donors_query

    def get_list_of_donations(self, id):
        """
            Returns a list of donations from the donor specified
        """

        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        donations_query = (Donations.select(Donations.donation)
                                    .where(Donations.donor_id == id))

        return donations_query

    def get_donor_id(self, name):
        """
            Returns the primary key of a donor based on their name
        """

        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        id = ""

        id_query = (Donors.select(Donors.id)
                          .where(Donors.donor_name == name))

        for row in id_query:
            id = row.id

        return id

    def get_donation_id(self, donation):
        """
            Returns the primary key of a donor based on their name
        """

        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        id = ""

        id_query = (Donations.select(fn.max(Donations.id))
                             .where(Donations.donation == donation))

        for row in id_query:
            id = row.id

        return id

    def get_formatted_list_of_donors(self):
        """
            Returns a formatted list of donor names
        """

        donor_list = self.get_list_of_donors()
        names = []

        for row in donor_list:
            names.append(row.donor_name)

        print("\nList of current donors: ")
        print(*names, sep=", ")

    def get_formatted_list_of_donations(self, name):
        """
            # Returns a formatted list of donations
            for the given donor name
        """

        id = self.get_donor_id(name)
        donations_list = self.get_list_of_donations(id)
        donations = []

        for row in donations_list:
            donations.append("$" + str(row.donation))

        print("\nList of current donations for {}: ".format(name))
        print(*donations, sep=", ")

    # Returns the total donations for each donor
    @property
    def donation_totals(self):
        return {sum(self.donor_dict[key]) for key in self.donor_dict}

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
        """
            Returns a summary of the last donation and total
            contribution of each donor
        """
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
        """
            Returns the last donation for the specified donor
        """
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


class DonationError(Exception):
    """Raised when the donation value is not found"""
    pass
