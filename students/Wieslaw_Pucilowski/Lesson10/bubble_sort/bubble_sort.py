import random

def bubble(lst):
    swap = True
    cnt = 0
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
def main():
    bubble(my_list)
    
if __name__ == "__main__":
    my_list = random.sample(range(1000), 1000)
    main()