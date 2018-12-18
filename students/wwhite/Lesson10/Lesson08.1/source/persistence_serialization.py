import json
import utilities
import pprint

log = utilities.configure_logger('default', '../logs/persistence_serialization.log')


def run_json():
    log.info("\n\n====")
    log.info("Look at working with json data")
    employees = [{'name': 'michael scott', 'age': '40', 'hair color': 'brown', 'height': '165cm', 'weight': '200lbs'},
                 {'name': 'pam beasley', 'age': '30', 'hair color': 'light brown', 'height': '150cm', 'weight': '120lbs'},
                 {'name': 'jim halpert', 'age': '31', 'hair color': 'brown', 'height': '185cm', 'weight': '190lbs'},
                 {'name': 'creed bratton', 'age': '55', 'hair color': 'grey', 'height': '160cm', 'weight': '165lbs'},
                 {'name': 'toby flenderson', 'age': '45', 'hair color': 'light brown', 'height': '160cm', 'weight': '170lbs'},
                 {'name': 'kelly kapoor', 'age': '28', 'hair color': 'black', 'height': '152cm', 'weight': '125lbs'},
                 {'name': 'andy bernard', 'age': '35', 'hair color': 'brown', 'height': '170cm', 'weight': '173lbs'},
                 {'name': 'angela martin', 'age': '38', 'hair color': 'blond', 'height': '142cm', 'weight': '82lbs'},
                 {'name': 'dwight schrute', 'age': '37', 'hair color': 'brown', 'height': '176cm', 'weight': '195lbs'},
                 {'name': 'stanley hudson', 'age': '41', 'hair color': 'black', 'height': '168cm', 'weight': '220lbs'},
                 ]

    log.info("Write json string to a file")
    with open('data.json', 'w') as outfile:
        json.dump(employees, outfile)

    log.info("Read json string from file")
    with open('data.json') as infile:
        data = json.load(infile)
        log.info("print the data")
        pprint.pprint(data)


run_json()