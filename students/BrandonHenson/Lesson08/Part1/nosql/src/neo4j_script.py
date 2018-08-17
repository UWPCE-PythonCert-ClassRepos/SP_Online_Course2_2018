"""
    neo4j example
"""
import utilities
import login_database


log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():

    log.info('\n\nStep 1: First, clear the entire database, so we can start over')
    log.info("\nRunning clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("\n\nStep 2: Add a few people")

    with driver.session() as session:

        log.info('Adding a few Person nodes')
        log.info('The cypher language is analagous to sql for neo4j')
        for first, last in [('Bob', 'Jones'),
                                ('Nancy', 'Cooper'),
                                ('Alice', 'Cooper'),
                                ('Fred', 'Barnes'),
                                ('Mary', 'Evans'),
                                ('Marie', 'Curie'),
                                ('Brandon', 'Henson'),
                                ('Alicia', 'Henson'),
                                ('Michael', 'Green')]:
                
                cypher = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (first, last)
                session.run(cypher)
        
        new_person = "CREATE (rummy:Person {first_name:'Kaiya', last_name:'Henson'}) RETURN rummy"
        session.run(new_person)
        new_person = "CREATE (rummy:Person {first_name:'Brent', last_name:'Preston'}) RETURN rummy"
        session.run(new_person)
        new_person = "CREATE (rummy:Person {first_name:'Jessie', last_name:'Berner'}) RETURN rummy"
        session.run(new_person)
        cypher = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cypher)
        for record in result:
            print(record['first_name'], record['last_name'])
                
        log.info('\n\nAdd colors')
        for color in ['red', 'orange', 'yellow', 'green', 'blue', 'purple' ]:
            cyphery = "CREATE (c:Color {color:'%s'})" % (color)
            session.run(cyphery)

        log.info("\n: Get people")
                
        cyphery = """MATCH (c:Color)
        RETURN c.color as color"""
        
        result = session.run(cypher)
        for record in result:
            print(record['first_name'], record['last_name'])
            
        result1 = session.run(cyphery)
        print("\nColors in database:")
        for c in result1:
            print(c['color'])
    
        log.info('\nStep 4: Create some relationships')
        log.info("\nBob Jones likes Alice Cooper, Fred Barnes and Marie Curie")
    
        for first, last in [("Alice", "Cooper"),
                            ("Fred", "Barnes"),
                            ("Marie", "Curie")]:
            cypherer = """
              MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            session.run(cypherer)
            
        log.info('\nStep 4A: Create color/person relationships')
        cypher = """MATCH (p:Person {first_name:'Brandon'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'blue'})
                RETURN p, f, c
                """
        session.run(cypher)
        
        cypher = """MATCH (p:Person {first_name:'Alicia'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'yellow'})
                RETURN p, f, c
                """
        session.run(cypher)
        
        cypher = """MATCH (p:Person {first_name:'Michael'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'green'})
                RETURN p, f, c
                """
        session.run(cypher)
        
        cypher = """MATCH (p:Person {first_name:'Mary'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'blue'})
                RETURN p, f, c
                """
        session.run(cypher)
        
        cypher = """MATCH (p:Person {first_name: "Michael", last_name:'Green'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'yellow'})
                RETURN p, f, c
                """
        session.run(cypher)
        
        cypher = """MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person)
                RETURN c.color, p.first_name
                """
        result = session.run(cypher)
        for rec in result:
            print(rec.values()[0], "is a favorite color of", rec.values()[1])
        
        log.info('\n\nFind who\'s favorite color is blue')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='blue') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for rec in result:
            print(rec.values()[1])
            
        log.info('\n\nFind who\'s favorite color is yellow')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='yellow') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for rec in result:
            print(rec.values()[1])
            
        log.info('\n\nFind who\'s favorite color is green')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='green') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for rec in result:
            print(rec.values()[1])
            
        log.info('\n\nFind who\'s favorite color is red')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='red') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for rec in result:
            print(rec.values()[1]) 
            
        log.info("\n\nall the colors")
        q = """MATCH (c:Color)
                RETURN c"""
        results = session.run(q)  
        
        c = set()
        for color in results:
            for i in color.values():
                c.add(i['color'])
        print(c)
        c = list(c)
        
        log.info('\n\nWho likes what colors')
        q = """MATCH (c:Color)<-[:FAV_COLOR]-(p:Person) 
            RETURN c.color AS Color, collect(p.last_name) AS Last_Name"""
        results = session.run(q)
        for rec in results:
            print(rec.values()[0], "is a favorite color of", rec.values()[1])
            
        log.info("\n\nStep 5: Find all of Bob's friends")
        cypher = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FRIEND]->(bobFriends)
          RETURN bobFriends
          """
        result = session.run(cypher)
        print("\nBob's friends are:")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])

        log.info("\nSetting up Marie's friends")

        for first, last in [("Mary", "Evans"),
                            ("Alice", "Cooper"),
                            ('Fred', 'Barnes'),
                            ]:
            cypherer = """
              MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)

            session.run(cypherer)

        print("\nStep 6: Find all of Marie's friends?")
        cypher = """
          MATCH (marie {first_name:'Marie', last_name:'Curie'})
                -[:FRIEND]->(friends)
          RETURN friends
          """
        result = session.run(cypher)
    print("\nMarie's friends are:")
    for rec in result:
        for friend in rec.values():
            print(friend['first_name'], friend['last_name'])

        
        
        
        
        
        
