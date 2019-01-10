"""
    Clears neo4j database
"""

import login_neo4j

def clear_database():

    driver = login_neo4j.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

if __name__ == '__main__':
    clear_database()