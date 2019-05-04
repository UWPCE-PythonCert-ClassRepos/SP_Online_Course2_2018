import unittest
import Mailroom
import os.path
import io
import sys


class TestMailroom(unittest.TestCase):
    def setUp(self):
        donor_dict = {}
        donor_dict['papa'] = [100, 5, 15]
        donor_dict['mama'] = [12, 200, 2, 66]
        donor_dict['bompa'] = [1000]
        donor_dict['bobonne'] = [500, 500]
        donor_dict['onbekende'] = [1000000]

        self.DonorDict = Mailroom.Donor_Collection(donor_dict)
        
    def test_saving(self):
        Mailroom.save(self.DonorDict)
        with open(f'save.txt', 'r') as outfile:
            assert outfile.read() == '{"__obj_type": "MyClass", "x": {"papa": [100, 5, 15], "mama": [12, 200, 2, 66], "bompa": [1000], "bobonne": [500, 500], "onbekende": [1000000]}}'

    def test_loading(self):
        Mailroom.load(self.DonorDict)
        assert self.DonorDict._donors == {"papa": [100, 5, 15], \
    "mama": [12, 200, 2, 66], "bompa": [1000], "bobonne" : [500, 500], "onbekende" : [1000000]}




if __name__ == '__main__':
    unittest.main()