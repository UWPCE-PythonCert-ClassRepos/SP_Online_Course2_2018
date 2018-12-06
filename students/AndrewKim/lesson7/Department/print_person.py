import create_person as cp

with cp.database as db:
    db.execute_sql('PRAGMA foreign_keys = ON;')

    data = (cp.Job.select(cp.Job.person_employed,cp.Job.job_name,cp.Job.job_deptartment).order_by(cp.Job.person_employed.asc(),cp.Job.start_date.asc()))

    for index in data:
        print("------------------------------")
        print(f'{"Person Name: "}{str(index.person_employed)}')
        print(f'{"Job: "}{index.job_name}')
        print(f'{"Department Name: "}{str(index.job_deptartment)}')
