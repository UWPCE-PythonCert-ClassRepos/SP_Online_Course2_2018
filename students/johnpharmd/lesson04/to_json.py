#!/usr/bin/env python3
import json
from original_json_save_meta import *


donors_dct = {'Gates': {'title': 'Mr.', 'donations': 150000,
						'num_donations': 3},
			  'Brin': {'title': 'Mr.', 'donations': 150000,
					   'num_donations': 3},
			  'Cerf': {'title': 'Mr.', 'donations': 50000,
					   'num_donations': 2},
			  'Musk': {'title': 'Mr.', 'donations': 100000,
					   'num_donations': 1},
			  'Berners-Lee': {'title': 'Mr.', 'donations': 50000,
			                  'num_donations': 2},
			  'Wojcicki': {'title': 'Ms.', 'donations': 125000,
						   'num_donations': 1},
			  'Avey': {'title': 'Ms.', 'donations': 200000,
					   'num_donations': 2}}


with open('test_mailroom_json.txt', 'w') as outfile:
		json.dump(donors_dct, outfile)
