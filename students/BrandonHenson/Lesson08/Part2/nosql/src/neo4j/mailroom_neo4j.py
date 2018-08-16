"""
    neo4j example
"""
import logging
import login_database
from pprint import pprint as pp
from neo4j.v1 import GraphDatabase

class Run_Ex():


    log = logging.getLogger("neo4j.bolt")
    log.setLevel(logging.WARNING)

    driver = login_database.login_neo4j_cloud()
    session = driver.session()


    person_1 = session.run("create (n:Person {first_name: 'Brandon', last_name: 'Henson', donation: 1005.49})")
    person_2 = session.run("create (n:Person {first_name: 'Alicia', last_name: 'Henson', donation: 21.47})")
    person_3 = session.run("create (n:Person {first_name: 'Michael', last_name: 'Green', donation: 2400.54})")
    person_4 = session.run("create (n:Person {first_name: 'Brandon', last_name: 'Henson jr', donation: 355.42})")
    person_5 = session.run("create (n:Person {first_name: 'Kaiya', last_name: 'Henson', donation: 636.9})")

         

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
                        print('Enter a name or list')
                        input2 = input()
                        if input2 == 'list':
                            donor_names = self.session.run("match (n:Person)\
return n.first_name as first, n.last_name as last, count(*) order by last, first")
                            for i in donor_names:
                                print(i[0], i[1])
                            Run_Ex()
                            self.menu_selection()
                            self.selection()
                        else:
                            first_name = input('First Name: ')
                            last_name = input('Last Name: ')
                            donation = float(input('Donation amount: '))
                            self.session.run("create (n:Person {first_name: '%s', last_name: '%s', donation: %02.2f})"
                                             % (first_name, last_name, donation))
                            self.thank_you(first_name, last_name, donation)
                            Run_Ex()
                            self.menu_selection()
                            self.selection()
                    elif int(input1) == 2:
                        self.create_report()
                        Run_Ex()
                        self.menu_selection()
                        self.selection()
                    elif int(input1) == 3:
                        self.thank_everyone()
                        Run_Ex()
                        self.menu_selection()
                        self.selection()
                    elif int(input1) == 4:
                        self.delete_user()
                        Run_Ex()
                        self.menu_selection()
                        self.selection()
                elif int(input1) == 5:
                    
                    raise SystemExit()

            except ValueError:
                print("\nPick from the listed options.")
                
    def thank_you(self, name, amount):
        letter = "Dear {} {},\nThank you for your generous donation in the amount \
of ${}; \nThe money will be put to good use.\n\nSincerely, \n                -\
The Team".format(first, last, amount)
        with open('{}.txt'.format(first.upper(), last.upper().
                                  replace(' ', '_')), 'w') as f:
            f.write(letter)

    def create_report(self):
        print('\n{:<20} {:>20} {:>20} {:>20}'.format('Donor Name',
                                                     '| Total Given', '| Num Gifts', '| Average Gift'))
        print('{}'.format('-' * 83))

        cyph = self.session.run("match (n:Person) return n.first_name,"
                                "n.last_name, count(*), sum(n.donation)as sum, avg(n.donation)order by sum desc")

        for i in cyph:
            name = ' '.join([i[0], i[1]])
            print('{:<20} {:>20} {:>20.02f} {:>20.02f}'.format(name, i[2], i[3], i[4]))
            
    def thank_everyone(self):
        
        notes = 'Dear {},\n\nThank you for your generous donations totaling \
${}. The money will be put to good use.\n\nSincerely,\n\t\t-The Team'
        
        cyph = self.session.run("match (n:Person)\
return n.first_name, n.last_name, count(*), sum(n.donation) as sum, avg(n.donation) order by sum desc")
        
        for i in cyph:
            name = ' '.join([i[0], i[1]])
            with open('{}.txt'.format(name.title().replace(' ', '_')), 'w') as f:
                f.write(notes.format(name, i[3]))
        
        
    def delete_user(self):
        
        print('\nType "list" to see names.')
        input2 = input()
        if input2 == 'list':
            donor_names = self.session.run\
("match (n:Person)  return n.first_name as first, n.last_name as last, count(*) order by last, first")
            for i in donor_names:
                print(i[0], i[1])
            Run_Ex()
            self.menu_selection()
            self.selection()
        else:
            first_name = input('First Name: ')
            last_name = input('Last Name: ')
            _del = "match (n:Person {first_name: '%s', last_name: '%s'}) delete n" % (first_name, last_name)
            self.session.run(_del)
            print('Deleted {} {}'.format(first_name, last_name))


if __name__ == '__main__':
    ex = Run_Ex()
    ex.menu_selection()
    ex.selection()