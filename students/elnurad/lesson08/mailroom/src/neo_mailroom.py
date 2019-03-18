import utilities
import login_database
import utilities
import pprint
import os

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def list():
    """
       Print list of donors
    """
    cyph = """MATCH (d:Donor)
              RETURN d.donor as donor, d.donations as donations
           """
    result = session.run(cyph)
    print("Donors in database:")
    for record in result:
        print(record['donor'])


def create_report():
    """
       Create report
    """
    print("{0:<20}{1:>12}{2:>12}{3:>15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift"))
    print("--------------------------------------------------------------")
    cyph = """MATCH (d:Donor)
              RETURN d.donor as donor, d.donations as donations
           """
    result = session.run(cyph)
    donors = []
    for record in result:
        total = sum(record['donations'])
        num = len(record['donations'])
        average = total/num
        donors.append([record['donor'], total, num, average])
    donors = sorted(donors, key = lambda x: x[1], reverse = True)
    for donor in donors:
        pprint.pprint("{:<20} ${:>12,.2f}{:^12} ${:>12,.2f}".format(donor[0], donor[1], donor[2], donor[3]))
    
      
def letter_to_all():
    """
        Save a letter to all donors to a disk
    """
    cyph = """MATCH (d:Donor)
              RETURN d.donor as donor, d.donations as donations
           """
    result = session.run(cyph)
    
    for record in result:
        name = record['donor']
        directory = str(input("Please specify the directory name for this file: "))
        filepath = os.path.join(os.sep, directory)
        with open(f"{filepath}\\{name}.txt", "w") as f:
            f.write("Dear {0},\n\n\tThank you for your very kind donation. It will be put to very good use.\n\n\t\t\t Sincerely,\n\t\t\t -The Team".format(name))


def add_donor_donation():
    """
        Add new donor and donation
    """
    donor_name = input("Enter new donor's name ")
    donations = input("Enter donation amount ")
    for donor, donations in [(donor_name, donations)]:
      cyph = "CREATE (n: Donor {donor:'%s', donations: [%s]})" % (donor, donations)
      result = session.run(cyph)


def update():
    """
        Update name of an existing donor
    """
    donor_name = input("Enter name of the donor to be updated ")
    new_name = input('Enter a new name for this donor ')
    for donor_name, new_name in [(donor_name, new_name)]:
        cyph = "MATCH (n) WHERE n.donor = '%s' SET n.donor = '%s' RETURN n" % (donor_name, new_name) 
        result = session.run(cyph)    


def delete():
    """
        Delete donor from database
    """
    donor_name = input('Enter name of the donor you  wish to delete ')
    cyph = "MATCH (n) WHERE n.donor = '%s' DELETE n" % donor_name
    result = session.run(cyph)


def thank_you_note():
    """
        Send a thank you note
    """
    name = input("Please, type the full name of an existing sponsor from the list: ")
    while name == "list":
        list()
        name = input("Please, type the full name of a sponsor: ")
    while name.isnumeric():
        name = input("Please, type the full name of a sponsor. Your input should be a string: ")
    print(f"Dear {name},\n\n\tThank you for your generous donation!.\n\n\t\t\t\t\t\t\tSincerely, your Charity")


def quit():
    exit()



dict_select = {
1: thank_you_note,
2: create_report,
3: letter_to_all,
4: update,
5: add_donor_donation,
6: delete,
7: quit
}


if __name__ == '__main__':
    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add a few people")

    with driver.session() as session:

        log.info('Adding a few Person nodes')
        log.info('The cyph language is analagous to sql for neo4j')
        for donor, donations in [('Bill Gates', [6000, 456, 33]),
                            ('Jeff Bezos', [10000, 3000]),
                            ('Hannah Smith', [60000, 7800]),
                            ('John Clark', [3000, 890]),
                            ('Andrew Jones', [8000, 500]),
                            ]:
            cyph = "CREATE (n:Donor {donor:'%s', donations: %s})" % ( #creating reusable node
                donor, donations)
            session.run(cyph)


        while True:
            action = int(input(("Please tell us what you would like to do: 'send a thank you: type 1',"
                                " 'create a report: type 2', 'send a letter to all donors: type 3', update a donor name: type 4'"
                                "'add a new donor: type 5', 'delete a donor record: type 6', 'quit: type 7' ")))
            dict_select[action]()
    

       