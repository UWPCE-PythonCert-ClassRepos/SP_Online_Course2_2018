from timeit import timeit as timer


lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826
times = 10000000

v0 = timer(
    'v0.great_circle(lon1, lat1, lon2, lat2)',
    setup='import great_circle_v0 as v0',
    globals=globals(), number=times
)
v1 = timer(
    'v1.great_circle(lon1, lat1, lon2, lat2)',
    setup='import great_circle_v1 as v1',
    globals=globals(), number=times
)
v2 = timer(
    'v2.great_circle(lon1, lat1, lon2, lat2)',
    setup='import great_circle_v2 as v2',
    globals=globals(), number=times
)
v3 = timer(
    'v3.great_circle(lon1, lat1, lon2, lat2)',
    setup='import great_circle_v3 as v3',
    globals=globals(), number=times
)
print(f'v0: {v0}', f'v1: {v1}', f'v2: {v2}', f'v3: {v3}', sep='\n')
