import peewee


class Donor:
    """
        Donor class is a convenience class to abstract
        away the details of how the actual saving and
        loading is done. Basically, the rest of the mailroom
        operates on the donor class, but the actual saving
        is not guaranteed have the capabilities of this donor
        class, so this class mediates the 2 methodologies.
    """

    def __init__(self, firstname, lastname, donations=[]):
        self.name = (firstname, lastname)
        self.donations = donations

    def add_donation(self, amount):
        self.donations.append(amount)

    def get_donations(self):
        return self.donations

    def get_key(self):
        return self.name

    def get_name(self):
        return "{0} {1}".format(*self.name)


# This is where things are saved
donations = peewee.SqliteDatabase("donotions_db.db")

class BaseModel(peewee.Model):
    class Meta:
        database = donations

# Make the donor table
class DonorData(BaseModel):
    """
        Donors
    """
    donor_name = peewee.CharField(unique=True)
    last_name_index = peewee.IntegerField()

# Make the donations table

class Donations(BaseModel):
    """
        Donations table
    """
    amount = peewee.IntegerField()
    donated_by = peewee.ForeignKeyField(DonorData, related_name='donations')


class DonorCollection:
    """
        Encapsulates the db. Gets data from it
        and returns the data as a Donor. Inserts data
        when necessary.
    """

    def __init__(self):
        DonorData.create_table()
        Donations.create_table()

    def get_donors(self):
        # Get the list of donors
        all_donors = DonorData.select()

        # Iterate over each donor
        for d in all_donors:
            # Convert this donors donations to a list
            all_donations = list()
            for donation in d.donations:
                all_donations.append(donation.amount)

            # Split up the name for convenience
            first_name = d.donor_name[:d.last_name_index]
            last_name = d.donor_name[d.last_name_index:]
            yield Donor(first_name, last_name, all_donations)

    def add_donation(self, firstname, lastname, amount):
        name = firstname + lastname
        index = len(firstname)
        donors = DonorData.select().where(DonorData.donor_name == name)

        # If the donor doesn't exist, add the donor to the database
        if len(donors) == 0:
            donor = DonorData.create(
                donor_name=name,
                last_name_index=index
            )
        else:
            # The donor exists, get the donor
            donor = donors.get()

        Donations.create(amount=amount, donated_by=donor)
