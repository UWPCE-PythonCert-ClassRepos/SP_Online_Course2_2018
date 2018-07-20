from helpers import main_menu, set_donor_name
from db_ops import update_donations, list_donors, add_donor, create_report, send_thankyou, save_report
import sys


def thankyou_procedure():
    donor_name = set_donor_name()
    if donor_name.lower() == 'list':
        print(list_donors())
    elif donor_name in list_donors():
         send_thankyou(donor_name)
    else:
        add_donor(donor_name)


def main():
    while True:
        users_choice = main_menu()
        selection = {
            '1': thankyou_procedure,
            '2': create_report,
            '3': save_report,
            '4': sys.exit
        }
        try:
            selection[users_choice]()
        except KeyError:
            print('Choose 1 to 4')
            pass
