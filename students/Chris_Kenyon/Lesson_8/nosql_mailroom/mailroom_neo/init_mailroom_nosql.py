import login_database
import utilities
import os
from neo4j.v1 import GraphDatabase, basic_auth

log = utilities.configure_logger('default', '../mongo_mailroom.log')


def init_neo():
    """
    connect to neo4j server and populate initial data
    """
    driver = login_database.login_neo4j_cloud()
    
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    with driver.session() as session:
        p1 = session.run("create (n:Person {full_name: 'Justin Thyme', donation: [1, 1, 1]})")
        p2 = session.run("create (n:Person {full_name: 'Crystal Clearwater', donation: [80082]})")
        p3 = session.run("create (n:Person {full_name: 'Harry Shins', donation: [1.00, 2.00, 3.00]})")
        p4 = session.run("create (n:Person {full_name: 'Al Kaseltzer', donation: [1010101, 666.00]})") 

if __name__ == '__main__':
    init_neo()