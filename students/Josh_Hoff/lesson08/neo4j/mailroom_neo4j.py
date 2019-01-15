"""
    Mailroom utilizing a database
"""
import sys
import logging
import login_neo4j

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Donorhandle:
    def __init__(self, name):
        self.name = name
        cyph = """
            MATCH (n: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
            RETURN n.name as name, i.invoice as inv, d.donation as don
            """ % (name)
        result = session.run(cyph)
        self.donations = []
        for item in result:
            self.donations += [item['don']]
        self.first = self.donations[-1]
        self.last = self.donations[0]
        
    @property
    def gifts(self):
        cypher = """MATCH (n: Donor {name:'%s'})
        SET n.transactions = %d
        RETURN n.transactions
        """ % (self.name, len(self.donations))
        session.run(cypher)
        return len(self.donations)

    @property
    def total_donations(self):
        cypher = """MATCH (n: Donor {name:'%s'})
        SET n.total_donations = %f
        RETURN n.total_donations
        """ % (self.name, sum(self.donations))
        session.run(cypher)
        return sum(self.donations)

    @property
    def average(self):
        cypher = """
        MATCH (n: Donor {name:'%s'})
        RETURN n.transactions as transactions, n.total_donations as total
        """ % (self.name)
        details = session.run(cypher)
        for item in details:
            total = item['total']
            transactions = item['transactions']
        try:
            average = total / transactions
        except ZeroDivisionError:
            average = 0
        cypher = """MATCH (n: Donor {name:'%s'})
        SET n.average = %f
        RETURN n.average
        """ % (self.name, average)
        session.run(cypher)
        return average

    @property
    def first_gift(self):
        cypher = """MATCH (n: Donor {name:'%s'})
        SET n.first_gift = %f
        RETURN n.first_gift
        """ % (self.name, self.first)
        session.run(cypher)
        return self.first

    @property
    def last_gift(self):
        cypher = """MATCH (n: Donor {name:'%s'})
        SET n.last_gift = %f
        RETURN n.last_gift
        """ % (self.name, self.last)
        session.run(cypher)
        return self.last

def set_variables(name):
    setting = Donorhandle(name)
    setting.gifts
    setting.total_donations
    setting.first_gift
    setting.last_gift
    setting.average

def new_donor(name, donation):
    numbers = adjust_numbers(1)
    new_inv = numbers[0]
    new_cust = numbers[1]
    email = input(f'What is the email?: ')
    phone = input(f'What is the phone number?: ')
    new_cust_num = f"{name[0]}{str(new_cust)}"
    cyph = """
    CREATE (n: Donor {name:'%s', cust: '%s',
            total_donations:%f, average:%f, first_gift:%f,
            last_gift:%f, transactions:%d, email:'%s', phone:'%s'})
            """ % (name, new_cust_num, donation,
            donation, donation, donation, 1, email, phone)
    session.run(cyph)
    cypher = """
    MATCH (n: Donor {name: '%s'})
    CREATE (i: Invoice {invoice:%d}),(d:Donation {donation:%f}),
           (n)-[:INVOICE]->(i)-[:DONATION]->(d)
    RETURN n
    """ % (name, new_inv, donation)
    session.run(cypher)
    return
    
def adjust_numbers(int = 0):
    numbers = """MATCH (t: Count)
    RETURN t.inv as inv, t.cust as cust
    """
    result = session.run(numbers)
    for item in result:
        items = [item['inv'], item['cust']]
    increase = """MATCH (t: Count)
    SET t.inv = %d, t.cust = %d
    RETURN t.inv, t.cust
    """ % (items[0] + 1, items[1] + int)
    session.run(increase)
    return items

def existing_donor(name, donation):
    new_inv = adjust_numbers()[0]
    cypher = """
    MATCH (n: Donor {name: '%s'})
    CREATE (i: Invoice {invoice:%d}),(d:Donation {donation:%f}),
           (n)-[:INVOICE]->(i)-[:DONATION]->(d)
    RETURN n
    """ % (name, new_inv, donation)
    session.run(cypher)
    return

def show_list():
    names = get_names()
    for name in names:
        print(name)
    return names
    
