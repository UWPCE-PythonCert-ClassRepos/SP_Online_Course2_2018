"""
This module defines the mailroom functionality using a Redis
database setup for the donor information.
"""
#!/usr/bin/env python3

import logging
import os
import datetime
import mailroom_db_login


def strip_text(text):
    """
    Return text stripped of leading and trailing spaces. If the input
    is not an instance of a string, just return an empty string. This
    function is used to avoid exceptions (for example, if `text` is
    `None`.)
    """
    result = ''
    if isinstance(text, str):
        result = text.strip()
    return result

class DonorCollection():
    """Contains methods and properties for an entire donor roster."""

    def __init__(self):
        """Initialize the database and clear the data."""
        self.logger = self.set_up_logging()
        self.database = None
        self.prefix_person = '(PERSON)'
        self.prefix_donation = '(DONATION)'
        self.logger.info(
            "The formats for keys in the database are "
            f"'{self.prefix_person}_Firstname Lastname' for a person and "
            f"'{self.prefix_donation}_Firstname Lastname_GiftDate' for a gift."
        )
        self.connect_to_database()

    def __repr__(self):
        return "DonorCollection()"

    def set_up_logging(self):
        """Set up the logging template and start logging."""
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(
            '../logs/' +
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
        self.logger.info("Connect to database.")
        self.database = mailroom_db_login.login_redis_cloud()

    def build_pattern(self, record_type, str1, *additional_strs):
        """
        Return a database key pattern to use in a query.

        :record_type:  The record type prefix (for persons or donations).

        :str1:  A required string to join to the record type.  Can be a
                wildcard ('*') or the first key name (f/a composite key.)

        :additional_strs:  Additional strings to join to the key pattern.
                           If specified, usually ends with a wildcard ('*')
                           unless an exact key string is desired.

        :return:  The string containing the database key pattern.
        """
        self.logger.info(f"Build DB key pattern with {record_type} and {str1}")
        self.logger.info(
            "If additional_strs is a string or string iterable, it's included "
            f"(even f/an empty string). Here's its value: {additional_strs}.")
        result = '_'.join([record_type, str1, *additional_strs])
        self.logger.info(f"Here's the pattern: '{result}'.")
        return result

    def get_keys(self, pattern):
        """
        Return sorted list of database keys matched by the pattern.
        """
        self.logger.info(f"Scanning DB for key pattern {pattern}.")
        result = self.database.keys(pattern)
        if not result:
            self.logger.info(f"No records found.")
        else:
            result.sort()
            num_keys = len(result)
            self.logger.info(
                f"Found these {num_keys} key(s): {result}."
            )
        return result

    def get_db_value(self, key):
        """
        Get the value associated with a database key.

        :key:  The actual intended key name; no wildcards allowed.

        :return:  The database key's value.
        """
        self.logger.info(f"Getting the value for this DB key: '{key}'.")
        result = self.database.get(key)
        self.logger.info(f"DB key '{key}' value: {result}.")
        return result

    def get_donor_list(self):
        """
        Query the Person table for all potential donor names.

        :return:  The list of person-phone dicts, sorted by name.
        """
        self.logger.info("Query for donor names.")
        result = {}
        key_pattern = self.build_pattern(self.prefix_person, '*')
        key_list = self.get_keys(key_pattern)
        if key_list:
            for key in key_list:
                result[key.split('_')[1]] = self.get_db_value(key)
        self.logger.info(f"The donor-phone info is: {result}.")
        return result

    def get_donors_who_donated(self):
        """Return the list of donors who have actually given already."""
        self.logger.info("Get a list of donors who actually donated.")
        self.logger.info("Don't include donor names who haven't given yet.")
        result = None
        donation_key_pattern = self.build_pattern(self.prefix_donation, '*')
        donation_key_list = self.get_keys(donation_key_pattern)
        if donation_key_list:
            clean_donors = set(
                map(lambda x: x.split('_')[1], donation_key_list)
            )
            self.logger.info(f"Unique real donors: {len(clean_donors)}.")
            self.logger.info(f"Clean donor set: {clean_donors}.")

            result = list(clean_donors)
            result.sort()
            self.logger.info(f"Unique real donors: {len(result)}.")
            self.logger.info(f"Unique real donor list: {result}.")
        return result

    def get_donor_info(self, name):
        """
        Query the Person table for a donor's personal information.
        Right now the only available data is the name and phone number.

        :name:  A string containing the donor name to retrieve.

        :return:  A tuple containing the donor name and their phone #.
        """
        clean_name = strip_text(name)
        self.logger.info(f"Get information about donor '{clean_name}'.")
        result = tuple()
        name_as_key = self.build_pattern(self.prefix_person, clean_name)
        info = self.get_db_value(name_as_key)
        if info is not None:
            result = (clean_name, info)
        self.logger.info(f"Donor info: {result}.")
        return result

    def delete_data(self):
        """Delete all data in the database tables."""

        # Delete all donations
        donation_key_pattern = self.build_pattern(self.prefix_donation, '*')
        self.logger.info(
            f"Number of records in database: {self.database.dbsize()}.")
        donations_to_delete = self.get_keys(donation_key_pattern)
        if donations_to_delete:
            self.logger.info("Delete all donations.")
            self.database.delete(*donations_to_delete)
            self.logger.info(
                f"Number of records in DB now: {self.database.dbsize()}.")
            self.logger.info(
                "Number of donations now: "
                f"{len(self.database.keys(donation_key_pattern))}."
            )

        # Delete all persons
        person_key_pattern = self.build_pattern(self.prefix_person, '*')
        persons_to_delete = self.get_keys(person_key_pattern)
        if persons_to_delete:
            self.logger.info("Delete all persons.")
            self.database.delete(*persons_to_delete)
            self.logger.info(
                f"Number of records in DB now: {self.database.dbsize()}.")
            self.logger.info(
                "Number of persons now: "
                f"{len(self.database.keys(person_key_pattern))}."
            )

    def delete_donor_data(self, name):
        """
        Delete a donor's donations from the Donations table and the
        donor from the Person table.
        """
        clean_name = strip_text(name)

        self.logger.info(
            f"Number of records in DB: {self.database.dbsize()}.")
        self.logger.info(f"Deleting '{clean_name}' donations.")
        donation_key_pattern = self.build_pattern(
            self.prefix_donation, clean_name, '*')
        person_donations = self.get_keys(donation_key_pattern)
        if person_donations:
            self.logger.info(f"Found {len(person_donations)} donations.")
            self.database.delete(*person_donations)
            self.logger.info(
                f"Number of records in DB now: {self.database.dbsize()}.")

        self.logger.info(f"Deleting '{clean_name}' from donor list.")
        person_as_key = self.build_pattern(self.prefix_person, clean_name)
        self.database.delete(person_as_key)
        self.logger.info(
            f"Number of records in database now: {self.database.dbsize()}.")

    def create_gift_report(self):
        """
        Print out donation statistics for the entire donor roster.

        :return:  None.
        """
        self.logger.info('Print out donation stats for all donors.')
        clean_donors = self.get_donors_who_donated()
        if not clean_donors:
            print("\nNo donations from anyone yet.\n")
        else:
            self.logger.info(f"Total donors: {len(clean_donors)}.")

            # Print and log column headings and heading rule
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

            for donor in clean_donors:
                donor_key_pattern = self.build_pattern(
                    self.prefix_donation, donor, '*')
                donor_keys = self.get_keys(donor_key_pattern)
                donor_gifts = []
                for key in donor_keys:
                    donor_amount = float(self.get_db_value(key))
                    donor_gifts.append(donor_amount)
                data = (donor, len(donor_gifts), sum(donor_gifts),
                        1.0 * sum(donor_gifts) / len(donor_gifts),  # average
                        max(donor_gifts), min(donor_gifts))
                self.logger.info(data_str.format(*data))
                print(data_str.format(*data))
            print('\n')

    def add_or_update_donor(self, donor, phone):
        """
        Add a donor or update a donor's phone# in the database.

        :donor:  The name of the donor to add or update.

        :phone:  The new or existing donor's phone number.

        :return:  None.
        """
        clean_name, clean_phone = strip_text(donor), strip_text(phone)
        self.logger.info(
            f"Attempting to add donor '{clean_name}' "
            f"with phone number '{clean_phone}'."
        )
        if not clean_name or not clean_phone:
            print("Exiting - must enter a non-null donor name and phone #.")
        else:
            self.database.set(
                self.build_pattern(self.prefix_person, clean_name),
                clean_phone
            )

    def add_new_amount(self, donor, amount, date):
        """
        Add a new donation with the specified donor name and amount.
        The donor must currently be in the donation history.
        The key is formed using the donor and the date.

        :name:  The name of the existing donor.

        :amount:  The amount given.

        :date:  The date of the donation, in YYYY-MM-DD format.

        :return:  None.
        """
        clean_name = strip_text(donor)
        self.logger.info(f"Donor '{donor}' giving '{amount}' on '{date}'.")
        if not clean_name:
            self.logger.info("Donor name is empty.")
            raise ValueError("No donor name specified.")

        try:
            cnv_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            str_date = datetime.date.isoformat(cnv_date)
        except ValueError:
            self.logger.info(f"Problem with date format in {date}.")
            raise ValueError(f"'{date}' is an invalid date format.")

        try:
            amount = float(amount)
        except ValueError:
            self.logger.info(f"Specified gift amount must be a number.")
        if amount < 0.005:
            self.logger.info(f"Gift of {amount} must be at least one penny.")
            raise ValueError(
                f"'{amount}' is invalid - must be at least $0.01.")

        self.logger.info(f"Make sure '{clean_name}' already in donor list.")
        donor_key = self.build_pattern(self.prefix_person, clean_name)
        if not self.get_db_value(donor_key):
            self.logger.info(f"'{clean_name}' not in donor list - aborting.")
        else:
            self.logger.info("Adding the donation to the database.")
            self.database.set(
                self.build_pattern(self.prefix_donation, clean_name, str_date),
                round(amount, 2)
            )

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
            if not query:
                self.logger.info("No donations yet, so no letters to send.")
            else:
                self.logger.info("Create dict of filenames and letter text.")
                for i in query:
                    letters[f'_{i}.txt'] = self.form_letter(i)
                self.logger.info(f"The letter filenames are: {letters.keys()}")
                for filename, text in letters.items():
                    self.logger.info(f"Text contents for {filename}:")
                    lines = text.splitlines()
                    with open(filename, 'w') as f:
                        for line in lines:
                            self.logger.info(f'Writing line: {line}')
                            f.write(line + '\n')
            self.logger.info(f"Change current directory back to '{cur_dir}''.")
            os.chdir(cur_dir)
            self.logger.info(f"Return folder with the letters: '{folder}'.")
            return folder

    def form_letter(self, name, donation_date=None):
        """
        Create a thank you form letter for a specific donation.

        :name:  The name of the donor to send the letter to.

        :donation_date:  The date of the donation. If this value isn't
                         specified, the form letter contains the most
                         recent gift amount.

        :return:  A string containing the filled-in form letter.
        """
        gift_sum = 0.0
        clean_name, clean_date = strip_text(name), strip_text(donation_date)
        self.logger.info(
            f"Creating form letter for '{clean_name}', with specified "
            f"donation date of '{clean_date}'.")
        donor_gift_keys = self.get_keys(
            self.build_pattern(self.prefix_donation, clean_name, '*')
        )
        if not donor_gift_keys:
            self.logger.info(f"No donations from {clean_name} yet.")
            return None

        donor_gift_keys.sort()  # 'YYYY-MM-DD' string sorts in calendar order
        donor_gift_count = len(donor_gift_keys)
        self.logger.info(
            f"Donor {clean_name} has made {donor_gift_count} donations.")
        self.logger.info(f"Donor {clean_name} has made these donations:")
        for key in donor_gift_keys:
            gift_date = key.split('_')[2]
            gift_amount = self.get_db_value(key)
            gift_sum += float(gift_amount)
            self.logger.info(
                f"\t{gift_date}: ${gift_amount} (cumulative: ${gift_sum})")

        if not donation_date:
            specific_gift_date = donor_gift_keys[-1].split('_')[2]
            specific_gift_amount = float(
                self.get_db_value(donor_gift_keys[-1])
            )
        else:
            specific_gift_date = clean_date
            specific_gift_key = self.build_pattern(
                self.prefix_donation, clean_name, clean_date
            )
            specific_gift_amount = float(self.get_db_value(specific_gift_key))
            if not specific_gift_amount:
                self.logger.info(
                    f"'{clean_name}' did not donate on '{clean_date}'.")
                return None

            self.logger.info(
                f"Send letter to {clean_name} about gift "
                f"on {specific_gift_date} for amount {specific_gift_amount}."
            )
            text = """\n\n\n
                    From:     Random Worthy Cause Foundation
                    To:       {0:s} (phone # {1:s})
                    Subject:  Your generous donation on {2:s}

                    Dear {0:s},

                    We want to express our gratitude for your donation of ${3:,.2f}
                    {4:s}to the Random Worthy Cause Foundation.  To show our
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
            if donor_gift_count > 1:
                self.logger.info(f"Also note total donations of ${gift_sum}.")
                extra = '(and total donations of ${0:,.2f} from {1:,d} gifts)' \
                        '\n'.format(gift_sum, donor_gift_count)
            donor_name_key = self.build_pattern(self.prefix_person, clean_name)
            phone_num = self.get_db_value(donor_name_key)
            return text.format(
                clean_name,
                phone_num,
                specific_gift_date,
                specific_gift_amount,
                extra
            )
