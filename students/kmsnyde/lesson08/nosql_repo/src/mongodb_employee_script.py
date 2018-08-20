"""
    mongodb example
"""

from pprint import pprint as pp
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(employee_items):
    """
    mongodb data manipulation
    """

    with login_database.login_mongodb_cloud() as client:
        log.info('\n\nStep 1: We are going to use a database called employees')
        log.info('\n\nBut if it doesnt exist mongodb creates it')
        db = client['employees']

        log.info('\n\nAnd in that database use a collection called Employee')
        log.info('\n\nIf it doesnt exist mongodb creates it')

        employee = db['employee']
        
        log.info('Insert an item into the document')
        new_item = {
            'name': {'first_name': 'Karl', 'last_name': 'Test'},
            'location': 'Remote-3',
            'Skills': ['Python'],
            'Divison': 'Student',
            'Salary': 100000}
        new_item_id = employee.insert_one(new_item).inserted_id
        
        log.info('\n\nStep 2: Now we add data from the dictionary above')
        employee.insert_many(employee_items)

        log.info('\n\nStep 3: Find the employees that are described as "Python"')
        query = {'Skills': 'Python'}
        results = employee.find(query)
        
        log.info('\n\nStep 3A: Retieve and print people at PLANT')
        query1 = {'location': 'PLANT'}
        results1 = employee.find(query1)

        log.info('\n\nStep 4: Print employees using Python')
        print('\n\nEmployees using Python')
        for item in results:
            pp(item)
            print()
        log.info('\n\nStep 4A: Print employees at PLANT')
        print('\nPLANT employees')
        for i in results1:
            pp(i)
            print()
        
        log.info('Step 5: Delete the postion of Student (actually deletes all "Students")')
        employee.remove({'Division': 'Student'})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'Division': 'Student'}
        results = employee.find_one(query)
        print('The Student(s) is deleted, print should show none:')
        pp(results)

        log.info('\n\nStep 7: Find employees with salaries > $100,000')

        cursor = employee.find({'Salary': {'$gte': 100000}}).sort('Salary', 1)
        print('\nResults of search')
        log.info('\nNotice how we parse out the data from the document')

        for doc in cursor:
            print(f"Salary: {doc['Salary']} of employee: {doc['name']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('employee')
