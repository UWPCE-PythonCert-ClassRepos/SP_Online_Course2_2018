def bubble(lsta):
    swap = True
    cdef int cnt = 0
    cdef int lst[1000]
    if len(lsta) > 1000:
        lst = lsta[:1000]
    while swap:
        swap = False
        for i in range(len(lst)-1):
            cnt += 1
            if lst[i] > lst[i+1]:
                swap = True
                temp = lst[i]
                lst[i] = lst[i+1]
                lst[i+1] = temp
    # print("For Loop run {} times".format(cnt))
    # for sorted list[n] run = n, for unsorted n < run <=n**2 