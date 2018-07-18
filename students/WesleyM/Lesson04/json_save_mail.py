from mailroom_6 import *
import json_save.json_save_dec as js
import os

@js.json_save
class json_dh:
    Donors = js.List()
    def __init__(self, dh):
        self.Donors = [{'name': donor_object.name, 'donations': donor_object.donations} \
        for donor_object in dh.donors.values()]
    def save(self):
        with open('json_out.json', 'w') as outfile:
            self.to_json(fp=outfile)
    @classmethod
    def load(cls, file='json_in.json'):
        with open(file, 'r') as infile:
            return js.from_json(infile)
