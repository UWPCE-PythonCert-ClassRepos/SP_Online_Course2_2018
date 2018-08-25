import mailroom_db
import mailroom_actions
from datetime import datetime
import os
import json_save.json_save.json_save.json_save_dec as js


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


def save_json(db):
    # Write the database to a JSON file
    filename = "mail_db.json"
    with open(filename, 'w') as outfile:
        outfile.write(db.to_json())
    return f"\nSaved as {filename}\n"


def load_json(db):
    # Load the database from a JSON file
    filename = "mail_db.json"
    with open(filename, 'r') as infile:
        the_json = infile.read()
    db.load_db(js.from_json(the_json))
    return f"\nLoaded database from {filename}\n"


main_menu_list = [
    "Pick an action by number",
    "1: Send 'Thank You' note",
    "2: Create Report",
    "3: Send letters to everyone",
    "4: Save to JSON file",
    "5: Load from JSON file",
    "q: Quit"
]


main_menu_actions = {
    '1': send_thank_you,
    '2': mailroom_actions.create_report,
    '3': send_letters,
    '4': save_json,
    '5': load_json
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
            print(main_menu_actions[user_input](db))
        running = user_input != 'q'
