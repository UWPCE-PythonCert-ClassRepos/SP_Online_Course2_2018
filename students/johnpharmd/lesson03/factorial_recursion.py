

def fac_recur(num=1):
    num = list(range(1, num + 1))
    if num:
        return num.pop(-1) * fac_recur(len(num))
    elif None:
        return []
