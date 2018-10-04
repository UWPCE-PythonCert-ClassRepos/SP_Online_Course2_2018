#!/usr/bin/env python3

"""
Lesson7 - Metaprogrammed DB
"""

import os
import datetime
import logging
from peewee import *  # noqa F403
from models import *  # noqa F403
from queries import *  # noqa F403
from helpers import *  # noqa F403

now = datetime.datetime.now()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('mailroom.db')  # noqa F403
database.execute_sql('PRAGMA foreign_keys = ON;')


class Mailroom:

    def __init__(self):
        self.donors = None

    @staticmethod
    def list_donors():
        q = Queries()  # noqa F403
        dl = q.get_donors()
        dl = [f"id: {d.id} -- {d.first_name} {d.last_name}" for d in dl]
        print('\n\nSelect donor ID (int):')
        print(*dl, sep='\n')
        print('\n\n')

    @staticmethod
    def sort_donors():
        q = Queries()  # noqa F403
        donors = q.get_donor_multiple_summary()
        sd = sorted(donors, key=lambda d: d[2], reverse=True)
        logger.info('Donors sorted.')
        return sd

    @staticmethod
    def prep_donor_summary(donors):
        """ pass summary list of strings that is ready for parsing """
        summary = []
        for d in donors:
            name = f"{d[0]} {d[1]}"
            str_total = Helpers.format_currency_str(str(d[2]))  # noqa F403
            str_number = str(d[3])
            str_average = Helpers.format_currency_str(str(d[4]))  # noqa F403
            summary.append([name, str_total, str_number, str_average])
        return summary

    @staticmethod
    def donor_single_email(first_name, last_name, donation):
        m = ('\n\nDear {} {},\n\n'
             '        Thank you for your very kind donation of {}.\n\n'
             '        It will be put to very good use.\n\n'
             '               Sincerely,\n'
             '                  -The Team\n\n')
        print(m.format(first_name, last_name, donation))

    @staticmethod
    def donor_multiple_email(first_name, last_name, donations):
        m = ('\n\nDear {} {},\n\n'
             '        Thank you for your very kind donations totalling {}.\n\n'
             '        It will be put to very good use.\n\n'
             '               Sincerely,\n'
             '                  -The Team\n\n')
        print(m.format(first_name, last_name, donations))

    def generate_letters(self):
        cwd = os.getcwd()
        date = now.strftime('%Y-%m-%d')
        path = cwd + '/letters/'
        ext = '.txt'
        mc = Mailroom()
        q = Queries()  # noqa F403
        donors = mc.sort_donors()
        for d in donors:
            file_path = "{}{}_{}_{}{}".format(path, date,
                                              d[0],
                                              d[1],
                                              ext)
            donations = Helpers.format_currency_str(d[2])  # noqa F4033
            with open(file_path, 'w') as letter:
                text = ('\n\nDear {} {},\n\n'
                        '        Thank you for your very kind '
                        'donations totaling {}.\n\n'
                        '        It will be put to very good use.\n\n'
                        '               Sincerely,\n'
                        '                  -The Team\n\n')
                body = text.format(d[0], d[1], donations)
                letter.write(body)
        print('\n\n========== Letters Created ==========\n\n')

    def create_report(self):
        sorted_donors = self.sort_donors()
        rows = self.prep_donor_summary(sorted_donors)
        self.print_report(rows)

    @staticmethod
    def print_report(rows):
        # table heading
        h = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gift']
        hs = ' | '
        hf = '{0:<25}{1}{2}{3}{4}{5}{6}'
        # table rows
        print('\n\n')
        print(hf.format(h[0], hs, h[1], hs, h[2], hs, h[3]))
        for r in rows:
            name = "{}".format(r[0])
            f0 = '{0:<' + str(max(len(name), 25)) + '}'
            f2 = '{2:>' + str(max(len(r[1]), len(h[1]))) + '}'
            f4 = '{4:>' + str(max(len(r[2]), len(h[2]))) + '}'
            f6 = '{6:>' + str(max(len(r[3]), len(h[3]))) + '}'
            rf = f0 + '{1}' + f2 + '{3}' + f4 + '{5}' + f6
            args = [name, '  $', r[1], ' | ', r[2], '  $', r[3]]
            print(rf.format(*args))
        print('\n\n')


