

def fac_recur(num=1):
    num = list(range(1, num + 1))
    nlist = [1]
    if len(num) > 0:
        return nlist[0] * num.pop(-1) * fac_recur(len(num))
    return nlist[0]
