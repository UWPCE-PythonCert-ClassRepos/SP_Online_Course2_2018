"""
Module for querying Neo4j
"""
import login_database
import utilities
import sample_data

log = utilities.configure_logger('default', './logs/redis_script.log')
sample_data = sample_data.get_data()


class QueriesNeo4j:
    """ Defines Queries class for interacting with DB """

    # ::: SETUP :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def setup_data():
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:

                # add sample data
                for d in sample_data:
                    cs1 = ("first_name: '{}', "
                           "last_name: '{}', "
                           "email: '{}', "
                           "phone: '{}', "
                           "zip_code: '{}', "
                           "donations: {}")

                    cs2 = cs1.format(
                        d['first_name'],
                        d['last_name'],
                        d['email'],
                        d['phone'],
                        d['zip_code'],
                        d['donations']
                    )

                    cyph = "CREATE (d:Donor {{{}}})".format(cs2)
                    session.run(cyph)

        except Exception as e:
            log.info(e)

    @staticmethod
    def drop_donors():
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                session.run("MATCH (d) DETACH DELETE d")
        except Exception as e:
            log.info(e)

    # ::: SEARCH :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def get_donor_by_last(last_name):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE d.last_name = '%s'
                    RETURN d
                """ % last_name
                d = None
                result = session.run(cypher)
                for nodes in result:
                    for p in nodes:
                        d = p

                if d:
                    return True
                else:
                    return False

        except Exception as e:
            log.info(e)

    @staticmethod
    def get_donor_by_id(donor_id):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE ID(d) = %s
                    RETURN d
                """ % donor_id
                result = session.run(cypher)
                for nodes in result:
                    for p in nodes:
                        d = p
                        break
            return d
        except Exception as e:
            log.info(e)

    @staticmethod
    def get_donors():
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    RETURN d
                """
                dl = []
                result = session.run(cypher)
                for nodes in result:
                    for p in nodes:
                        dl.append(p)
            return dl
        except Exception as e:
            log.info(e)

    # ::: MODIFY :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def insert_donor(d):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cs1 = ("first_name: '{}', "
                       "last_name: '{}', "
                       "email: '{}', "
                       "phone: '{}', "
                       "zip_code: '{}', "
                       "donations: [{}]")
                cs2 = cs1.format(
                    d.first_name,
                    d.last_name,
                    d.email,
                    d.phone,
                    d.zip_code,
                    d.donations
                )
                cyph = "CREATE (d:Donor {{{}}})".format(cs2)
                session.run(cyph)

        except Exception as e:
            log.info(e)

    @staticmethod
    def insert_donation(d, donation):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE ID(d) = %s
                    SET d.donations = d.donations + %s
                    RETURN d
                """ % (d.id, donation)
                session.run(cypher)

        except Exception as e:
            log.info(e)

    @staticmethod
    def update_donor(d, ud):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE ID(d) = %s
                    SET d.first_name = '%s',
                        d.last_name = '%s',
                        d.email = '%s',
                        d.phone = '%s',
                        d.zip_code = '%s'
                    RETURN d
                """ % (d.id,
                       ud.first_name,
                       ud.last_name,
                       ud.email,
                       ud.phone,
                       ud.zip_code)
                session.run(cypher)
        except Exception as e:
            log.info(e)

    @staticmethod
    def delete_donor(d):
        """ deletes donor """
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE ID(d) = %s
                    DETACH DELETE d
                """ % (d.id)
                session.run(cypher)
        except Exception as e:
            log.info(e)

    # ::: PREPARE :::::::::::::::::::::::::::::::::::::::::: #
    def get_donor_multiple_summary(self):
        try:
            """
            Compiles a list for printing multiple donor summaries
            Called methods establish DB connection
            """
            nl = list()
            nodes = self.get_donors()
            for n in nodes:
                total = self.donations_total(n) if self.donations_total(n) else 0
                count = self.donations_count(n) if self.donations_count(n) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl.append([n['first_name'], n['last_name'], total, count, average])
            return nl

        except Exception as e:
            log.info(e)

    @staticmethod
    def donations_total(d):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE ID(d) = %s
                    RETURN d
                """ % (d.id)
                result = session.run(cypher)
                d = None
                for nodes in result:
                    for p in nodes:
                        d = p
                        break

            return sum(d['donations'])

        except Exception as e:
            log.info(e)

    @staticmethod
    def donations_count(d):
        try:
            driver = login_database.login_neo4j_cloud()
            with driver.session() as session:
                cypher = """
                    MATCH (d)
                    WHERE ID(d) = %s
                    RETURN d
                """ % (d.id)
                result = session.run(cypher)
                d = None
                for nodes in result:
                    for p in nodes:
                        d = p
                        break

            return len(d['donations'])

        except Exception as e:
            log.info(e)

    def get_donor_single_summary(self, d):
        try:
            """
            Compiles a list for printing a single donor summary
            Called methods establish DB connection
            """
            nl = list()
            total = self.donations_total(d) if self.donations_total(d) else 0
            count = self.donations_count(d) if self.donations_count(d) else 0
            average = 0
            if total > 0 and count > 0:
                average = total / count
            nl.append([d['first_name'],
                       d['last_name'],
                       total, count, average])
            return nl

        except Exception as e:
            log.info(e)
