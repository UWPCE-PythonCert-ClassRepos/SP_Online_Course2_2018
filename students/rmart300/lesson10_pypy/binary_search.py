import random, sys

def binary_search_recursive(search_list, element):
    if len(search_list) == 0:
        return False
    else:
        mid = len(search_list)//2
        if (element == search_list[mid]):
            return True 
        else:
            if element > search_list[mid]:
                return binary_search_recursive(search_list[mid+1:],element)
            else:
                return binary_search_recursive(search_list[:mid],element)

def build_list(size=1000, max_num=10000):

    if max_num < size:
        raise Exception('max_num must be larger than size')

    search_list = set()
    while len(search_list) < size:
        rand = random.randrange(max_num)
        search_list.add(rand)

    sorted_list = list(search_list)
    sorted_list.sort()
    return sorted_list

if __name__ == '__main__':

    size = int(sys.argv[1])
    max_num = int(sys.argv[2])
    
    #size = int(input('what is size of array? '))
    #max_num = int(input('what is max num in array? '))

    #print('building list')
    search_list = build_list(size, max_num)
    #print(search_list)
       
    elem = search_list[random.randrange(size)]
 
    #elem = int(input('what number would you like to look for? '))

    index = binary_search_recursive(search_list, elem)

    if index:
        print(f'found {elem} in list')
    else:
        print(f'{elem} not found in list')

