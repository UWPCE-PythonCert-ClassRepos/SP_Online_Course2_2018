"""
This module defines the mailroom functionality using a Neo4J
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
        """Set up logging & manage the Neo4J driver and its sessions."""
        self.logger = self.set_up_logging()
        self.logger.info('This is the mailroom donor database '
                         'functionality, implemented using Neo4J.')
        self.driver = None
        self.session = None
        self.connect_to_driver()
        self.open_driver_session()

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

    def connect_to_driver(self):
        """Connect to the Neo4J database driver."""
        self.logger.info("Connect to the Neo4J database driver.")
        self.driver = mailroom_db_login.login_neo4j_cloud()

    def disconnect_from_driver(self):
        """Disconnect from the Neo4J database driver."""
        self.logger.info("Disconnect from the Neo4J database driver.")
        self.driver.close()

    def open_driver_session(self):
        """Open a session with the Neo4J driver."""
        self.logger.info("Open a Neo4J driver session.")
        self.session = self.driver.session()

    def close_driver_session(self):
        """Close the Neo4J database driver session."""
        self.logger.info('Close the database driver session.')
        self.session.close()

    def bulk_insert_donors(self, list_of_dicts):
        """Insert a bunch of donors under the Person label."""
        self.logger.info(f"Bulk inserting under the Person label.")
        self.logger.info(f"Here's the data: {list_of_dicts}.")
        for one_dict in list_of_dicts:
            clean_dict = {}
            clean_dict['person_name'] = strip_text(one_dict['person_name'])
            clean_dict['ssn'] = strip_text(one_dict['ssn'])
            self.logger.info(f"Merge create Person vertex for: {clean_dict}.")
            cypher = """
                MERGE (p:Person {person_name: '%(person_name)s'})
                ON MATCH SET p.ssn = '%(ssn)s'
                ON CREATE SET p.ssn = '%(ssn)s'
            """ % clean_dict
            self.log_cypher_run(cypher)

    def bulk_insert_gifts(self, list_of_dicts):
        """Insert a bunch of gifts under the Donation label."""
        self.logger.info(f"Bulk inserting under the Donation label.")
        self.logger.info(f"Will also relate them to Person vertices.")
        self.logger.info(f"Here's the data: {list_of_dicts}.")
        for one_dict in list_of_dicts:
            clean_dict = {}
            clean_dict['donor_name'] = strip_text(one_dict['donor_name'])
            clean_dict['donation_date'] = strip_text(one_dict['donation_date'])
            clean_dict['donation_amount'] = float(one_dict['donation_amount'])
            self.logger.info(
                f"Merge donation and relate to person for: {clean_dict}.")
            cypher = """
                MATCH (p:Person {person_name: '%(donor_name)s'})
                MERGE (p)-[gives:GIVES]->(d:Donation
                    {
                        donor_name: '%(donor_name)s',
                        donation_date: '%(donation_date)s'
                    }
                )
                ON MATCH SET d.donation_amount = %(donation_amount)s
                ON CREATE SET d.donation_amount = %(donation_amount)s
                RETURN d.donor_name as donor_name,
                       d.donation_date as donation_date,
                       d.donation_amount as donation_amount
            """ % clean_dict
            self.log_cypher_run(cypher)

    def log_cypher_run(self, cypher_string):
        """
        Log the cypher string and return the executed cypher results.
        """
        self.logger.info(f"Running this cypher: {cypher_string}")
        result = self.session.run(cypher_string)
        return result

    def log_iterator_results(self, rows):
        """
        Log count and values of Neo4J cypher result rows, and convert
        the results from an iterator to an iterable (and return them).

        :rows:  The result of a Neo4J cypher.

        :return:  A list of each document (in dict form).
        """
        result = []
        if not rows:
            self.logger.info(f"No cypher rows found.")
        else:
            self.logger.info(f"Found the following row(s):")
            for row in rows:
                self.logger.info(f"\t{row}")
                self.logger.info(f"\tKeys: {row.keys()}")
                self.logger.info(f"\tValues: {row.values()}")

                row_dict = {}
                for key, val in row.items():
                    row_dict[key] = val
                result.append(row_dict)
            self.logger.info(f"There are {len(result)} row(s).")
        self.logger.info(f"Here's the returned result: {result}.")
        return result

    def get_donor_list(self):
        """
        Cypher the Person vertices for all potential donor names.

        :return:  The dict of person key /social security number values.
        """
        self.logger.info("Cypher for donor names.")
        cypher = """
            MATCH (p:Person)
            RETURN p.person_name as person_name,
                   p.ssn as ssn
            ORDER BY p.person_name
        """
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        return_dict = {}
        for row in ite:
            return_dict[row['person_name']] = row['ssn']
        return return_dict

    def get_donors_who_donated(self):
        """
        Return the donors who have actually given already.

        :return:  The list of persons who've given, sorted by name.
        """
        self.logger.info("Cypher f/the names of donors who've already given.")
        cypher = """
            MATCH (p:Person)-[:GIVES]->(d:Donation)
            RETURN DISTINCT p.person_name as person_name
            ORDER BY person_name
        """
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        donors_as_list = map(lambda x: x['person_name'], ite)
        return donors_as_list

    def get_single_donor_info(self, name):
        """
        Cypher Person vertices for a donor's personal information.
        Right now the only available data is the name and social
        security number (SSN).

        :name:  A string containing the donor name to retrieve.

        :return:  A dict containing the donor name and the donor SSN.
        """
        self.logger.info("Cypher for a person's information.")
        clean_name = strip_text(name)
        cypher = """
            MATCH (p:Person {person_name: '%s'})
            RETURN p.person_name as person_name,
                   p.ssn as ssn
        """ % clean_name
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        return_dict = {}
        for row in ite:  # Should get only be one row but still needs iteration
            return_dict['person_name'] = row['person_name']
            return_dict['ssn'] = row['ssn']
        return return_dict

    def delete_data(self):
        """Delete all data in the graph database."""
        self.logger.info("Delete all data in the database.")

        # Delete Donation vertices
        cypher = "MATCH (d:Donation) RETURN d"
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        if ite:
            cypher = "MATCH (d:Donation) DETACH DELETE d"
            self.log_cypher_run(cypher)

        # Delete Person vertices
        cypher = "MATCH (p:Person) RETURN p"
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        if ite:
            cypher = "MATCH (p:Person) DETACH DELETE p"
            self.log_cypher_run(cypher)

    def delete_donor_data(self, name):
        """
        Delete a donor's donations from the Donation vertices and the
        Person vertex for the person. Also delete any connecting edges.
        """
        clean_name = strip_text(name)
        self.logger.info(
            f"Delete donation and person entries for {clean_name}.")

        # Delete Donation vertices for the donor
        cypher = """
            MATCH (d:Donation)<-[:GIVES]-(p:Person {person_name: '%s'})
            RETURN d
        """ % clean_name
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        if ite:
            cypher = """
                MATCH (d:Donation)<-[:GIVES]-(p:Person {person_name: '%s'})
                DETACH DELETE d
            """ % clean_name
            self.log_cypher_run(cypher)

        # Delete the Person vertex for the donor
        cypher = "MATCH (p:Person {person_name: '%s'}) RETURN p" % clean_name
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        if ite:
            cypher = """
                MATCH (p:Person {person_name: '%s'})
                DETACH DELETE p
            """ % clean_name
            self.log_cypher_run(cypher)

    def create_gift_report(self):
        """
        Print out donation statistics for the entire donor roster.

        :return:  None.
        """
        self.logger.info('Print out donation stats for all donors.')
        cypher = """
            MATCH (d:Donation)<-[:GIVES]-(p:Person)
            RETURN p.person_name as donor_name,
                   count(d) as gifts,
                   sum(d.donation_amount) as total,
                   avg(d.donation_amount) as average,
                   max(d.donation_amount) as largest,
                   min(d.donation_amount) as smallest
            ORDER BY p.person_name
        """
        self.logger.info(f"Cypher spec is: {cypher}.")
        result = self.log_cypher_run(cypher)

        # Put the 6 data points into a tuple in display column order
        data = []
        for val in result:
            self.logger.info(f"\tKeys: {val.keys()}")
            self.logger.info(f"\tValues: {val.values()}")
            data.append(
                (
                    val['donor_name'], val['gifts'], val['total'],
                    val['average'], val['largest'], val['smallest']
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
        for val in data:
            row_string = data_str.format(*val)
            self.logger.info(row_string)
            print(row_string)
        print('\n')

    def add_or_update_donor(self, donor, ssn):
        """
        Add or update a donor's SSN in the Person vertex.

        :donor:  The name of the donor to add or update.

        :ssn:  The new or existing donor's social security number.

        :return:  None.
        """
        clean_name, clean_ssn = strip_text(donor), strip_text(ssn)
        self.logger.info(
            f"Merge create Person vertex f/'{clean_name}' (SSN {clean_ssn}).")
        cypher = """
            MERGE (p:Person {person_name: '%s'})
            ON MATCH SET p.ssn = '%s'
            ON CREATE SET p.ssn = '%s'
        """ % (clean_name, clean_ssn, clean_ssn)
        self.log_cypher_run(cypher)

    def add_new_amount(self, donor, amount, date):
        """
        Add a new donation with the specified donor name and amount.
        If the donor is not currently in the donation history, a new
        entry is added.

        :name:  The name of the donor.

        :amount:  The amount given.

        :date:  The date of the donation, in YYYY-MM-DD format.

        :return:  The new Donation vertex.
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
            clean_amount = float(amount)
        except ValueError:
            self.logger.info(f"Specified gift amount must be a number.")
            raise ValueError("A number was not specified for the gift amount.")
        if clean_amount < 0.005:
            self.logger.info(f"Gift of '{amount}' must be at least one penny.")
            raise ValueError(
                f"'{amount}' is invalid - must be at least $0.01.")

        cypher = """
            MATCH (p:Person {person_name: '%s'})
            MERGE (d:Donation {donor_name: '%s', donation_date: '%s'})
            ON MATCH SET d.donation_amount = %s
            ON CREATE SET d.donation_amount = %s
            CREATE (p)-[gives:GIVES]->(d)
            RETURN d.donor_name as donor_name,
                   d.donation_date as donation_date,
                   d.donation_amount as donation_amount
        """ % (clean_name, clean_name, str_date, clean_amount, clean_amount)
        result = self.log_cypher_run(cypher)
        ite = self.log_iterator_results(result)
        if not ite:
            self.logger.info("Couldn't add the donation, probably because "
                             f"'{clean_name}' isn't a Person vertex.")
        else:
            self.logger.info(f"Donation successfully added: {ite}.")
        return ite

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
            real_donors = self.get_donors_who_donated()
            if not real_donors:
                self.logger.info("No donations yet, so no letters to send.")
            else:
                self.logger.info("Create dict of filenames and letter text.")
                for i in real_donors:
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
        self.logger.info(f"Creating form letter for '{clean_name}' "
                         f"for their gift on '{clean_date}'.")

        cypher = """
            MATCH (d:Donation)<-[:GIVES]-(p:Person {person_name: '%s'})
            RETURN d.donation_date as donation_date,
                   d.donation_amount as donation_amount
        """ % clean_name
        rows = self.log_cypher_run(cypher)

        for row in rows:
            gift_dict[row['donation_date']] = round(
                float(row['donation_amount']), 2)
            self.logger.info(f"'{row['donation_date']}' just assigned "
                             f"to '{gift_dict[row['donation_date']]}'.")
        if not gift_dict:
            self.logger.info(f"No donations from '{clean_name}' yet.")
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
        ssn = self.get_single_donor_info(clean_name)['ssn']
        return text.format(
            clean_name,
            ssn,
            specific_gift_date,
            specific_gift_amount,
            extra
        )
