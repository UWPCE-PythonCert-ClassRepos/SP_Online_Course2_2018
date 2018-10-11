#!/usr/bin/env python3
import os
import datetime
import json_save.json_save_meta as js
from collections import OrderedDict
from inspect import Parameter, Signature

now = datetime.datetime.now()

"""
Lesson4 - Metaprogrammed Mailroom
"""


def format_currency_str(amount=None):
    return "${0:.2f}".format(float(amount))


class DonorData(js.JsonSaveable):
    data = js.List()

    def __init__(self, data):
        self.data = data


class Donors:

    def __init__(self):
        self.donors = None

    def read_from_file(self, filename):
        with open(filename) as f:
            return f.read()

    def write_to_file(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)

    def load_donors(self, reset=False):
        filename = 'donors_reset.json' if reset else 'donors.json'
        data = self.read_from_file(filename)
        dObj = js.from_json(data)
        self.donors = dObj

    def save_donors(self):
        data = DonorData(self.donors.data)
        formatted = data.to_json()
        self.write_to_file('donors.json', formatted)

    def list_donors(self):
        for d in self.donors.data:
            print(f"{d['fname']} {d['lname']}")

    def sort_donors(self):
        sl = sorted(self.donors.data, key=lambda x: sum(x['donations']),
                    reverse=True)
        return sl

    def donor_found(self, fname='', lname=''):
        return any(d['fname'] == fname and
                   d['lname'] == lname for d in self.donors.data)

    @staticmethod
    def get_donor_summary(donors):
        """ pass summary list of strings that is ready for parsing """
        summary = []
        for d in donors:
            name = f"{d['fname']} {d['lname']}"
            donations = d['donations']
            total = float(sum(donations))
            number = len(donations)
            str_total = format_currency_str(total)
            str_number = str(len(donations))
            str_average = format_currency_str(total / max(number, 1))
            summary.append([name, str_total, str_number, str_average])
        return summary

    @staticmethod
    def donor_email(fname, lname, donations):
        m = ('\n\nDear {} {},\n\n'
             '        Thank you for your very kind donations totalling {}.\n\n'
             '        It will be put to very good use.\n\n'
             '               Sincerely,\n'
             '                  -The Team\n\n')
        print(m.format(fname, lname, donations))

    def generate_letters(self):
        cwd = os.getcwd()
        date = now.strftime('%Y-%m-%d')
        path = cwd + '/letters/'
        ext = '.txt'
        for d in self.donors.data:
            total_donations = sum(d['donations'])
            file_path = "{}{}_{}_{}{}".format(path, date,
                                              d['fname'],
                                              d['lname'],
                                              ext)
            donations = format_currency_str(total_donations)
            donations = format_currency_str(total_donations)
            with open(file_path, 'w') as letter:
                text = ('\n\nDear {} {},\n\n'
                        '        Thank you for your very kind '
                        'donation of {}.\n\n'
                        '        It will be put to very good use.\n\n'
                        '               Sincerely,\n'
                        '                  -The Team\n\n')
                body = text.format(d['fname'], d['lname'], donations)
                letter.write(body)
        print('\n\n========== Letters Created ==========\n\n')

    def create_report(self):
        sorted_donors = self.sort_donors()
        rows = self.get_donor_summary(sorted_donors)
        self.print_report(rows)

    @staticmethod
    def print_report(rows):
        # table heading
        h = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gift']
        hs = ' | '
        hf = '{0:<25}{1}{2}{3}{4}{5}{6}'
        print(hf.format(h[0], hs, h[1], hs, h[2], hs, h[3]))
        # table rows
        for r in rows:
            name = "{}".format(r[0])
            f0 = '{0:<' + str(max(len(name), 25)) + '}'
            f2 = '{2:>' + str(max(len(r[1]), len(h[1]))) + '}'
            f4 = '{4:>' + str(max(len(r[2]), len(h[2]))) + '}'
            f6 = '{6:>' + str(max(len(r[3]), len(h[3]))) + '}'
            rf = f0 + '{1}' + f2 + '{3}' + f4 + '{5}' + f6
            args = [name, '  $', r[1], ' | ', r[2], '  $', r[3]]
            print(rf.format(*args))

    def donor_summary(self, fname, lname):
        summary = ('\n\n===========================\n'
                   'Donor: {} {}\n'
                   'Total Donations: {}.\n'
                   'Donation Count: {}\n'
                   'Donation Average: {}\n'
                   '===========================\n\n')
        total = self.donations_total(fname, lname)
        count = self.donations_count(fname, lname)
        average = self.donations_average(fname, lname)
        print(summary.format(fname, lname, total, count, average))

    def donations_total(self, fname=None, lname=None):
        for d in self.donors.data:
            if d['fname'] == fname and d['lname'] == lname:
                return format_currency_str(sum(d['donations']))

    def donations_count(self, fname=None, lname=None):
        for d in self.donors.data:
            if d['fname'] == fname and d['lname'] == lname:
                return len(d['donations'])

    def donations_average(self, fname=None, lname=None):
        for d in self.donors.data:
            if d['fname'] == fname and d['lname'] == lname:
                total = sum(d['donations'])
                count = len(d['donations'])
        return format_currency_str(total / count)


