"""
    Mailroom utilizing a database
"""
import sys
import logging
import login_redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Donorhandle:
    def __init__(self, name, cust_num = None):
        self.name = name
        self.cust_num = cust_num

    @property
    def gifts(self):
        length = len(r.lrange(self.cust_num, 0, -1))
        r.hset(self.name, 'transactions', length)
        return length

    @property
    def total_donations(self):
        invoices = r.lrange(self.cust_num, 0, -1)
        details = r.hgetall(self.name)
        total = []
        for item in invoices:
            total += [float(details[item])]
        total = sum(total)
        r.hset(self.name, 'total_donations', total)
        return total

    @property
    def average(self):
        details = r.hgetall(self.name)
        total = float(details['total_donations'])
        invoices = float(details['transactions'])
        try:
            average = r.hset(self.name, 'average', total / invoices)
        except ZeroDivisionError:
            r.hset(self.name, 'average', 0)
        return average

    @property
    def first_gift(self):
        first = min([int(item) for item in r.lrange(self.cust_num, 0, -1)])
        first = float(r.hget(self.name, first))
        r.hset(self.name, 'first_gift', first)
        return first

    @property
    def last_gift(self):
        last = max([int(item) for item in r.lrange(self.cust_num, 0, -1)])
        last = float(r.hget(self.name, last))
        r.hset(self.name, 'last_gift', last)
        return last

def set_variables(name, cust_num):
    setting = Donorhandle(name, cust_num)
    setting.gifts
    setting.total_donations
    setting.average
    setting.first_gift
    setting.last_gift

def new_donor(name, donation):
    new_cust_num = f"{name[0]}{r.incr('customer_count')}"
    email = input('What is the email?: ')
    phone = input('What is the phone number?: ')
    r.hset(name, 'total_donations', donation)
    r.hset(name, 'average', donation)
    r.hset(name, 'first_gift', donation)
    r.hset(name, 'last_gift', donation)
    r.hincrby(name, 'transactions', 1)
    r.hset(name, 'average', donation)
    r.hset(name, 'email', email)
    r.hset(name, 'phone', phone)
    r.hset(name, 'cust_num', new_cust_num)
    r.hset(name, r.incr('invoice'), donation)
    r.rpush(new_cust_num, r.get('invoice'))

def existing_donor(name, donation):
    cust_num = r.hget(name, 'cust_num')
    r.hset(name, r.incr('invoice'), donation)
    r.rpush(cust_num, r.get('invoice'))
    return cust_num

def show_list():
    names = [item for item in r.scan()[1] if r.type(item) == 'hash']
    for donor in names:
        print(donor)
    return names

def report():
    names = [item for item in r.scan()[1] if r.type(item) == 'hash']
    for donor in names:
        print(donor)
        details = r.hgetall(donor)
        cust_num = details['cust_num']
        invoices = r.lrange(cust_num, 0, -1)
        print(f'   Donations:')
        for item in invoices:
            dono = float(details[item])
            print(f'      {dono:.2f}')
        total = float(details['total_donations'])
        print(f'   Total Donos - {total:.2f}')
        average = float(details['average'])
        print(f'   Average - {average:.2f}')
        first = float(details['first_gift'])
        print(f'   First Gift - {first:.2f}')
        last = float(details['last_gift'])
        print(f'   Last Gift - {last:.2f}')
        print(f'   Transactions - {details["transactions"]}')
        print(f'   Email - {details["email"]}')
        print(f'   Phone # - {details["phone"]}')

def letters():
    tab = '    '
    names = [item for item in r.scan()[1] if r.type(item) == 'hash']
    for donor in names:
        details = r.hgetall(donor)
        with open(f'{donor}.txt', 'w') as outfile:                
            donation = float(details['total_donations'])
            val = float(details['last_gift'])
            outfile.write(f'Dear {donor}, \n\n{tab}Thank you very much for your most recent donation \
of ${val:.2f}! \n\n{tab}You have now donated a total of ${donation:.2f}. \n\n{tab}Your support \
is essential to our success and will be well utilized. \n\n{tab*2}Sincerely, \n{tab*3}-The Company')

