from memory_profiler import profile
import math
lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.826, 54.826

sample_list = [('Migos', 'Bad and Boujee (feat. Lil Uzi Vert)', 0.927, -5.313),
('Drake', 'Fake Love', 0.927, -9.433),
('Kendrick Lamar', 'HUMBLE.', 0.904, -6.8420000000000005),
('21 Savage', 'Bank Account', 0.884, -8.228),
('Jax Jones', "You Don't Know Me - Radio Edit", 0.8759999999999999, -6.053999999999999)]

# Function with no factorization
@profile(precision=4)
def great_circle_raw(lon1, lat1, lon2, lat2, sample_list):
    radius = 3956 # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))
    #adding random calculations for mememory filing purposes
    f = []
    for i in range(100000):
        f.append(math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta))))
    d = a ** 6 + math.log(b)
    e = c * d / math.factorial(6) + ((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))
    sample_list.append(('Jax Jones', "This is a Real Song", 0.825, -6.053))
    print(sample_list)
    return radius * c + e


# Funciton with acos factored out to a function

""" def calculate_acos(a, b, theta):
    return math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))


def great_circle_acos(lon1, lat1, lon2, lat2):
    radius = 3956 # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    # c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))
    c = calculate_acos(a, b, theta)
    return radius * c


# Great Circle algorithm with most steps factored out as a function

def calculate_x():
    return math.pi / 180.0


def calculate_coordinate(lat, x):
    return (90.0 - lat) * x


def calculate_theta(lon2, lon1, x):
    return (lon2 - lon1) * x


def great_circle_factored(lon1, lat1, lon2, lat2):
    radius = 3956 # miles
    x = calculate_x()
    a = calculate_coordinate(lat1, x)
    b = calculate_coordinate(lat2, x)
    theta = calculate_theta(lon2, lon1, x)
    c = calculate_acos(a, b, theta)
    return radius * c """


if __name__ == "__main__":

    great_circle_raw(lon1, lat1, lon2, lat2, sample_list)
    # great_circle_acos(lon1, lat1, lon2, lat2)
    # great_circle_factored(lon1, lat1, lon2, lat2)

    # for use as follows:
    #   $ /usr/bin/time -p python great_circle.py
    #   $ /usr/bin/time -p pypy great_circle.py

    #for i in range(100):
    #    great_circle_raw(lon1, lat1, lon2, lat2)
        # great_circle_acos(lon1, lat1, lon2, lat2)
        # great_circle_factored(lon1, lat1, lon2, lat2)