import pymongo
import utilities
import login_database
import donor_data
import pprint
import json

pp = pprint.PrettyPrinter(width=120)
from pymongo.errors import OperationFailure

__author__ = "Wieslaw Pucilowski"

pp = pprint.PrettyPrinter(width=120)

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

class Main():
    def run_example():
        with login_database.login_mongodb_cloud() as client:
            log.info('Step 1: We are going to use a database called donors')
            log.info('But if it doesnt exist mongodb creates it')
            db = client['donors']
            
            log.info('And in that database use a collection called donor')
            log.info('If it doesnt exist mongodb creates it')

            donor = db['donor']
            log.info('\n\nStep 2: Now we add data from the dictionary above')
            donor_items = donor_data.get_donor_data()
            donor.insert_many(donor_items)
            
            log.info('Step 3: List donor collection:')
            records = donor.find()
            for i in records:
                print(i)

            ##########################################################################################
            # Donations report Total, Average, Count
            ##########################################################################################
            
            log.info('Step 4: List report: donor, sum, average of donation:')
            try:
                records = donor.aggregate(
                    [
                        {
                            '$unwind' : '$donations' # must $unwind array for aggregation
                        },
                        {
                            '$group' : {
                                '_id' : '$name',
                                'Total' : {
                                        '$sum': '$donations'
                                    },
                                'Average' : {
                                        '$avg': '$donations'
                                    },
                                # mind count implemented as sum of aggregated rows
                                'Count' : {
                                        '$sum': 1
                                    }
                            }
                        },
                        {
                            '$sort' : {'Total' : -1 }
                        }
                    ]
                )
            except OperationFailure as e:
                print(e)

            for i in records:
                print(i)
            
            

            # log.info('\n\nStep 5: Prints number of donation per donor:')
            # try:
                # records = donor.aggregate([
                                    # {
                                        # '$unwind' : '$donations' # must $unwind array for aggregation
                                    # },
                                    # {
                                        # "$group" : {
                                                    # '_id' :"$name", 
                                                    # 'Number' :{'$sum':1}
                                        # }
                                    # }
                                # ])


            # except OperationFailure as e:
                # print(e)
            # for i in records:
                # print(i)

            ##########################################################################################
            # List donors
            ##########################################################################################
            log.info('Step 5: List donors:')
            records = donor.find().sort('name.last_name')
            for i in records:
                print("{} {}".format(i['name']['first_name'],
                      i['name']['last_name']))

            ##########################################################################################
            # Projection Challenge
            ##########################################################################################
            log.info('Step 6: Projection factor, min=20, max=200:')
            factor = 2
            _min=20
            _max=200
            # try:
            cursor1 = donor.aggregate([
                        {
                            '$unwind' : '$donations'
                        },
                        {
                            '$match' : { 'donations' : { '$gt' : _min, '$lt' : _max} # mind 'donations' without '$'
                            
                            }
                        },
                        {
                            '$group' : {'_id' : '$name',
                                        'Total' : {
                                                    '$sum': '$donations'
                                            }
                            }
                        }
                        
            ])
            
            cursor2 = donor.aggregate([
                        {
                            '$unwind' : '$donations'
                        },
                        {
                            '$match' : {'$or': [
                                                {'donations' : {'$lte' : _min}},
                                                {'donations' : {'$gte' : _max}},
                                    ]
                            }
                        },
                        {
                            '$group' : {'_id' : '$name',
                                        'Total' : {
                                                    '$sum': '$donations'
                                            }
                            }
                        }
                        
            ])
            
            
            cursor3 = donor.aggregate([
                        {
                            '$unwind' : '$donations'
                        },
                        {
                            '$match' : { 'donations' : { '$gt' : _min, '$lt' : _max} # mind 'donations' without '$'
                            
                            }
                        },
                        {
                            '$project' : { 'name' : 1, 'donations' : 1,  'projected' : {'$multiply' : ['$donations', factor]}
                                        }
                        
                        }
                        
            ])
            
            cursor4 = donor.aggregate([
                        # pipe1
                        {
                            '$unwind' : '$donations'
                        }, # pipe1 => pipe2
                        # pipe2
                        {
                            '$match' : { 'donations' : { '$gt' : _min, '$lt' : _max} # mind 'donations' without '$'
                            
                            }
                        }, # pipe2 => pipe3
                        # pipe3
                        {
                            '$project' : { 'name' : 1, 'donations' : 1,  'projected' : {'$multiply' : ['$donations', factor]}
                                        }
                        
                        }, # pipe3 => to group aggregation - mind sum is done on created above column: 'projected'
                        {
                            '$group' : {'_id' : '$name',
                                        'Total' : {
                                                    '$sum': '$projected'
                                            }
                            }
                        }
                        
            ])
            # except OperationFailure as e:
            #    print(e)
            
            print("Total of projected donations must be multiply by factor")
            for i in cursor1:
                print(i)
            print("*"*80)
            
            # print("Total of multiplied by 2 projected donations")
            # for i in cursor4:
            #     print(i)
            
            projection_dict = {}
            for i in cursor4:
                projection_dict[(i['_id']['first_name'], i['_id']['last_name'])] = i['Total']
           
            # print("total of non projected donations")
            # for i in cursor2:
            #     print(i)
            
            for i in cursor2:
                if (i['_id']['first_name'], i['_id']['last_name']) not in projection_dict.keys():
                    projection_dict[(i['_id']['first_name'], i['_id']['last_name'])] = i['Total']
                else:
                    projection_dict[(i['_id']['first_name'], i['_id']['last_name'])] += i['Total']

            print("*** Projected values:")
            for k, v in sorted(projection_dict.items(), key=lambda item: item[1], reverse=True):
                pp.pprint("{} {} Total: {}".format(k[0], k[1], v))
                
            

            ####
            #### Looking for UNION ALL like operation to MERGE two cursors: cursor4 and cursor2, then to perform aggregation on it
            ####
            ##########################################################################################
            # Projection Update
            ##########################################################################################
            log.info('Step 7: Apply projected changes: factor, min=20, max=200:')
            factor = 2
            _min=20
            _max=200
            
            # option 1
            
            # for update pipe processing doesn't apply, either $unwind for array elements
            # result = donor.update(
            #             {
            #                 '$unwind' : '$donations'
            #             }, # pipe1
            #             {
            #                 '$match' : { 'donations' : { '$gt' : _min, '$lt' : _max} # mind 'donations' without '$'
            #                 }
            #             }, # pipe2
            #             { '$mul': { '$donations': factor }
            #              },
            #             { '$upsert' : 'False' },
            #             { '$multi' : 'True' }
            # 
            # )
            
            # option 2
            
            # select_upd = { 'donations' : {
            #                                 '$elemMatch' : { '$gt' : _min, '$lt' : _max}
            #                               }
            #      }
            # new_values = { '$mul': { 'donations.$[]':  factor} # multiplies all elements in array
            #               }
            # 
            # new_values = { '$mul': { 'donations.$':  factor} # multiplies single elements in array
            #               }
            
            ### Looking for the way to update all array lements meeting the search criteria
            
            # result = donor.update_many(select_upd, new_values)
            
            print("+++ in database after update:")
            records = donor.find()
            for i in records:
                print(i)
            
            ##########################################################################################
            # Add new donor, donation
            ##########################################################################################
            # looking for donor, if exist then add/append donation, if not create/insert new donot and donation
            log.info('Step 8: Add/Update donor/donation:')
            first = "Ivan"
            last = "Smirnoff"
            location = "Moscow" # update
            # location = "Bothell" # insert
            donation = 10
            
            record = {
                    'name': {'first_name': first, 'last_name': last},
                    'location': location,
                    'donations' : [donation]
                }
            
            query = { '$and': [
                        {'name.first_name' : {'$eq' : first}},
                        {'name.last_name' : {'$eq' : last}},
                        {'location' : {'$eq' : location}}
                    ]}
            update = { '$push' : {'donations' : donation}}
            
            result = donor.find(query)
            
            for i in result:
                print(i)
            if result.count() > 0:
                print("found, record to update:")
                print(record)
                result = donor.update_one(query, update)
            else:
                print("not found, record to insert:")
                print(record)
                result = donor.insert_one(record)
                # print("insterted records: {}".format(result.inserted_count))

            
            records = donor.find()
            for i in records:
                print(i)
            

            log.info('Step 9: Delete the collection so we can start over')
            db.drop_collection('donor')
            

if __name__ == '__main__':
    Main.run_example()