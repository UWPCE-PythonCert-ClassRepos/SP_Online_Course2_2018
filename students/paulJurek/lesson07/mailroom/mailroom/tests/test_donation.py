"""tests donation behavior."""
import pytest
from mailroom.Donation import Donation

@pytest.mark.parametrize("input, output", [
    (100, 100.00),
    (100.12221, 100.12),
    (1.9099, 1.90),
])
def test_donation_shows_in_dollars(input, output):
    """when donation is created
    the values are shown as dollars
    the decimals should be dropped off if they extend beyond limit"""
    d1 = Donation(donation_amount=input, donation_donor='test')
    assert d1.donation_amount == output