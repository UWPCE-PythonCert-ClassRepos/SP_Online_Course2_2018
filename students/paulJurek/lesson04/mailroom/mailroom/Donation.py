"""donor class controlling donor behavior"""

from collections import namedtuple
import datetime
from json_save.json_save import json_save_meta as js


class Donation(js.JsonSaveable):
    id = js.Int()
    amount = js.Float()
    date = js.DateTime()

    def __init__(self, id: int, amount: float, date: datetime=datetime.datetime.utcnow()):
        self.id = id
        self.amount = amount
        self.date = date

    def __repr__(self):
            return str(self.to_json_compat())