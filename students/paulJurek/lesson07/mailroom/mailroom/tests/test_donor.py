"""tests the donor class"""

import pytest

from mailroom.Donor import Donor

@pytest.mark.parametrize("new_donor", [Donor(donor_name='Santa Claus', email='stnick@gmail.com'),
                                       Donor(donor_name='Santa Claus', email='stnick@gmail.com'),
                                      Donor(donor_name='Santa Claus', email='stnick@gmail.com'),
                                        ]
                                        )
def test_donor_initiaztion(new_donor):
    """when donor is initiated
    the object is avaliable"""
    assert isinstance(new_donor, Donor)
