#!/usr/bin/env python3

"""
Lesson8 - Mailrom Neo4j
"""

import os
import datetime
import re
from queries_neo4j import *  # noqa F403
from utilities import *  # noqa F403
from model import *  # noqa F403

now = datetime.datetime.now()
log = utilities.configure_logger('default', './logs/redis_script.log')  # noqa F403


class Mailroom:

    @staticmethod
    def list_donors():
        qn = QueriesNeo4j()  # noqa F403
        dl = qn.get_donors()
        nl = []
        for i, d in enumerate(dl, start=1):
            nl.append(f"{i} - {d['first_name']} {d['last_name']}")
        print('\n\nSelect donor ID (int):')
        print(*nl, sep='\n')
        print('\n\n')
        return dl

    @staticmethod
    def sort_donors():
        qn = QueriesNeo4j()  # noqa F403
        donors = qn.get_donor_multiple_summary()
        sd = sorted(donors, key=lambda d: d[2], reverse=True)
        log.info('Donors sorted.')
        return sd

    @staticmethod
    def prep_donor_summary(donors):
        """ pass summary list of strings that is ready for parsing """
        summary = []
        for d in donors:
            name = f"{d[0]} {d[1]}"
            str_total = Utilities.format_currency_str(str(d[2]))  # noqa F403
            str_number = str(d[3])
            str_average = Utilities.format_currency_str(str(d[4]))  # noqa F403
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
        donors = mc.sort_donors()
        for d in donors:
            file_path = "{}{}_{}_{}{}".format(path, date,
                                              d[0],
                                              d[1],
                                              ext)
            donations = Utilities.format_currency_str(d[2])  # noqa F4033
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


class MailroomPrompts:

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

    def prompt_index(self):
        mc = Mailroom()
        qn = QueriesNeo4j()  # noqa F403
        nodes = mc.list_donors()  # Use main DB here

        while True:
            index = self.prompt('Enter the numer of the donor (int): ')
            try:
                index = int(index)
                if index < 1 or index > len(nodes):
                    print('Please choose a number from the list above')
                    continue

                d = qn.get_donor_by_id(nodes[index - 1].id)

                if not d:
                    print('Sorry, this ID does not exist.')
                    continue

                break
            except ValueError:
                print('Please enter an integer.')

        return d

    def prompt_donor_update(self):
        qn = QueriesNeo4j()  # noqa F403
        d = self.prompt_index()

        first_name = self.prompt("Updated first name: ").strip()
        last_name = self.prompt("Updated last name: ").strip()
        email = self.prompt("Updated email: ").strip()
        phone = self.prompt("Updated phone: ").strip()
        zip_code = self.prompt("Updated zip code: ").strip()

        ud = Donor()  # noqa F403
        ud.first_name = first_name
        ud.last_name = last_name
        ud.email = email
        ud.phone = phone
        ud.zip_code = zip_code
        qn.update_donor(d, ud)

    def prompt_donor_insert(self):

        while True:
            qn = QueriesNeo4j()  # noqa F403
            first_name = self.prompt("Enter first name: ").strip()
            last_name = self.prompt("Enter last name: ").strip()
            donor = qn.get_donor_by_last(last_name)
            if donor:
                print('Donor already exists, use append.')
            else:
                break

        while True:
            email = self.prompt('Email address: ')
            try:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    continue
                break
            except ValueError:
                print('Please enter a valid email.')

        phone = self.prompt('Phone: ')
        zip_code = self.prompt('Zip code: ')

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
        d.email = email
        d.phone = phone
        d.zip_code = zip_code
        d.donations = donation
        qn.insert_donor(d)

        donation = Utilities.format_currency_str(donation)  # noqa F403
        mc = Mailroom()
        mc.donor_single_email(first_name, last_name, donation)

    def prompt_donor_delete(self):
        qn = QueriesNeo4j()  # noqa F403
        d = self.prompt_index()
        qn.delete_donor(d)

    def prompt_donation_insert(self):
        mc = Mailroom()
        qn = QueriesNeo4j()  # noqa F403
        d = self.prompt_index()

        while True:
            donation = self.prompt('Enter donation amount: ')
            try:
                donation = float(donation)
                break
            except ValueError:
                print('Please enter a float.')

        qn.insert_donation(d, donation)
        mc.donor_single_email(d['first_name'], d['last_name'], donation)

    def prompt_summary(self):
        mc = Mailroom()
        qn = QueriesNeo4j()  # noqa F403
        d = self.prompt_index()
        dl = qn.get_donor_single_summary(d)
        dl = mc.prep_donor_summary(dl)
        mc.print_report(dl)

    def prompt_thank_donor(self):
        mc = Mailroom()
        qn = QueriesNeo4j()  # noqa F403
        d = self.prompt_index()

        donations = qn.donations_total(d)
        donations = Utilities.format_currency_str(donations)  # noqa F403
        mc.donor_multiple_email(d['first_name'], d['last_name'], donations)

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
    MailroomPrompts().main_menu()
    # qn = QueriesNeo4j()  # noqa F403
    # qn.setup_data()
    # qn.drop_donors()
    # qn.get_donors()
    # qn.get_donor_by_last('Halpert')
    # qn.get_donor_by_id(14)
