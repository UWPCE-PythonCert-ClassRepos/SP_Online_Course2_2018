"""
Populate mailroom.db with existing donor data.
"""

from mailroom_model import *

donors = [
    ('han solo', [3468.34, 457, 34.2]),
    ('luke skywalker', [5286286.3, 567, 23.5678]),
    ('chewbacca', [432, 679.4553]),
    ('princess leia', [5.3434]),
    ('bobba fett, bounty hunter', [67])
    ]

database = SqliteDatabase('mailroom.db')
database.connect()

for donor in donors:
    new_donor = Donor.create(name=donor[0])
    new_donor.save()

    for donation in donor[1]:
        new_donation = Donation.create(
            amount=donation,
            donor=donor[0]
            )
        new_donation.save()
