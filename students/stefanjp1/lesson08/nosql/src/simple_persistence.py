import csv

peopledata = [
            ('John', 'second guitar', 117.45, 'in hall of fame', 5),
            ('Paul', 'bass', 22.01, 'in hall of fame', 5),
            ('George', 'lead guitar', 45.99, 'in hall of fame', 5),
            ('Ringo', 'drume', 77.0, 'not in hall of fame', 5),
            ('Roger', 'vocals', 12.5, 'not in hall of fame', 2),
            ('Keith', 'drums', 6.25, 'not in hall of fame', 1),
            ('Pete', 'guitar', 0.1, 'not in hall of fame', 6),
            ('John', 'bass', 89.71, 'in hall of fame', 12)
            ]
print('People Data:')
for person in peopledata:
    print(person)

print('Write people data')
with open('../data/rockstars.csv', 'w') as people:
    peoplewriter = csv.writer(people)
    peoplewriter.writerow(peopledata)

print('Read people data')
peopledata_new = list()
with open('../data/rockstars.csv', 'r') as people:
    people_reader = csv.reader(people, delimiter=',', quotechar='"')
    for row in people_reader:
        peopledata_new.extend(row)

print('New People Data:')
for person in peopledata_new:
    print(person)