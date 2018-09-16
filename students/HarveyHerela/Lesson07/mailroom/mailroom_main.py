import mailroom_db
import mailroom_actions
from datetime import datetime
import os


def send_thank_you(db):
    name_queries = ("First name", "Last name")
    full_name = list()
    q = 0
    while q < len(name_queries):
        print("Enter {}, 'list' for names in db, or ~ to go back".format(
            name_queries[q]))
        name = input(": ")
        if name == '~':
            return ""
        elif name.lower() == 'list':
            for donor in db.get_donors():
                print(donor.get_name())
        else:
            full_name.append(name)
            q += 1
    amount = ""
    while not amount.isnumeric():
        print("Donation amount, or '~' to go to main menu:")
        amount = input("$ ")
        if amount == '~':
            return
    amount = float(amount)
    return mailroom_actions.send_thank_you(
        db, full_name[0], full_name[1], amount)


def send_letters(db):
    """Create letters for everyone in the database, and write them to files."""
    subdir = str(datetime.now())
    subdir = subdir.replace(':', '_')
    try:
        os.mkdir(subdir)
    except OSError as oserr:
        print(oserr)
        print("\nThere was an error creating the directory.\n")
        return "Failed!"

    # Read in the template
    try:
        with open("template.txt", 'r') as infile:
            template_in = infile.read()
    except FileNotFoundError as fnferr:
        print(fnferr)
        print("\nThere was an error reading the template file")
        return "Failed!"

    letters = mailroom_actions.send_letters(db, template_in)

    # Write the letters to file
    for letter in letters:
        filename = "./{dir}/{name}.txt".format(name=letter[0], dir=subdir)
        with open(filename, 'w') as outfile:
            outfile.write(letter[1])
    return "{num} letters created!".format(num=len(letters))

def select_donor(db):
    # Print out a list of donors, get the selected one
    donor_names = dict()
    count = 1
    for donor in db.get_donors():
        donor_names[str(count)] = donor.get_name_tuple()
        count += 1
    # Now print out the list
    print("Select a donor by number, or 0 to go back")
    for k, v in donor_names.items():
        print("{num}: {first} {last}".format(
            num=k,
            first=v[0],
            last=v[1]))
    selection = input(":")
    status = None
    if selection in donor_names:
        status = donor_names[selection]
    return status

def delete_donor(db):
    # Create a list of donor names, print it out
    donor = select_donor(db)
    status = "No donor deleted."
    if donor is not None:
        db.delete_donor(donor[0], donor[1])
        status = "Deleted donor {0} {1}".format(*donor)
    return status

def change_donor_data(db):
    # Get the donor to change
    donor = select_donor(db)
    status = "No changes were made."
    if donor is not None:
        first_name = input("New first name: ")
        last_name = input("New last name: ")
        if first_name is not None and last_name is not None:
            db.change_donor_name(donor[0], donor[1], first_name, last_name)
            status = f"Changed donor name to {first_name} {last_name}"
    return status

def change_donation(db):
    donor = select_donor(db)
    print("Select an item to change, by number.")
    donor_data = dict()
    count = 1
    for donation in db.get_donations(donor[0], donor[1]):
        donor_data[str(count)] = "Donation. {amount}".format(amount=donation)
        count += 1
    # Now print out the data
    for k, v in donor_data.items():
        print(f"{k}: {v}")
    selection = input("Change which donation: ")
    if selection in donor_data:
        amount = input("New value: ")
        db.change_donation(donor[0], donor[1], int(selection) - 1, float(amount))


def delete_donation(db):
    donor = select_donor(db)
    print("Select a donation to change, by number.")
    donor_data = dict()
    count = 1
    for donation in db.get_donations(donor[0], donor[1]):
        donor_data[str(count)] = "Donation. {amount}".format(amount=donation)
        count += 1
    # Now print out the data
    for k, v in donor_data.items():
        print(f"{k}: {v}")
    status = "No donation was deleted"
    selection = input("Delete which donation: ")
    if selection in donor_data:
        db.delete_donation(donor[0], donor[1], int(selection) - 1)
        status = "Deleted " + donor_data[selection]
    return status

main_menu_list = [
    "Pick an action by number",
    "1: Send 'Thank You' note",
    "2: Create Report",
    "3: Send letters to everyone",
    "4: Delete donor",
    "5: Change donor name",
    "6: Delete a donor donation",
    "7: Change a donor donation",
    "q: Quit"
]


main_menu_actions = {
    '1': send_thank_you,
    '2': mailroom_actions.create_report,
    '3': send_letters,
    '4': delete_donor,
    '5': change_donor_data,
    '6': delete_donation,
    '7': change_donation
}


def draw_main_menu():
    print("\n".join(main_menu_list))


def get_main_menu_input():
    user_input = input(":")
    user_input = user_input.lower().strip()
    return user_input


if __name__ == "__main__":
    db = mailroom_db.DonorCollection()
    # Some default data
    db.add_donation("Jimmy", "Stewart", 50)
    db.add_donation("Cary", "Grant", 30)
    db.add_donation("Cary", "Grant", 40)
    db.add_donation("Audrey", "Hepburn", 80)
    db.add_donation("Audrey", "Hepburn", 90)
    db.add_donation("Audrey", "Hepburn", 100)

    # Now on to the meat and potatos of the mailroom
    running = True
    while running:
        draw_main_menu()
        user_input = get_main_menu_input()
        if user_input in main_menu_actions.keys():
            print(main_menu_actions[user_input](db), "\n\n")
        running = user_input != 'q'
