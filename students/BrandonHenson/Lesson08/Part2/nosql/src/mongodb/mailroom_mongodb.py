"""
    mongodb example
"""
from donor_data import get_donor_data
from pprint import pprint as pp
import login_database
import utilities
import donor_data


log = utilities.configure_logger('default', '../logs/mongodb_script.log')


class Main:
    log.info('Initialize Class "Main".')
    log = utilities.configure_logger('default', '../logs/nosql_dev.log')
    log.info('\n\nRunning mongodb_mailroom_script')

    log.info("Initialize the Database.")
    with login_database.login_mongodb_cloud() as client:
        log.info('\n\nStep 1: We are going to use a database called donors')
        log.info('\n\nBut if it doesnt exist mongodb creates it')
        db = client['donors']

        log.info('\n\nAnd in that database use a collection called Donor')
        log.info('\n\nIf it doesnt exist mongodb creates it')

        donor = db['donor']

        log.info('Insert an item into the document')
        new_donor = {'name': {'first_name': 'Test', 'last_name': 'Guy'},
                     'donation': 1234.56}

        donor.insert_one(new_donor)

        log.info('\n\nStep 2: Now we add data from the dictionary above')
        donor_items = get_donor_data()
        donor.insert_many(donor_items)

        log.info("Show the collections in the DB.")
        print(db.list_collection_names())

    def __init__(self):
        self.prompt = {1: 'Send A Thank You To New Or Exsisting Donor',
                       2: 'Create a Report',
                       3: 'Send notes to everyone',
                       4: 'Delete a Donor',
                       5: 'Exit'}

    def menu_selection(self):
        print("\nPick from the listed options.")
        return {(print(str(k) + ':', v)) for k, v in self.prompt.items()}

    def selection(self):

        while True:
            input1 = input("Selection: ")
            try:
                if int(input1) in range(1, 5):
                    if int(input1) == 1:
                        print('\n"Enter a name or list"')
                        input2 = input()
                        if input2 == 'list':
                            donor_names = set()
                            for i in self.donor.find():
                                name = ' '.join([i['name']['first_name'],
                                                 i['name']['last_name']])
                                donor_names.add(name)
                            for i in donor_names:
                                print(i)
                            Main()
                            self.menu_selection()
                            self.selection()
                        else:
                            first_name = input('First Name: ')
                            last_name = input('Last Name: ')
                            donation = float(input('Donation amount: '))
                            new_donor = {'name': {'first_name': first_name,
                                         'last_name': last_name},
                                         'donation': donation}
                            self.donor.insert_one(new_donor)
                            self.thank_you(first_name, last_name, donation)
                            Main()
                            self.menu_selection()
                            self.selection()
                    elif int(input1) == 2:
                        self.create_report()
                    elif int(input1) == 3:
                        self.thank_everyone()
                    elif int(input1) == 4:
                        self.delete_user()
                elif int(input1) == 5:
                    raise SystemExit()

            except ValueError:
                print("\nPick from the listed options.")

    def thank_you(self, first, amount):
        letter = "Dear {},\nThank you for your generous donation in the amount \
of ${}; \nThe money will be put to good use.\n\nSincerely, \n                -\
The Team".format(first, amount)
        with open('{}.txt'.format(first.upper().
                                  replace(' ', '_')), 'w') as f:
            f.write(letter)

    def create_report(self):
        print('\n{:<20} {:>20} {:>20} {:>20}'.format('Donor Name',
              '| Total Given', '| Num Gifts', '| Average Gift'))
        print('{}'.format('-' * 83))

        result = self.donor.aggregate([{'$group': {'_id': {'name': '$name'},
                                      'sum': {'$sum': '$donation'},
                                      'count': {'$sum': 1}, 'avg':
                                      {'$avg': '$donation'}}},
                                      {'$sort': {'sum': -1}}])

        for i in result:
            i_name = ' '.join([i['_id']['name']['first_name'],
                               i['_id']['name']['last_name']])
            i_sum = i['sum']
            i_count = i['count']
            i_avg = i['avg']
            print('{:<20} {:>20.02f} {:>20} {:>20.02f}'.format(i_name,
                                                               i_sum, i_count,
                                                               i_avg))
        Main()
        self.menu_selection()
        self.selection()

    def thank_everyone(self):

        notes = 'Dear {},\n\nThank you for your generous donations totaling \
${}. The money will be put to good use.\n\nSincerely,\n\t\t-The Team'

        result = self.donor.aggregate(
            [{'$group': {'_id': {'name': '$name'},
              'sum': {'$sum': '$donation'}, 'count': {'$sum': 1},
              'avg': {'$avg': '$donation'}}}, {'$sort': {'sum': -1}}])

        for i in result:
            i_name = ' '.join([i['_id']['name']['first_name'],
                               i['_id']['name']['last_name']])
            i_sum = i['sum']
            i_count = i['count']
            i_avg = i['avg']
            with open('{}.txt'.format(i_name.title().replace(' ',
                      '_')), 'w') as f:
                f.write(notes.format(i_name, i_sum))

        Main()
        self.menu_selection()
        self.selection()

    def delete_user(self):

        print('\nPress ENTER or type list')
        input2 = input()
        if input2 == 'list':
            donor_names = set()
            for i in self.donor.find():
                name = ' '.join([i['name']['first_name'],
                                 i['name']['last_name']])
                donor_names.add(name)
            for i in donor_names:
                print(i)
            Main()
            self.menu_selection()
            self.selection()
        else:
            first_name = input('First Name: ')
            last_name = input('Last Name: ')
            del_donor = {'name': {'first_name': first_name,
                         'last_name': last_name}}
            check = self.donor.count_documents(del_donor) > 0
            if check:
                self.donor.delete_many(del_donor)
            else:
                print("That donor is not in our database; please try again.")
            Main()
            self.menu_selection()
            self.selection()

if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    ex = Main()
    ex.menu_selection()
    ex.selection()
