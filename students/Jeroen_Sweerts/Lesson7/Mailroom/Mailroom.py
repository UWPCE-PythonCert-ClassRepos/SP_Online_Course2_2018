from mailroom_database import *

import logging
from peewee import *

class Donor():
    logger = logging.getLogger(__name__)
    def __init__(self, name=None):
        self._name = name
        self._donations = []

    @property
    def name(self):
        """Property for the donor's name."""
        return self._name

    @name.setter
    def name(self, val):
        """Setter for the donor's name."""
        self._name = val

    @property
    def donations(self):
        """Property for the donor's list of donations."""
#         return self._donations
        query = Donation_Table.select().where(Donation_Table.donor == self._name).order_by(Donation_Table.donation_amt.desc())
        return f"\n{'-'*10} Donations by {self._name} {'-'*10}\n" + '\n'.join(["{:.2f}".format(donation.donation_amt) for donation in query])

    @donations.setter
    def donations(self, val):
        """Setter for the donor's list of donations."""
        self._donations = val

    def add_donation(self, donation):
        """
        Add a new donation entry for this donor to the database
        :param donation: the new donation amount        """
        
        try:
            with database.transaction():
                new_donation = Donation_Table.create(
                    donor = Donor_Table.get(Donor_Table.full_name == self.name),
                    donation_amt = int(donation))                    
                new_donation.save()
        except Exception as e:
            logger.error(f"Failed to add donation {donation} for {self._name}", e)

class Donor_Collection():
    logger = logging.getLogger(__name__)
    
    def __init__(self):
        self._donors = []
        for donor in Donor_Table.select():
            self._donors.append(Donor(donor.full_name))

    @property
    def donors(self):
        """Property for the Donor_Collection's list of donors."""
        return self._donors

    @donors.setter
    def donors(self, val):
        """Setter for the Donor_Collection's list of donors."""
        self._donors = val

    def add_donor(self, donor):
        """Add a new donor to the list."""
        self._donors.append(donor)
        
    def find_donor(self, name):
        """
        Find a donor by name
        :param name: the name of the donor to search for
        :return: The donor if found else None
        """
        for donor in self._donors:
            if donor.name == name:
                return donor
        return None
    
    def donate(self, name, donation):
        """Add a donation to the list of donations for a specific donor.
        If the donor doesn't exist yet, then add it to the donor collection first."""
        donor = self.find_donor(name)
        if donor is None:
            donor = Donor(name)
            try:
                with database.transaction():
                    new_donor = Donor_Table.create(
                        full_name = name)
                    new_donor.save()
                self.add_donor(donor)
            except Exception as e:
                logger.error(f"Failed to add new donor {name} to database", e)
        donation = int(donation)
        donor.add_donation(donation)
        

    def createfile(self):
#         """create .txt file containing thank you letter for each person who made a donation"""
        query = Donation_Table.select(Donation_Table.donor,fn.SUM(Donation_Table.donation_amt).alias('sum'),fn.COUNT(Donation_Table.donation_amt).alias('count')).join(Donor_Table).group_by(Donation_Table.donor)
        for donation in query:
            d = {'name': donation.donor.full_name,'donation':donation.sum}
            outfile = open(donation.donor.full_name +'.txt', 'w')
            outfile.write("Dear {name} , \n\n".format(**d))
            outfile.write("\t Thank you very much for your generous donation of ${donation}. \n\n".format(**d))
            outfile.write("\t It will be put to very good use. \n\n")
            outfile.write("\t\t Sincerely, \n")
            outfile.write("\t\t   -The Team \n")
            outfile.close()
            

    def create_report(self):
        """For all donors in the Donor_Collection class, write a report containing
        the donor's name, how much he gave in total, how many gifts the donor made and
        how much the donor gave on average."""
        print(f'{"Donor Name":20s} {"|  Total Given":20s} {"|  Num Gifts  |":20s} {"Average Gift":20s}')
        print(f'{"-"*76}')

        query = Donation_Table.select(Donation_Table.donor,fn.SUM(Donation_Table.donation_amt).alias('sum'),fn.COUNT(Donation_Table.donation_amt).alias('count')).join(Donor_Table).group_by(Donation_Table.donor)             
        [print(f'{donation.donor.full_name:20s} ${donation.sum:20.2f} {donation.count:13d}${donation.sum/donation.count:20.2f}') for donation in query]