def show_donations():
    names = show_list()
    while True:
        choice = input(f'Whose donations do you want to see?: ')
        if choice == 'quit':
            return
        for donor in names:
            if choice == donor:
                details = r.hgetall(donor)
                invoices = r.lrange(details['cust_num'], 0, -1)
                print(f'\n{choice}')
                for item in invoices:
                    dono = float(details[item])
                    print(f'   {dono:.2f}')
                return
        print('\nDonator does not exist.\n')
        continue

def delete():
    names = show_list()
    while True:
        choice = input(f'Which donor would you like to edit?: ')
        if choice == 'quit':
            return
        for donor in names:
            if choice == donor:
                details = r.hgetall(donor)
                cust_num = details['cust_num']
                invoices = r.lrange(cust_num, 0, -1)
                for item in invoices:
                    print(f'Invoice {item}: {details[item]}')
                number = input(f'Which invoice would you like to delete?: ')
                if number == 'quit':
                    return
                r.hdel(donor, number)
                r.lrem(cust_num, 0, number)
                set_variables(donor, cust_num)
                return
        print('\nDonator does not exist.\n')
        continue

def edit():
    names = show_list()
    while True:
        choice = input(f'Which donor would you like to edit?: ')
        if choice == 'quit':
            return
        for donor in names:
            if choice == donor:
                details = r.hgetall(donor)
                cust_num = details['cust_num']
                invoices = r.lrange(cust_num, 0, -1)
                for item in invoices:
                    print(f'Invoice {item}: {details[item]}')
                while True:
                    number = input(f'Which invoice would you like to edit?: ')
                    if number == 'quit':
                        return
                    break
                while True:
                    new_amount = input(f'What is the correct donation amount?: ')
                    if new_amount == 'quit':
                        return
                    try:
                        float(new_amount)
                    except ValueError:
                        print('\nPlease give a number instead.\n')
                        continue
                    r.hset(donor, number, new_amount)
                    set_variables(donor, cust_num)
                    return
        print('\nDonator does not exist.\n')
        continue

def thank_you():
    while True:
        name = input('\nWhat is the name of the donor?: ')
        if name == 'list':
            show_list()
            continue
        elif name == 'quit':
            return
        while True:
            try:
                donation = float(input('\nWhat is the donation amount?: '))
            except ValueError:
                print('\nPlease give a number instead.\n')
                continue
            break
        names = [item for item in r.scan()[1] if r.type(item) == 'hash']
        for donor in names:
            if name == donor:
                print('Existing donor - adding donation to database')
                cust_num = existing_donor(name, donation)
                set_variables(name, cust_num)
                return
        print('New donor - adding donor to database')
        new_donor(name, donation)
        return

def quitting():
    """
    quits the program
    """
    sys.exit()

def continuing():
    """
    continues the program
    """
    print('Try Again.\n')

switch_func_dict = {
    '1':thank_you,
    '2':edit,
    '3':delete,
    '4':report,
    '5':letters,
    '6':show_donations,
    '7':quitting,
    'quit':quitting,
    'list':show_list
    }

if __name__ == '__main__':
    try:
        r = login_redis.login_redis_cloud()
        while True:
            choice = input(f'\n1: Add Donation' +\
            f'\n2: Edit Donation' +\
            f'\n3: Delete Donation' +\
            f'\n4: Create a Report' +\
            f'\n5: Send Letters to Everyone' +\
            f'\n6: Show Donations' +\
            f'\n7: Quit' +\
            f'\n\nChoose an Option: '
            )
            c = switch_func_dict.get(choice, continuing)()
    except Exception as e:
        print(f'Redis error: {e}')
