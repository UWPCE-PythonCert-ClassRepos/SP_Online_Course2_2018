#!/usr/bin/env python3
"""This module contains the Donor Database class"""

import configparser
import datetime
import json
import redis
from pathlib import Path
from collections import defaultdict
from donor import Donor

config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


class DonorDict(defaultdict):
    """A database of Donors"""

    name_key = 'name'
    donations_key = 'donations'
    email_key = 'email'
    thank_you_fmt = ('\nDear {:s},\n'
                     'Thank you for your generous donation of ${:,.2f}.\n'
                     '\t\tSincerely,\n'
                     '\t\t  -Your conscience')

    def __init__(self):
        super().__init__(Donor)
        self.min_col_width = 12
        self.def_pad = 7
        self.col_sep = ' | '
        self.cols = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gift']

        try:
            config.read(config_file)
            host = config['redis_cloud']['host']
            port = config['redis_cloud']['port']
            psw = config['redis_cloud']['pw']
        except KeyError as e:
            print('Unable to read config file: ', e)
            raise e

        self.db_name = 'Mailroom'
        self._redis = redis.StrictRedis(
            host=host, port=port, password=psw, decode_responses=True)
        self._update_dict()

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret

    def _update_dict(self):
        d_str = self._redis.get(self.db_name)
        if d_str:
            donors = json.loads(d_str)
            for d in donors:
                self[d[self.name_key]] = Donor(d[self.name_key],
                                               d[self.donations_key])

    def add_donation(self, donor, donation):
        """Adds donation to database

        Args:
            donor (str): Donor name
            donation (float): Donation amount
        """
        donors = json.loads(self._redis.get(self.db_name))
        for d in donors:
            if d[self.name_key].lower() == donor.lower():
                d[self.donations_key].append(donation)
                break
        else:
            donors.append({
                self.name_key: donor,
                self.donations_key: [donation]
            })

        self._redis.set(self.db_name, json.dumps(donors))
        self._update_dict()

    def challenge(self, factor, min_don=None, max_don=None):
        """Return a new database with all donations multiplied by the factor
           value if within the specified min and max donation range.

        Args:
            factor (float): Factor value
            min_don (float, optional): Defaults to None. Min donation value
            max_don (float, optional): Defaults to None. Max donation value

        Returns:
            DonorDict: New DonorDict with factor value applied
        """
        new_donors = []
        for donor in self.values():
            new_donors.append(Donor(donor.name,
                                    self.filter_and_factor(factor,
                                                           donor.donations,
                                                           min_don=min_don,
                                                           max_don=max_don)))
        return DonorDict(*new_donors)

    def create_report(self):
        """Generate report of all donors and donations in database."""
        sorted_dnr_keys = sorted(self,
                                 key=lambda d: self[d].total_donations,
                                 reverse=True)

        max_name = len(max([dnr
                            for dnr in self.keys()], default=[], key=len)) + self.def_pad
        max_total = len(max([str(d.total_donations)
                             for d in self.values()], default=[], key=len)) + self.def_pad
        max_gifts = len(max([str(d.num_donations)
                             for d in self.values()], default=[], key=len)) + self.def_pad
        max_ave = max_total

        if max_name < self.min_col_width:
            max_name = self.min_col_width
        if max_total < self.min_col_width:
            max_total = max_ave = self.min_col_width
        if max_gifts < self.min_col_width:
            max_gifts = self.min_col_width

        hdr_fmt = (f'\n{{:^{max_name}s}}{self.col_sep}{{:^{max_total}s}}'
                   f'{self.col_sep}{{:^{max_gifts}s}}{self.col_sep}'
                   f'{{:^{max_ave}s}}\n' +
                   '-' * (max_name + max_total + max_gifts + max_ave +
                          len(self.col_sep) * 3) +
                   '\n')

        row_fmt = (f'{{:<{max_name}s}}{self.col_sep}${{:>{max_total - 1},.2f}}'
                   f'{self.col_sep}{{:>{max_gifts}d}}{self.col_sep}'
                   f'${{:>{max_ave - 1},.2f}}')

        header = hdr_fmt.format(*self.cols)

        rows = [row_fmt.format(dnr, self[dnr].total_donations,
                               self[dnr].num_donations,
                               self[dnr].average_donations)
                for dnr in sorted_dnr_keys]

        return header + '\n'.join(rows)

    def donor_names(self):
        """Generator yielding all donor names in database"""
        donors = json.loads(self._redis.get(self.db_name))
        for donor in donors:
            yield donor[self.name_key]

    @staticmethod
    def filter_and_factor(factor, donations, min_don=None, max_don=None):
        """For each donation, multiply by the factor value if the donation is
           within the min and max donation range, if set.

        Args:
            factor (float): Factor value
            donations (list): List of donations to filter and factor
            min_don (float, optional): Defaults to None. Min donation value
            max_don (float, optional): Defaults to None. Max donation value

        Raises:
            ValueError: Min donation value is greater than max value

        Returns:
            list: New list of filtered and factored donations
        """
        if min_don and max_don:
            if min_don > max_don:
                raise ValueError('Min donation value is greater than max')

            return list(map(lambda x: x * factor,
                            filter(lambda d: min_don <= d <= max_don, donations)))
        elif min_don:
            return list(map(lambda x: x * factor,
                            filter(lambda d: d >= min_don, donations)))
        elif max_don:
            return list(map(lambda x: x * factor,
                            filter(lambda d: d <= max_don, donations)))
        else:
            return list(map(lambda x: x * factor, donations))

    def lookup_email(self, donor):
        """Looks up the email address for the specified donor.

        Args:
            donor (str): Donor name.

        Returns:
            str: Donor email address, None if done does not exist.
        """
        d_str = self._redis.get(self.db_name)
        if d_str:
            donors = json.loads(d_str)
            for d in donors:
                if d[self.name_key].lower().startswith(donor.lower()):
                    return d[self.email_key]
        return None

    def purge_db(self):
        """Purges the database"""
        donors = self._redis.delete(self.db_name)
        donors = [d for d in self]
        for d in donors:
            del self[d]

    def projection(self, factor, min_don=None, max_don=None):
        """Return projection for a contribution that multiplies all current
        donations by 'factor' that are within the specified min and max
        donation range, if specified.

        Args:
            factor (float): Factor value
            min_don (float, optional): Defaults to None. Min donation value
            max_don (float, optional): Defaults to None. Max donation value

        Returns:
            float: Projected contribution value
        """
        projection = 0
        for donor in self.values():
            projection += sum(self.filter_and_factor(factor,
                                                     donor.donations,
                                                     min_don=min_don,
                                                     max_don=max_don))
        return projection

    def send_letters(self):
        """Create a letter for each donor and write to disk as a text file"""
        now = datetime.datetime.today().strftime('%m-%d-%Y')

        for donor, data in self.items():
            f_name = f'{donor.replace(" ", "_")}_{now}.txt'
            with open(f_name, 'w') as f:
                f.write(self.thank_you_fmt.format(donor, data.total_donations))
