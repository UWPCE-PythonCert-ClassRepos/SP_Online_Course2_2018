from neo4j.v1 import GraphDatabase, basic_auth
import configparser
from pathlib import Path
import pprint


config_file = Path(__file__).parent.parent / '../.config/config.ini'
config = configparser.ConfigParser()


def connect():
    config.read(config_file)

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-opmhmhgpkdehgbkejbochpal.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(
        graphenedb_url,
        auth=basic_auth(graphenedb_user, graphenedb_pass)
    )

    return driver

def create_donor_data(name, gifts):
    return {'name': name, 'key': name.lower(), 'gifts': gifts}


def get_donor_data():
    donor_data = [
        create_donor_data('Sleve McDichael', [86457.89,2346.43,9099.09]),
        create_donor_data('Willie Dustice', [505.05,43.21]),
        create_donor_data('Rey McScriff', [666.0]),
        create_donor_data('Mike Truk', [70935.3,12546.7,312.0]),
        create_donor_data('Bobson Dugnutt', [1234.56,789.0]),
        create_donor_data('Todd Bonzalez', [10352.07,2394.32]),
        create_donor_data('andrew', [9473.65],)
    ]
    return donor_data

def populate_graph():
    driver = connect()

    with driver.session() as session:
        session.run("MATCH(d:Donor) DELETE d")
        for n, k, g in [(d['name'], d['key'], d['gifts'])
                        for d in get_donor_data()]:
            cyph = "CREATE (n:Donor {name:'%s', key:'%s', gifts:%s})" %(n, k, g)
            session.run(cyph)
        cyph = "MATCH (d:Donor) RETURN d.name as n, d.key as k, d.gifts as g"
        result = session.run(cyph)
        for record in result:
            print(record['n']+' '+record['k']+' '+str(record['g']))
        print()
        empty_cyph = "MATCH (d:Donor {name: 'Bob Jones'}) RETURN d"
        empty_result = session.run(empty_cyph)
        if not empty_result.peek():
            print('empty')
        else:
            print('keep trying')
        
if __name__ == '__main__':
    populate_graph()
            
