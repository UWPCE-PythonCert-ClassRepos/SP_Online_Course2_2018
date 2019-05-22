import logging
import utilities
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log = utilities.configure_logger('default', '../logs/donors_neo4j.log')


class Group:
    """This Class will be used to query the database and return the results
    of the required queries."""

    def __init__(self, driver):
        self.driver = driver

    def search(self, person):
        """Return None if donor is not in database."""

        try:
            logger.debug('Trying to count number of donations.')
            with self.driver.session() as session:
                cyph = """MATCH (p:Person {donor: '%s'})
                    RETURN p.donor as donor, p.donations as donations""" % person
                result = session.run(cyph)
                record = result.single()
                if record is None:
                    logger.debug('Could not find the donor.')
                    return None
                else:
                    log.debug(f'Found {record["donor"]}')
                    return record['donor']
        except Exception as e:
            logger.debug(f'Error searching for = {person}')
            logger.debug(e)
        finally:
            print(f'All done searching donors for {person}.')

    def print_donors(self):
        # This prints the list of donors

        try:
            donor_list = []
            with self.driver.session() as session:
                cyph = """MATCH (p:Person)
                    RETURN p.donor as donor, p.donations as donations"""
                result = session.run(cyph)
                for record in result:
                    donor_list.append(record['donor'])
                    print(record['donor'])

        except Exception as e:
            logger.debug(f'Error printing donors.')
            logger.debug(e)
            logger.debug('Failed to print a list of donors.')
        finally:
            logger.debug('database closes')
            return donor_list

    def summary(self):
        """Create a new dictionary with Total, number of donations,
        and average donation amount"""
        donor_summary = {}
        individual = Individual(self.driver)

        try:
            with self.driver.session() as session:
                cyph = """MATCH (p:Person)
                    RETURN p.donor as donor, p.donations as donations"""
                result = session.run(cyph)
                for record in result:
                    donor_summary[record['donor']] = \
                        [individual.sum_donations(record['donor']),
                         individual.number_donations(record['donor']),
                         individual.avg_donations(record['donor'])]

        except Exception as e:
            logger.debug(f'Error creating database summary.')
            logger.debug(e)
            logger.debug('Failed to iterate through database '
                         'to create a summary.')
        finally:
            logger.debug('database closes')
            return donor_summary

    @staticmethod
    def column_name_width(donor_summary):
        # creates a list of keys
        name_list = list(donor_summary.keys())
        name_wi = 11  # Establish minimum column width
        for i in name_list:
            if len(i) > name_wi:
                name_wi = (len(i))  # width of name column
        return name_wi

    @staticmethod
    def column_total_width(donor_summary):
        tot_wi = 12
        for name, summary in donor_summary.items():
            if len(str(summary[0])) > tot_wi:
                # width of total column
                tot_wi = (len(str(summary[0]))) + 3
                # width of number of donations column
        return tot_wi

    @staticmethod
    def column_average_width(donor_summary):
        ave_wi = 12
        for name, summary in donor_summary.items():
            if len(str(summary[2])) > ave_wi:
                # width of total column
                ave_wi = (len(str(summary[2]))) + 3
                # width of number of donations column
        return ave_wi

    @staticmethod
    def column_number_width(donor_summary):
        num_wi = 12
        for name, summary in donor_summary.items():
            if len(str(summary[1])) > num_wi:
                # width of total column
                num_wi = (len(str(summary[1]))) + 3
                # width of number of donations column
        return num_wi

    @staticmethod
    def sort_list(donor_summary):
        list_sorted = sorted(donor_summary,
                             key=donor_summary.__getitem__, reverse=True)
        return list_sorted

    def report(self):
        """Return a report on all the donors"""
        donor_summary = self.summary()
        name_wi = Group.column_name_width(donor_summary)
        tot_wi = Group.column_total_width(donor_summary)
        num_wi = Group.column_number_width(donor_summary)
        ave_wi = Group.column_average_width(donor_summary)

        list_sorted = Group.sort_list(donor_summary)

        rows = ['\n''A summary of your donors donations:',
                f"{'Donor Name':{name_wi}}| {'Total Given':^{tot_wi}}| "
                f"{'Num Gifts':^{num_wi}}| {'Average Gift':^{ave_wi}}",
                f"{'-':-^{(name_wi+tot_wi+ave_wi+num_wi+8)}}"]

        for key in list_sorted:
            temp = donor_summary[key]
            rows.append(f"{key:{name_wi}}${temp[0]:{tot_wi}.2f}"
                        f"{temp[1]:^{num_wi}}   "
                        f"${temp[2]:>{ave_wi}.2f}")
        return '\n'.join(rows)

    def letters(self):
        """Send letters to everyone base on their last donation amount."""
        individual = Individual(self.driver)
        try:
            with self.driver.session() as session:
                cyph = """MATCH (p:Person)
                    RETURN p.donor as donor, p.donations as donations"""
                result = session.run(cyph)
                for record in result:
                    logger.debug(f'{record["donor"]}')
                    letter = f'Dear {record["donor"]}, ' \
                            f'thank you so much for your ' \
                            f'last contribution of ' \
                            f'${individual.last_donation(record["donor"]):.2f}! ' \
                            f'You have contributed a total of $' \
                            f'{individual.sum_donations(record["donor"]):.2f}, ' \
                            f'and we appreciate your support!'
                # Write the letter to a destination
                    with open(record["donor"] + '.txt', 'w') as to_file:
                        to_file.write(letter)
        except Exception as e:
            logger.debug(f'Error writing letters to everyone.')
            logger.debug(e)
        finally:
            logger.debug('Done writing letters.')


