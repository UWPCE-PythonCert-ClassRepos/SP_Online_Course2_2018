#!/usr/bin/python3

## Author/student:  Roy Tate (githubtater)

import os
import json_save_dec as jsd
import json

@jsd.json_save
class Donor:
    name = jsd.String()
    donations = jsd.List()

    def __init__(self, name, donations=None):
        self.name = name.title()
        self.donations = donations if donations else []


    def __str__(self):
        return 'Donor name: {}  Donations: {}'.format(self.name, str(sum(self.donations)))

    def __repr__(self):
        return 'Donor({}, {})'.format(self.name, self.donations)

    def add_donation(self, new_donation):
        return self.donations.append(new_donation)

    @property
    def total_donations(self):
        return round(sum(self.donations), 2)

    @property
    def average(self):
        return round(self.total_donations / self.num_gifts, 2)

    @property
    def num_gifts(self):
        return len(self.donations)

    @property
    def max_donation(self):
        return max(self.donations)

    @property
    def min_donation(self):
        return min(self.donations)

    @property
    def all_donations(self):
        return self.donations

    @property
    def letter(self):
        text = '''\n
From:    A Charity Thankful For Your Kindness
To:      {0}
Subject:  This Year's Challenge!

Dear {0},

First, we would like to thank you for your continued generosity throughout the 
years. Without contributions like yours, the good things that we are able to do 
simply would not be possible. 

Your contributions to date have totaled ${1:.2f}. 

This years challenge is to see if you can donate more than your current total
in one year. This would effectively double your current donations to the 
organization!  Remember, it is for a good cause!

Sincerely,

The good guys at the best organization
'''

        return text.format(self.name, sum(self.donations))


@jsd.json_save
class DonorCollection:
    donors = jsd.List()

    def __init__(self, donors=None):
        self.donors = donors if donors else []

    def __repr__(self):
        return 'DonorCollection()'

    def save_json(self):
        """Save Donor DB to JSON file."""
        donors_json = jsd._to_json_compat(self)
        filename = 'donorsDB.json'
        with open(filename, 'w+') as f:
            json.dump(donors_json, f)
        print(f'Donors saved to JSON file: {os.path.realpath(filename)}')

    def load_json(self):
        """Load a Donor JSON file to application"""
        global donors
        filename = 'donorsDB.json'
        with open(filename, 'r') as infile:
            donor_dict = json.load(infile)
            donor_list = self.from_json_dict(donor_dict)
            self.donors = donor_list.donors
            print(f'Successfully loaded file: {filename}')
        return self.donors

    def add_donor(self, other):
        new_donation = 0
        for donor in self.donors:
            if donor.name == other.name:
                if isinstance(other.donaations, list):
                    for d in list:
                        donor.donations.append(d)
                if isinstance(other.donations, (int, float)):
                    donor.donations.append(other.donations)
        else:
            self.donors.append(other)

    def create_report(self, title='DONATION REPORT'):
        format_str = '{:<25}${:<15}{:<15}{:<15}{:<15}{:<15}'
        report = '\n{:-^100}\n'.format(title)
        report += (format_str+'\n').format('Name', 'Total Given', '# of Gifts', 'Average', 'Max', 'Min')
        total_sum = 0
        for d in self.donors:
            donor_values = (d.name, str(d.total_donations), d.num_gifts, str(d.average),
                            str(d.max_donation), str(d.min_donation))
            report += (format_str + '\n').format(*donor_values)
            total_sum += d.total_donations
        report += format_str.format('TOTAL', total_sum, '', '', '', '')
        return report

    def create_projection_report(self, title):
        format_str = '{:<25}{:<17}{:<15}{:<15}{:<15}'
        report = '\n{:*^100}\n'.format(f'  Projection Report - {title}  ')
        report += (format_str+'\n').format('Name', 'New_Total_Given', 'New_Max', 'New_Min', 'Average')
        for donor in self.donors.values():
            donor_values = (v.name, '$' + str(v.total_donations), str(v.max_donation), str(v.max_donation),
                            str(v.min_donation), str(v.average))
            report += (format_str + '\n').format(*donor_values)
        return report

    def save_emails(self, directory=''):
        cwd = os.getcwd()
        if not directory:
            directory = cwd
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        finally:
            os.chdir(directory)
            directory = os.getcwd()
            letters = [donor.letter for donor in self.donors]
            donor_names = [donor.name+'.txt' for donor in self.donors]
            for letter, donor_name in zip(letters, donor_names):
                full_file_path = os.path.join(directory, donor_name.replace(' ', '_'))
                with open(full_file_path, 'w+') as f:
                    f.write(letter)
                    print(f'File written: {full_file_path}')
            return directory

    def challenge(self, factor, min_donation=1.00, max_donation=1e11):
        """Increase all donations in the database by a factor
        Args:
            factor:  the amount to multiply the donatoins by
            min_donation:  the minimum donation to filter
            max_donation:  the maximum donation to filter
        Return
            self.new_collection:  a DonorCollection() of the donors with donation values multiplied by the factor"""
        # print('The Challenge module was broken in this release.')
        self.factor = factor
        self.new_collection = DonorCollection()
        for donor in self.donors:
            multiplied_data = map(lambda x: x * factor, donor.all_donations)
            self.new_collection.add(donor.name, list(multiplied_data))
        return self.new_collection


    def run_projections(self, min_donation=50, max_donation=100):
        """Run an automated projection report for tripling donations under $50 and doubling donations over $100
        Args:
            None
        Returns:
            projection_collection50:  a DonorCollection() with donors and their donations under $50, tripled
            projection_collection100:  a DonorCollection() with donors and their donations over $100, doubled"""
        projection_coll50 = DonorCollection()
        projection_coll50.donors = self.donors
        projection_coll100 = DonorCollection()
        projection_coll100.donors = self.donors
        for donor in projection_coll50.donors:
            under_50_filter = map(lambda x: x * 3, filter(lambda y:  y <= min_donation, donor.donations))
            print(list(under_50_filter))
            over_100_filter = map(lambda x: x * 2, filter(lambda y:  y >= max_donation, donor.donations))
        return projection_coll50, projection_coll100
