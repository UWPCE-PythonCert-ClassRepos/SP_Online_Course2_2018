#!/usr/bin/env python3

import pytest
import os
from run_mailroom import save, load, add_donor, number_of_donors
from mailroom import Donor

def test_save():
    save()
    fileExisted = os.path.isfile("data_file.json")
    assert fileExisted == True

def test_load():
    # add a donor to collection
    add_donor(Donor("Test1", [1]))
    # total of donors should be 3
    assert number_of_donors() == 3
    #load the original data base
    load()
    # total of oritinal donors shouold be 2
    assert number_of_donors() == 2
