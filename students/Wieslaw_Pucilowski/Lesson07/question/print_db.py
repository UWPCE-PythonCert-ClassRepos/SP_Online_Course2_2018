from pprint import pprint as pp
from create_personjob import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')


def main():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select())
        pp('{:25} - {:10} - {:10} - {:10} - {:5}'.format(
            'Job Name', 'Start', 'End', 'Duration', 'Name', 'Department'))
        for job in query:
            pp('{:25} - {:10} - {:10} - {:10} - {:5}'.format(
                job.job_name, job.start_date, job.end_date, job.duration, str(job.person_employed), str(job.job_department
            )))
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

    # SELECT person.person_name, job.job_name, department.department_name, job.salary, job.duration, department.department_manager
    # FROM person 
    # INNER JOIN job on person.person_name = job.person_employed_id
    # LEFT OUTER JOIN department on job.job_department_id = department.department_number;
    print("************** JOIN 1 ****************")
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                .select(Person.person_name,
                        Job.job_name,
                        Department.department_name,
                        Job.salary,
                        Job.duration,
                        Department.department_manager)
                .join(Job,
                      JOIN.INNER,
                      on=['Person.person_name = Job.person_employed_id']) # joins person -> job
                .join(Department, 
                      JOIN.LEFT_OUTER,
                      on=['Job.job_department_id = Department.department_number']) # joins job -> department
        )
    
        pp('{:15} - {:15} - {:15} - {:10} - {:10} - {:10}'.format(
                                    'Person',
                                    'Job',
                                    'Department',
                                    'Salary',
                                    'Duration',
                                    'Manager')
                                )
        for job in query:
                pp('{:15} - {:15} - {:15} - {:10} - {:10} - {:10}'.format(
                                            Person.person_name,
                                            Job.job_name,
                                            Department.department_name,
                                            Job.salary,
                                            Job.duration,
                                            Department.department_manager
                                        )
                   )
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

    print("************** JOIN 2 ****************")
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                    .select(Person.person_name, Job.job_name)
                    .join(Job,
                        JOIN.LEFT_OUTER
                        # on=['person.person_name = job.person_employed_id']
                        )
                )
    
        pp('{:15} - {:15}'.format('Person', 'Job'))
        for job in query:
                pp('{:15} - {:15}'.format(Person.person_name, Job.job_name))
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

if __name__ == '__main__':
    main()
