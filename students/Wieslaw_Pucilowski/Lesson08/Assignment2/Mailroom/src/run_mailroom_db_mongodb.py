import pymongo
import login_database
import donor_data
import utilities
import pprint
pp = pprint.PrettyPrinter(width=120)
from pymongo.errors import OperationFailure

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

__author__ = "Wieslaw Pucilowski"

class Main():

    def clear_db():
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            donor = db['donor']
            log.info('Step 9: Delete the collection so we can start over')
            db.drop_collection('donor')

    def isResultRecord(results):
        pass

    def populate_db():
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            
            log.info('And in that database use a collection called donor')
            log.info('If it doesnt exist mongodb creates it')

            donor = db['donor']
            log.info('\nStep 2: Now we add data from the dictionary above')
            donor_items = donor_data.get_donor_data()
            donor.insert_many(donor_items)
            
    def report():
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            donor = db['donor']
            log.info('Step 4: List report: donor, sum, average of donation:')
            try:
                records = donor.aggregate(
                    [
                        {
                            '$unwind' : '$donations' # must $unwind array for aggregation
                        },
                        {
                            '$group' : {
                                '_id' : '$name',
                                'Total' : {
                                        '$sum': '$donations'
                                    },
                                'Average' : {
                                        '$avg': '$donations'
                                    },
                                # mind count implemented as sum of aggregated rows
                                'Count' : {
                                        '$sum': 1
                                    }
                            }
                        },
                        {
                            '$sort' : {'Total' : -1 }
                        }
                    ]
                )
            except OperationFailure as e:
                print(e)
            
            pp.pprint('{:30} | {:20} | {:15} | {:17}'.format(
                                        'Donor',
                                        'Number',
                                        'Total',
                                        'Average')
                                )
            pp.pprint('='*91)
            for i in records:
                pp.pprint('{:<30} | {:<20} | {:<15.2f} | {:<17.2f}'.format(
                                                    i['_id']['first_name'] + " " + i['_id']['last_name'],
                                                    i['Count'] if i['Count'] else 0,
                                                    i['Total'] if i['Total'] else 0.00,
                                                    i['Average'] if i['Average'] else 0.00
                                                    
                                                )
                           )

            # for i in records:
            #     print(i)
          

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
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            donor = db['donor']
            try:
                records = donor.aggregate(
                    [
                        {
                            '$unwind' : '$donations' # must $unwind array for aggregation
                        },
                        {
                            '$group' : {
                                '_id' : '$name',
                                'Total' : {
                                        '$sum': '$donations'
                                    }
                            
                            }
                        }
                    ]
                )
            except OperationFailure as e:
                print(e)

            for i in records:
                Main.write_letter(i['_id']['first_name'] + " " + i['_id']['last_name'],
                                    i['Total']
                             )


    def add_donor_donation():
        """
        Adds new donor and donation,
        or adds donation to existing donor
        """
        log.info('Step 8: Add/Update donor/donation:')
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            
            db = client['donors']
            donor = db['donor']
            
            first = input("Donor name to add firs name:")
            last = input("Donor name to add last name:")
            location = input("Type donor's location:")
            try:
                donation = float(input(" Donation in USD: "))
            except ValueError:
                    print("""
                          Donation must be in USD...
                          Donor not added
                          """)
                    return()
            
            query = { '$and': [
                        {'name.first_name' : {'$eq' : first}},
                        {'name.last_name' : {'$eq' : last}},
                        {'location' : {'$eq' : location}}
                    ]}
            
            update = { '$push' : {'donations' : donation}}
            
            record = {
                    'name': {'first_name': first, 'last_name': last},
                    'location': location,
                    'donations' : [donation]
                }
            
            result = donor.find(query)
            
            if result.count() > 0:
                print("Donor found in DB, record to update:")
                print(record)
                result = donor.update_one(query, update)
            else:
                print("Adding new donor, record to insert:")
                result = donor.insert_one(record)

            Main.print_greetings(Main.greetings(first + " " + last,
                                                donation))


    def delete_donor():
        """
        Working with Donor table...
        """
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            
            db = client['donors']
            donor = db['donor']
            
            first = input("Donor name to remove firs name:")
            last = input("Donor name to remove last name:")
            location = input("Type donor's location:")
            
            donor.remove(
                { '$and': [
                        {'name.first_name' : {'$eq' : first}},
                        {'name.last_name' : {'$eq' : last}},
                        {'location' : {'$eq' : location}}
                    ]}
            )
            log.info('Donor: {} {} from {} has been removed from DB'.format(first, last, location))
            


    def show():
        """
        Print list of donors
        """
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            donor = db['donor']
            pp.pprint('{:<30}'.format('List of donors:'))
            pp.pprint('{}'.format('=' *60))
            records = donor.find().sort('name.last_name')
            # for i in records:
            #     print(i)
            for i in records:
                pp.pprint("{:<20} {:<20} {:<20}".format(i['name']['first_name'],
                                     i['name']['last_name'],
                                     i['location']))
  

    def challenge(factor, min_donation=None, max_donation=None):
        """
        Updating Donations according to projections
        """
        pass

    def project(factor, min_donation, max_donation):
        log.info('Step 6: Projection factor, min, max:')
        factor = factor
        _min = min_donation
        _max = max_donation
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            donor = db['donor']
            
            # not projected docations ( <MIN or >MAX):
            cursor2 = donor.aggregate([
                        {
                            '$unwind' : '$donations'
                        },
                        {
                            '$match' : {'$or': [
                                                {'donations' : {'$lte' : _min}},
                                                {'donations' : {'$gte' : _max}},
                                    ]
                            }
                        },
                        {
                            '$group' : {'_id' : '$name',
                                        'Total' : {
                                                    '$sum': '$donations'
                                            }
                            }
                        }
                        
            ])
            
            # Total of projected donations per donor after multiplied by factor:
            cursor4 = donor.aggregate([
                        {
                            '$unwind' : '$donations'
                        }, # pipe1
                        {
                            '$match' : { 'donations' : { '$gt' : _min, '$lt' : _max} # mind 'donations' without '$'
                            
                            }
                        }, # pipe2
                        {
                            '$project' : { 'name' : 1, 'donations' : 1,  'projected' : {'$multiply' : ['$donations', factor]}
                                        }
                        
                        }, # pipe3
                        {
                            '$group' : {'_id' : '$name',
                                        'Total' : {
                                                    '$sum': '$projected'
                                            }
                            }
                        }
                        
            ])
            
            # aggregate cursor2 and cursor4 in dict
            projection_dict = {}
            for i in cursor4:
                projection_dict[(i['_id']['first_name'], i['_id']['last_name'])] = i['Total']
            
            for i in cursor2:
                if (i['_id']['first_name'], i['_id']['last_name']) not in projection_dict.keys():
                    projection_dict[(i['_id']['first_name'], i['_id']['last_name'])] = i['Total']
                else:
                    projection_dict[(i['_id']['first_name'], i['_id']['last_name'])] += i['Total']
                    
            print("*** Projected values:")
            for k, v in sorted(projection_dict.items(), key=lambda item: item[1], reverse=True):
                pp.pprint("{} {} Total: {}".format(k[0], k[1], v))
            
        

    def backup():
        log.info('+++ Backup DB to JSON')
        print("sqlite3 DB backup to JSON file not implemented !")
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
        4 - Projections
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

