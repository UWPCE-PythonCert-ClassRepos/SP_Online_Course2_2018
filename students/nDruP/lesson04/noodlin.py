from donor import Donor
from donor_dict import Donor_Dict

print('Creating donor instance')

d1 = Donor('Donor1', [1, 2, 3.5, 6.27])
print(d1)

d1_js = d1.to_json_compat()
print(d1_js)

d1_2 = Donor.from_json_dict(d1_js)
assert d1_2 == d1

print(d1.to_json())

print("Testing donor_dict")
d2 = Donor('Donor2', 100.0)
print(d1.history)
d3 = Donor('Donor3', [99.999, 97.0, 1.2])
print(d1.history)

d_dict = Donor_Dict(d1, d2, d3)
d_dict_js = d_dict.to_json_compat()
print(d_dict_js)

d_dict_2 = Donor_Dict.from_json_dict(d_dict_js)

assert d_dict_2 == d_dict

print(d_dict.to_json())
