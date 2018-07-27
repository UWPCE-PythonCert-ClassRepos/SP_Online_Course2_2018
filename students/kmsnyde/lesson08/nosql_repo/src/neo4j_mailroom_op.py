"""
    neo4j example
"""
import logging
#import utilities
import login_database
from pprint import pprint as pp
from neo4j.v1 import GraphDatabase

class Run_Ex():

    #log = utilities.configure_logger('default', '../logs/neo4j_script.log')
    log = logging.getLogger("neo4j.bolt")
    log.setLevel(logging.WARNING)
    
    
    #log.info('\n\nClear the entire database')
    #log.info("\nRunning clear_all")

    driver = login_database.login_neo4j_cloud()
    #with driver.session() as session:
    session = driver.session()
    session.run("MATCH (n) DETACH DELETE n")

    #log.info("\n\nPopulate a Donor Database")

    p1 = session.run("create (n:Person {first_name: 'Ben', last_name: 'Master', donation: 100})")
    p2 = session.run("create (n:Person {first_name: 'Karl', last_name: 'Evers', donation: 600.77})")
    p3 = session.run("create (n:Person {first_name: 'Tommy', last_name: 'Boy', donation: 484.60})")
    p4 = session.run("create (n:Person {first_name: 'Wendi', last_name: 'Shirt', donation: 2421.19})")
    p5 = session.run("create (n:Person {first_name: 'Moose', last_name: 'Claws', donation: 40.99})")
    p2 = session.run("create (n:Person {first_name: 'Sal', last_name: 'Matrix', donation: 88})")
    p2 = session.run("create (n:Person {first_name: 'Ben', last_name: 'Master', donation: 110})")
    p2 = session.run("create (n:Person {first_name: 'Karl', last_name: 'Evers', donation: 98})")
    p2 = session.run("create (n:Person {first_name: 'Can', last_name: 'Do', donation: 765.43})")

         

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
                            donor_names = self.session.run("match (n:Person)  return n.first_name as first, n.last_name as last, count(*) order by last, first")
                            for i in donor_names:
                                print(i[0], i[1])
                            Run_Ex()
                            self.main_menu()
                            self.selection()
                        else:
                            first_name = input('First Name: ')
                            last_name = input('Last Name: ')
                            donation = float(input('Donation amount: '))
                            self.session.run("create (n:Person {first_name: '%s', last_name: '%s', donation: %02.2f})" % (first_name, last_name, donation))
                            self.send_thanks(first_name, last_name, donation)
                            Run_Ex()
                            self.main_menu()
                            self.selection()
                    elif int(input1) == 2:
                        self.create_report()
                        Run_Ex()
                        self.main_menu()
                        self.selection()
                    elif int(input1) == 3:
                        self.send_letters_all()
                        Run_Ex()
                        self.main_menu()
                        self.selection()
                    elif int(input1) == 4:
                        self.delete_donor()
                        Run_Ex()
                        self.main_menu()
                        self.selection()
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
        
        cyph = self.session.run("match (n:Person) return n.first_name, n.last_name, count(*), sum(n.donation) as sum, avg(n.donation) order by sum desc")
        
        for i in cyph:
            name = ' '.join([i[0], i[1]])
            print('{:<20} {:>20} {:>20.02f} {:>20.02f}'.format(name, i[2], i[3], i[4]))
            
    def send_letters_all(self):
        
        letters = 'Dear {},\n\n\tThank you for your total contributions in the amount of ${}.\n\n\tYou are making a difference in the lives of others.\n\n\t\tSincerely,\n\t\t"Working for America"'
        
        cyph = self.session.run("match (n:Person) return n.first_name, n.last_name, count(*), sum(n.donation) as sum, avg(n.donation) order by sum desc")
        
        for i in cyph:
            name = ' '.join([i[0], i[1]])
            with open('Thank_You_Letter_{}.txt'.format(name.title().replace(' ', '_')), 'w') as f:
                f.write(letters.format(name, i[3]))
        print('\nYour letters have been printed to the current directory!')
        
    def delete_donor(self):
        
        print('\nType "list" to show names or hit the "Return/Enter" key to delete a name.')
        input2 = input('-> ')
        if input2 == 'list':
            donor_names = self.session.run("match (n:Person)  return n.first_name as first, n.last_name as last, count(*) order by last, first")
            for i in donor_names:
                print(i[0], i[1])
            Run_Ex()
            self.main_menu()
            self.selection()
        else:
            first_name = input('First Name: ')
            last_name = input('Last Name: ')
            _del = "match (n:Person {first_name: '%s', last_name: '%s'}) delete n" % (first_name, last_name)
            self.session.run(_del)
            print('{} {} has been removed from the database.'.format(first_name, last_name))


if __name__ == '__main__':
    """
    orchestrate nosql examples2
    """

    ex = Run_Ex()
    ex.main_menu()
    ex.selection()