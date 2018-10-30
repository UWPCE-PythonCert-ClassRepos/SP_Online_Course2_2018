from mailroom_class import *


def generate_report():
    """ Prints out a report of each donor's total donations and average gift """
    
    print("Donor Name                | Total Given | Num Gifts | Average Gift\n")
    print('------------------------------------------------------------------')

    all_donors = Donor_Records.select(Donor_Records.donor_name)

    for donor in all_donors:
        total_donations, total_donated = donor_totals(donor.donor_name)
        if total_donations > 0:
            donations_avg = total_donated / total_donations
        else:
            donations_avg = 0
            total_donations = 0
            total_donated = 0
        print("{:25} ${:13.2f}{:11} ${:13.2f}".format(donor.donor_name, total_donated,
                                                total_donations, donations_avg))


if __name__ == '__main__':
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    generate_report()

    database.close()