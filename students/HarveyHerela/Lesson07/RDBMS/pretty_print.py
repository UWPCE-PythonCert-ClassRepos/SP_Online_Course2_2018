import peewee
from personjob_model import Person, Job
from datetime import date


def datefield_to_date(datefield):
    date_list = datefield.split('-')
    return date(
        int(date_list[0]),
        int(date_list[1]),
        int(date_list[2]))


def pretty_printer(name):
    """
    Prints the person, and every job that person had.
    For every job, print the duration and department
    """

    database = peewee.SqliteDatabase('personjob.db')
    database.connect()

    # First get the person
    person = Person.select().where(
        Person.person_name == name).get()

    print(person.person_name)

    # Now get the jobs that person has had
    jobs = Job.select().where(
        Job.person_employed == person)

    # And get the department for each job
    line_format = '   {job_name:<30} {dept_name:<30} {dur:>20} days'.format
    for j in jobs:
        duration = datefield_to_date(j.end_date) - datefield_to_date(j.start_date)
        print(line_format(
            job_name=j.job_name,
            dept_name=j.department.dept_name,
            dur=duration.days))


if __name__ == '__main__':
    pretty_printer("Jimmy Stewart")
