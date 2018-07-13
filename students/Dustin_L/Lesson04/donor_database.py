#!/usr/bin/env python3
"""This module contains the Donor Database class"""

import datetime
import json
import json_save_meta as js
from collections import defaultdict
from donor import Donor


class DonorDict(defaultdict, js.Dict):
    """A default dictionary intended for containing Donor objects"""
    def __init__(self, *donors):
        if not donors:
            donors = []
        super().__init__(Donor, {d.name: d for d in donors})

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class DonorDatabase(js.JsonSaveable):
    """A database of Donors"""

    _donors = DonorDict()
    min_col_width = js.Int()
    def_pad = js.Int()
    col_sep = js.String()
    cols = js.List()
    thank_you_fmt = js.String()

    def __init__(self, *donors):
        if not donors:
            donors = []

        self._donors = DonorDict(*donors)
        self.min_col_width = 12
        self.def_pad = 7
        self.col_sep = ' | '
        self.cols = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gift']
        self.thank_you_fmt = ('\nDear {:s},\n'
                              'Thank you for your generous donation of ${:,.2f}.\n'
                              '\t\tSincerely,\n'
                              '\t\t  -Your conscience')

    def __contains__(self, item):
        return item in self._donors.values()

    def __getitem__(self, key):
        return self._donors[key]

    def __iter__(self):
        for donor in self._donors.values():
            yield donor
        return

    # def __next__(self):
    #     for donor in self._donors.values():
    #         yield donor
    #     return

    def __setitem__(self, key, value):
        self._donors[key] = value

    def challenge(self, factor, min_don=None, max_don=None):
        """Return a new database with all donations multiplied by the factor
           value if within the specified min and max donation range.

        Args:
            factor (float): Factor value
            min_don (float, optional): Defaults to None. Min donation value
            max_don (float, optional): Defaults to None. Max donation value

        Returns:
            DonorDatabase: New DonorDatabase with factor value applied
        """
        new_donors = []
        for donor in self:
            new_donors.append(Donor(donor.name,
                                    self.filter_and_factor(factor,
                                                           donor.donations,
                                                           min_don=min_don,
                                                           max_don=max_don)))
        return DonorDatabase(*new_donors)

    def create_report(self):
        """Generate report of all donors and donations in database."""
        sorted_dnr_keys = sorted(self.keys(),
                                 key=lambda d: self[d].total_donations,
                                 reverse=True)

        max_name = len(max([name for name in self.keys()], key=len)) + self.def_pad
        max_total = len(max([str(d.total_donations)
                             for d in self], key=len)) + self.def_pad
        max_gifts = len(max([str(d.num_donations)
                             for d in self], key=len)) + self.def_pad
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

    def keys(self):
        """Generator providing name of each donor in database"""
        for donor in self._donors:
            yield donor

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

    def items(self):
        """Generator yielding name of each donor and the donor itself"""
        for name, donor in self._donors.items():
            yield (name, donor)

    @classmethod
    def load(cls, _json):
        """Generates a Donor Database based on the passed json file"""
        if isinstance(_json, str):
            return cls.from_json_dict(json.loads(_json))
        else:  # assume a file-like object
            return cls.from_json_dict(json.load(_json))

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
        for donor in self:
            projection += sum(self.filter_and_factor(factor,
                                                     donor.donations,
                                                     min_don=min_don,
                                                     max_don=max_don))
        return projection

    def save(self):
        """Saves the current Donor Database to a json file"""
        now = datetime.datetime.today().strftime('%m-%d-%Y')
        f_name = f'donor_dict_{now}.json'

        with open(f_name, 'w') as f:
            f.write(self.to_json())

    def send_letters(self):
        """Create a letter for each donor and write to disk as a text file"""
        now = datetime.datetime.today().strftime('%m-%d-%Y')

        for donor, data in self.items():
            f_name = f'{donor.replace(" ", "_")}_{now}.txt'
            with open(f_name, 'w') as f:
                f.write(self.thank_you_fmt.format(donor, data.total_donations))
