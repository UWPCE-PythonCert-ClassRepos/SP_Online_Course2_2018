import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """
       Define BaseModel for Donor Class
    """
    class Meta:
        database = database


class Donor(BaseModel):#donor class with existing donors and their donation history
    """
       Define Donor class which maintains donor name.
    """
    donor_name = CharField(max_length = 50, unique = True)
    
#donor_name, t_d, d_n, a_d
#bill        1300 2    750
#(Bill, Andrew)


class Donation(BaseModel):
    """Define Donation class which maintains donor name
    and donation amount.
    """
    donor_name = ForeignKeyField(Donor, related_name = 'donated by', null = False)
    donation_amount = FloatField()
    
#(Bill,[400, 500]
# Andrew, [400, 700])? foreign key connects to donor class 
#if add new donor: 
#how would be calculate ave_don, total_don, don_num? 
#print(for donor, donation in Donation.select(): print(donor_name, sub(donation), len(donation), sum/len ))?
#query = Donor.select(Donor, fn.COUNT(Donor.donation_amount).alias(donation_number))
#join(Donation, JOIN.LEFT_OUTER)
#.group_by(Donor)
#.order_by(Donor.donation.donation_amount)(or better by total_donation)
#use this query to print report
#donor name, donation_amount
#Bill        500, 800
#new donation will be added to this table and will increase total_don&aver_don&don_num in Donor table total_don += new_don, 
#don_num +=1, 
#new donor goes here and also Donor needs to be updated(if donor_name exist, donation is added, if not: add new_donor + donation)
#update: search for donor_name, if found update


database.create_tables([
        Donor,
        Donation
    ])

database.close()
