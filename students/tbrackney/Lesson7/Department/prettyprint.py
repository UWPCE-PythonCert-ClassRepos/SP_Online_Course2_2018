"""
select p.person_name, p.lives_in_town, j.job_name, j.start_date from person as p
inner join job as j on (p.person_name = j.person_employed_id)
where (j.start_date > '2012-01-01');
"""
import logging
import peewee
from personjob_model import *


database = SqliteDatabase('personjob.db')

query = Person.select(Person, Job).join(Person)

for p  in query:
    print(p.person_name, p.lives_in_town)

q2 = (Person
      .select(Person,
              Job,
              Department,
              (fn.JULIANDAY(Job.end_date) - fn.JULIANDAY(Job.start_date)).cast('int').alias('job_length')
              )
      .join(Job)
      .join(Department)
      .group_by(Job)
      .order_by(Person.person_name)
      )



query = (Job
        .select(Job.person_employed_id,
              Job.job_name,
              Department.dept_name,
              (fn.JULIANDAY(Job.end_date) - fn.JULIANDAY(Job.start_date)).cast('int').alias('job_length')
              )
        .join(Department)
        .group_by(Job)
        .order_by(Job.person_employed_id)
        )

for p in query:
    print(p.)
# q3 =(Person
#     .select(Person, Job.job_name, Job.start_date, Job.end_date)
#     .join(Job)
#     .where(Person.person_name == 'Peter')
#     )

# select cast ((julianday(end_date) - julianday(start_date)) as Integer) from job;

q3 = Job.select(Job.job_name, fn.DATEDIFF(Job.start_date, Job.end_date).alias('duration'))
q3 = Job.select(Job.job_name, (fn.JULIANDAY(Job.end_date) - fn.JULIANDAY(Job.start_date)).cast('int').alias('job_length'))
q3 = Job.select(Job.job_name, Job.end_date)


query = Job.update(end_date='2018-01-05').where(Job.end_date == '2018-01,05')
query = Job.update(end_date='2014-11-10').where(Job.end_date == '2014-11,10')
