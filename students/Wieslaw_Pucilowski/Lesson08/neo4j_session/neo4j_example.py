from neo4j.v1 import GraphDatabase, basic_auth
import logging
import pprint
pp = pprint.PrettyPrinter(width=120)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_neo4j_cloud():
    """
        connect to neo4j and login

    """

    logger.info('Here is where we use the connect to neo4j.')
    logger.info('')
    graphenedb_user = "<user>"
    graphenedb_pass = "password string"
    graphenedb_url = 'bolt://connection string'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver


if __name__ == "__main__":

    ################################################################
    # Clear entire database
    ################################################################
    
    logger.info('Step 1: First, clear the entire database, so we can start over')
    logger.info("Running clear_all")

    driver = login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    ################################################################
    # Add some entries
    ################################################################
    
    logger.info("Step 2: Add a few people")
    with driver.session() as session:
        logger.info('Adding a few Person nodes')
        logger.info('The cyph language is analagous to sql for neo4j')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)
    
    ################################################################
    # Retrieve entries from DB
    ################################################################

        logger.info("Step 3: Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])
        
        ################################################################
        # Create relationship
        ################################################################
    
        logger.info('Step 4: Create some relationships')
        logger.info("Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie")
    
        for first, last in [("Alice", "Cooper"),
                            ("Fred", "Barnes"),
                            ("Marie", "Curie")]:
            cypher = """
              MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            session.run(cypher)
        ################################################################
        # Find all of Bob's friends
        ################################################################
        logger.info("Step 5: Find all of Bob's friends")
        cyph = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FRIEND]->(bobFriends)
          RETURN bobFriends
          """
        result = session.run(cyph)
        print("Bob's friends are:")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])
        
        logger.info("Setting up Marie's friends")
    
        for first, last in [("Mary", "Evans"),
                            ("Alice", "Cooper"),
                            ('Fred', 'Barnes'),
                            ]:
            cypher = """
                MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
                CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
                RETURN p1
              """ % (first, last)
    
            session.run(cypher)
    
        ################################################################
        # find all of Marie's friends
        ################################################################
        logger.info("Step 6: Find all of Marie's friends?")
        cyph = """
          MATCH (marie {first_name:'Marie', last_name:'Curie'})
                -[:FRIEND]->(friends)
          RETURN friends
          """
        result = session.run(cyph)
        print("\nMarie's friends are:")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])
