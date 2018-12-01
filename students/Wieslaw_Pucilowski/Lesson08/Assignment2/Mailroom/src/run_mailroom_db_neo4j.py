from neo4j.v1 import GraphDatabase, basic_auth
import login_database
import utilities
import pprint
pp = pprint.PrettyPrinter(width=120)


log = utilities.configure_logger('default', '../logs/neo4j_script.log')

__author__ = "Wieslaw Pucilowski"
# database has been created during create_donors_db import

class Main():


    def clear_db():
        log.info('Step 1: First, clear the entire database, so we can start over')
        log.info("Running clear_all")

        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def isResultRecord(results):
        """
        Checks if cypher returns any record, based in peek() - Obtain the next record from this result
        without consuming it. This leaves the record in the buffer for further processing.
        """
        try:
            if not results.peek():
                return False
        except ResultError:
            return False
        else:
            return True

    def populate_db():
        log.info('Step 1: First, clear the entire database, so we can start over')
        log.info("Running clear_all")

        Main.clear_db()
        log.info("Step 2: Populating database with donors history")

        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
    
            log.info('Adding donors/donations')
            log.info('The cyph language is analagous to sql for neo4j')
            p1 = session.run("create (n:Donor {full_name: 'Bill Gates', donation: [100, 200, 300]})")
            p2 = session.run("create (n:Donor {full_name: 'Mike Dell', donation: [50, 200]})")
            p3 = session.run("create (n:Donor {full_name: 'Jeff Bezo', donation: [668.99, 1999]})")
            p4 = session.run("create (n:Donor {full_name: 'Harry Potter', donation: [88]})")
            
            l1 = session.run("create (n:Location {location: 'London'})")
            l2 = session.run("create (n:Location {location: 'Seattle'})")
            l3 = session.run("create (n:Location {location: 'Everett'})")
            l3 = session.run("create (n:Location {location: 'Redmond'})")
            
            for i in [('Bill Gates', 'Redmond'),
                        ('Mike Dell', 'Seattle'),
                        ('Jeff Bezo', 'Everett'),
                        ('Harry Potter', 'London')]:
                session.run("""  MATCH (a:Donor {full_name: '%s'})
                            CREATE (a) -[r:LIVE_IN]-> (l:Location {location: '%s'})
                            RETURN type(r)
                            """ % (i[0], i[1])
                            )
            
            

    def create_location(loc):
        log.info('Adding location to DB')
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph =  """MATCH (l:Location {location : '%s'})
                        RETURN l.location
                    """ % (loc)
            result = session.run(cyph)
            if not Main.isResultRecord(result):
                session.run("""create (n:Location {location: '%s'})""" % loc)


    def report():
        log.info("Step 4: List donors in the DB:")
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            # option 1
            cyph = """
                MATCH (p:Donor) -[r:LIVE_IN]->(l:Location)
                WITH reduce(Tot=0, n IN p.donation | Tot + n) AS Total,
                reduce(Tot=0, n IN p.donation | Tot + 1) AS Count,
                p.full_name AS name,
                l.location AS location
                RETURN name,
                       location,
                       Total,
                       Count,
                       Total/Count AS Avg
                ORDER BY Total Desc
            """

            # Total , Average by Location
            cyph2 = """
                    MATCH (d:Donor)-[r:LIVE_IN]->(l:Location)
                    WITH d.donation AS dd, l.location AS location
                    UNWIND dd AS dn
                    RETURN  location,
                            sum(dn) AS Total,
                            avg(dn) AS Avg
                    ORDER BY location
            """
                
            results = session.run(cyph)
            # results = session.run(cyph1)
            print("Donors & donations in database:")
            # for i in results:
            #     print(i['name'],i['Total'],i['Count'], i['Avg'])
            pp.pprint('{:30} | {:20} | {:20} | {:15} | {:17}'.format(
                                        'Donor',
                                        'Location',
                                        'Number',
                                        'Total',
                                        'Average')
                                )
            pp.pprint('='*114)
            for i in results:
                pp.pprint('{:<30} | {:<20} | {:20} | {:<15.2f} | {:<17.2f}'.format(
                                                str(i['name']),
                                                str(i['location']),
                                                str(i['Count']) if i['Count'] else 0,
                                                i['Total'] if i['Total'] else 0.00,
                                                i['Avg'] if i['Avg'] else 0.00
                                            )
                       )
            results = session.run(cyph2)
            print()
            pp.pprint('{:^61}'.format("Total, Average per Location"))
            print()
            pp.pprint('{:20} | {:20} | {:15}'.format(
                                        'Location',
                                        'Total',
                                        'Average')
                     )

            pp.pprint('='*61)
            for i in results:
                pp.pprint('{:<20} | {:<20.2f} | {:<15.2f}'.format(
                                                str(i['location']),
                                                i['Total'] if i['Total'] else 0.00,
                                                i['Avg'] if i['Avg'] else 0.00
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
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = """
                    MATCH (p:Donor)
                    WITH p.donation AS dd, p.full_name AS name
                    UNWIND dd AS dn
                    RETURN  name, 
                            sum(dn) AS Total
                    ORDER BY name
                """
            result = session.run(cyph)

            for record in result:
                Main.write_letter(str(record['name']),
                                    str(record['Total'])
                             )


    def add_donor_donation():
        """
        Adds new donor and donation,
        or adds donation to existing donor
        """
        log.info("Step 4: Add Donor Update Donation")
        driver = login_database.login_neo4j_cloud()
        #
        name = input("Type donor first and last name: ")
        location = input("Type donor location: ")
        Main.create_location(location)
        try:
            don = float(input(" Donation in USD: "))
        except ValueError:
                print("""
                      Donation must be in USD...
                      Donor not added
                      """)
                return()
        
        with driver.session() as session:
            cyph =  """MATCH (p:Donor {full_name : '%s'})
                        RETURN p.full_name, p.donation
                    """ % (name)
            result = session.run(cyph)
   
            if Main.isResultRecord(result):
                print("+++ {} in DB, adding donation".format(name))
                for record in result:
                        print(record['p.full_name'], record['p.donation'])
                        cyph = """
                                    MATCH (p:Donor {full_name : '%s'})
                                    RETURN p.donation
                                """ % (name)
                        for i in session.run(cyph):
                            d = i['p.donation']
                            d.append(don)
                            cyph = """
                                    MATCH (p:Donor {full_name : '%s'})
                                    SET p.donation = %s
                                    RETURN p.full_name, p.donation
                                """ % (name, d)
                            result = session.run(cyph)      
            else:
                print("+++ {} not in DB, creating new donor".format(name))
                d = session.run("create (n:Donor {full_name: '%s', donation: [%s]})" % (name, don))
                session.run("""  MATCH (a:Donor {full_name: '%s'})
                            CREATE (a) -[r:LIVE_IN]-> (l:Location {location: '%s'})
                            RETURN type(r)
                            """ % (name, location)
                            )
                
            Main.print_greetings(Main.greetings(name, don))


    def delete_donor():
        """
        Working with Donor table...
        """
        driver = login_database.login_neo4j_cloud()
        name = input("Type donor to delete: ")
        log.info("Removing donor {} from database...".format(name))
        with driver.session() as session:
            cyph = """MATCH (p:Donor {full_name : '%s'})
                        DELETE p
                    """ % (name)
            result = session.run(cyph)


    def show():
        """
        Print list of donors
        """
        log.info("Step 3: Get all of people in the DB:")
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = """MATCH (d:Donor)-[r:LIVE_IN]->(l:Location)
                    RETURN d.full_name AS name, l.location AS location
                    ORDER BY name
                """
            
            result = session.run(cyph)
            print("Donors in database:")
            for record in result:
                # print(record['p.full_name'])
                print("{} living in {}".format(record['name'], record['location']))                          

    def challenge(factor, min_donation=None, max_donation=None):
        """
        Updating Donations according to projections
        """
        pass

    def project(factor, min_donation, max_donation):
        MIN = 100
        MAX = 400
        FACTOR = 2
        log.info("Step 4: List donors in the DB:")
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = """
                    MATCH (p:Donor)
                    WITH [x in p.donation WHERE x > %s  AND x < %s] AS dd, p.full_name AS name
                    UNWIND dd AS dn
                    RETURN   name, sum(dn * %s) AS Tot
                    ORDER BY name
                """ % (min_donation, max_donation, factor)
            results = session.run(cyph)
            
            cyph = """
                    MATCH (p:Donor)
                    WITH [x in p.donation WHERE x <= %s OR x >= %s] AS dd, p.full_name AS name
                    UNWIND dd AS dn
                    RETURN   name, sum(dn) AS Tot
                    ORDER BY name
                """ % (min_donation, max_donation)
            results2 = session.run(cyph)
            
            cyph = """
                    MATCH (p:Donor)
                    WITH [x in p.donation WHERE x > %s  AND x < %s] AS dd, p.full_name AS name
                    UNWIND dd AS dn
                    WITH COLLECT({name_:name,dn_:dn*%s}) AS Rows_
                    MATCH (p:Donor)
                    WITH [x in p.donation WHERE x <= %s OR x >= %s] AS dd, p.full_name AS name, Rows_ as Rows
                    UNWIND dd AS dn
                    WITH Rows + COLLECT({name_:name,dn_:dn}) AS AllRows
                    UNWIND AllRows AS rows
                    WITH rows.name_ as name, rows.dn_ as dn
                    return name, SUM(dn) AS Tot, collect(dn) AS lst
                    
                """  % (min_donation,
                        max_donation,
                        factor,
                        min_donation,
                        max_donation
                        )
                
            results5 = session.run(cyph)
            
            print("+++ Projected donations:")
            for i in results:
                print(i['name'],i['Tot'])
            print("+++ Not Projected donations:")
            for i in results2:
                print(i['name'],i['Tot'])
            print("+++++++ Combined (Projected + Non Projected): +++++++")
            pp.pprint('{:30} | {:20}'.format(
                                        'Donor',
                                        'Projected Total')
                                )
            pp.pprint('='*53)
            # {:<20.2f}'
            new_donations = []
            for i in results5:
                pp.pprint('{:<30} | {:<20.2f}'.format(
                                                str(i['name']),
                                                i['Tot']
                                            )
                       )
                new_donations.append((i['name'],i['lst']))
            
            # prompt for chellenge 
            answer = None
            while answer not in ['Yes', 'No']:
                answer = input("Whould you like to multiply by factor" +
                               "(above min, below max) donations: [Yes, No]:")
            if answer == "Yes":
                for i in new_donations:
                    session.run("""
                                MATCH (p:Donor {full_name : '%s'})
                                SET p.donation = %s
                                RETURN p.full_name, p.donation
                                """ % (i[0], i[1]) 
                    )
                log.info("Changes applied to DB...")
            else:
                log.info("No changes applied to DB...")

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

