"""
This module defines the mailroom functionality using a peewee and
MongoDB database setup for the donor information.
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
        self.logger.info(f'Import donor database.')
        self.client = mailroom_db_login.login_mongodb_cloud()
        self.database = None
        self.persons = None
        self.donations = None
        self.connect_to_database()
        self.create_collections()
        self.client.close()

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
        self.database = self.client['mr']

    def create_collections(self):
        """Create the collections in the database."""
        self.logger.info("Creating the 'Persons' collection.")
        self.persons = self.database['Persons']
        self.logger.info("Creating the 'Donations' collection.\n")
        self.donations = self.database['Donations']

    def bulk_insert_donors(self, list_of_dicts):
        """Insert a bunch of donors into the Persons collection."""
        self.logger.info(f"Bulk inserting into the Persons collection.")
        self.logger.info(f"Here's the data: {list_of_dicts}.")
        for one_dict in list_of_dicts:
            self.persons.update_one(
                {
                    'person_name': one_dict['person_name']
                },
                {'$set': {
                    'person_name': one_dict['person_name'],
                    'ssn': one_dict['ssn']
                }},
                upsert=True
            )
        docs = self.persons.find()
        self.log_document_list(docs)

    def bulk_insert_gifts(self, list_of_dicts):
        """Insert a bunch of gifts into the Donations collection."""
        self.logger.info(f"Bulk inserting into the Donations collection.")
        self.logger.info(f"Here's the data: {list_of_dicts}.")
        donors = self.persons.distinct('person_name')
        donors.sort()
        self.logger.info(
            f"Donations must come from someone in the donor list: {donors}."
        )
        for one_dict in list_of_dicts:
            if one_dict['donor_name'] in donors:
                self.donations.update_one(
                    {
                        'donor_name': one_dict['donor_name'],
                        'donation_date': one_dict['donation_date']
                    },
                    {'$set': {
                        'donor_name': one_dict['donor_name'],
                        'donation_date': one_dict['donation_date'],
                        'donation_amount': one_dict['donation_amount']
                    }},
                    upsert=True
                )
        docs = self.donations.find()
        self.log_document_list(docs)

    def get_documents(self, collection, pattern={}, sorter={}):
        """
        Return sorted list of database documents matched by the pattern.

        :collection:  The collection object (for persons or donations).

        :sorter:  The collection field to sort on.

        :pattern:  The query specification string.

        :return:  The matching documents, sorted as specified.
        """
        self.logger.info(
            f"Scanning collection '{collection.name}' for query '{pattern}', "
            f"sorting on '{sorter}'."
        )
        result = collection.find(pattern).sort(sorter)
        self.log_document_list(result)
        return result

    def log_document_list(self, documents):
        """Log count and values of a MongoDB query document list."""
        if not documents:
            self.logger.info(f"No documents found.")
        else:
            num_docs = documents.count()
            self.logger.info(f"Found {num_docs} document(s):")
            for doc in documents:
                self.logger.info(f"\t{doc}")

    def get_donor_list(self):
        """
        Query the Persons collection for all potential donor names.

        :return:  The list of person-social security number dicts,
                  sorted by name.
        """
        self.logger.info("Query for donor names.")
        result = {}
        names = self.get_documents(self.persons, {}, 'person_name')
        if not names:
            self.logger.info("No donors found.")
        else:
            for doc in names:
                result[doc['person_name']] = doc['ssn']
        self.logger.info(f"There are {len(result)} donors: {result}.")
        return result

    def get_donors_who_donated(self):
        """
        Return the donors who have actually given already.

        :return:  The list of persons who've given, sorted by name.
        """
        self.logger.info("Query for donors who've actually donated.")
        names = self.donations.distinct('donor_name')
        if not names:
            self.logger.info("No donors found.")
        else:
            names.sort()
            self.logger.info(f"Number of generous donors: {len(names)}")
            self.logger.info(f"The generous donors are: {names}.")
        return names

    def get_donor_info(self, name):
        """
        Query the Persons collection for a donor's personal information.
        Right now the only available data is the name and social
        security number (SSN).

        :name:  A string containing the donor name to retrieve.

        :return:  A dict containing the donor name and the donor SSN.
        """
        clean_name = strip_text(name)
        self.logger.info(f"Get information about donor '{clean_name}'.")
        result = {}
        info = self.persons.find_one({'person_name': clean_name})

        if info:
            result = {
                'person_name': info['person_name'],
                'ssn': info['ssn']
            }
        self.logger.info(f"Donor info: {result}")
        return result

    def delete_data(self):
        """Delete all data in the database collections."""
        # Delete Donations collection data
        self.logger.info(
            "Number of documents in the Donations collection: "
            f"{self.donations.count_documents({})}."
        )
        self.logger.info("Delete all data from the Donations collection.")
        try:
            self.donations.delete_many({})
        except Exception as exc:
            self.logger.info(exc)
            self.logger.info('Donations collection deletion unsuccessful.')
        else:
            self.logger.info(
                "Number of documents in the Donations collection now: "
                f"{self.donations.count_documents({})}."
            )
            # Delete Persons collection data
            self.logger.info(
                "Number of documents in the Persons collection: "
                f"{self.persons.count_documents({})}."
            )
            self.logger.info("Delete all data from the Persons collection.")
            try:
                self.persons.delete_many({})
            except Exception as exc:
                self.logger.info(exc)
                self.logger.info('Persons collection deletion unsuccessful.')
            else:
                self.logger.info(
                    "Number of documents in the Persons collection now: "
                    f"{self.persons.count_documents({})}."
                )

    def delete_donor_data(self, name):
        """
        Delete a donor's donations from the Donations collection and the
        donor from the Persons collection.
        """
        # Delete Donations collection data from the donor
        clean_name = strip_text(name)
        self.logger.info(
            "Number of documents in the Donations collection: "
            f"{self.donations.count_documents({})}."
        )
        self.logger.info(f"Deleting donations from '{clean_name}'.")
        try:
            self.donations.delete_many({'donor_name': clean_name})
        except Exception as exc:
            self.logger.info(exc)
        else:
            self.logger.info(
                "Number of documents in the Donations collection now: "
                f"{self.donations.count_documents({})}."
            )

            # Delete donor from Persons collection
            self.logger.info(
                "Number of documents in the Persons collection: "
                f"{self.persons.count_documents({})}."
            )
            self.logger.info(f"Deleting '{clean_name}' from donor list.")
            try:
                self.persons.delete_one({'person_name': clean_name})
            except Exception as exc:
                self.logger.info(exc)
            else:
                self.logger.info(
                    "Number of documents in the Persons collection now: "
                    f"{self.persons.count_documents({})}."
                )

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
        pipe = [
            {'$match': {'donor_name': {'$ne': ''}}},
            {'$group': {
                '_id': '$donor_name',
                'gifts': {'$sum': 1},
                'total': {'$sum': '$donation_amount'},
                'average': {'$avg': '$donation_amount'},
                'largest': {'$max': '$donation_amount'},
                'smallest': {'$min': '$donation_amount'}
            }},
            {'$sort': {'_id': 1}}
        ]
        query = self.donations.aggregate(pipe)
        self.logger.info(f"Query is: {query}.")

        data = []
        for doc in query:
            data.append(
                (
                    doc['_id'], doc['gifts'], doc['total'],
                    doc['average'], doc['largest'], doc['smallest']
                )
            )
            self.logger.info(f"Added ({data[-1]}).")
        self.logger.info(f"Total donors: {len(data)}.")

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
        for doc in data:
            row_string = data_str.format(*doc)
            self.logger.info(row_string)
            print(row_string)
        print('\n')

    def add_or_update_donor(self, donor, ssn):
        """
        Add or update a donor's SSN in the Persons collection.

        :donor:  The name of the donor to add or update.

        :ssn:  The new or existing donor's social security number.

        :return:  The old document, if it exists; otherwise None.
        """
        clean_name, clean_ssn = strip_text(donor), strip_text(ssn)
        old_document = None
        self.logger.info(
            f"Add or update person '{clean_name}' "
            f"with SS #{clean_ssn} to the Persons collection.")
        if not clean_name or not clean_ssn:
            print("Exiting - must enter a non-null donor name and SS #.")
        else:
            try:
                old_document = self.persons.find_one_and_update(
                    {'person_name': clean_name},
                    {'$set': {'ssn': clean_ssn}},
                    upsert=True
                )
            except Exception as exc:
                self.logger.info(exc)
                self.logger.info('Donor change/addition unsuccessful.')
        if old_document:
            self.logger.info(
                f"Update made to '{clean_name}', overwriting the previous SSN "
                "of '{clean_ssn}'.")
        return old_document

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
        clean_name, clean_date = strip_text(donor), strip_text(date)
        self.logger.info(
            f"Donor '{clean_name}' giving '{amount}' on '{clean_date}'.")
        if not donor:
            self.logger.info("Donor name is empty.")
            raise ValueError("No donor name specified.")
        try:
            cnv_date = datetime.datetime.strptime(clean_date, "%Y-%m-%d")
            str_date = datetime.date.isoformat(cnv_date)
        except ValueError:
            self.logger.info(f"Problem with date format in '{clean_date}'.")
            raise ValueError(f"'{date}' is an invalid date format.")

        try:
            amount = float(amount)
        except ValueError:
            self.logger.info(f"Specified gift amount must be a number.")
            raise ValueError("A number was not specified for the gift amount.")
        if amount < 0.005:
            self.logger.info(f"Gift of '{amount}' must be at least one penny.")
            raise ValueError(
                f"'{amount}' is invalid - must be at least $0.01.")

        try:
            old_document = self.donations.find_one_and_update(
                {'donor_name': clean_name, 'donation_date': str_date},
                {'$set': {'donation_amount': round(amount, 2)}},
                upsert=True
            )
        except Exception as exc:
            self.logger.info(exc)
            self.logger.info('Donation unsuccessful.')
        else:
            self.logger.info('Successfully added donation.')
            if old_document:
                self.logger.info(
                    f"Donor '{clean_name}' on '{clean_date}' - old amount "
                    f"of '{old_document['donation_amont']}' replaced "
                    f"with '{amount}'."
                )
            return old_document

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
                    with open(filename, 'w') as fobj:
                        for line in lines:
                            self.logger.info(f'Writing line: {line}')
                            fobj.write(line + '\n')
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
        clean_name, clean_date = strip_text(name), strip_text(donation_date)
        gift_dict, specific_gift_date, specific_gift_amount = {}, None, 0.0
        self.logger.info(f"Creating form letter for {clean_name}.")
        query_all = self.get_documents(
            self.donations,
            {'donor_name': clean_name},
            [('donor_name', 1), ('donation_date', 1)]
        )

        for doc in query_all:
            gift_dict[doc['donation_date']] = round(
                float(doc['donation_amount']), 2)
            self.logger.info(f"'{doc['donation_date']}' just assigned "
                             f"to '{gift_dict[doc['donation_date']]}'.")
        if not gift_dict:
            self.logger.info(f"No donations from {clean_name} yet.")
            return ''
        self.logger.info(
            f"Donor '{clean_name}' has made {len(gift_dict)} gifts total: "
            f"{gift_dict}")

        if not clean_date:
            specific_gift_date = max(gift_dict.keys())
        elif clean_date in gift_dict.keys():
            specific_gift_date = clean_date
        else:
            self.logger.info(f"No donation from {clean_name} on {clean_date}.")
            return ''
        specific_gift_amount = gift_dict[specific_gift_date]
        gift_sum = sum(gift_dict.values())
        gift_count = len(gift_dict)

        text = """\n\n\n
                From:     Random Worthy Cause Foundation
                To:       {0:s} (SS # {1:s})
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
        if gift_count > 1:
            self.logger.info(f"Also note total donations of ${gift_sum}.")
            extra = '(and total donations of ${0:,.2f} from {1:,d} gifts)' \
                    '\n'.format(gift_sum, gift_count)
        ssn = self.get_donor_info(clean_name)['ssn']
        return text.format(
            clean_name,
            ssn,
            specific_gift_date,
            specific_gift_amount,
            extra
        )
