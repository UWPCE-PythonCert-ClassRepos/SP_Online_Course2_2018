"""
Unit tests for the personjobdept module
"""
from .fill_personjobdept_database import *

from unittest import TestCase

class Database_tester(TestCase):

    def setUp(self):
        populate_db_person()
        populate_db_dept()
        populate_db_job()

    def test_person(self):
        database = SqliteDatabase('personjob.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Person.select())
            expected = ['Andrew', 'Peter', 'Susan', 'Pam', 'Steven']
            for result, expect in zip(query, expected):
                self.assertEqual(result.person_name, expect)

            expected = ['Sumner', 'Seattle', 'Boston', 'Coventry', 'Colchester']
            for result, expect in zip(query, expected):
                self.assertEqual(result.lives_in_town, expect)

            expected = ['Andy', None, 'Beannie', 'PJ', None]
            for result, expect in zip(query, expected):
                self.assertEqual(result.nickname, expect)

        finally:
            database.close()

    def test_department(self):
        database = SqliteDatabase('personjob.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Department.select())
            expected = ['E109', 'G202', 'S101']
            for result, expect in zip(query, expected):
                self.assertEqual(result.department_number, expect)

            expected = ['Human_Resources', 'Graphics_Department', 'Sales']
            for result, expect in zip(query, expected):
                self.assertEqual(result.department_name, expect)

            expected = ['Jackie_Love', 'Evan_Picasso', 'Janet_Everson']
            for result, expect in zip(query, expected):
                self.assertEqual(result.department_manager, expect)

        finally:
            database.close()

    def test_job(self):
        database = SqliteDatabase('personjob.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Job.select())
            expected = ['Andrew', 'Peter', 'Susan', 'Pam', 'Steven']
            for result, expect in zip(query, expected):
                self.assertEqual(result.person_employed.person_name, expect)

            expected = ['Analyst', 'Graphic_Designer', 'District_Manager', 'Salesperson', 'Help_Desk_Associate']
            for result, expect in zip(query, expected):
                self.assertEqual(result.job_name, expect)

            expected = ['2016-09-01', '2010-01-01', '2014-04-10', '2012-03-01', '2017-01-01']
            for result, expect in zip(query, expected):
                self.assertEqual(result.start_date, expect)

            expected = ['2018-09-01', '2012-05-05', '2017-02-14', '2012-09-01', '2017-02-01']
            for result, expect in zip(query, expected):
                self.assertEqual(result.end_date, expect)

            expected = [730, 855, 1041, 184, 31]
            for result, expect in zip(query, expected):
                self.assertEqual(result.duration, expect)

            expected = [60000, 45000, 85000, 75000, 38000]
            for result, expect in zip(query, expected):
                self.assertEqual(result.salary, expect)

            expected = ['E109', 'G202', 'S101', 'S101', 'E109']
            for result, expect in zip(query, expected):
                self.assertEqual(result.job_dept.department_number, expect)

        finally:
            database.close()

    def test_department(self):
        database = SqliteDatabase('personjob.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Department.select())
            expected = ['E109', 'G202', 'S101']
            for result, expect in zip(query, expected):
                self.assertEqual(result.department_number, expect)

            expected = ['Human_Resources', 'Graphics_Department', 'Sales']
            for result, expect in zip(query, expected):
                self.assertEqual(result.department_name, expect)

            expected = ['Jackie_Love', 'Evan_Picasso', 'Janet_Everson']
            for result, expect in zip(query, expected):
                self.assertEqual(result.department_manager, expect)

        finally:
            database.close()
