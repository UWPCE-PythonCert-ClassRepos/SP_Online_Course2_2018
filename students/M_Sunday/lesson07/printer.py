import logging
import peewee
import sqlite3
from pprint import pprint


def print_data():

    try:
        conn = sqlite3.connect('personjob.db')
        cur = conn.cursor()
        cur.execute("SELECT name_of_job, person_employed, start_date, "
                    "employment_duration, salary, department_manager, "
                    "department_name FROM "
                    "department "
                    "INNER JOIN job ON (department.name_of_job = "
                    "job.job_name)")

        jobs = cur.fetchall()

        print(
            "----------------------------------------------------------------"
            "-----------------------------------------------------------------"
            "---------")
        print("Employee | Job Name                | Department Name      "
              "   | Department Manager | Start Date | Employment Duration ["
              "days] | Salary [USD]")
        print(
            "----------------------------------------------------------------"
            "-----------------------------------------------------------------"
            "---------")

        for job in jobs:
            # job is a tuple with the following, in order:
            # 0 - Job name
            # 1 - Employee Name
            # 2 - Start Date
            # 3 - Employement Duration
            # 4 - Salary
            # 5 - Department Manager
            # 6 - Department Name

            print("{:<9}| {:<24}| {:<24}| {:<19}| {:<11}| {:<27}| {"
                  ":<10}".format(
                job[1], job[0], job[6], job[5], job[2], job[3], job[4]))

    except Error as e:
        print(e)

    finally:
        conn.close()


if __name__ == '__main__':
    print_data()
