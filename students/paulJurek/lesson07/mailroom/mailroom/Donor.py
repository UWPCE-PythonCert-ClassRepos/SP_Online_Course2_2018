"""donor class controlling donor behavior"""

import datetime
from mailroom.BaseModel import BaseModel

class Donor(BaseModel):
    """donor giving to organization"""
    donor_name = CharField(primary_key=True, max_length=50)
    email = CharField( max_length=50)

    def donation_total(self):
        """returns the total amount the donor has donated"""
        if self.donations:
            print(self.donations)
            return sum([i.amount for i in self.donations])
        else:
            return 0

    def add_donation(self, amount, date=datetime.datetime.utcnow()):
        """adds donation for user"""
        self._donations.append(Donation(amount=amount, date=date, id=self._donation_id))
        self._donation_id += 1

    def donation_count(self):
        """returns count of donations"""
        return len(self._donations)

    @property
    def donations(self):
        """returns donations"""
        return self._donations

    @property
    def fullname(self):
        """returns combine first and last name"""
        return " ".join([self.firstname, self.lastname])

    def summarize_donor(self):
        """provides summary tuple of donor"""
        return (self.id, self.fullname, self.donation_total(), self.donation_count(), self.donation_total()/self.donation_count())

    def __repr__(self):
            return str(self.to_json_compat())
            
def increase_donation(donation, factor):
    return Donation(amount=donation.amount*factor, date=donation.date, id=donation.id)