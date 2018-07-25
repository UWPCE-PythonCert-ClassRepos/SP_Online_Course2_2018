#!/usr/bin/env python3
"""Simple printer script to print the personnel database."""
import personnel_db_model as model

with model.database as db:
    db.execute_sql('PRAGMA foreign_keys = ON;')

    query = (model.Job.select(model.Job.person_employed,
                              model.Job.job_name,
                              model.Job.job_dept)
             .order_by(model.Job.person_employed.asc(),
                       model.Job.start_date.asc()))

    print('=============================================')
    for job in query:
        print(f'{"Person:": <15}{str(job.person_employed): <25}')
        print(f'{"Job:": <15}{job.job_name: <25}')
        print(f'{"Department:": <15}{str(job.job_dept): <25}')
        print('=============================================')
