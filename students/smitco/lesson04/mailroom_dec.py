# lesson 04 mailroom metaprogramming
# based on mailroom FP
# !/usr/bin/env python3


import os
import datetime
import json
import json_save.json_save_dec as js


@js.json_save
class Donor:
    name = js.String()
    donations = js.List()
    
    def __init__(self, name, donations):
        self.name = name
        self.donations = donations
    
    @property
    def total(self):
        return sum(self.donations)
    
    @property
    def count(self):
        return len(self.donations)
    
    @property
    def average(self):
        return sum(self.donations)/len(self.donations)
    
    def add(self, donation):
        self.donations.append(donation)
    
    def get_letter_text(self):
        letter = ("Dear {},\n\n"
                  "Thank you for supporting The Brave Heart Foundation.\n"
                  "Your donations totaling ${:,.0f} have made a positive,\n"
                  "life-changing impact for teens nationwide.\n\n"
                  "Blessings,\n"
                  "BHF".format(self.name, self.total))
        return letter


@js.json_save
class AllDonors:
    donors = js.Dict()
    
    def __init__(self, donors=None):
        self.donors = donors or {}
    
    def load_data(self):
        global donors
        with open("Donor_Data.json", "r") as load_file:
            data = json.load(load_file)
            donors = self.from_json_dict(data)
        return donors
        
        # original 
        # initial_entries = [("John Travolta", 5000), ("John Travolta", 7500), 
                       # ("Jane Fonda", 10000), ("Jane Fonda", 8000), ("Jane Fonda", 6500),
                       # ("Judy Blume", 3000), ("Judy Blume", 3500), ("Joey Tribbiani", 9000),
                       # ("Jenny Gump", 10300), ("Jenny Gump", 13750), ("Jenny Gump", 12500)]
        # for i in initial_entries:
            # self.add_donation(i[0], i[1])
    
    def add_donation(self, donor_name, donation):
        if donor_name in self.donors:
            self.donors[donor_name].add(donation)
        else:
            self.donors[donor_name] = Donor(donor_name, [donation])
    
    def thank_yous(self):
        while True:
            name = input("\nTo whom would you like to send a thank you?\n"
                         "'List' will display current donors.\n"
                         "'Exit' will return to main menu.\n"
                         ">>")
            if name.lower() == "exit":
                print("\nExiting.\n")
                break
            elif name.lower() == "list":
                names = []
                for donor in self.donors.values():
                    names.append(f"{donor.name}")
                print(names)
            else:
                donation = input("\nWhat is the donation amount?\n>>")
                try:
                    donation = int(donation)
                    if donation >= (10 ** 6):
                        print("\nThe amount entered is too large.")
                    else:
                        self.add_donation(name, donation)
                        print("\nThank you, {}, for your generous donation of ${:,.0f} "
                              "to the Brave Heart Foundation.".format(name, donation))
                except ValueError:
                    if donation.lower() == "exit":
                        print("\nExiting.")
                    else:
                        print("\nInvalid entry.")
        
    def get_report(self):
        rows =[]
        for donor in self.donors.values():
            rows.append((donor.name, donor.total, donor.count, donor.average))
        sorted_rows = sorted(rows, key=lambda x: x[1], reverse=True)
        print("\n{:<20} {:<12}  {:^10} {:<12}".format("Donor", "Total", "Count", "Average"))
        for r in sorted_rows:
            print("{:<20} ${:>12,.2f} {:^10} ${:>12,.2f}".format(r[0], r[1], r[2], r[3]))
        print("")
    
    def send_letters(self):
        current = datetime.datetime.now()
        date = [str(current.month), str(current.day), str(current.year)]
        current_date = "_".join(date)
        for donor in self.donors.values():
            letter_name = donor.name + " " + current_date + ".txt"
            with open(letter_name, "w") as donor_letter:
                donor_letter.write(donor.get_letter_text())
        print("\nFiles completed.\n")
    
    def match(self):
        donation_list = []
        for donor in self.donors.values():
            for d in donor.donations:
                donation_list.append(d)
        print("\nThe donation range is ${:,.0f}-{:,.0f}.".format(min(donation_list), max(donation_list)))
        min_match = input("\nWhat is the minimum value to match?\n>>")
        max_match = input("\nWhat is the maximum value to match?\n>>")
        match_range_partial = list(filter(lambda x: int(min_match) <= x, donation_list))
        match_range = list(filter(lambda x: x <= int(max_match), match_range_partial))
        original_sum = sum(match_range)
        print("\nThe total in this range is ${:,.0f}.".format(original_sum))
        factor = input("\nBy what factor would you like to match?\n>>")
        match_sum = sum(map(lambda x: x * int(factor), match_range))
        print("\nThe matching contribution would be ${:,.0f}.\n".format(match_sum))
    
    def save_data(self):
        data_saved = self.to_json_compat()
        with open("Donor_Data.json", "w") as save_file:
            json.dump(data_saved, save_file)
              
        #original
        # with open("Donor_Data.txt", "w") as save_file:
            # for donor in self.donors.values():
                # save_file.write(f"{donor.name}, {donor.donations}\n")
                
        print("\nDonor data saved.\n")
        
    def quit(self):
        print("\nGoodbye.")
        exit()


if __name__ == '__main__':
    donors = AllDonors()
    donors.load_data()
    
    while True:
        ask = input("Please choose an action:\n"
                "1) Send thank yous\n"
                "2) Create a report\n"
                "3) Send letters to all donors\n"
                "4) Analyze for contribution matching\n"
                "5) Save data\n"
                "6) Quit\n"
                ">>")
        options = {"1": donors.thank_yous, "2": donors.get_report, "3": donors.send_letters, 
                   "4": donors.match, "5": donors.save_data, "6": donors.quit}
        try:
            options[ask]()
        except KeyError:
            print("\nThere was an error. Please try again.\n")