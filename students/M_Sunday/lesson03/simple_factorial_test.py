from factorial import factorial as fact

results = {"1": 1,
           "2": 2,
           "3": 6,
           "4": 24,
           "5": 120,
           "10": 3628800,
           "30": 265252859812191058636308480000000}

for val in results.keys():
    assert fact(int(val)) == results[val]

