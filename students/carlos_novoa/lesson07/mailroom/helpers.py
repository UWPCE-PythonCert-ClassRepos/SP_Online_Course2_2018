"""
Module contains helper functions
"""


class Helpers():

    @staticmethod
    def format_currency_str(amount):
        return "${0:.2f}".format(float(amount))
