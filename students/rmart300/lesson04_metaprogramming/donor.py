import json_save.json_save.json_save_dec as js
import json

@js.json_save
class Donor(object):

    first_name = js.String()
    last_name = js.String()
    amount_list = js.List()

    def __init__(self, name, amount_list = (500, 100, 1000, 20)):

        try:
            name.split()[1]
        except IndexError as e:
            print('The first and last name of donor must be provided\n')
            raise
        else:
            self.first_name = name.split()[0]
            self.last_name = name.split()[1]

        self.amount_list = list(amount_list)

    @property
    def donation_total(self):
        return sum(int(v) for v in self.amount_list)

    @property
    def donation_count(self):
        return len(self.amount_list)

    @property
    def donation_average(self):
        return round(self.donation_total/self.donation_count,2)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def save_data(self):
        with open(f"data/{self.first_name}_{self.last_name}.json", 'w') as infile:
            infile.write(json.dumps(self.to_json_compat()))

    def load_data(self, json_file):
        """ reads in json file and loads to json dict """

        with open(json_file,'r') as infile:
            donor_data = json.loads(infile.read())
            print(donor_data)
        return self.from_json_dict(donor_data)
