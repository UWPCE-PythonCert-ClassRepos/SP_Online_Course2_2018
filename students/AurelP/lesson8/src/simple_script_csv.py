"""
    Persistence
"""
import csv
import pprint
import utilities


log = utilities.configure_logger('default', '../logs/csv_script.log')

def run_csv_hw():
    """
    write and read a csv
    """
    #log = utilities.configure_logger('default', '../logs/csv_script.log')
    log.info("\n\n====")
    donors = [('Donor A', 117.45),
              ('Donor B', 22.01),
              ('Donor C', 45.99),
              ('Donor D', 77.0),
              ('Donor E', 12.5),
              ('Donor F', 6.25)
             ]

    log.info("Writing to csv file")
    with open('../data/donors_file.csv', 'w') as donors_data:
        donor_writer = csv.writer(donors_data)
        donor_writer.writerow(donors)

    log.info("Read csv file back")
    with open('../data/donors_file.csv', 'r') as donors_data:
        donor_reader = csv.reader(donors_data, delimiter=',', quotechar='"')
        for row in donor_reader:
            pprint.pprint(row)
    return

if __name__ == "__main__":
    pass
    #run_csv_hw()
