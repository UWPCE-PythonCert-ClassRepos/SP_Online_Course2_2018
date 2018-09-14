import mailroom_db


def send_thank_you(db, firstname, lastname, amount):
    db.add_donation(firstname, lastname, amount)
    return "Thank you {fn} {ln} for your generous donation of ${amount:.2f}".format(
        fn=firstname, ln=lastname, amount=amount)


def create_report(db):
    """Prints a list of all donors, sorted by total amount given."""

    def get_total(donor_data):
        return donor_data[1]

    def create_row(donor):
        fullname = donor.get_name()
        total = sum(donor.get_donations())
        num = len(donor.get_donations())
        avg = total / num
        return [fullname, total, num, avg]

    report = list()
    report.append("Donor Name    | Total Given   | Num Gifts | Average Gift")
    report.append("--------------------------------------------------------")

    # Create a list with the data we want
    data_list = [create_row(donor) for donor in db.get_donors()]

    # Sort the list by total amount given
    data_list.sort(key=get_total, reverse=True)

    # Define the formatter
    line_fmtr = "{name:<14}  ${total:>13.2f}   {num:>9d}  ${avg:>12.2f}".format

    # Apply the formatting to all the data
    for d in data_list:
        report.append(line_fmtr(name=d[0], total=d[1], num=d[2], avg=d[3]))

    return '\n'.join(report)


def send_letters(db, template_in):

    donor_template = template_in
    donor_template = donor_template.replace('{amount}', '{amount:.2f}')
    donor_template = donor_template.replace('{total}', '{total:.2f}')

    letters = list()

    for donor in db.get_donors():
        # Setup up the data to write
        donations = donor.get_donations()
        last = donations[-1]
        total = sum(donations)

        # Create the personalized letter
        # Replace the keys with the data
        try:
            letters.append(
                (donor.get_name(),
                    donor_template.format(
                    name=donor.get_name(), amount=last, total=total)))
        except KeyError as kerr:
            print("Key Error:", kerr, "is not a valid key.",
                "The only valid keys are: ",
                "{name}, {amount}, and {total}")
            return "Failed!"

    return letters
