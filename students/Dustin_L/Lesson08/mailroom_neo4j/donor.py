#!/usr/bin/env python3
"""Module containing the Donor class"""


class Donor:
    """Contains all information for a single donor"""

    def __init__(self, name, donations=None):
        if not donations:
            donations = []

        self.name = str(name)
        self._donations = list(donations)
        self._total = sum(self._donations)
        self._ave = self._total / len(self._donations) if donations else 0

    @property
    def donations(self):
        """Get list of donations for this donor"""
        return self._donations

    @property
    def num_donations(self):
        """Get number of donations given by this donor"""
        return len(self._donations)

    @property
    def total_donations(self):
        """Get total amount of donations given by this donor"""
        return self._total

    @property
    def average_donations(self):
        """Get average donation amount for this donor"""
        return self._ave

    def add_donation(self, amount):
        """Add donation to this donor's donation history

        Args:
            donation (int): donation amount
        """
        self._donations.append(amount)
        self._total += amount
        self._ave = self._total / self.num_donations
