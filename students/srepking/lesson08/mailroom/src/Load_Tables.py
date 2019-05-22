import utilities as utilities


def get_people_data():
    """
    Create some people for the mailroom MongoDB database.
    """

    people_data = [
        {
            'donor': 'Shane',
            'donations': [6, 5, 10],
        },
        {
            'donor': 'Pete',
            'donations': [7, 8],
        },
        {
            'donor': 'Zach',
            'donations': [10],
        },
        {
            'donor': 'Fitz',
            'donations': [1],
        },
        {
            'donor': 'Joe',
            'donations': [5, 4, 3, 2, 1],
        }

    ]
    return people_data


def populate_redis(r):
    """Create a cache of data for Lesson 08 mailroom"""
    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        # login_database.login_redis_cloud()
        log.debug('For Lesson 08 Assignment, add name, tele, and email.')
        # first delete the key if it exists already
        r.delete('Shane')
        # then create a new entry
        r.rpush('Shane', 'Repking')
        r.rpush('Shane', '677-0180')
        r.rpush('Shane', 'sr@gmail.com')

        # first delete the key if it exists already
        r.delete('Zach')
        r.rpush('Zach', 'Gillis')
        r.rpush('Zach', '677-0181')
        r.rpush('Zach', 'zg@gmail.com')

        # first delete the key if it exists already
        r.delete('Joe')
        r.rpush('Joe', 'Slinger')
        r.rpush('Joe', '677-0182')
        r.rpush('Joe', 'js@gmail.com')

        # first delete the key if it exists already
        r.delete('Fitz')
        r.rpush('Fitz', 'Patrick')
        r.rpush('Fitz', '677-0183')
        r.rpush('Fitz', 'fp@gmail.com')

        # first delete the key if it exists already
        r.delete('Pete')
        r.rpush('Pete', 'Chair')
        r.rpush('Pete', '876-9546')
        r.rpush('Pete', 'pc@gmail.com')

    except Exception as e:
        print(f'Redis error: {e}')


def load_neo4j(driver):
    """Load our mailroom rdbms into a graph database. Each row in an entity
    table is a node. Columns on those tables become a node property.
    For each person, we will have a node with two properties, the person's
    name and the person's donations. The node will have a label :Person.
    Because donations are unique to the donor, it makes sense to make this a
    node property along with the name of donor. If we were storing email,
    address, and telephone, it would also make sense to store these as node
    properties since they are unique to the donor.."""

    log = utilities.configure_logger('default', '../logs/neo4j_LoadTables.log')

    log.debug('Step 1: First, clear the entire database, so we can start over')
    log.debug("Running clear_all")

    # driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        log.debug("Step 2: Add a few people")
        cyph = "CREATE (n:Person {donor:'Zach', donations:[10]})"
        session.run(cyph)
        cyph = "CREATE (n:Person {donor:'Shane', donations:[6, 5, 10]})"
        session.run(cyph)
        cyph = "CREATE (n:Person {donor:'Pete', donations:[7, 8]})"
        session.run(cyph)
        cyph = "CREATE (n:Person {donor:'Fitz', donations:[1]})"
        session.run(cyph)
        cyph = "CREATE (n:Person {donor:'Joe', donations:[5, 4, 3, 2, 1]})"
        session.run(cyph)
