import login_database
from donor_data import get_donor_data

with login_database.login_mongodb_cloud() as client:
    db = client['donors']
    db.drop_collection('donor')

    donor = db['donor']

    donor_items = get_donor_data()
    donor.insert_many(donor_items)
    

r = login_database.login_redis_cloud()

r.flushdb()

donor_items = get_donor_data()

for donor in donor_items:
    r.set(donor['name'], donor['donation'])


driver = login_database.login_neo4j_cloud()

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")
        
with driver.session() as session:
    for donor in donor_items:
        cyph = "CREATE (n:Person {name:'%s'})" % (donor['name'])
        session.run(cyph)

    for donor in donor_items:
        cyphery = "CREATE (c:Donation {donation:'%s'})" % (donor['donation'])
        session.run(cyphery) 

    cyph = """MATCH (p:Person {name:'Andrew'})  
            CREATE (p)-[f:DONATION]->(c:Donation {donation:'1005.49'})
            RETURN p, f, c
            """
    session.run(cyph)

    cyph = """MATCH (p:Person {name:'Peter'})  
            CREATE (p)-[f:DONATION]->(c:Donation {donation:'21.47'})
            RETURN p, f, c
            """
    session.run(cyph)

    cyph = """MATCH (p:Person {name:'Susan'})  
            CREATE (p)-[f:DONATION]->(c:Donation {donation:'2400.54'})
            RETURN p, f, c
            """
    session.run(cyph)

    cyph = """MATCH (p:Person {name:'Pam'})  
            CREATE (p)-[f:DONATION]->(c:Donation {donation:'355.42'})
            RETURN p, f, c
            """
    session.run(cyph)

    cyph = """MATCH (p:Person {name:'Steven'})  
            CREATE (p)-[f:DONATION]->(c:Donation {donation:'636.9'})
            RETURN p, f, c
            """
    session.run(cyph)