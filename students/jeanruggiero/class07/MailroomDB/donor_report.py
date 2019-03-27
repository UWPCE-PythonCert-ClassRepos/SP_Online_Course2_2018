#!/usr/bin/env python
"""
This module contains the functions to create a donor report.
"""
from mailroom_model import *


def create_report():
    """
    Print a report of donors with a summary of their donation
    history.
    """
    donors = (Donor.select().order_by(Donor.donation_total))

    # Determine table size_report
    table_size = size_report(donors)

    # Build format strings for header and table rows
    head_string = '{:{}s} | {:^{}s} | {:^{}s} | {:^{}s}'
    row_string = '{:{}s} | $ {:>{}.2f} | {:>{}d} | $ {:>{}.2f}'

    # Table header - Add 2 to width of dollar value fields to account for
    # dollar sign and space
    report_str = head_string.format(
        'Donor Name', table_size[0], 'Total Given',
        table_size[1] + 2, 'Num Gifts', table_size[2],
        'Average Gift', table_size[3] + 2) + '\n'
    # report_str = report_str +  ('-'*(sum(table_size) + 13)) + '\n')

    # Table rows
    report_list = []
    for donor in donors:
        report_list.append(row_string.format(
            donor.name, table_size[0], donor.donation_total,
            table_size[1], donor.donation_count, table_size[2],
            donor.donation_average, table_size[3]))
    print(report_str + '\n'.join(report_list))


def size_report(donors):
    """Determine column widths for a donor report."""
    # Determine width of columns based on data in donors data structure
    # Convert numbers to strings to determine their length in characters
    # Convert the dollar amounts to an integer to remove decimal places (since
        # there are an unknown number of them), then add 3 to the length to
        # accomodate for a period and 2 decimal places
    # Ensure column size is at least as wide as header text

    name_width = max(len(donor.name) for donor in donors)
    name_width = max(name_width, len('Donor Name'))

    total_width = max(len(str(int(
        donor.donation_total))) for donor in donors)+3
    total_width = max(total_width, len('Total Given'))

    num_width = max(len(str(donor.donation_count)) for donor in donors)
    num_width = max(num_width, len('Num Gifts'))

    avg_width = max(len(str(int(
        donor.donation_average))) for donor in donors)+3
    avg_width = max(avg_width, len('Average Gift'))

    return [name_width, total_width, num_width, avg_width]


if __name__ == '__main__':
    database = SqliteDatabase('mailroom.db')
    database.connect()
    create_report()
