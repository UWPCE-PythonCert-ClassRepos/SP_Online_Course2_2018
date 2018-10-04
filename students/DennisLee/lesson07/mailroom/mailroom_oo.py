"""
This module defines the mailroom functionality using a peewee and
SQLite database setup for the donor information.
"""
#!/usr/bin/env python3

import logging
import os
import datetime
import peewee as pw
import mailroom_model as mdl


class DonorCollection():
    """Contains methods and properties for an entire donor roster."""

    def __init__(self):
        """Initialize the database and clear the data."""
        self.logger = self.set_up_logging()
        self.logger.info(f'Import database {mdl.db_name}.')
        self.database = pw.SqliteDatabase(mdl.db_name)
        self.connect_to_database()
        self.create_tables()

    def __repr__(self):
        return "DonorCollection()"

    def set_up_logging(self):
        """Set up the logging template and start logging."""
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(
            datetime.datetime.now().isoformat().replace(':', '-') + '_' +
            __name__ + '.log'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_formatter)

        file_logger = logging.getLogger()
        file_logger.setLevel(logging.INFO)
        file_logger.addHandler(file_handler)

        return file_logger

    def connect_to_database(self):
        """Open the database file."""
        self.logger.info('Connect to database.')
        self.database.connect()
        self.logger.info('Allow foreign keys in database.')
        self.database.execute_sql('PRAGMA foreign_keys = ON;')

    def create_tables(self):
        """Create the tables in the database."""
        self.logger.info("Creating the Person table.")
        self.database.create_tables([mdl.Person])
        self.logger.info("Creating the Donations table.\n")
        self.database.create_tables([mdl.Donations])

    def get_donor_list(self):
        """
        Query the Person table for all potential donor names.

        :return:  The list of donors, sorted by name.
        """
        self.logger.info("Query for donor names.")
        result = {}
        names = mdl.Person.select(
            mdl.Person.person_name,
            mdl.Person.lives_in_town
        ).order_by(mdl.Person.person_name)
        if names:
            for x in names:
                result[x.person_name] = x.lives_in_town
        self.logger.info(f"The donors are: {result}.")
        return result

    def get_donors_who_donated(self):
        """
        Query the Person table for only donor who have given gifts.

        :return:  The list of donors, sorted by name.
        """
        self.logger.info("Query for donor names.")
        result = {}
        names = mdl.Person.select(
            mdl.Person.person_name,
            mdl.Person.lives_in_town
        ).join(
            mdl.Donations
        ).order_by(
            mdl.Person.person_name
        ).where(mdl.Person.person_name == mdl.Donations.donor_name)
        if names:
            for x in names:
                result[x.person_name] = x.lives_in_town
        self.logger.info(f"The generous donors are: {result}.")
        return result

    def get_donor_info(self, name):
        """
        Query the Person table for a donor's personal information.
        Right now the only available data is the name and hometown.

        :name:  A string containing the donor name to retrieve.

        :return:  None.
        """
        self.logger.info(f"Get information about donor {name}.")
        result = {}
        info = mdl.Person.select(
            mdl.Person.person_name,
            mdl.Person.lives_in_town
        ).where(mdl.Person.person_name == name)
        if len(info) == 1:
            result = {
                'donor': info[0].person_name,
                'hometown': info[0].lives_in_town
            }
        self.logger.info(f"Donor info: {result}")
        return result

    def update_donor(self, name, hometown):
        """Change an existing donor's hometown."""
        self.logger.info(f"Set {name}'s hometown to {hometown}.")
        result = mdl.Person.update(
            lives_in_town=hometown
        ).where(mdl.Person.person_name == name).execute()
        self.logger.info(f"Update result: {result}.")
        new_info = self.get_donor_info(name)
        self.logger.info(f"New donor info: {new_info}.")

    def delete_data(self):
        """Delete all data in the database tables."""
        # Delete Donations table data
        self.logger.info(
            "Number of records in the Donations table: "
            f"{len(mdl.Donations.select())}."
        )
        self.logger.info("Delete all data from the Donations table.")
        mdl.Donations.delete().execute()
        self.logger.info(
            "Number of records in the Donations table now: "
            f"{len(mdl.Donations.select())}."
        )
        # Delete Person table data
        self.logger.info(
            "Number of records in the Person table: "
            f"{len(mdl.Person.select())}."
        )
        self.logger.info("Delete all data from the Person table.")
        mdl.Person.delete().execute()
        self.logger.info(
            "Number of records in the Person table now: "
            f"{len(mdl.Person.select())}."
        )

    def delete_donor_data(self, name):
        """
        Delete a donor's donations from the Donations table and the
        donor from the Person table.
        """
        self.logger.info(f"Deleting {name}'s donations.")
        mdl.Donations.delete().where(mdl.Donations.donor_name == name).execute()
        self.logger.info(f"Deleting {name} from donor list.")
        mdl.Person.delete().where(mdl.Person.person_name == name).execute()

    def close_database(self):
        """Close the database."""
        self.logger.info('Close database.')
        self.database.close()

    def create_gift_report(self):
        """
        Print out donation statistics for the entire donor roster.

        :return:  None.
        """
        self.logger.info('Print out donation stats for all donors.')
        query = mdl.Donations.select(
            mdl.Donations.donor_name,
            pw.fn.COUNT(mdl.Donations.donation_date).alias('gifts'),
            pw.fn.SUM(mdl.Donations.donation_amount).alias('total'),
            pw.fn.AVG(mdl.Donations.donation_amount).alias('average'),
            pw.fn.MAX(mdl.Donations.donation_amount).alias('largest'),
            pw.fn.MIN(mdl.Donations.donation_amount).alias('smallest')
        ).group_by(
            mdl.Donations.donor_name
        ).order_by(mdl.Donations.donor_name)

        if not query:
            self.logger.info("No donations to report.")
            print("\nNo donations from anyone yet.\n")
        else:
            self.logger.info(f"Total donors: {len(query)}.")
            col_heads = (
                'Donor name', 'Number of gifts', 'Total given',
                'Average gift', 'Largest gift', 'Smallest gift')
            col_head_str = ('{:<30s} | {:>15s}' + 4*' |  {:>13s}'
                           ).format(*col_heads)
            head_borderline = (
                '{:<30s} | {:>15s}' + 4*' | {:>14s}'
            ).format(
                '-'*30, '-'*15, '-'*14, '-'*14, '-'*14, '-'*14
            )
            data_str = '{:<30s} | {:>15d}' + 4*' | ${:>13,.2f}'
            self.logger.info(col_head_str)
            self.logger.info(head_borderline)
            print('\n')
            print(col_head_str)
            print(head_borderline)
            for i in query:
                data = (i.donor_name.__str__(), i.gifts, i.total,
                        i.average.__float__(), i.largest.__float__(),
                        i.smallest.__float__())
                self.logger.info(data)
                self.logger.info(data_str.format(*data))
                print(data_str.format(*data))
            print('\n')

    def add_or_update_donor(self, donor, town):
        """
        Add a donor or update a donor's hometown in the Person table.

        :donor:  The name of the donor to add or update.

        :town:  The new or existing donor's new hometown.

        :return:  None.
        """
        clean_name, clean_town = donor.strip(), town.strip()
        self.logger.info(
            f"Check whether {clean_name} with hometown {clean_town} "
            f"is in the Person table.")
        query = mdl.Person.select(
            mdl.Person.person_name,
            mdl.Person.lives_in_town
        ).where(mdl.Person.person_name == clean_name)
        if not query:
            self.logger.info(f"Person {clean_name} not in table - will add.")
            try:
                with self.database.transaction():
                    new_person = mdl.Person.create(
                        person_name=clean_name,
                        lives_in_town=clean_town
                    )
                    new_person.save()
            except Exception as e:
                self.logger.info(e)
        elif clean_town and query[0].lives_in_town != clean_town:
            self.logger.info(
                f"Person {clean_name} is in table but with another hometown "
                "update the record to change to the new hometown.")
            try:
                with self.database.transaction():
                    updated_person = mdl.Person.update(
                        lives_in_town=clean_town
                    ).where(mdl.Person.person_name == clean_name)
                    updated_person.save()
            except Exception as e:
                self.logger.info(e)

    def add_new_amount(self, donor, amount, date):
        """
        Add a new donation with the specified donor name and amount.
        If the donor is not currently in the donation history, a new
        entry is added.

        :name:  The name of the donor.

        :amount:  The amount given.

        :date:  The date of the donation, in YYYY-MM-DD format.

        :return:  None.
        """
        self.logger.info(f"Donor {donor} contributing {amount} on {date}.")
        amount = float(amount)
        if amount < 0.005:
            raise ValueError("The 'amount' argument must be at least $0.01.")

        with self.database.transaction():
            try:
                single_donation = mdl.Donations.create(
                    donor_name=donor,
                    donation_amount=round(amount, 2),
                    donation_date=date
                )
            except Exception as e:
                self.logger.info(e)
                self.logger.info('Donation unsuccessful.')
            else:
                single_donation.save()
                self.logger.info('Successfully added donation.')

    def save_letters(self, folder=""):
        """
        Save the donor thank-you letters to disk.

        :folder:  The folder in which to save the files. If an invalid
                  folder is specified or no folder is specified, the
                  current folder is used. If the folder does not exist,
                  the method attempts to create the folder and save
                  the letters in the created folder.

        :return:  The folder containing the thank-you letters.
        """
        self.logger.info("Save thank-you letters.")
        cur_dir, letters = os.getcwd(), {}
        if not folder:
            folder = cur_dir
        try:
            self.logger.info(f'Create the "{folder}" directory, if necessary.')
            os.mkdir(folder)
        except FileExistsError:  # Okay if folder already exists
            self.logger.info("Folder already exists.")
        finally:  # Save each letter, with donor name in each file name
            self.logger.info(f'Change current directory to "{folder}".')
            os.chdir(folder)
            folder = os.getcwd()  # Set folder name to the full OS path
            self.logger.info(f'Current directory is now "{folder}".')

            # Create dict of letter names+letter texts, then write files
            self.logger.info("Get list of actual donors.")
            query = self.get_donors_who_donated()
            self.logger.info("Create dict of filenames and letter text.")
            for i in query:
                letters[f'_{i}.txt'] = self.form_letter(i)
            self.logger.info(f"The letter filenames are: {letters.keys()}")
            for filename, text in letters.items():
                self.logger.info(f"Text contents for {filename}:")
                lines = text.splitlines()
                with open(filename, 'w') as f:
                    for line in lines:
                        self.logger.info('Writing line: ' + line)
                        f.write(line + '\n')
            self.logger.info(f"Change current directory back to '{cur_dir}''.")
            os.chdir(cur_dir)
            self.logger.info(f"Return folder with the letters: '{folder}'.")
            return folder

    # @property
    def form_letter(self, name, index=-1):
        """
        Create a thank you form letter for a specific donation.

        :name:  The name of the donor to send the letter to.

        :index:  An index to a certain gift within the donation history.
                 This value defaults to the most recent gift amount.

        :return:  A string containing the filled-in form letter.
        """
        self.logger.info(f"Creating form letter for {name}.")
        query_all = mdl.Donations.select(
            mdl.Donations.donation_amount,
            mdl.Donations.donation_date
        ).where(
            mdl.Donations.donor_name == name
        ).order_by(mdl.Donations.donation_date)
        query_count = len(query_all)
        self.logger.info(f"Donor {name} has made {query_count} donations.")

        if index not in range(-query_count, query_count):
            self.logger.info(f"Donor '{name}' has donated '{query_count}' "
                             f"times, so gift # '{index}' is out of range.")
        else:
            text = """\n\n\n
                    From:     Random Worthy Cause Foundation
                    To:       {0:s}
                    Subject:  Your generous donation

                    Dear {0:s},

                    We want to express our gratitude for your donation of ${1:,.2f}
                    {2:s}to the Random Worthy Cause Foundation.  To show our
                    appreciation, we have enclosed a set of address labels
                    and a custom tote bag that lets people know that you are a
                    generous supporter of our cause.
                    
                    Thank you again, and please think of us the next time you
                    want to give to a worthy cause.

                    Sincerely,



                    Mister E. Partner
                    Random Worthy Cause Foundation

                    """
            text = '\n'.join([line.lstrip() for line in text.splitlines()])
            # If a donor has given before, add a parenthetical clause
            # stating the total donation amount and number of donations
            extra = ''
            if query_count > 1:
                query_sum = mdl.Donations.select(
                    pw.fn.SUM(mdl.Donations.donation_amount)
                ).where(mdl.Donations.donor_name == name)
                donation_total = query_sum.scalar()
                self.logger.info(f"List total donations of ${donation_total}.")
                extra = '(and total donations of ${0:,.2f} from {1:,d} gifts)' \
                        '\n'.format(donation_total, query_count)
            self.logger.info(f"Text = {text}.")
            self.logger.info(f"Extra = {extra}.")
            self.logger.info(f"Name = {name}.")
            self.logger.info(f"Donation amount = {query_all[index].donation_amount}.")
            return text.format(name, query_all[index].donation_amount, extra)
