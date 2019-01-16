"""
    This module populates neo4j with data for the mailroom program
"""

import login_neo4j

def populate_database():
    driver = login_neo4j.login_neo4j_cloud()
    with driver.session() as session:
        check = """MATCH (t: Count)
        RETURN t.inv as inv, t.cust as cust
        """
        result = session.run(check)
        bool = False
        for item in result:
            bool = True
        if not bool:
            init = """CREATE (t: Count {inv:%d, cust:%d})""" % (1, 100)
            result = session.run(init)

        for dict in donator_data:
            numbers = """MATCH (t: Count)
            RETURN t.inv as inv, t.cust as cust
            """
            result = session.run(numbers)
            for item in result:
                items = [item['inv'], item['cust']]
            print(items)
            increase = """MATCH (t: Count)
            SET t.inv = %d, t.cust = %d
            RETURN t.inv, t.cust
            """ % (items[0] + 1, items[1] + 1)
            session.run(increase)
            
            new_inv = items[0]
            new_cust = items[1]
            new_cust_num = f"{dict['name'][0]}{str(new_cust)}"
            cyph = "CREATE (n: Donor {name:'%s', cust: '%s',\
            total_donations:%f, average:%f, first_gift:%f,\
            last_gift:%f, transactions:%d, email:'%s', phone:'%s'})\
            " % (dict['name'], new_cust_num, dict['total_donations'],
            dict['average'], dict['first_gift'], dict['last_gift'],
            dict['transactions'], dict['email'], dict['phone'])
            session.run(cyph)
            
            cypher = """
            MATCH (n: Donor {name: '%s'})
            CREATE (i: Invoice {invoice:%d}),(d:Donation {donation:%f}),
                   (n)-[:INVOICE]->(i)-[:DONATION]->(d)
            RETURN n
            """ % (dict['name'], new_inv, dict['donation2'])
            session.run(cypher)
            
        for dict in donator_data:
            cyph = """
            MATCH (p1: Donor {name:'%s'})-[r1:INVOICE]-(i)-[r2:DONATION]-(d)
            RETURN p1.name as name, d.donation as don, i.invoice as inv
            """ % (dict['name'])
            result = session.run(cyph)
            
            for item in result:
                print(item['name'], item['inv'], item['don'])
            
#            cyph = """
#            MATCH (p1: Donor {name:%s'})-[r1:INVOICES]->(invoices)
#            RETURN p1
#            """ % (name)
            

#        for dono in donator_data:
#            cypher = """
#            MATCH (p1: Donor {name:'%s'})
#            CREATE (p1)-[donations:DONATIONS]->(c:Donation {donation:'%s'})
#            RETURN p1
#            """ % (dono['name'], dono['donation1'])
#            session.run(cypher)

#must run a new session 
                    
        
#        for dono in donator_data:
#            cypher = """
#            MATCH (p1: Donor {name:'%s'})
#            CREATE (p1)-[donations:DONATIONS]->(c:Donation {donation:'%s'})
#            RETURN p1
#            """ % (dono['name'], dono['donation2'])
#            session.run(cypher)
            
#        cyph = """MATCH (p:Donor)
#                RETURN p.name as name, p.cust_num as cust_num,
#                p.total_donations as total_donations, p.average as average,
#                p.first_gift as first_gift, p.last_gift as last_gift,
#                p.transactions as transactions, p.email as email,
#                p.phone as phone
#                """
#must run a new session 
#        result = session.run(cyph)
#        a, b, c = [], [], []
#        names = []
#        for item in result:
#            names += [item['name']]
#        for name in names:
#            cyph = """MATCH (p1: Donor {name:'%s'})
#                    -[:DONATIONS]->(donations)
#              RETURN donations
#              """ % (name)
#            result = session.run(cyph)
#            print(f"\n{name}'s donations are:")
#            for rec in result:
#                for ind in rec.values():
#                    print(ind['donation'])

#            b += [item['cust_num']]
#            c += [item['total_donations']]
#        print(a)
#        print(b)
#        print(c)
#        a = [record['name'] for record in result]
#        result = session.run(cyph)
#        b = [record2['cust_num'] for record2 in result]
#        for ind in a:
#            print(ind)
#        for ind in b:
#            print(ind)

donator_data = [
    {
        'name': 'Andrew Braddock',
        'total_donations': 800,
        'average': 400,
        'first_gift': 200,
        'last_gift': 600,
        'transactions': 2,
        'email': 'abraddock@gmail.com',
        'phone': '509-777-9999',
        'cust_num': 'A100',
        'donation1': [200, 600],
        'donation2': 600, 
    },
    {
        'name': 'Janet Jackson',
        'donation1': [300, 500],
        'donation2': 500,
        'total_donations': 800,
        'average': 400,
        'first_gift': 300,
        'last_gift': 500,
        'transactions': 2,
        'email': 'jjackson@gmail.com',
        'phone': '503-334-5029',
        'cust_num': 'J100'
    },
    {
        'name': 'Joshua Hoff',
        'donation1': 100,
        'donation2': 400,
        'average': 500,
        'first_gift': 100,
        'last_gift': 500,
        'total_donations': 500,
        'transactions': 2,
        'email': 'jhoff@gmail.com',
        'phone': '222-333-5555',
        'cust_num': 'J101'
    },
    {
        'name': 'Melanie Scott',
        'donation1': 400,
        'donation2': 550,
        'total_donations': 950,
        'average': 475,
        'first_gift': 400,
        'last_gift': 550,
        'transactions': 2,
        'email': 'abraddock@gmail.com',
        'phone': '604-867-5309',
        'cust_num': 'M100'
    },
    {
        'name': 'Tatsiana Kisel',
        'donation1': 600,
        'donation2': 600,
        'total_donations': 1200,
        'average': 600,
        'first_gift': 600,
        'last_gift': 600,
        'transactions': 2,
        'email': 'tkisel@gmail.com',
        'phone': '509-253-3377',
        'cust_num': 'T100'
    }
    ]




if __name__ == '__main__':
    populate_database()