        log.info("Setting up Marie's friends")

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

        print("Step 6: Find all of Marie's friends?")
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