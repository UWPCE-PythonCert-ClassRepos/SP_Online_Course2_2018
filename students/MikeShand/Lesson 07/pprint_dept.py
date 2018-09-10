import pprint

from personjobdept_model import *

import logging





logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)



database = SqliteDatabase('personjobdept.db')





def main():

    try:

        database.connect()

        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info("Querying the database")

        query = (Job.select(Job.person_employed, Job.job_name).order_by(Job.person_employed.desc()))

        for person in query:
            items = [person.person_employed, person.job_name]


            pprint(items)



    except Exception as error:

        logger.info(error)

    finally:

        database.close()





if __name__ == '__main__':

    main()