def thankyou(donordict):
    """If the user types ‘list’, show them a list of the donor names and re-prompt
    If the user types a name not in the list, add that name to the data structure
    and use it.
    If the user types a name in the list, use it.
    Once a name has been selected, prompt for a donation amount.
    """
    while True:
        name = input('Please enter a name or type "list" to see a list of names > ')
        if name == 'list':
            query = Donor_Table.select()
            for donor in query:
              print(donor.full_name)
        else:
            break

    success = False
    while not success:
        donation = input('Please enter a donation amount > ')
        try:
            donordict.donate(name, donation)
            success = True
        except Exception as err:
            print(err.args[0])
            success = False

    d = {'name':name, 'donation':donation}
    print("Dear {name} , thank you very much for your generous donation of {donation}. Looking forward receiving even more money next time.".format(**d))


def report(donordict):
    """call the create_report() method of the Donor_Collection class
    and write report with summary of the donations of all donors."""
    donordict.create_report()

def thankyoueveryone(donordict):
    """call the createfile() method of the Donor_Collection class
    and write thank you letter for each donor."""
#     [donordict.createfile(name) for name in self.donors]
    donordict.createfile()

def fill_db():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
        
    database = SqliteDatabase('donations.db')
    donors = [('papa', [100, 5, 15]), ('mama', [12, 200, 2, 66]),
              ('bompa', [1000]), ('bobonne', [500, 500]),
              ('onbekende', [1000000])]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor, donations in donors:
            with database.transaction():
                new_donor = Donor_Table.create(full_name=donor)
                new_donor.save()
                logger.info('{} Donor add successful'.format(donor))
            for donation in donations:              
                new_donation = Donation_Table.create(donor=new_donor,
                                                       donation_amt=donation)
                new_donation.save()
                logger.info('{} ${} added'.format(donor, donation))

        logger.info('Print the donor records we saved...')
        for donor in Donor_Table:
            logger.info(f'{donor.full_name} donated.')

        logger.info('Print the donation records we saved...')
        for donation in Donation_Table:
            logger.info(f'{donation.donor.full_name} donated '
                        f'{donation.donation_amt}.')

    except Exception as e:
        logger.info(f'Error on {donor}.')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()
              


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger(__name__)
    if not not db_exists:
        fill_db()
    DonorDict = Donor_Collection()      
              
    response = input('Please choose between the following 3 actions:\
    1. Send a Thank You; 2. Create a Report; 3. Send letters to everyone; 4. quit >  ')
    try:
        int(response)
    except:
        while not response.isdigit():
            print("You didn't enter a number.")
            print()
            response = input('Please choose between the following 3 actions:\
            1. Send a Thank You; 2. Create a Report; 3. Send letters to everyone; 4. quit >  ')
    arg_dict = {1:thankyou, 2:report, 3:thankyoueveryone}

    while int(response) != 4:
        try:
            arg_dict.get(int(response))(DonorDict)

        except (TypeError, ValueError):
            print('This is an invalid choice. Please enter a number between 1 and 4.')
            print()
            response = input('Please choose between the following 3 actions:\
            1. Send a Thank You; 2. Create a Report; 3. Send letters to everyone; 4. quit >  ')
        else:
            response = input('Please choose between the following 3 actions:\
                1. Send a Thank You; 2. Create a Report; 3. Send letters to everyone; 4. quit >   ')
        finally:
            if not response.isdigit():
                response = '99999'