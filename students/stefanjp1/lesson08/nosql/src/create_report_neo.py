from mailroom_neo import *


def generate_report():
    """ Prints out a report of each donor's total donations and average gift """
    
    print("Donor Name                | Total Given | Num Gifts | Average Gift\n")
    print('------------------------------------------------------------------')

    with driver.session() as session:
        q = """
            MATCH (p:Person) RETURN p
            """
        result = session.run(q)
        
    all_donors = list()
    for rec in result:
        for donor in rec.values():
            all_donors.append(donor['name'])
            
    all_donors = list(set(all_donors))

    for donor in all_donors:
        total_donations, total_donated = donor_totals(donor)
        if total_donations > 0:
            donations_avg = total_donated / total_donations
        else:
            donations_avg = 0
            total_donations = 0
            total_donated = 0
        print("{:25} ${:13.2f}{:11} ${:13.2f}".format(donor, total_donated,
                                                total_donations, donations_avg))


if __name__ == '__main__':
    driver = login_database.login_neo4j_cloud()
    
    generate_report()
