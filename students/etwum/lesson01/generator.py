

def int_sum(n=0, next_num=0):
    while True:
        next_num += n
        yield next_num
        n += 1




