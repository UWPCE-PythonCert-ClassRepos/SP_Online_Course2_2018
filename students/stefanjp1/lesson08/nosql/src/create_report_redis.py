from mailroom_redis import *


def generate_report():
    """ Prints out a report of each donor's total donations and average gift """
    
    print("Donor Name                | Total Given | Num Gifts | Average Gift\n")
    print('------------------------------------------------------------------')

    all_donors = r.keys()

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
    r = login_database.login_redis_cloud()
    
    generate_report()
