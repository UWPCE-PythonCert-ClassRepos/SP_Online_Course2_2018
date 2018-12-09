import redis
import utilities
import json
import login_database
import pprint
pp = pprint.PrettyPrinter(width=120)
from functools import reduce


log = utilities.configure_logger('default', '../logs/redis_script.log')

__author__ = "Wieslaw Pucilowski"
# database has been created during create_donors_db import

class Main():


    def clear_db():
        log.info('*** Inside clear_db()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 12: Clear database')
        r.flushdb()

    def populate_db():
        log.info('*** Inside populate_db()')
        # try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        
        log.info('Step 2: cache some data in Redis')
        # donor's hash
        name = 'Brandon Henson'
        donations = [
            {'donation': 70},
            {'donation': 180},
            {'donation': 220},
            {'donation': 60},
        ]
        json_donation = json.dumps(donations)
        r.hmset(name,
                {   'Telephone': '425-355-3355',
                    'Zip': '98275',
                    # 'Donations' : ['100', '200'], # <-- does not work here !
                    'email': 'bigbrandonh@ggmail.com',
                    'Donations' : json_donation
                }
            )

        ###
        name = 'Ivan Smirnoff'
        donations = [
            {'donation': 100},
            {'donation': 200},
            {'donation': 300}
        ]
        json_donation = json.dumps(donations)

        r.hmset(name,
                {   'Telephone': '425-355-3355',
                    'Zip': '98001',
                    # 'Donations' : ['300', '50'], # <-- does not work here !
                    'email': 'ivan.smirnoff@ggmail.com',
                    'Donations' : json_donation
                }
            )

        ###
        name = 'Alice Cooper'
        donations = [
            {'donation': 80},
            {'donation': 200}
        ]
        json_donation = json.dumps(donations)
        r.hmset(name,
                {   'Telephone': '206-315-1234',
                    'Zip': '60123',
                    # 'Donations' : ['300', '50'], # <-- does not work here !
                    'email': 'alice.cooper@ggmail.com',
                    'Donations' : json_donation
                }
            )


    def sum_donations(json_don):
        lst = json.loads(json_don)
        return reduce((lambda x, y: x+y),
                      [ lst[x]['donation'] for x in range(len(lst))])
    
    def avg_donations(json_don):
        lst = json.loads(json_don)
        if len(lst) > 0:
            return Main.sum_donations(json_don)/len(lst)
        else:
            return 0
    
    def cnt_donations(json_don):
        lst = json.loads(json_don)
        return len(lst)
    
    def upd_donations(rdb, donor_name, don):
        json_don = json.loads(rdb.hget(donor_name, 'Donations'))
        json_don.append({'donation': don})
        json_donation = json.dumps(json_don)
        rdb.hmset(donor_name, {'Donations': json_donation})
        
    
    def report():
        log.info('*** Inside report()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        a, index = r.scan()
        names = [i for i in index if r.type(i) == 'hash']
        donations = [i for i in index if r.type(i) == 'list']
        pp.pprint('{:30} | {:20} | {:15} | {:17}'.format(
                                        'Donor',
                                        'Number',
                                        'Total',
                                        'Average')
                                )
        pp.pprint('='*91)
        for i in names:
            json_donations = r.hget(i, 'Donations')
            pp.pprint('{:<30} | {:<20} | {:<15.2f} | {:<17.2f}'.format(
                                                str(i),
                                                Main.cnt_donations(json_donations) if Main.cnt_donations(json_donations) else 0,
                                                Main.sum_donations(json_donations) if Main.sum_donations(json_donations) else 0.00,
                                                Main.avg_donations(json_donations) if Main.avg_donations(json_donations) else 0.00
                                                
                                            )
                       )


    def greetings(name, amount):
        gr = """
    Ex Programmers Charity
    1999 Heartbeat Avenue
    11111 Fresh Spring, Alaska

    Dear {}

    Thank you so much for your generous donation of ${}

    It will be put to very good use.

                       Sincerely,
                          -The Team

    """.format(name, amount)
        return(gr)

    def print_greetings(gr):
        print(gr)

    def write_letter(name, amount):
        try:
            with open("_".join(name.split()) +'.txt', 'w') as f:
                f.write(Main.greetings(name, amount))
        except IOErrors as e:
            print("""
                Cannot write a file, cought
                {}
            """.format(e))

    def letters():
        log.info('Writing letters to all Donors...')
        log.info("Step 3: Get all of people in the DB:")
        r = login_database.login_redis_cloud()
        a, index = r.scan()
        names = [i for i in index if r.type(i) == 'hash']
        for i in sorted(names, key=lambda x: x.split()[1]):
            Main.write_letter(i,
                              Main.sum_donations(r.hget(i, 'Donations'))
                             )
       
    def check_donor(name):
        log.info('*** Inside check_donor()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        a, index = r.scan()
        names = [i for i in index if r.type(i) == 'hash']
        
        if name in names:
            return True
        else:
            return False

    def add_donor_donation():
        log.info('*** Inside add_donor_donation()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        name = input("Type donor first and last name: ")
        if Main.check_donor(name):
            print("Donor {} exist, adding donation".format(name))
            try:
                donation = float(input(" Donation in USD: "))
            except ValueError:
                    print("""
                          Donation must be in USD...
                          Donor not added
                          """)
                    return()
            Main.upd_donations(r, name, donation) 
        else:
            print("Adding new donor {}".format(name))
            try:
                donation = float(input(" Donation in USD: "))
            except ValueError:
                    print("""
                          Donation must be in USD...
                          Donor not added
                          """)
                    return()
            phone = input("Type donor phone: ")
            email = input("Type donor email: ")
            zipcod = input("Type donor zip: ")
            donations = [
                {'donation': donation}
            ]
            json_donation = json.dumps(donations)
            r.hmset(name,
                {   'Telephone': phone,
                    'Zip': zipcod,
                    'email': email,
                    'Donations' : json_donation
                }
            )
            Main.print_greetings(Main.greetings(name, donation))


    def delete_donor():
        """
        Working with Donor table...
        """
        log.info('Step: 1 connect to Redis')
        r = login_database.login_redis_cloud()
        name = input("Type donor name to remove: ")
        
        r.delete(name)
        r.delete('_'.join(name.split()))
        log.info('Donor {} has been deleted'.format(name))
        log.info('Changes will be visible in the next session'.format(name))
        


    def show():
        log.info('*** Inside list_donors()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        a, index = r.scan()
        names = [i for i in index if r.type(i) == 'hash']
        print("List of donors:")
        pp.pprint("{:<20} {:<10} {:<15} {:<20}".format('Name',
                                                       'Zip',
                                                       'Phone',
                                                       'Email')
                  )
        for i in sorted(names, key=lambda x: x.split()[1]):
            pp.pprint("{:<20} {:<10} {:<15} {:<20}".format(i,
                                                           r.hget(i, 'Zip'),
                                                           r.hget(i, 'Telephone'),
                                                           r.hget(i, 'email')
                                                        ))                     


    def project(factor, min_donation, max_donation):
        log.info('+++ Projection no implemented for redis')
        pass
            

    def backup():
        log.info('+++ Backup DB to JSON')
        print("DB backup to JSON file not implemented !")
        pass


if __name__ == "__main__":

    Main.populate_db()

    def menu_selection(prompt, dispatcher):
            while True:
                response = input(prompt)
                try:
                    if dispatcher[response]() == "exit menu":
                        break
                except KeyError:
                    print(response, "Wrong response !")
    
    def quit(msg):
        print("{}".format(msg))
        return "exit menu"

    def main_quit():
        Main.clear_db()
        return quit("Goodbye...")

    def sub_quit():
        return quit("Back to Main menu...")

    def sub_menu():
        menu_selection(submenu, subfeatures)

    def projections_prompt():
        try:
            factor = int(input("What is the multiplication factor:"))
        except ValueError:
            print("Multiplication factor should be integer...")
            return
        try:
            x = input("Above Min donation:")
            min_donation = float(x) if x != '' else None
            y = input("Below Max donation:")
            max_donation = float(y) if y != '' else None
        except ValueError:
            print("Min, Max donation should be in USD...")
            return
        Main.project(factor=factor, min_donation=min_donation, max_donation=max_donation)

    def restore():
        log.info('+++ Restoring DB from JSON')
        print("sqlite3 DB restore from JSON file not implemented!")
        pass


    menu = """
        {:-^30}

        1 - Send a Thank You
        2 - Create a Report
        3 - Send letters to everyone
        4 - Projections (pending)
        5 - Backup to JSON (pending)
        6 - Restore from JSON (pending)
        q - Quit
    """.format(' Main Menu ')

    submenu = """
        {:-^30}

        1 - Add new donor, donation
        2 - List donors
        3 - delete donor/donation
        q - Go to Main Menu

    """.format(' Add/List donors ')

    features = {
            '1': sub_menu,
            '2': Main.report,
            '3': Main.letters,
            '4': projections_prompt,
            '5': Main.backup,
            '6': restore,
            'q': main_quit,
            }

    subfeatures = {
            '1': Main.add_donor_donation,
            '2': Main.show,
            '3': Main.delete_donor,
            'q': sub_quit,
            }


    # start program menu
    menu_selection(menu, features)