class MailroomCli:

    @staticmethod
    def prompt(msg):
        while True:
            val = input(msg)
            try:
                if val is None:
                    raise ValueError()
            except ValueError:
                print('Value required.')
                continue
            return val

    def prompt_donor_update(self):
        mc = Mailroom()
        q = Queries()  # noqa F403
        mc.list_donors()
        donor = None

        while True:
            donor_id = self.prompt('Enter ID of the donor: ')
            try:
                donor_id = int(donor_id)
                donor = q.get_donor_by_id(donor_id)

                if donor is False:
                    print('Sorry, this ID does not exist.')
                    continue

                break
            except ValueError:
                print('Please enter an integer.')

        first_name = self.prompt("Updated first name: ").strip()
        last_name = self.prompt("Updated last name: ").strip()
        q.update_donor(donor.id, first_name, last_name)

    def prompt_donor_insert(self):
        mc = Mailroom()
        while True:
            q = Queries()  # noqa F403
            first_name = self.prompt("Enter first name: ").strip()
            last_name = self.prompt("Enter last name: ").strip()
            donor = q.get_donor_by_last(last_name)
            if donor is False:
                break
            else:
                print('Donor already exists, use append.')

        while True:
            donation = self.prompt('Enter donation amount: ')
            try:
                donation = float(donation)
                break
            except ValueError:
                print('Please enter a float.')

        d = Donor()  # noqa F403
        d.first_name = first_name
        d.last_name = last_name
        q.insert_donor_donation(d, float(donation))
        donation = Helpers.format_currency_str(donation)  # noqa F403
        mc.donor_single_email(first_name, last_name, donation)

    def prompt_donor_delete(self):
        mc = Mailroom()
        q = Queries()  # noqa F403
        mc.list_donors()
        donor = None

        while True:
            donor_id = self.prompt('Enter ID of the donor: ')
            try:
                donor_id = int(donor_id)
                donor = q.get_donor_by_id(donor_id)

                if donor is False:
                    print('Sorry, this ID does not exist.')
                    continue

                break
            except ValueError:
                print('Please enter an integer.')

        q.delete_donor_donations(donor_id)

    def prompt_donation_insert(self):
        mc = Mailroom()
        q = Queries()  # noqa F403
        mc.list_donors()
        donor = None

        while True:
            donor_id = self.prompt('Enter ID of the donor: ')
            try:
                donor_id = int(donor_id)
                donor = q.get_donor_by_id(donor_id)

                if donor is False:
                    print('Sorry, this ID does not exist.')
                    continue

                break
            except ValueError:
                print('Please enter an integer.')

        while True:
            donation = self.prompt('Enter donation amount: ')
            try:
                donation = float(donation)
                break
            except ValueError:
                print('Please enter a float.')

        q.insert_donation(donor_id, donation)
        mc.donor_single_email(donor.first_name, donor.last_name, donation)

    def prompt_summary(self):
        mc = Mailroom()
        q = Queries()  # noqa F403
        mc.list_donors()
        donor = None

        while True:
            donor_id = self.prompt('Enter ID of the donor: ')
            try:
                donor_id = int(donor_id)
                donor = q.get_donor_by_id(donor_id)

                if donor is False:
                    print('Sorry, this ID does not exist.')
                    continue

                break
            except ValueError:
                print('Please enter an integer.')

        dl = q.get_donor_single_summary(donor_id)
        dl = mc.prep_donor_summary(dl)
        mc.print_report(dl)

    def prompt_thank_donor(self):
        mc = Mailroom()
        q = Queries()  # noqa F403
        mc.list_donors()
        donor = None

        while True:
            donor_id = self.prompt('Enter ID of the donor: ')
            try:
                donor_id = int(donor_id)
                donor = q.get_donor_by_id(donor_id)

                if donor is False:
                    print('Sorry, this ID does not exist.')
                    continue

                break
            except ValueError:
                print('Please enter an integer.')

        donations = q.donations_total(donor_id)
        donations = Helpers.format_currency_str(donations)  # noqa F403
        mc.donor_multiple_email(donor.first_name, donor.last_name, donations)

    @staticmethod
    def quit_menu():
        return 'break'

    def main_menu(self):
        main_prompt = ("\n--- MAIN MENU ---\n"
                       "What do you want to do?\n"
                       "Type '1' - Donors Menu\n"
                       "Type '2' - Reports Menu\n"
                       "Type '3' - Gratitude Menu\n"
                       "Type 'q' - Quit >> "
                       )
        main_dispatch = {'1': self.donors_sub_menu,
                         '2': self.reports_sub_menu,
                         '3': self.gratitude_sub_menu,
                         'q': self.quit_menu
                         }
        self.menu_selection(main_prompt, main_dispatch)

    def donors_sub_menu(self):
        mc = Mailroom()
        donors_prompt = ("\n--- DONOR SUB MENU ---\n"
                         "Type '1' - Add Donor\n"
                         "Type '2' - Edit Donor\n"
                         "Type '3' - Delete Donor\n"
                         "Type '4' - Add Donation\n"
                         "Type '5' - List Donors\n"
                         "Type 'q' - Quit >> "
                         )
        donors_dispatch = {'1': self.prompt_donor_insert,
                           '2': self.prompt_donor_update,
                           '3': self.prompt_donor_delete,
                           '4': self.prompt_donation_insert,
                           '5': mc.list_donors,
                           'q': self.quit_menu,
                           }
        self.menu_selection(donors_prompt, donors_dispatch)

    def reports_sub_menu(self):
        mc = Mailroom()
        reports_prompt = ("\n--- REPORTS SUB MENU ---\n"
                          "Type '1' - Donors Report\n"
                          "Type '2' - Donor Summary\n"
                          "Type 'q' - Quit >> "
                          )
        reports_dispatch = {'1': mc.create_report,
                            '2': self.prompt_summary,
                            'q': self.quit_menu,
                            }
        self.menu_selection(reports_prompt, reports_dispatch)

    def gratitude_sub_menu(self):
        mc = Mailroom()
        gratitude_prompt = ("\n--- GRATITUDE SUB MENU ---\n"
                            "Type '1' - Print Individual Letter\n"
                            "Type '2' - Generate Letters for All Donors\n"
                            "Type 'q' - Quit >> "
                            )
        gratitude_dispatch = {'1': self.prompt_thank_donor,
                              '2': mc.generate_letters,
                              'q': self.quit_menu,
                              }
        self.menu_selection(gratitude_prompt, gratitude_dispatch)

    @staticmethod
    def menu_selection(prompt, dispatch):
        while True:
            r = input(prompt)
            if r not in dispatch:
                print('Please choose a valid menu option.')
                continue
            if dispatch[r]() == "break":
                break


if __name__ == "__main__":
    MailroomCli().main_menu()