def make_signature(names):
    return Signature(Parameter(
                     name, Parameter.POSITIONAL_OR_KEYWORD)
                     for name in names)


class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Typed(Descriptor):
    ty = object  # Expected type

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError("Expected %s" % self.ty)
        super().__set__(instance, value)


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


class List(Typed):
    ty = list


class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Must be >= 0')
        super().__set__(instance, value)


class StructMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, clsname, bases, clsdict):
        fields = [key for key, val in clsdict.items()
                  if isinstance(val, Descriptor)]

        for name in fields:
            clsdict[name].name = name

        clsobj = super().__new__(cls, clsname, bases, dict(clsdict))

        sig = make_signature(fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj


class Structure(metaclass=StructMeta):
    _fields = []

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)


class Donor(Structure):
    fname = String()
    lname = String()
    donation = Float()  # New donation
    donations = List()  # Overall donations

    def donor_append(self):
        # append existing donor
        mc = Donors()
        mc.load_donors()
        for d in mc.donors.data:
            if d['fname'] == self.fname and d['lname'] == self.lname:
                d['donations'].append(self.donation)
        mc.save_donors()

    def donor_add(self):
        # add new donor
        mc = Donors()
        mc.load_donors()
        mc.donors.data.append({'fname': self.fname, 'lname': self.lname,
                              'donations': [self.donation]})
        mc.save_donors()

    def donor_edit(self, pfname, plname):
        # edit existing donor
        mc = Donors()
        mc.load_donors()
        for d in mc.donors.data:
            if d['fname'] == pfname and d['lname'] == plname:
                d['fname'] = self.fname
                d['lname'] = self.lname
                d['donations'] = self.donations
        mc.save_donors()

    def donor_email(self):
        m = ('\n\nDear {} {},\n\n'
             '        Thank you for your very kind donation of {}.\n\n'
             '        It will be put to very good use.\n\n'
             '               Sincerely,\n'
             '                  -The Team\n\n')
        print(m.format(self.fname, self.lname, self.donation))

    def __str__(self):
        msg = []
        for name, val in vars(self).items():
            msg.append("{}: {}".format(name, val))
        return "\n".join(msg)


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

    def prompt_edits(self):
        mc = Donors()
        mc.load_donors()

        while True:
            fname = self.prompt('Enter first name: ')
            lname = self.prompt('Enter last name: ')
            if mc.donor_found(fname.strip(), lname.strip()) is True:
                for d in mc.donors.data:
                    if d['fname'] == fname and d['lname'] == lname:
                        donations = d['donations']
                break
            else:
                print('\n\nType the exact donor name (see list): ', end='\n\n')
                mc.list_donors()

        dc = Donor(fname, lname, 0.00, donations)

        while True:
            att = input("\n\nWhat attribute would you like to update for:\n\n"
                        "{}\n"
                        '(Type "q" to quit) >> '.format(dc)
                        )
            if att.strip().lower() == "q":
                break
            if not hasattr(dc, att):
                ans = input("This person does not have that attribute.")
                continue

            if att == 'donations':
                ans = input('Enter comma separated floats: ')
                ans = [float(x.strip()) for x in ans.split(',')]
                break
            else:
                ans = input("\n\nWhat would you like to set it to? >> ")
                if att == 'donation':
                    ans = float(ans)
                    donations.append(ans)

            setattr(dc, att, ans)
            dc.donor_edit(fname, lname)
            print(f"\n\nDonor updated: \n\n{dc}")
            break

    def prompt_new_donor(self):
        mc = Donors()
        mc.load_donors()

        while True:
            fname = self.prompt("Enter first name: ")
            lname = self.prompt("Enter last name: ")
            if mc.donor_found(fname.strip(), lname.strip()) is False:
                break
            else:
                print('Donor already exists, use append.')

        donation = self.prompt('Enter donation amount: ')

        dc = Donor(fname, lname, float(donation), [])
        dc.donor_add()
        dc.donor_email()

    def prompt_donation(self):
        mc = Donors()
        mc.load_donors()

        while True:
            fname = self.prompt('Enter first name: ')
            lname = self.prompt('Enter last name: ')
            if mc.donor_found(fname, lname) is False:
                print('\n\nType the exact donor name (see list): ')
                mc.list_donors()
                continue
            else:
                break

        donation = self.prompt('Enter donation amount: ')
        dc = Donor(fname, lname, float(donation), [])
        dc.donor_append()
        dc.donor_email()

    def call_summary(self):
        mc = Donors()
        mc.load_donors()

        while True:
            fname = self.prompt('Enter first name: ')
            lname = self.prompt('Enter last name: ')
            if mc.donor_found(fname.strip(), lname.strip()) is False:
                print('\n\nType the exact donor name (see list): ', end='\n\n')
                mc.list_donors()
                continue
            else:
                break
        mc.donor_summary(fname, lname)

    def thank_donor(self):
        mc = Donors()
        mc.load_donors()

        while True:
            fname = self.prompt('Enter first name: ')
            lname = self.prompt('Enter last name: ')
            if mc.donor_found(fname.strip(), lname.strip()) is True:
                amount = mc.donations_total(fname, lname)
                break
            else:
                print('\n\nType the exact donor name (see list): ', end='\n\n')
                mc.list_donors()
        mc.donor_email(fname, lname, amount)  # total donations

    @staticmethod
    def call_report():
        mc = Donors()
        mc.load_donors()
        mc.create_report()

    @staticmethod
    def call_list():
        mc = Donors()
        mc.load_donors()
        mc.list_donors()

    @staticmethod
    def call_letters():
        mc = Donors()
        mc.load_donors()
        mc.generate_letters()

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
                         'q': self.quit_menu,
                         }
        self.menu_selection(main_prompt, main_dispatch)

    def donors_sub_menu(self):
        donors_prompt = ("\n--- DONOR SUB MENU ---\n"
                         "Type '1' - Add Donor\n"
                         "Type '2' - Edit Donor\n"
                         "Type '3' - Append Donation\n"
                         "Type '4' - List Donors\n"
                         "Type 'q' - Quit >> "
                         )
        donors_dispatch = {'1': self.prompt_new_donor,
                           '2': self.prompt_edits,
                           '3': self.prompt_donation,
                           '4': self.call_list,
                           'q': self.quit_menu,
                           }
        self.menu_selection(donors_prompt, donors_dispatch)

    def reports_sub_menu(self):
        reports_prompt = ("\n--- REPORTS SUB MENU ---\n"
                          "Type '1' - Donors Report\n"
                          "Type '2' - Donor Summary\n"
                          "Type 'q' - Quit >> "
                          )
        reports_dispatch = {'1': self.call_report,
                            '2': self.call_summary,
                            'q': self.quit_menu,
                            }
        self.menu_selection(reports_prompt, reports_dispatch)

    def gratitude_sub_menu(self):
        gratitude_prompt = ("\n--- GRATITUDE SUB MENU ---\n"
                            "Type '1' - Print Individual Letter\n"
                            "Type '2' - Generate Letters for All Donors\n"
                            "Type 'q' - Quit >> "
                            )
        gratitude_dispatch = {'1': self.thank_donor,
                              '2': self.call_letters,
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