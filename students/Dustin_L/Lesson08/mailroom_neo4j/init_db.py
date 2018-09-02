#!/usr/bin/env python3
from donor_dict import DonorDict


def main():
    """Populates the Redis database"""
    db = DonorDict()
    donor_data = [{db.name_key: 'Toni Morrison', db.donations_key: [1000, 5000, 100]},
                  {db.name_key: 'Mike McHargue', db.donations_key: [12000, 5000, 2500]},
                  {db.name_key: "Flannery OConnor", db.donations_key: [38734, 6273, 67520]},
                  {db.name_key: 'Angelina Davis', db.donations_key: [74846, 38470, 7570, 50]},
                  {db.name_key: 'Bell Hooks', db.donations_key: [634547, 47498, 474729, 4567]}]

    with db._driver.session() as session:
        session.run("MATCH(d:Donor) DELETE d")
        for donor in donor_data:
            cyph = "CREATE (n:Donor {%s:'%s', %s:%s})" % (db.name_key,
                                                          donor[db.name_key],
                                                          db.donations_key,
                                                          donor[db.donations_key])
            session.run(cyph)


if __name__ == '__main__':
    main()
