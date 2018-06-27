from peewee import *
from donor_peewee_model import Donation


sqlite_db = SqliteDatabase('donor.db')


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


@for_all_methods(sqlite_db.connection_context())
class Donation_Operations():

    def __init__(self, database=sqlite_db):
        self.database = database

    @property
    def row_id_list(self):
        row_ids = []
        for row in Donation.select():
            row_ids.append(row.id)
        return row_ids

    @property
    def name_list(self):
        names = []
        for row in Donation.select():
            names.append(row.donor)
        return names

    def create_donation(self, new_donor, new_gift):
        with self.database.atomic():
            new_donation = Donation.create(donor=new_donor, gift=new_gift)
            new_donation.save()

    def update_donation_by_id(self, row_id, update_value):
        with self.database.atomic():
            for row in Donation.select().where(Donation.id == row_id):
                row.gift = update_value
                row.save()

    def update_donation_by_name_amt(self, donor, update_gift, update_value):
        with self.database.atomic():
            for row in Donation.select().where(
                    Donation.donor == donor &
                    Donation.gift == update_gift):
                row.gift = update_value
                row.save()

    def delete_donation_by_id(self, row_id):
        with self.database.atomic():
            for row in Donation.select().where(Donation.id == row_id):
                row.delete_instance()

    def delete_donation_by_name_amt(self, name, gift_amt):
        with self.database.atomic():
            for row in Donation.select().where(
                    Donation.donor == name &
                    Donation.gift == gift_amt):
                row.delete_instance()
                
    def delete_all_from_name(self, name):
        with self.database.atomic():
            for row in Donation.select().where(Donation.donor == name):
                row.delete_instance()


    @staticmethod
    def select_print_donor_info(self, order_by_field=0):
        col_names = ['name', 'num_gift', 'sum_gift', 'avg_gift']
        donor_info_query = (
            Donation.select(
                Donation.donor.alias(col_names[0]),
                fn.COUNT(Donation.gift).alias(col_names[1]),
                fn.SUM(Donation.gift).alias(col_names[2]),
                fn.AVG(Donation.gift).alias(col_names[3])
            ).group_by(Donation.donor)
            .order_by(SQL(col_names[order_by_field]))
        )
        print(f'{"Donor":10}\tNum_Gifts\tSum_Gifts\tAvg_Gift')
        for row in donor_info_query:
            print(f'{row.name:10}\t{row.num_gift}\t\t'
                  f'${row.sum_gift:<10.2f}\t${row.avg_gift:.2f}')

    @staticmethod
    def select_print_all_rows(self):
        for row in Donation.select():
            print(f'ID: {row.id:<}', end='\t')
            print(f'Donor: {row.donor:20}', end='\t')
            print(f'Gift Amt: ${row.gift:.2f}')
