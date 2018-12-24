def primes_py(nb_primes):
    # cdef int n, i, len_p
    # cdef int p[1000]
    if nb_primes > 1000:
        nb_primes = 1000
    p = []

    len_p = 0  # The current number of elements in p.
    n = 2
    while len_p < nb_primes:
        # Is n prime?
        for i in p[:len_p]:
            # print("++++ n:{}, i:{}".format(n, i))
            if n % i == 0:
                # print("++++ break n: {} not prime".format(n))
                break

        # If no break occurred in the loop, we have a prime.
        else:
            # p[len_p] = n
            # print("insert {} list element into list p, n = {} ".format(len_p, n))
            p.insert(len_p, n)
            len_p += 1
        n += 1
        # print("p: {}".format(p))

    # Let's return the result in a python list:
    result_as_list  = [prime for prime in p[:len_p]]
    return result_as_list

def main():
    for i in range(1000):
        primes_py(10)

if __name__ == "__main__":
    main()