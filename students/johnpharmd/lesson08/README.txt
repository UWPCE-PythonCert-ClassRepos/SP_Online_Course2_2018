from
https://startlearning.uw.edu/courses/course-v1:UW+PYTHON220+2018_Spring/courseware/
# [add onto url above] 94643cc6006e4fac8f6306a0ccc9695a/68729b1ed2384225b0e4f66fafcafd54/:

Q: "[C]ompare and contrast the ease of development, and the value delivered by each database.
Submit some comments to reflect this thinking with your assignment."

A: For me, querying is easiest in mongodb, then Cypher for neo4j, then redis. For the mailroom
data, if no associations are made between donors, then my pick for persisting the data would
be mongodb, then redis, then neo4j.

It took me quite a while to write the Python code for the mongodb version of mailroom. Maybe
this was because it was the first nosql db I've worked with. I spent the least amount of time
writing the code for the neo4j db.

Given mongodb's rich querying, redis's speed, and neo4j's powerful relationship mapping, each
of the db's is equally valuable, in my opinion. 