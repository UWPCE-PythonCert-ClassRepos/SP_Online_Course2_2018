# --------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: run_mailroom.py
# DATE CREATED: 11/4/2018
# UPDATED: 11/7/2018
# PURPOSE: Lesson 04
# DESCRIPTION: Interface page for all files.
# --------------------------------------------------------------------------------
import os
from mailroom_json import EachDonor, DonorList
import json
import mailroom_functions as m

existing_donors = DonorList(EachDonor('Harry Potter', [100, 2.48, 2048]),
                            EachDonor('Ron Weasley', [56.12, 1982]),
                            EachDonor('Hermione Grainger', [1500, 1250, 250.65]),
                            EachDonor('Albus Dumbledore', [3500, 5280, 314.15]),
                            EachDonor('Severus Snape', [2018, 19.01, 750, 690.99]))


prompt = '''
--------------------------------------------------------------------------------------------------------------
                                                MAIL ROOM MENU
--------------------------------------------------------------------------------------------------------------

                                             -- Menu Options --
                                        
                                        A. Add Donor/Edit Existing
                                        B. Create Donor Report
                                        C. Write Letters to all Donors
                                        D. Load
                                        E. Save
                                        Q. Quit (Exit)
                                        
                                        Menu Selection: '''


input_directory = "\nChoose file-path or press enter for default"


if __name__ == '__main__':
    m.menu_selection(prompt, m.menu_dict)
