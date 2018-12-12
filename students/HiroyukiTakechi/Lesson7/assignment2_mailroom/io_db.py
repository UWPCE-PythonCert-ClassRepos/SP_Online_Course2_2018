"""
    Assignment 2: Input/Output operation of mailroom database
"""

from create_db import *
import logging

    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

databse = SqliteDatabase('mailroom.db')

logger.info('mailroom database input and output operations')

def thank_you_loop():
    pass

    

def create_report():
    pass

    print("{msg1: <50}| {msg2: <12}| " \

        "{msg3:<10}| {msg4: <12}".format(msg1="Donor Name",

                                        msg2="Total Given",

                                        msg3="Num Gifts",

                                        msg4="Average Gift"))
    for d in self.donor_dict:
        t = sum(self.donor_dict[d])
        n = len(self.donor_dict[d])
        a = t / n

    print("{d: <50} ${t: 12.2f}{n: 12d}{a: 14.2f}".format(d=d, t=t, n=n, a=a))

def send_letters():
    pass

def mainloop():
    pass


def quit():
    pass

    print("quit function is called")

    try:
        selection = self.select_quit()
        if (selection == 'Y'):
            print("Good bye...")
            sys.exit()
        else:
            return self.mainloop()

    except ValueError as e:
        print("Error happened. Error is ",type(e),"Please type 1, 2 or 3")
    except KeyError as k:
        print("Error happened. Error is ",type(k),"Please type 1, 2 or 3")


def print_list():
    pass

    print("{msg1: <50}| {msg2: <12}| " \

            "{msg3:<10}| {msg4: <12}".format(msg1="Donor Name",

                                               msg2="Total Given",

                                               msg3="Num Gifts",

                                               msg4="Average Gift"))
    for d in self.donor_dict:
        t = sum(self.donor_dict[d])
        n = len(self.donor_dict[d])
        a = t / n

"""
def query_db():

    try:
        databse.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (Department
                 .select(Department, Job)
                 .join(Job, JOIN.LEFT_OUTER)
                 .group_by(job.person_employed))

        for department in query:
            pprint.pprint('{}, {}, {}'.format(department.department_name, job.job_name, job.person_employed))


    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closes')
        dabase.close()        


"""

if __name__ == '__main__':
    thank_you_loop()

    
















