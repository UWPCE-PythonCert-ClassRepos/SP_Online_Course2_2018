"""
This module creates a database based on an imported database model,
fills the database tables with data, and runs a query to display all
of the job stints for each person who worked at a company.
"""

import logging
import peewee as pw
import DennisLee_model as mdl

class ManipulateDb:
    """
    This class creates the database and performs database transactions.
    """
    def __init__(self):
        self.db_name = 'DennisLee.db'

        self.set_up_logging()
        self.open_database(self.db_name)
        self.create_tables()
        self.fill_person_table()
        self.fill_department_table()
        self.fill_deptjobs_table()
        self.fill_job_table()
        self.get_all_job_stints()
        self.close_database()

    def set_up_logging(self):
        """Set up the logging template and start logging."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def open_database(self, db_file):
        """Open the database file."""
        self.logger.info(f'Import database {db_file}.')
        self.database = pw.SqliteDatabase(db_file)
        self.logger.info('Connecting.\n')
        self.database.connect()
        self.database.execute_sql('PRAGMA foreign_keys = ON;')

    def create_tables(self):
        """Create the tables in the database."""
        self.logger.info("Creating the Person table.")
        self.database.create_tables([mdl.Person])
        self.logger.info("Creating the Department table.")
        self.database.create_tables([mdl.Department])
        self.logger.info("Creating the DeptJobs table.")
        self.database.create_tables([mdl.DeptJobs])
        self.logger.info("Creating the Job table.\n")
        self.database.create_tables([mdl.Job])

    def fill_person_table(self):
        """Fill the Person table with data."""
        PERSON_NAME, LIVES_IN_TOWN, NICKNAME = 0, 1, 2
        people = (
            ('Andrew', 'Sumner', 'Andy'),
            ('Peter', 'Seattle', None),
            ('Susan', 'Boston', 'Beannie'),
            ('Pam', 'Coventry', 'PJ'),
            ('Steven', 'Colchester', None),
            ('Sophia', 'Lynnwood', 'Soph')
        )
        self.logger.info("Add people to the Person table.")
        for person in people:
            try:
                with self.database.transaction():
                    new_person = mdl.Person.create(
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME]
                    )
                    new_person.save()
                    self.logger.info('Database add successful.')
            except Exception as e:
                self.logger.info(f'Error creating = {person[PERSON_NAME]}')
                self.logger.info(e)
        self.logger.info('Read and print all Person records we created.')
        for person in mdl.Person:
            self.logger.info(
                f'{person.person_name} lives in {person.lives_in_town} '
                f'and likes to be known as {person.nickname}.'
            )
        person_query = mdl.Person.select(
            pw.fn.COUNT(mdl.Person.person_name)
        )
        person_count = person_query.scalar()
        self.logger.info(f'Number of Person records: {person_count}.\n')

    def fill_department_table(self):
        """Fill the Department table with data."""
        DEPT_NUM, DEPT_NAME, DEPT_MGR = 0, 1, 2
        dept_details = (
            ('A147', 'Administration', "Neil O'Neal"),
            ('M258', 'Accounting', 'Shelly Belly'),
            ('E369', 'Engineering', "Frank Furter"),
            ('A999', 'Circus', "Ring M. Aster"),
            ('C96', 'Purgatory6', 'Watts Miname5'),  # Invalid-won't be added
            ('H40X', 'Purgatory8', 'Whose Whom')  # Ditto
        )
        self.logger.info('Add departments to the Department table.')
        for dept in dept_details:
            try:
                with self.database.transaction():
                    new_department = mdl.Department.create(
                        department_number=dept[DEPT_NUM],
                        department_name=dept[DEPT_NAME],
                        manager=dept[DEPT_MGR]
                    )
                    new_department.save()
                    self.logger.info('Database add successful.')
            except Exception as e:
                self.logger.info(f'Error creating = {dept[DEPT_NUM]}.')
                self.logger.info(e)
        self.logger.info('Read and print all Department records we created.')
        for dept in mdl.Department:
            self.logger.info(
                f'{dept.department_number}: {dept.department_name} managed by '
                f'{dept.manager}.'
            )
        dept_query = mdl.Department.select(
            pw.fn.COUNT(mdl.Department.department_number)
        )
        dept_count = dept_query.scalar()
        self.logger.info(f'Number of Department records: {dept_count}.\n')

    def fill_deptjobs_table(self):
        """Fill the DeptJobs table with data."""
        DJ_JOBNAME, DJ_DEPTNUM = 0, 1
        jobs_in_dept = (
            ('Analyst', 'E369'),
            ('Senior analyst', 'E369'),
            ('Senior business analyst', 'M258'),
            ('Clown', 'A999'),
            ('Lion tamer', 'A999'),
            ('Admin supervisor', 'A147'),
            ('Admin manager', 'A147')
        )
        self.logger.info("Add departments and jobs to the DeptJobs table.")
        for job in jobs_in_dept:
            try:
                with self.database.transaction():
                    dept_job_link = mdl.DeptJobs.create(
                        job_name=job[DJ_JOBNAME],
                        department_number=job[DJ_DEPTNUM]
                    )
                    dept_job_link.save()
                    self.logger.info('Database add successful.')
            except Exception as e:
                self.logger.info(
                    f'Error creating = {job[DJ_JOBNAME]}, {job[DJ_DEPTNUM]}.'
                )
                self.logger.info(e)
        self.logger.info('Read and print all DeptJobs records we created.')
        for job in mdl.DeptJobs:
            self.logger.info(f'Added {job.job_name}: {job.department_number}.')
        dept_job_query = mdl.DeptJobs.select(
            pw.fn.COUNT(mdl.DeptJobs.job_name)
        )
        dept_job_count = dept_job_query.scalar()
        self.logger.info(f'Number of DeptJobs records: {dept_job_count}.\n')

    def fill_job_table(self):
        """Fill the Job table with data."""
        JOB_NAME, JOB_START, JOB_END, JOB_SALARY, JOB_PERSON = 0, 1, 2, 3, 4
        jobs = (
            ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew'),
            ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
            ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew'),
            ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter'),
            ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter')
        )
        self.logger.info('Add jobs to the Job table.')
        for job in jobs:
            try:
                with self.database.transaction():
                    job_stint = mdl.Job.create(
                        job_name=job[JOB_NAME],
                        start_date=job[JOB_START],
                        end_date=job[JOB_END],
                        salary=job[JOB_SALARY],
                        person_employed=job[JOB_PERSON]
                    )
                    job_stint.save()
            except Exception as e:
                self.logger.info(
                    f'Error creating job stint for {job[JOB_PERSON]} '
                    f'starting {job[JOB_START]}.'
                )
                self.logger.info(e)
        self.logger.info('Read and print all Job records we created.')
        for job in mdl.Job:
            self.logger.info(
                f'Added {job.person_employed} as a {job.job_name} from '
                f'{job.start_date} to {job.end_date} for {job.salary}.'
            )
        job_query = mdl.Job.select(pw.fn.COUNT(mdl.Job.person_employed))
        job_count = job_query.scalar()
        self.logger.info(f'Number of Job records: {job_count}.\n')

    def get_all_job_stints(self):
        """Return info about each person's job."""
        self.logger.info(
            "Query for people's jobs, departments, managers, and durations."
        )
        data_query = (mdl.Job.select(
            mdl.Job.person_employed,
            mdl.Job.job_name.alias('job'),
            mdl.Department.department_name.alias('dept_name'),
            mdl.Department.manager.alias('mgr'),
            (
                pw.fn.JULIANDAY(mdl.Job.end_date) -
                pw.fn.JULIANDAY(mdl.Job.start_date) + 1
            ).alias('duration')
        ).join(mdl.DeptJobs).join(mdl.Department, pw.JOIN.LEFT_OUTER).where(
            mdl.Job.job_name == mdl.DeptJobs.job_name and
            mdl.DeptJobs.department_number == mdl.Department.department_number
        ).order_by(mdl.Department.department_name, pw.SQL('duration').desc()))
        self.logger.info(f"Length of data_query: {len(data_query)}.")
        for gig in data_query:
            self.logger.info(vars(gig))
            self.logger.info(
                f'Person {gig.person_employed} '
                f'worked as a {gig.job} '
                # f'in department {gig.dept_name} for '
                # f'manager {gig.mgr} '
                f'for a total of {gig.duration} days.'
            )
        data_count_query = pw.fn.COUNT(data_query)
        data_total = data_count_query.scalar()
        self.logger.info(f'Number of job stints: {data_total}.\n')

    def close_database(self):
        """Close the database."""
        self.logger.info("Close the database.\n")
        self.database.close()

if __name__ == '__main__':
    ManipulateDb()