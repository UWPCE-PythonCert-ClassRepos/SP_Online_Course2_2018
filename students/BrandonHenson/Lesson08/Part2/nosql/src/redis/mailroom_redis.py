"""
Redis
"""


import login_database
import utilities


class Run_Ex():

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('\n\nStep 1: connect to Redis')
        r = login_database.login_redis_cloud()

        log.info('\n\nStep 2: cache some data in Redis')
        r.hmset('Brandon Henson', {'Telephone': '425-355-3355', 'Zip': '98275',
                'Donation': ['1005.49', '3116.72', '5200'],
                'email': 'bigbrandonh@gmail.com'})
        r.hmset('Alicia Henson', {'Telephone': '916-635-6789', 'Zip': '98223',
                'Donation': ['21.47', '1500'],
                'email': 'Aliciahenson@gmail.com'})
        r.hmset('Michael Green', {'Telephone': '360-691-9021',
                'Zip': '98252', 'Donation': ['2400.54'],
                                  'email': 'michael@fake.com'})
        r.hmset('Brandon Henson Jr', {'Telephone': '360-722-9769',
                'Zip': '95670', 'Donation': ['355.42', '579.31'],
                                      'email': 'littlebrandon@fake.com'})
        r.hmset('Kaiya Henson', {'Telephone': '425-315-3797', 'Zip': '98275',
                'Donation': ['636.9', '850.13', '125.23'],
                'email': 'kaiya@fake.com'})

    except Exception as e:
        print(f'Error: {e}')

    def __init__(self):

        self.prompt = {1: 'List Donors',
                       2: 'Add a Donor',
                       3: 'Find email',
                       4: 'List donations',
                       5: 'Find record',
                       6: 'Delete record',
                       7: 'Exit'}

    def menu_selection(self):
        print("\nPick from the listed options.")
        return {(print(str(k) + ':', v)) for k, v in self.prompt.items()}

    def selection(self):

        while True:
            input1 = input("Selection: ")
            try:
                if int(input1) in range(1, 7):
                    if int(input1) == 1:
                        for i in self.r.keys():
                            print(i)

                    if int(input1) == 2:
                        name = input('Name:  ')
                        telephone = input('Phone# XXX-XXX-XXXX:  ')
                        _zip = input('Zip Code: XXXXX ')
                        donation = input('Donation amount:  ')
                        email = input('Email address:  ')
                        try:
                            self.r.hmset(name, {'Telephone': telephone,
                                                'Zip': _zip,
                                                'Donation': [donation],
                                                'email': email})
                            print('DONE')
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()
                        except:
                            print("DIDN'T WORK. TRY AGAIN.")
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()

                    if int(input1) == 3:
                        name = input('ENTER NAME TO GET EMAIL:    ')
                        if self.r.exists(name):
                            print(self.r.hget(name, 'email'))
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()
                        else:
                            print('NOT IN DATABASE')
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()

                    if int(input1) == 4:
                        name = input('ENTER NAME TO GET DONATIONS:    ')
                        if self.r.exists(name):
                            print(self.r.hget(name, 'Donation'))
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()
                        else:
                            print('NOT IN DATABASE')
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()

                    if int(input1) == 5:
                        name = input('ENTER NAME TO GET RECORDS:    ')
                        if self.r.exists(name):
                            print(self.r.hgetall(name))
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()
                        else:
                            print('NOT IN DATABASE')
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()

                    if int(input1) == 6:
                        name = input('ENTER NAME TO DELETE RECORDS:    ')
                        if self.r.exists(name):

                            self.r.delete(name)
                            for i in self.r.keys():
                                print(i)
                                Run_Ex()
                                ex.menu_selection()
                                ex.selection()
                            print(f'\n\n{name} is GONE.')
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()
                        else:
                            print('NOT IN DATABASE')
                            Run_Ex()
                            ex.menu_selection()
                            ex.selection()

                elif int(input1) == 7:
                    raise SystemExit()

            except ValueError:
                print("\nPick from the listed options.")

if __name__ == '__main__':
    ex = Run_Ex()
    ex.menu_selection()
    ex.selection()
