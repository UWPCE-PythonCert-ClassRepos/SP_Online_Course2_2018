"""
    updated donor/donation database implementation
       for Python 220 Lesson 8 assignment (non-relational databases)

    Database implementation using Neo4j
"""

import logging
import login_database
from os import mkdir
from os.path import isdir

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Donations():
    """
        This class defines a Donation database.
        Implemented with Neo4j.
    """

    def __init__(self):
        self._driver = login_database.login_neo4j_cloud()


    def clear_db(self):
        with self._driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")


    def close_db(self):
        self._driver.close()


    def list_donors(self):
        with self._driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN DISTINCT p.name as name")
            return [record[0] for record in result]


    def add_donation(self, name, amount):
        with self._driver.session() as session:
            session.run(f"CREATE (p:Person {{name: '{name}', donation: toFloat('{amount}'), timestamp: timestamp()}})")


    def summary_report(self):
        with self._driver.session() as session:
            report = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n"
            cypher = f"""
                      MATCH (p:Person)
                      RETURN p.name as name, sum(p.donation) as sum, count(*) as count, avg(p.donation) as avg
                      ORDER BY sum DESC, name
                      """
            result = session.run(cypher)
            for r in result:
                report += f"{r['name']:20s}   ${r['sum']:12,.2f} {r['count']:3d}" \
                        + f"               ${r['avg']:11,.2f}\n"
        return report


    def donation_log(self):
        with self._driver.session() as session:
            report = ""
            result = session.run(f"MATCH (p:Person) RETURN p.name as name, p.donation as amount")
            for r in result:
                report += f"{r['name']}: ${r['amount']:.2f}\n"
            return report


    def thank_you_letter(self, name):
        with self._driver.session() as session:
            cypher = f"""
                      MATCH (p:Person {{name:'{name}'}})
                      RETURN p.name as name, p.donation as amount
                      ORDER BY timestamp() DESC LIMIT 1
                      """
            result = session.run(cypher).single()
            return f"Dear {result['name']},\n" \
                   f"Thank you very much for your generous donation of ${result['amount']:,.2f}.\n" \
                   f"Sincerely,\n" \
                   f"PYTHON220 Class of 2019"


    def send_all_letters(self, dir_name):
        if not isdir(dir_name):
            mkdir(dir_name)
        donor_list = self.list_donors()
        for donor in donor_list:
            file_name = dir_name + '/' + donor.replace(',', '').replace(' ', '_') + '.txt'
            with open(file_name, 'w') as f:
                f.write(self.thank_you_letter(donor))


    def challenge(self, factor, min_donation=0, max_donation=1e10):
        with self._driver.session() as session:
            cypher = f"""
                      MATCH (p:Person)
                      WHERE {min_donation} <= p.donation <= {max_donation}
                      RETURN p.name as name, sum(p.donation) as sum
                      ORDER BY name
                      """
            result = session.run(cypher)
            total = 0
            report = ""
            for r in result:
                report += f"   {r['name']}: ${factor*float(r['sum']):,.2f} = " \
                        + f"{factor} * ${float(r['sum']):,.2f}\n"
                total += factor * float(r['sum'])
            report += f"\n   Total contribution required: ${total:,.2f}\n"
            return report


    def delete_donation(self, name, amount):
        with self._driver.session() as session:
            cypher = f"""
                      MATCH (p:Person {{name: '{name}'}})
                      WHERE p.donation = {amount}
                      WITH p LIMIT 1
                      DELETE p RETURN count(*) as count
                      """
            result = session.run(cypher).single()['count']
        return result


    def delete_donor(self, name):
        with self._driver.session() as session:
            cypher = f"""
                      MATCH (p:Person {{name: '{name}'}})
                      DELETE p RETURN count(*) as count
                      """
            result = session.run(cypher).single()['count']
        return result


    def update_donation(self, name, old_amount, new_amount):
        with self._driver.session() as session:
            cypher = f"""
                      MATCH (p:Person {{name: '{name}'}})
                      WHERE p.donation = {old_amount}
                      WITH p LIMIT 1
                      set p.donation = {new_amount} RETURN count(*) as count
                      """
            result = session.run(cypher).single()['count']
        return result


    def update_donor(self, old_name, new_name):
        with self._driver.session() as session:
            check = session.run(f"MATCH (p:Person {{name: '{new_name}'}}) RETURN count(*) as count")
            if check.single()['count'] > 0:
                return 0
            cypher = f"""
                      MATCH (p:Person {{name: '{old_name}'}})
                      SET p.name = '{new_name}'
                      RETURN count(*) as count
                      """
            result = session.run(cypher).single()['count']
        return result


def create_default_db():
    donor_data = [
        ('William Gates, III', 653772.32),
        ('William Gates, III', 12.17),
        ('Jeff Bezos', 877.33),
        ('Paul Allen', 663.23),
        ('Paul Allen', 43.87),
        ('Paul Allen', 1.32),
        ('Mark Zuckerberg', 1663.23),
        ('Mark Zuckerberg', 4300.87),
        ('Mark Zuckerberg', 10432.0),
        ('Colleen Kaku', 50000),
        ('Colleen Kaku', 1000000)
    ]

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:

        session.run("MATCH (n) DETACH DELETE n")

        for name, amount in donor_data:
            session.run(f"CREATE (p:Person {{name: '{name}', donation: toFloat('{amount}'), timestamp: timestamp()}})")

    driver.close()

def print_db():
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:

        result = session.run("MATCH (p:Person) RETURN p.name as name, p.donation as amount, p.timestamp as timestamp")

        for record in result:
            print(f"{record['name']}, {record['amount']}, {record['timestamp']}")

    driver.close()


if __name__ == '__main__':
    create_default_db()
    print_db()