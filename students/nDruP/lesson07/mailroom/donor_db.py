from donor_peewee_model import *

donor_query = Donation.select(
    fn.distinct(Donation.donor)
)

aggregate_query = (
    Donation.select(
        Donation.donor,
        fn.Count(Donation.gift).alias('Number of Gifts')
        fn.Sum(Donation.gift).alias('Total Gifts')
        fn.Avg(Donation.gift).alias('Avg Gift')
    ).order_by(
        SQL(user_in)
    )
)
