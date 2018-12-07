#!/usr/bin/env python3

import pytest
import json_save_mailroom as mail

@pytest.fixture
def test_case():
    test_db = mail.Mailroom('Mailroom A',
                            [mail.Donor('Donor C', [3.0]),
                            mail.Donor('Donor A', [1, 3, 5]),
                            mail.Donor('Donor B', [10, 20])])
    return test_db
    
def test_save_load():
    database = test_case()
    database.save
    load_db = database.load
    assert 'Donor C' == load_db.donorlist[0].name
    assert 'Donor A' == load_db.donorlist[1].name
    assert 'Donor B' == load_db.donorlist[2].name
    assert [3.0] == load_db.donorlist[0].donation
    assert [1, 3, 5] == load_db.donorlist[1].donation
    assert [10, 20] == load_db.donorlist[2].donation