class Individual:
    """Connects to neo4j and works with individual data 'donor' and
     a list of 'donations'.
     """
    def __init__(self, driver):
        #self.db = client_path
        self.driver = driver


    def add_donation(self, person, contribution):

        log.debug('In add_donation')
        try:
            # first look to see if the donor exists
            log.debug('Search for donor.')
            with self.driver.session() as session:
                cyph = """MATCH (p:Person {donor: '%s'})
                    RETURN p.donor as donor, p.donations as donations""" % (person)
                result = session.run(cyph)
                record = result.single()
                # if person does not exist in the database, create a new entry
                log.debug(f'{record} is record.')
                if record is None:
                    log.debug('Inserting a new donor')
                    cyph = "CREATE (n:Person {donor:'%s', donations:[%s]})" \
                        % (person, contribution)
                    session.run(cyph)

                else:
                    # if person does exist, update the donation
                    log.debug('in else......')
                    log.debug(f'{result} is result')
                    log.debug(f'{record} is record')
                    log.debug(f'{record["donor"]} is record["donor"].')

                    # create a list to store the donations temporarily
                    donations = record['donations']
                    log.debug(f'donations are {donations}')

                    # append new donation to list
                    donations.append(contribution)
                    log.debug('Just added a donation')
                    log.debug(f' Donor is {record["donor"]}, Donations are {donations}')

                    # Set the new list of donations back into database
                    cyph = """MATCH (p:Person {donor: '%s'})
                              SET p.donations= %s
                              """ % (person, donations )
                    session.run(cyph)

        except Exception as e:
            logger.debug(f'Error creating = {person}')
            logger.debug(e)
            logger.debug('Failed to add new donor.')
        finally:
            print('All done adding donor contribution')

    def number_donations(self, name):

        try:
            logger.debug('Trying to count number of donations.')
            with self.driver.session() as session:
                cyph = """MATCH (p:Person {donor: '%s'})
                    RETURN p.donor as donor, p.donations as donations""" % (name)
                result = session.run(cyph)
                record = result.single()
                if record is None:
                    return None
                donations = record['donations']
                return int(len(donations))

        except Exception as e:
            logger.debug(f'Error counting # of donations.')
            logger.debug(e)
        finally:
            logger.debug(f'Returning the # of donations made by {name}')


    def sum_donations(self, name):

        try:
            logger.debug(f'Summing all the donations by {name}.')
            with self.driver.session() as session:
                cyph = """MATCH (p:Person {donor: '%s'})
                    RETURN p.donor as donor, p.donations as donations""" % (name)
                result = session.run(cyph)
                record = result.single()
                if record is None:
                    return None
                sum_donations = sum(record['donations'])
                return sum_donations

        except Exception as e:
            logger.debug(f'Error counting # of donations.')
            logger.debug(e)
        finally:
            logger.debug(f'Returning the # of donations made by {name}')



    def avg_donations(self, name):
        return self.sum_donations(name)/self.number_donations(name)


    def last_donation(self, name):
        try:
            logger.debug(f'Trying to find the last record of {name}.')
            with self.driver.session() as session:
                cyph = """MATCH (p:Person {donor: '%s'})
                    RETURN p.donor as donor, p.donations as donations""" % (name)
                result = session.run(cyph)
                record = result.single()
                if record is None:
                    return None
                logger.debug(f'Finding the last donation made by {name}')
                donation_list = record['donations']
                return donation_list[-1]

        except Exception as e:
            logger.debug(f'Error finding last donation.')
            logger.debug(e)
        finally:
            logger.debug(f'Returning the last donation made by {name}.')


    @staticmethod
    def thank_you(person, contribution):
        """Add a donation to a donors records and print a report."""
        return ('Thank you so much for the generous gift of ${0:.2f}, {1}!'
                .format(contribution, person))

    def delete_donor(self, name):
        try:
            logger.debug(f'Trying to delete {name}.')
            with self.driver.session() as session:
                cyph = """MATCH (p:Person {donor: '%s'})
                        DELETE p
                        """ % name
                session.run(cyph)

        except Exception as e:
            logger.debug(f'Error deleting {name}')
            logger.debug(e)
            logger.debug('Failed to delete donor.')
        finally:

            logger.debug(f'Deletion of {name} successful.')

    @staticmethod
    def donor_verification(path, name):
        """Before entering a new  donor or donation into the database,
         verify that the donor's email, telephone, and address
         of the donor are correct. Add or revise data on record."""

        print(f'Check the information on file for {name}.')
        print(f"{name}'s last name is {path.lindex(name,0)}")
        print(f"{name}'s telephone is {path.lindex(name, 1)}")
        print(f"{name}'s email is {path.lindex(name, 2)}")
        return [path.lindex(name, 0),
                path.lindex(name, 1),
                path.lindex(name, 2)]

    @staticmethod
    def update_last_name(path, name, new_last_name):
        """Update donor's last name in REDIS cache"""
        path.lset(name, 0, new_last_name)
        print(f'Check the information on file for {name}.')
        print(f"{name}'s last name is {path.lindex(name,0)}")
        print(f"{name}'s telephone is {path.lindex(name, 1)}")
        print(f"{name}'s email is {path.lindex(name, 2)}")
        return [path.lindex(name, 0),
                path.lindex(name, 1),
                path.lindex(name, 2)]

    @staticmethod
    def update_telephone(path, name, new_telephone):
        """Update donor's last name in REDIS cache"""
        path.lset(name, 1, new_telephone)
        print(f'Check the information on file for {name}.')
        print(f"{name}'s last name is {path.lindex(name,0)}")
        print(f"{name}'s telephone is {path.lindex(name, 1)}")
        print(f"{name}'s email is {path.lindex(name, 2)}")
        return [path.lindex(name, 0),
                path.lindex(name, 1),
                path.lindex(name, 2)]

    @staticmethod
    def update_email(path, name, new_email):
        """Update donor's last name in REDIS cache"""
        path.lset(name, 2, new_email)
        print(f'Check the information on file for {name}.')
        print(f"{name}'s last name is {path.lindex(name,0)}")
        print(f"{name}'s telephone is {path.lindex(name, 1)}")
        print(f"{name}'s email is {path.lindex(name, 2)}")
        return [path.lindex(name, 0),
                path.lindex(name, 1),
                path.lindex(name, 2)]

    @staticmethod
    def redis_add_new(path, name, last_name, tele, email):
        """Update donor's last name in REDIS cache"""
        path.delete(name)
        path.rpush(name, last_name)
        path.rpush(name, tele)
        path.rpush(name, email)
        print(f'Confirm the information on file for {name}.')
        print(f"{name}'s last name is {path.lindex(name,0)}")
        print(f"{name}'s telephone is {path.lindex(name, 1)}")
        print(f"{name}'s email is {path.lindex(name, 2)}")
        return [path.lindex(name, 0),
                path.lindex(name, 1),
                path.lindex(name, 2)]
