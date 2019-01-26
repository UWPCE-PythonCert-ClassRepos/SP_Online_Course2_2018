"""creates numerous generators as part of Python 220, lesson01"""

def generate_increasing_ints(start: int=0, step: int=1):
    """keep adding the next integer
    0 + 1 + 2 + 3 + 4 + 5 + …"""
    current_num = step
    current_total = start

    while True:
        yield current_total
        current_total += current_num
        current_num += 1