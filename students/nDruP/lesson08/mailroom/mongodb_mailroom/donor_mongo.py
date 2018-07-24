"""
Replicates most donor_dict functionality except it uses pymongo commands.
The format of the data is {'name': x, 'key': x.lower(), 'gifts': []}
The db it is accessing is dev and the collection it pulls from is donors
"""


import configparser
import pymongo
from pathlib import Path
from donor_dict import Donor_Dict
from donor import Donor


config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


class Donor_DB():
    def __init__(self):
        self._client = None
        user = None
        pw = None
        uri = None
        try:
            config.read(config_file)
            user = config["mongodb_cloud"]["user"]
            pw = config["mongodb_cloud"]["pw"]
            uri = config["mongodb_cloud"]["connection"]
        except Exception as e:
            print(f'error: {e}')

        self._client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=10000, authMechanism='SCRAM-SHA-1', username=user, password=pw)

    def __getitem__(self, key_name):
        with self._client as client:
            donors = client.get_database()['donors']
            query = {'key': key_name}
            d = donors.find_one(query)
        return d

    @property
    def all_donor_info(self):
        info = []
        with self._client as client:
            donors = client.get_database()['donors']
            info = [
                (d['name'],
                len(d['gifts']),
                sum(d['gifts']),
                sum(d['gifts'])/len(d['gifts']))
                for d in donors.find()
            ]
        return info

    @property
    def names(self):
        return [d[0] for d in self.all_donor_info]

    @property
    def histories(self):        
        with self._client as client:
            donors = client.get_database()['donors']
            hist = [d['gifts'] for d in donors.find()]
        return hist

    @property
    def total_gifts(self):
        return sum([d[1] for d in self.all_donor_info])

    @property
    def total_avg(self):
        return sum([d[3] for d in self.all_donor_info])/self.total_gifts

    @property
    def total_sum(self):
        return sum([d[2] for d in self.all_donor_info])

    @property
    def keys(self):
        with self._client as client:
            donors = client.get_database()['donors']
            keys = [d['key'] for d in donors.find()]
        return keys

    @property
    def col_len(self):
        name_col = max(len("Donor Name"), max([len(x) for x in self.names]))
        hist_col = max(len("Gifts"), len(str(self.total_gifts)))
        avg_col = max(len("Avg Gift"), len(str(self.total_avg)))
        sum_col = max(len("Total Given"), len(str(self.total_sum)))
        return [name_col, hist_col, avg_col, sum_col]

    def add_donor(self, d_name, contribution):
        key_name = d_name.lower()
        with self._client as client:
            donors = client.get_database()['donors']
            if not donors.find_one({'key': key_name}):
                print('Did not find')
                donors.insert_one(
                    {'name': d_name, 'key': key_name, 'gifts':[contribution]}
                )
            else:
                donors.update_one(
                    {'key': key_name},
                    {'$push': {'gifts': contribution}}
                )
    
    def challenge(self, alter, min_gift=-1.0, max_gift=-1.0, *filt_names):
        remain_names = [x for x in self.names if x not in filt_names]
        remain_d = []
        new_d = []
        if min_gift == -1.0:
            min_gift = min([min(g) for g in self.histories]) - .01
        if max_gift == -1.0:
            max_gift = max([max(g) for g in self.histories]) + .01
        with self._client as client:
            donors = client.get_database()['donors']
            donor_data = donors.find()
            for d in donor_data:
                if d['name'] in filt_names:
                    chal_d = Donor('*'+d['name'], d['gifts'])
                    new_d.append(chal_d.challenge(alter, min_gift, max_gift))
                else:
                    remain_d.append(Donor(d['name'], d['gifts']))
        return Donor_Dict(*(new_d+remain_d))

    def names_str(self, sep='\n', *excl_names):
        names = [x for x in self.names if x not in excl_names]
        return ((sep+"{}")*len(names)).format(*names)

    def sort_by_name(self, d_info):
        return d_info[0].lower()

    def sort_by_hist(self, d_info):
        return d_info[1]

    def sort_by_avg(self, d_info):
        return d_info[2]

    def sort_by_sum(self, d_info):
        return d_info[3]

    def sort_all_donor_info(self, by=0):
        sort_dict = {0: self.sort_by_name,
                     1: self.sort_by_hist,
                     2: self.sort_by_avg,
                     3: self.sort_by_sum}
        return sorted(self.all_donor_info, key=sort_dict[by], reverse=(by > 0))

    def donor_report_row(self, header=0):
        donor_col = "{:<" + f"{self.col_len[0]}" + "}"
        hist_col = "{:>" + f"{self.col_len[1]}" + "}"
        avg_col = "{:>" + f"{self.col_len[2]}" + ((".2f")*(not header)) + "}"
        sum_col = "{:>" + f"{self.col_len[3]}" + ((".2f")*(not header)) + "}"
        return (donor_col+"\t"+hist_col+"\t"+avg_col+"\t"+sum_col)

    def donor_report(self, sort_by):
        if sort_by == 5:
            donor_list = self.all_donor_info
        else:
            donor_list = self.sort_all_donor_info(sort_by-1)
        col_name_list = ["Donor Name", "Gifts", "Avg Gift", "Total Given"]
        report = self.donor_report_row(1).format(*col_name_list)
        row = self.donor_report_row()
        for name, hist, avg_gift, sum_gift in donor_list:
            row_data = [name, hist, avg_gift, sum_gift]
            report += "\n" + row.format(*row_data)
        total_row = ["TOTAL", self.total_gifts, self.total_avg, self.total_sum]
        report += "\n" + row.format(*total_row)
        return report

    def thank_u_letter_str(self, d_name, new_gift=False):
        key_name = d_name.lower()
        gifts = []
        with self._client as client:
            donors = client.get_database()['donors']
            donor = donors.find_one({'key': key_name})
            gifts = donor['gifts']
        thank_u_letter = f"Dearest {d_name},\n"
        if new_gift:
            thank_gift = gifts[len(gifts)-1]
            print(thank_gift)
            thank_u_letter += "\tThank you for your most recent donation of"
        else:
            thank_gift = sum(gifts)
            thank_u_letter += "\tThank you for your lifetime total of "
        thank_u_letter += (f" ${thank_gift:.2f}!\n"
                           "We will use your donation(s) to create real "
                           "living Pokemon.\n"
                           "You now have our eternal loyalty. Use it wisely.\n"
                           "Sincerely,\n"
                           f"We're a Pyramid Scheme & so is {d_name}")
        return thank_u_letter
