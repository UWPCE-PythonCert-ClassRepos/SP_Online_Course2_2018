"""
    demonstrate use of Redis
"""

 
import login_database
import utilities


class Run_Ex():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('\n\nStep 1: connect to Redis')
        r = login_database.login_redis_cloud()
        
        log.info('\n\nStep 2: cache some data in Redis')
        r.hmset('Karl', {'Telephone': '444-333-1234', 'Zip': '90120', 'Donation': ['500', '600'], 'email': 'karl@karl.com'})
        r.hmset('Mike', {'Telephone': '123-456-7890', 'Zip': '12345', 'Donation': ['100', '250.55'], 'email': 'mike@mike.com'})
        r.hmset('Sherri', {'Telephone': '888-777-6666', 'Zip': '42157', 'Donation': ['1000.10'], 'email': 'sherri@sherri.com'})
        r.hmset('Zulu', {'Telephone': '999-111-5555', 'Zip': '84591', 'Donation': ['55', '66', '77.77'], 'email': 'zulu@zulu.com'})
        r.hmset('Abbi', {'Telephone': '978-765-5432', 'Zip': '21478', 'Donation': ['123.45'], 'email': 'abbi@abbi.com'})
        r.hmset('Larry', {'Telephone': '789-345-5678', 'Zip': '62143', 'Donation': ['567.89'], 'email': 'larry@larry.com'})
        

    except Exception as e:
        print(f'Redis error: {e}')
        
    def __init__(self):
        
        self.menu = {1: 'List of Donors in the Database',
                     2: 'Add a new Donor',
                     3: 'Find an email address',
                     4: 'List a Donor\'s donations',
                     5: 'Find a Donor\'s complete record',
                     6: 'Delete a Donor\'s record',
                     7: 'Quit'}
    
    def main_menu(self):
        print('\n', 'Please select a number from the following choices:\n')
        return {(print(str(k) + ':', v)) for k, v in self.menu.items()}
    
    
    def selection(self):

        while True:
            input1 = input("Selection: ")
            try:
                if int(input1) in range(1, 7):
                    if int(input1) == 1:
                        for i in self.r.keys():
                            print(i.decode('utf-8'))
                            
                    
                    if int(input1) == 2:
                        print('Please provide the following Donor information for the database: ')
                        name = input('Name: -> ')
                        telephone = input('Telephone, in the format 123-45-6789: -> ')
                        _zip = input('5-digit zip code: -> ')
                        donation = input('Donation amount: -> ')
                        email = input('Email address: -> ')
                        try:
                            self.r.hmset(name, {'Telephone': telephone, 'Zip': _zip, 'Donation': [donation], 'email': email})
                            print('The new Donor has been added to the database.')
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                        except:
                            print('There was a problem adding the new Donor to the database.')
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
    
                    
                    if int(input1) == 3:
                        name = input('Type a persons name to find their email:   -> ')
                        if self.r.exists(name):
                            print(self.r.hget(name, 'email').decode('utf-8'))
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                        else:
                            print('That name is not in the database')
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                    
                    if int(input1) == 4:
                        name = input('Type a persons name to find their donatoions:   -> ')
                        if self.r.exists(name):
                            print(self.r.hget(name, 'Donation').decode('utf-8'))
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                        else:
                            print('That name is not in the database') 
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                            
                    if int(input1) == 5:
                        name = input('Type a persons name to find their complete record:   -> ')
                        if self.r.exists(name):
                            print(self.r.hgetall(name))
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                        else:
                            print('That name is not in the database') 
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                            
                    if int(input1) == 6:
                        name = input('Type a persons name to delete their complete record:   -> ')
                        if self.r.exists(name):
                            
                            self.r.delete(name)
                            for i in self.r.keys():
                                print(i.decode('utf-8'))
                                Run_Ex()
                                ex.main_menu()
                                ex.selection()
                            print(f'\n\nAs you can see, the record for {name} is no longer in the database.')
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                        else:
                            print('That name is not in the database') 
                            Run_Ex()
                            ex.main_menu()
                            ex.selection()
                    
                elif int(input1) == 7:
                    print("Exiting program...")
                    raise SystemExit()
                    
            except ValueError:
                print("You must use a menu number between 1-4; try again!")
        
if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    ex = Run_Ex()
    ex.main_menu()
    ex.selection()

