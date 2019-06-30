from iterator import IterateMe_1, Iterator_2

#test range behaves like IterateMe_1

def test_IterateMe_1():

    iter_test = IterateMe_1(4)

    iter_test_list = [i for i in iter_test]

    assert iter_test_list != list(range(4))

def test_Iterator_2():

    iter_test = Iterator_2(0,10,2)

    iter_test_list = [i for i in iter_test]

    assert iter_test_list == list(range(0,10,2))