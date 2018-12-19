from great_circle import great_circle

lon1, lat1, lon2, lat2 = -72.345, 32.323, -61.823, 54.826

if __name__ == "__main__":
    for i in range(10000000):
        great_circle(lon1, lat1, lon2, lat2)
