"""
    mongodb example
"""

from pprint import pprint as pp
from donor_data import get_donor_data

import login_database
import utilities
import donor_data


log = utilities.configure_logger('default', '../logs/mongodb_script.log')

class Main:
    log.info('Initialize Class "Main".')
    log = utilities.configure_logger('default', '../logs/nosql_dev.log')
    log.info('\n\nRunning mongodb_mailroom_script for PART 1 assignment from learnnosql.py')
   
    log.info("Initialize the Database.")
    with login_database.login_mongodb_cloud() as client:
        log.info('\n\nStep 1: We are going to use a database called donors')
        log.info('\n\nBut if it doesnt exist mongodb creates it')
        db = client['donors']

        log.info('\n\nAnd in that database use a collection called Donor')
        log.info('\n\nIf it doesnt exist mongodb creates it')

        donor = db['donor']
        
        log.info('Insert an item into the document')
        new_donor = {'name': {'first_name': 'Ben', 'last_name': 'Master'},
            'donation': 1000.11}
        
        donor.insert_one(new_donor)
        
        log.info('\n\nStep 2: Now we add data from the dictionary above')
        donor_items = get_donor_data()
        donor.insert_many(donor_items)
        
        
        log.info("Show the collections in the DB.")
        print(db.list_collection_names()) 
    
    def __init__(self):
        
        self.menu = {1: 'Send a Thank You (and add/update donor)',
                     2: 'Create a Report',
                     3: 'Send letters to everyone',
                     4: 'Delete a Donor',
                     5: 'Quit'}
    
    def main_menu(self):
        print('\n', 'Please select a number from the following choices:\n')
        return {(print(str(k) + ':', v)) for k, v in self.menu.items()}
    
    def selection(self):

        while True:
            input1 = input("Selection: ")
            try:
                if int(input1) in range(1, 5):
                    if int(input1) == 1:
                        print('\nType "list" to show names or hit the "Return/Enter" key to add names and/or donations.')
                        input2 = input('-> ')
                        if input2 == 'list':
                            donor_names = set()
                            for d in self.donor.find():
                                name = ' '.join([d['name']['first_name'], d['name']['last_name']])
                                donor_names.add(name)
                            for d in donor_names:
                                print(d)
                            Main()
                            self.main_menu()
                            self.selection()
                        else:
                            first_name = input('First Name: ')
                            last_name = input('Last Name: ')
                            donation = float(input('Donation amount: '))
                            new_donor = {'name': {'first_name': first_name, 'last_name': last_name}, 'donation': donation}
                            self.donor.insert_one(new_donor)
                            self.send_thanks(first_name, last_name, donation)
                            Main()
                            self.main_menu()
                            self.selection()
                    elif int(input1) == 2:
                        self.create_report()
                    elif int(input1) == 3:
                        self.send_letters_all()
                    elif int(input1) == 4:
                        self.delete_donor()
                elif int(input1) == 5:
                    print("Exiting program...")
                    raise SystemExit()
                    
            except ValueError:
                print("You must use a menu number between 1-4; try again!")
                
    def send_thanks(self, first, last, amount):
        letter = 'Thank you {} {} for your donation in the amount of ${}; it is very generous.'.format(first, last, amount)
        with open('Thank_You_{}, {}.txt'.format(last.lower(), first.lower()), 'w') as f:
            f.write(letter)
        print("Your thank you letter has been written to disk.")
        
    def create_report(self):
        print('\n{:<20} {:>20} {:>20} {:>20}'.format('Donor Name',
              '| Total Given', '| Num Gifts', '| Average Gift'))
        print('{}'.format('-' * 83))
        
        result = self.donor.aggregate([{'$group': {'_id': {'name': '$name'}, 'sum': {'$sum': '$donation'}, 'count': {'$sum':1}, 'avg': 
{'$avg': '$donation'}}}, {'$sort': {'sum': -1}}])
        
        for i in result:
            i_name = ' '.join([i['_id']['name']['first_name'], i['_id']['name']['last_name']])
            i_sum = i['sum']
            i_count = i['count']
            i_avg = i['avg']
            print('{:<20} {:>20.02f} {:>20} {:>20.02f}'.format(i_name, i_sum, i_count, i_avg))
        Main()
        self.main_menu()
        self.selection()
        
    def send_letters_all(self):
        
        letters = 'Dear {},\n\n\tThank you for your total contributions in the amount of ${}.\n\n\tYou are making a difference in the lives of others.\n\n\t\tSincerely,\n\t\t"Working for America"'
        
        result = self.donor.aggregate([{'$group': {'_id': {'name': '$name'}, 'sum': {'$sum': '$donation'}, 'count': {'$sum':1}, 'avg': {'$avg': '$donation'}}}, {'$sort': {'sum': -1}}])
        
        for i in result:
            i_name = ' '.join([i['_id']['name']['first_name'], i['_id']['name']['last_name']])
            i_sum = i['sum']
            i_count = i['count']
            i_avg = i['avg']
            with open('Thank_You_Letter_{}.txt'.format(i_name.title().replace(' ', '_')), 'w') as f:
                f.write(letters.format(i_name, i_sum))
        print('\nYour letters have been printed to the current directory!')
        
        Main()
        self.main_menu()
        self.selection()
        
    def delete_donor(self):
        
        print('\nType "list" to show names or hit the "Return/Enter" key to delete a name.')
        input2 = input('-> ')
        if input2 == 'list':
            donor_names = set()
            for d in self.donor.find():
                name = ' '.join([d['name']['first_name'], d['name']['last_name']])
                donor_names.add(name)
            for d in donor_names:
                print(d)
            Main()
            self.main_menu()
            self.selection()
        else:
            first_name = input('First Name: ')
            last_name = input('Last Name: ')
            del_donor = {'name': {'first_name': first_name, 'last_name': last_name}}
            check = self.donor.count_documents(del_donor) > 0
            if check:
                self.donor.delete_many(del_donor)
            else:
                print("That donor is not in our database; please try again.")
            Main()
            self.main_menu()
            self.selection()
                
if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    ex = Main()
    ex.main_menu()
    ex.selection()