def get_names():
    cyph = """
    MATCH (d:Donor)
    RETURN d.name as name
    """
    result = session.run(cyph)
    names = []
    for donor in result:
        names += [donor['name']]
    return names

def report():
    names = get_names()
    for donor in names:
        cyph = """
            MATCH (n: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
            RETURN n.name as name, n.total_donations as total_donations,
            n.average as average, n.first_gift as first, n.last_gift as last,
            n.transactions as transactions, n.email as email, n.phone as phone,
            n.cust as cust, d.donation as don, i.invoice as inv
            """ % (donor)
        result = session.run(cyph)
        print(donor)
        print(f'   Donations:')
        for item in result:
            print(f"      Invoice {item['inv']}: {item['don']}")
        print(f'   Total Donos - {item["total_donations"]:.2f}')
        print(f'   Average - {item["average"]:.2f}')
        print(f'   First Gift - {item["first"]:.2f}')
        print(f'   Last Gift - {item["last"]:.2f}')
        print(f'   Transactions - {item["transactions"]}')
        print(f'   Customer Number - {item["cust"]}')
        print(f'   Email - {item["email"]}')
        print(f'   Phone # - {item["phone"]}')

def letters():
    tab = '    '
    names = get_names()
    for donor in names:
        cyph = """
            MATCH (n: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
            RETURN n.name as name, n.total_donations as total_donations,
            n.last_gift as last
            """ % (donor)
        result = session.run(cyph)
        with open(f'{donor}.txt', 'w') as outfile:                
            outfile.write(f'Dear {donor}, \n\n{tab}Thank you very much for your most recent donation \
of ${result["last"]:.2f}! \n\n{tab}You have now donated a total of ${result["total_donations"]:.2f}. \n\n{tab}Your support \
is essential to our success and will be well utilized. \n\n{tab*2}Sincerely, \n{tab*3}-The Company')

def show_donations():
    names = show_list()
    while True:
        choice = input(f'Whose donations do you want to see?: ')
        if choice == 'quit':
            return
        for donor in names:
            if choice == donor:
                cyph = """
                MATCH (n: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
                RETURN n.name as name, d.donation as don, i.invoice as inv
                """ % (donor)
                invoices = session.run(cyph)
                print(f'\n{choice}')
                for item in invoices:
                    print(f'   Invoice {item["inv"]}: {item["don"]:.2f}')
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
                cyph = """
                MATCH (n: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
                RETURN n.name as name, d.donation as don, i.invoice as inv
                """ % (donor)
                invoices = session.run(cyph)
                for item in invoices:
                    print(f'Invoice {item["inv"]}: {item["don"]:.2f}')
                number = input(f'Which invoice would you like to delete?: ')
                if number == 'quit':
                    return
                cypher = """MATCH ((n: Donor {name:'%s'})-[INVOICE]->(i:Invoice {invoice: %d}))
                DETACH DELETE i
                """ % (choice, int(number))
                session.run(cypher)
                set_variables(choice)
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
                cyph = """
                MATCH (n: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
                RETURN n.name as name, d.donation as don, i.invoice as inv
                """ % (donor)
                invoices = session.run(cyph)
                for item in invoices:
                    print(f'Invoice {item["inv"]}: {item["don"]:.2f}')
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
                    cypher = """MATCH ((n: Donor {name:'%s'})-[INVOICE]-(i:Invoice {invoice: %d})-[DONATION]->(d))
                    SET d.donation = %f
                    """ % (choice, int(number), float(new_amount))
                    session.run(cypher)
                    set_variables(choice)
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
        names = get_names()
        for donor in names:
            if name == donor:
                print('Existing donor - adding donation to database')
                existing_donor(name, donation)
                set_variables(name)
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
    driver = login_neo4j.login_neo4j_cloud()
    with driver.session() as session:
        check = """MATCH (t: Count)
        RETURN t.inv as inv, t.cust as cust
        """
        result = session.run(check)
        bool = False
        for item in result:
            bool = True
        if not bool:
            init = """CREATE (t: Count {inv:%d, cust:%d})""" % (1, 100)
            result = session.run(init)
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
