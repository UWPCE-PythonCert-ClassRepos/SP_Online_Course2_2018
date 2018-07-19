"""
1. Create Data structure that holds Donor, Donation Amount.
2. Prompt user to Send a Thank You, Create a Report, or quit.
3. At any point, the user should be able to quit their current task and return
to the original prompt
4. From the original prompt, the user should be able to quit the scipt cleanly
"""


import sys
import os
import datetime
from donor import Donor
from donor_dict import Donor_Dict
from redis_mailroom import Redis_Mailroom_Client


d = Donor_Dict.from_file("dict_init.txt")
divider = "\n" + "*" * 50 + "\n"
validater = Redis_Mailroom_Client()


def main_menu(user_prompt=None):
    """
    Prompt user to send a Thank You, Create a report, create letters, or quit.
    """
    valid_prompts = {"1": add_donation,
                     "2": create_donor_report,
                     "3": simulate,
                     "4": mr_exit}
    options = list(valid_prompts.keys())
    print(divider + "We're a Pyramid Scheme & So Are You! E-Mailroom" +
          divider)
    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add new donation")
        print("2. Show Report")
        print("3. Run Projections")
        print("4. Quit")
        user_prompt = input(">")
        print(divider)
    return valid_prompts.get(user_prompt)


def verify_user():
    name = ''
    while True:
        print('Please input who is accessing this mailroom.')
        name = input('>')
        if name in validater.keys:
            print('Please input any of the following to verify: '
                  'Email, Phone Number, What is your favorite beverage?')
            answ = input('>')
            if (validater.validate_email(name, answ)
            or validater.validate_phone_num(name, answ)
            or validater.validate_security_q(name, answ)):
                break
        print('Could not verify')
    return d[name.lower()]

def user_input(some_str=""):
    """
    Display exit reminder and prompt user for input.
    """
    while not some_str:
        print("Return to the main menu by entering 'exit'")
        some_str = input(">")
    return check_not_exit(some_str) * some_str


def check_not_exit(check_str):
    """
    Check whether or not given string is "exit"
    """
    return check_str.lower() != "exit"


def conv_str(conv_str, conv_type=int):
    """
    Convert string to given conv_type.
    If it's unable to convert, return original string.
    """
    try:
        conv_yes = conv_type(conv_str)
        return conv_yes
    except ValueError:
        return None


def input_donor_float(d_amt=0):
    """
    Prompt user for valid float
    If input cannot be converted to float, prompt again.
    """
    while True:
        d_amt = user_input()
        if d_amt:
            d_amt = conv_str(d_amt, float)
        if d_amt is not None:
            break
        print("Enter a valid amount")
    return d_amt


def add_donation(donor):
    """
    Compose and print a thank you letter to the donor for their donation.
    Return to main
    """
    print(divider)
    print("\nEnter a Donation Amount:")
    gift_amt = input_donor_float()
    if gift_amt != "":
        d.add_donor(donor.name, gift_amt)
        print(donor.thank_u_letter_str(1))        
    return


def create_donor_report(donor, d_dict=d):
    """
    Print a list of donors sorted by method chosen in sort_report_by.
    Donor Name, Num Gifts, Average Gift, Total Given
    """
    report = donor.donor_report()
    print(divider + report + divider)
    return


def simulate(donor, d_dict=d):
    """
    Display Donor Report altered by user's specifications.
    """
    print("Input a factor to multiply contributions by.")
    fctr = input_donor_float()
    if fctr != "":
        print("Input a min donation such that all donations above" +
              " this amount will be altered.")
        print("Enter -1 for default value")
        min_g = input_donor_float()
        if min_g != "":
            print("Input a max donation such that all donations below" +
                  " this amount will be altered")
            print("Enter -1 for default value")
            max_g = input_donor_float()
            while max_g < min_g:
                print("Please enter a valid amount")
                max_g = input_donor_float()
            if max_g != "":
                if min_g == -1:
                    min_g = None
                if max_g == -1:
                    max_g == None
                sim_d = donor.challenge(fctr, min_g, max_g)
                create_donor_report(sim_d)
    return


def write_txt_to_dir(f_name, content, wrt_dir=os.getcwd()):
    """
    Write a personalized thank you letter for all the donors.
    Letters will be written to letter_dir.
    """
    curdate = (datetime.datetime.now()).strftime("%Y_%m_%d")
    file_name = f_name.replace(' ', '_') + "_" + curdate + ".txt"
    file_path = os.path.join(wrt_dir, file_name)
    with open(file_path, 'w+') as text:
        text.write(content)
    return "Wrote to " + file_path


def mr_exit(donor):
    """
    Prompt user to save donor dict before exiting program.
    """
    print("Before exiting would you like to save the donor info?[y/n]")
    save_confirm = ""
    while save_confirm not in ['y', 'n']:
        save_confirm = input('>').lower()
    if save_confirm == 'y':
        print(write_txt_to_dir("dict_init", d.dict_to_txt(), os.getcwd()))
        validater.write_lookup_file('lookup_list.txt')
    sys.exit()


if __name__ == '__main__':
    donor = verify_user()
    while True:
        main_menu()(donor)
        input("Press Enter to continue...........")
